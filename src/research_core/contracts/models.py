"""Versioned, project-neutral research interchange records.

These records carry metadata and small inference values only. They deliberately
avoid raw dataset arrays, fitted model objects, credentials, and child-project
implementation state. Large payloads are represented by explicit artifact
references with optional content hashes.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from math import isfinite
from types import MappingProxyType
from typing import Any

from .base import (
    ContractRecord,
    ContractValidationError,
    frozen_mapping,
    utc_now_iso,
    validate_finite_non_negative,
    validate_identifier,
    validate_iso_timestamp,
    validate_non_empty,
    validate_probability,
    validate_sha256,
    validate_uri_or_path,
)


class EvidenceClass(StrEnum):
    """Evidence class that prevents synthetic material being misreported as research data."""

    REAL = "real"
    SYNTHETIC = "synthetic"
    UNKNOWN = "unknown"


class RunStatus(StrEnum):
    """Lifecycle status of a registered execution."""

    PLANNED = "planned"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    IMPORTED = "imported"


class ArtifactRole(StrEnum):
    """Roles sufficient for provenance and reporting without owning artifact bytes."""

    CONFIGURATION = "configuration"
    MANIFEST = "manifest"
    METRICS = "metrics"
    MODEL = "model"
    PREDICTIONS = "predictions"
    REPORT = "report"
    TABLE = "table"
    FIGURE = "figure"
    LOG = "log"
    VIDEO = "video"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class SignalProvenanceRecord(ContractRecord):
    """Immutable provenance required for a canonical biosignal reference."""

    contract_kind: str = field(init=False, default="signal_provenance")
    origin: EvidenceClass = EvidenceClass.UNKNOWN
    source_dataset_id: str | None = None
    dataset_version: str | None = None
    source_uri: str | None = None
    license_id: str | None = None
    adapter_id: str | None = None
    adapter_version: str | None = None
    fallback_reason: str | None = None
    created_at_utc: str = field(default_factory=utc_now_iso)
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        ContractRecord.__post_init__(self)
        if not isinstance(self.origin, EvidenceClass):
            object.__setattr__(self, "origin", EvidenceClass(self.origin))
        for field_name in ("source_dataset_id", "license_id", "adapter_id", "adapter_version"):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, validate_identifier(value, field_name))
        if self.dataset_version is not None:
            object.__setattr__(self, "dataset_version", validate_non_empty(self.dataset_version, "dataset_version"))
        if self.source_uri is not None:
            object.__setattr__(self, "source_uri", validate_uri_or_path(self.source_uri, "source_uri"))
        if self.fallback_reason is not None:
            object.__setattr__(self, "fallback_reason", validate_non_empty(self.fallback_reason, "fallback_reason"))
        if self.origin is EvidenceClass.SYNTHETIC and not self.fallback_reason:
            raise ContractValidationError("synthetic provenance requires fallback_reason or generation rationale")
        object.__setattr__(self, "created_at_utc", validate_iso_timestamp(self.created_at_utc, "created_at_utc"))
        object.__setattr__(self, "details", frozen_mapping(self.details, "details"))

    @property
    def benchmark_eligible(self) -> bool:
        """Return whether the evidence class could be considered for a real-data benchmark."""
        return self.origin is EvidenceClass.REAL and bool(
            self.details.get("benchmark_eligible", True)
        )


@dataclass(frozen=True, slots=True)
class SignalRecord(ContractRecord):
    """Metadata-only canonical reference to a contiguous biosignal or window.

    The data itself is intentionally not persisted in this contract. ``data_uri``
    may point to an authorized local path or supported object reference outside
    the registry, preserving the rule that raw datasets remain external.
    """

    contract_kind: str = field(init=False, default="signal")
    signal_id: str = ""
    modality: str = ""
    sampling_rate_hz: float = 0.0
    channel_names: tuple[str, ...] = ()
    sample_count: int = 0
    provenance: SignalProvenanceRecord = field(default_factory=SignalProvenanceRecord)
    data_uri: str | None = None
    data_sha256: str | None = None
    units: tuple[str, ...] = ("unknown",)
    timestamp_start_utc: str | None = None
    duration_seconds: float | None = None
    subject_id: str | None = None
    session_id: str | None = None
    recording_id: str | None = None
    task_id: str | None = None
    window_id: str | None = None
    annotations: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        ContractRecord.__post_init__(self)
        object.__setattr__(self, "signal_id", validate_identifier(self.signal_id, "signal_id"))
        object.__setattr__(self, "modality", validate_identifier(self.modality.lower(), "modality"))
        sampling_rate = float(self.sampling_rate_hz)
        if not isfinite(sampling_rate) or sampling_rate <= 0:
            raise ContractValidationError("sampling_rate_hz must be finite and positive")
        object.__setattr__(self, "sampling_rate_hz", sampling_rate)
        channels = tuple(validate_non_empty(channel, "channel_names entry") for channel in self.channel_names)
        if not channels or len(set(channels)) != len(channels):
            raise ContractValidationError("channel_names must be non-empty and unique")
        object.__setattr__(self, "channel_names", channels)
        if not isinstance(self.sample_count, int) or isinstance(self.sample_count, bool) or self.sample_count <= 0:
            raise ContractValidationError("sample_count must be a positive integer")
        if not isinstance(self.provenance, SignalProvenanceRecord):
            raise ContractValidationError("provenance must be a SignalProvenanceRecord")
        if self.data_uri is not None:
            object.__setattr__(self, "data_uri", validate_uri_or_path(self.data_uri, "data_uri"))
        object.__setattr__(self, "data_sha256", validate_sha256(self.data_sha256, "data_sha256"))
        if self.data_sha256 and not self.data_uri:
            raise ContractValidationError("data_sha256 requires data_uri")
        units = tuple(validate_non_empty(unit, "units entry") for unit in self.units)
        if len(units) not in (1, len(channels)):
            raise ContractValidationError("units must contain one unit or one unit per channel")
        object.__setattr__(self, "units", units)
        if self.timestamp_start_utc is not None:
            object.__setattr__(self, "timestamp_start_utc", validate_iso_timestamp(self.timestamp_start_utc, "timestamp_start_utc"))
        if self.duration_seconds is not None:
            object.__setattr__(self, "duration_seconds", validate_finite_non_negative(self.duration_seconds, "duration_seconds"))
        for field_name in ("subject_id", "session_id", "recording_id", "task_id", "window_id"):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, validate_identifier(value, field_name))
        object.__setattr__(self, "annotations", frozen_mapping(self.annotations, "annotations"))


@dataclass(frozen=True, slots=True)
class RepresentationRecord(ContractRecord):
    """Versioned reference to an encoder representation or a small embedding vector."""

    contract_kind: str = field(init=False, default="representation")
    representation_id: str = ""
    modality: str = ""
    encoder_id: str = ""
    model_version: str = ""
    dimension: int = 0
    input_signal_ids: tuple[str, ...] = ()
    provenance: SignalProvenanceRecord = field(default_factory=SignalProvenanceRecord)
    values: tuple[float, ...] | None = None
    tensor_uri: str | None = None
    tensor_sha256: str | None = None
    window_ids: tuple[str, ...] = ()
    created_at_utc: str = field(default_factory=utc_now_iso)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        ContractRecord.__post_init__(self)
        for field_name in ("representation_id", "modality", "encoder_id", "model_version"):
            value = getattr(self, field_name)
            normalized = value.lower() if field_name == "modality" else value
            object.__setattr__(self, field_name, validate_identifier(normalized, field_name))
        if not isinstance(self.dimension, int) or isinstance(self.dimension, bool) or self.dimension <= 0:
            raise ContractValidationError("dimension must be a positive integer")
        signal_ids = tuple(validate_identifier(value, "input_signal_ids entry") for value in self.input_signal_ids)
        if not signal_ids:
            raise ContractValidationError("input_signal_ids must not be empty")
        object.__setattr__(self, "input_signal_ids", signal_ids)
        if not isinstance(self.provenance, SignalProvenanceRecord):
            raise ContractValidationError("provenance must be a SignalProvenanceRecord")
        if self.values is None and self.tensor_uri is None:
            raise ContractValidationError("representation requires values or tensor_uri")
        if self.values is not None:
            values = tuple(float(value) for value in self.values)
            if len(values) != self.dimension or not all(isfinite(value) for value in values):
                raise ContractValidationError("values must be finite and match dimension")
            object.__setattr__(self, "values", values)
        if self.tensor_uri is not None:
            object.__setattr__(self, "tensor_uri", validate_uri_or_path(self.tensor_uri, "tensor_uri"))
        object.__setattr__(self, "tensor_sha256", validate_sha256(self.tensor_sha256, "tensor_sha256"))
        if self.tensor_sha256 and not self.tensor_uri:
            raise ContractValidationError("tensor_sha256 requires tensor_uri")
        object.__setattr__(self, "window_ids", tuple(validate_identifier(value, "window_ids entry") for value in self.window_ids))
        object.__setattr__(self, "created_at_utc", validate_iso_timestamp(self.created_at_utc, "created_at_utc"))
        object.__setattr__(self, "metadata", frozen_mapping(self.metadata, "metadata"))


@dataclass(frozen=True, slots=True)
class IntentRecord(ContractRecord):
    """One discrete or continuous motor-intent estimate, never an actuator command."""

    contract_kind: str = field(init=False, default="intent")
    intent_id: str = ""
    timestamp_utc: str = field(default_factory=utc_now_iso)
    confidence: float = 0.0
    source_model_id: str = ""
    model_version: str = ""
    modalities: tuple[str, ...] = ()
    provenance: SignalProvenanceRecord = field(default_factory=SignalProvenanceRecord)
    label: str | None = None
    values: tuple[float, ...] | None = None
    probabilities: Mapping[str, float] = field(default_factory=dict)
    stream_time_seconds: float | None = None
    subject_id: str | None = None
    session_id: str | None = None
    window_id: str | None = None
    source_representation_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        ContractRecord.__post_init__(self)
        for field_name in ("intent_id", "source_model_id", "model_version"):
            object.__setattr__(self, field_name, validate_identifier(getattr(self, field_name), field_name))
        object.__setattr__(self, "timestamp_utc", validate_iso_timestamp(self.timestamp_utc, "timestamp_utc"))
        object.__setattr__(self, "confidence", validate_probability(self.confidence, "confidence"))
        modalities = tuple(validate_identifier(value.lower(), "modalities entry") for value in self.modalities)
        if not modalities:
            raise ContractValidationError("modalities must not be empty")
        object.__setattr__(self, "modalities", tuple(dict.fromkeys(modalities)))
        if not isinstance(self.provenance, SignalProvenanceRecord):
            raise ContractValidationError("provenance must be a SignalProvenanceRecord")
        if (self.label is None) == (self.values is None):
            raise ContractValidationError("exactly one of label or values must be supplied")
        if self.label is not None:
            object.__setattr__(self, "label", validate_non_empty(self.label, "label"))
        if self.values is not None:
            values = tuple(float(value) for value in self.values)
            if not values or not all(isfinite(value) for value in values):
                raise ContractValidationError("values must be a non-empty finite vector")
            object.__setattr__(self, "values", values)
        probability_values: dict[str, float] = {}
        for label, probability in self.probabilities.items():
            probability_values[validate_non_empty(str(label), "probabilities label")] = validate_probability(
                probability, "probabilities value"
            )
        if probability_values and abs(sum(probability_values.values()) - 1.0) > 1e-6:
            raise ContractValidationError("probabilities must sum to one when provided")
        object.__setattr__(self, "probabilities", MappingProxyType(probability_values))
        if self.stream_time_seconds is not None:
            object.__setattr__(self, "stream_time_seconds", validate_finite_non_negative(self.stream_time_seconds, "stream_time_seconds"))
        for field_name in ("subject_id", "session_id", "window_id"):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, validate_identifier(value, field_name))
        object.__setattr__(self, "source_representation_ids", tuple(
            validate_identifier(value, "source_representation_ids entry")
            for value in self.source_representation_ids
        ))
        object.__setattr__(self, "metadata", frozen_mapping(self.metadata, "metadata"))


@dataclass(frozen=True, slots=True)
class ControlCommandRecord(ContractRecord):
    """Auditable simulator-emitted command evidence derived from an intent record."""

    contract_kind: str = field(init=False, default="control_command")
    command_id: str = ""
    timestamp_utc: str = field(default_factory=utc_now_iso)
    mode: str = ""
    originating_intent_id: str = ""
    validity: str = "validated"
    actuator_targets: Mapping[str, float] = field(default_factory=dict)
    joint_targets_rad: Mapping[str, float] = field(default_factory=dict)
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        ContractRecord.__post_init__(self)
        for field_name in ("command_id", "mode", "originating_intent_id", "validity"):
            object.__setattr__(self, field_name, validate_identifier(getattr(self, field_name), field_name))
        object.__setattr__(self, "timestamp_utc", validate_iso_timestamp(self.timestamp_utc, "timestamp_utc"))
        if not self.actuator_targets and not self.joint_targets_rad:
            raise ContractValidationError("a control command requires actuator or joint targets")
        for field_name in ("actuator_targets", "joint_targets_rad"):
            raw_targets = getattr(self, field_name)
            targets: dict[str, float] = {}
            for target_name, target_value in raw_targets.items():
                value = float(target_value)
                if not isfinite(value):
                    raise ContractValidationError(f"{field_name} values must be finite")
                targets[validate_non_empty(str(target_name), f"{field_name} key")] = value
            object.__setattr__(self, field_name, MappingProxyType(targets))
        object.__setattr__(self, "provenance", frozen_mapping(self.provenance, "provenance"))


@dataclass(frozen=True, slots=True)
class ArtifactRecord(ContractRecord):
    """A hashable external artifact reference owned by its producing project."""

    contract_kind: str = field(init=False, default="artifact")
    artifact_id: str = ""
    role: ArtifactRole = ArtifactRole.OTHER
    uri: str = ""
    producing_run_id: str = ""
    evidence_class: EvidenceClass = EvidenceClass.UNKNOWN
    sha256: str | None = None
    media_type: str | None = None
    size_bytes: int | None = None
    created_at_utc: str = field(default_factory=utc_now_iso)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        ContractRecord.__post_init__(self)
        for field_name in ("artifact_id", "producing_run_id"):
            object.__setattr__(self, field_name, validate_identifier(getattr(self, field_name), field_name))
        if not isinstance(self.role, ArtifactRole):
            object.__setattr__(self, "role", ArtifactRole(self.role))
        if not isinstance(self.evidence_class, EvidenceClass):
            object.__setattr__(self, "evidence_class", EvidenceClass(self.evidence_class))
        object.__setattr__(self, "uri", validate_uri_or_path(self.uri, "uri"))
        object.__setattr__(self, "sha256", validate_sha256(self.sha256))
        if self.media_type is not None:
            object.__setattr__(self, "media_type", validate_non_empty(self.media_type, "media_type"))
        if self.size_bytes is not None and (not isinstance(self.size_bytes, int) or self.size_bytes < 0):
            raise ContractValidationError("size_bytes must be a non-negative integer when provided")
        object.__setattr__(self, "created_at_utc", validate_iso_timestamp(self.created_at_utc, "created_at_utc"))
        object.__setattr__(self, "metadata", frozen_mapping(self.metadata, "metadata"))


@dataclass(frozen=True, slots=True)
class ExperimentRecord(ContractRecord):
    """The minimum reproducible experiment identity required for benchmarking."""

    contract_kind: str = field(init=False, default="experiment")
    experiment_id: str = ""
    run_id: str = ""
    project_id: str = ""
    protocol_id: str = ""
    dataset_id: str = ""
    dataset_version: str = ""
    modality: str = ""
    subject_split: str = ""
    model_id: str = ""
    model_version: str = ""
    seed: int = 0
    configuration_hash: str = ""
    status: RunStatus = RunStatus.PLANNED
    code_commit: str | None = None
    environment: Mapping[str, Any] = field(default_factory=dict)
    metrics: Mapping[str, float] = field(default_factory=dict)
    artifact_ids: tuple[str, ...] = ()
    started_at_utc: str | None = None
    completed_at_utc: str | None = None
    error: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        ContractRecord.__post_init__(self)
        for field_name in (
            "experiment_id", "run_id", "project_id", "protocol_id", "dataset_id", "dataset_version",
            "modality", "subject_split", "model_id", "model_version", "configuration_hash",
        ):
            value = getattr(self, field_name)
            normalized = value.lower() if field_name == "modality" else value
            object.__setattr__(self, field_name, validate_identifier(normalized, field_name))
        if not isinstance(self.seed, int) or isinstance(self.seed, bool) or self.seed < 0:
            raise ContractValidationError("seed must be a non-negative integer")
        object.__setattr__(self, "configuration_hash", validate_sha256(self.configuration_hash, "configuration_hash") or "")
        if not isinstance(self.status, RunStatus):
            object.__setattr__(self, "status", RunStatus(self.status))
        if self.code_commit is not None:
            object.__setattr__(self, "code_commit", validate_non_empty(self.code_commit, "code_commit"))
        if self.started_at_utc is not None:
            object.__setattr__(self, "started_at_utc", validate_iso_timestamp(self.started_at_utc, "started_at_utc"))
        if self.completed_at_utc is not None:
            object.__setattr__(self, "completed_at_utc", validate_iso_timestamp(self.completed_at_utc, "completed_at_utc"))
        if self.status in {RunStatus.SUCCEEDED, RunStatus.FAILED, RunStatus.CANCELLED} and not self.completed_at_utc:
            raise ContractValidationError("terminal run status requires completed_at_utc")
        if self.status is RunStatus.FAILED and not self.error:
            raise ContractValidationError("failed run status requires error")
        if self.error is not None:
            object.__setattr__(self, "error", validate_non_empty(self.error, "error"))
        metric_values: dict[str, float] = {}
        for name, metric in self.metrics.items():
            numeric = float(metric)
            if not isfinite(numeric):
                raise ContractValidationError("metrics values must be finite")
            metric_values[validate_identifier(str(name), "metrics key")] = numeric
        object.__setattr__(self, "metrics", MappingProxyType(metric_values))
        object.__setattr__(self, "artifact_ids", tuple(
            validate_identifier(value, "artifact_ids entry") for value in self.artifact_ids
        ))
        object.__setattr__(self, "environment", frozen_mapping(self.environment, "environment"))
        object.__setattr__(self, "metadata", frozen_mapping(self.metadata, "metadata"))

    @property
    def benchmark_eligible(self) -> bool:
        """Return whether the record can be used as a completed, real-data benchmark input."""
        return self.status in {RunStatus.SUCCEEDED, RunStatus.IMPORTED} and bool(
            self.metadata.get("benchmark_eligible", True)
        ) and not bool(self.metadata.get("synthetic", False))


def ensure_real_benchmark_records(records: Sequence[ExperimentRecord]) -> tuple[ExperimentRecord, ...]:
    """Reject synthetic, incomplete, or non-benchmark records before aggregation."""
    normalized = tuple(records)
    if not normalized:
        raise ContractValidationError("at least one experiment record is required")
    ineligible = [record.run_id for record in normalized if not record.benchmark_eligible]
    if ineligible:
        raise ContractValidationError(
            "benchmark aggregation requires completed real-data eligible records; "
            f"ineligible runs: {', '.join(ineligible)}"
        )
    return normalized
