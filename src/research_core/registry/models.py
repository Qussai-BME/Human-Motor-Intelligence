"""Typed metadata entries owned by the local research registry.

Registry entries deliberately contain descriptive metadata and references only.
They never contain raw biosignal recordings, fitted model bytes, credentials, or
unreviewed scientific claims.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from enum import StrEnum
from math import isfinite
from types import MappingProxyType
from typing import Any

from research_core.contracts.base import (
    ContractValidationError,
    frozen_mapping,
    json_safe,
    utc_now_iso,
    validate_identifier,
    validate_iso_timestamp,
    validate_non_empty,
    validate_uri_or_path,
)


class DatasetAccess(StrEnum):
    """Access condition recorded before a dataset can be used in a registered run."""

    OPEN = "open"
    REGISTRATION_REQUIRED = "registration_required"
    CREDENTIALLED = "credentialed"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"


class ProtocolStatus(StrEnum):
    """Protocol governance state."""

    DRAFT = "draft"
    ACTIVE = "active"
    LOCKED_EXTERNAL = "locked_external"
    RETIRED = "retired"


class StatisticalUnit(StrEnum):
    """The valid unit of inference required by a protocol."""

    SUBJECT = "subject"
    SESSION = "session"
    RECORDING = "recording"
    WINDOW = "window"
    TASK_TRIAL = "task_trial"


@dataclass(frozen=True, slots=True)
class RegistryDefinition:
    """Base immutable metadata definition carrying a registry identity."""

    entity_type: str = field(init=False, default="")
    entity_id: str = ""
    created_at_utc: str = field(default_factory=utc_now_iso)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "entity_type", validate_identifier(self.entity_type, "entity_type"))
        object.__setattr__(self, "entity_id", validate_identifier(self.entity_id, "entity_id"))
        object.__setattr__(self, "created_at_utc", validate_iso_timestamp(self.created_at_utc, "created_at_utc"))
        object.__setattr__(self, "metadata", frozen_mapping(self.metadata, "metadata"))

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-safe normalized entry suitable for local persistence."""
        return json_safe({item.name: getattr(self, item.name) for item in fields(self)})  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class DatasetDefinition(RegistryDefinition):
    """Dataset card metadata; this references a source but never packages dataset content."""

    entity_type: str = field(init=False, default="dataset")
    name: str = ""
    modality: str = ""
    source_url: str = ""
    citation: str = ""
    license_access: DatasetAccess = DatasetAccess.UNKNOWN
    sampling_rate_hz: float | None = None
    channel_description: str = ""
    task_description: str = ""
    subject_count: int | None = None
    session_description: str = ""
    label_schema: Mapping[str, Any] = field(default_factory=dict)
    canonicalization_rules: tuple[str, ...] = ()
    known_limitations: tuple[str, ...] = ()
    version: str = ""

    def __post_init__(self) -> None:
        RegistryDefinition.__post_init__(self)
        for field_name in ("name", "channel_description", "task_description", "session_description", "version"):
            object.__setattr__(self, field_name, validate_non_empty(getattr(self, field_name), field_name))
        object.__setattr__(self, "modality", validate_identifier(self.modality.lower(), "modality"))
        object.__setattr__(self, "source_url", validate_uri_or_path(self.source_url, "source_url"))
        object.__setattr__(self, "citation", validate_non_empty(self.citation, "citation"))
        if not isinstance(self.license_access, DatasetAccess):
            object.__setattr__(self, "license_access", DatasetAccess(self.license_access))
        if self.sampling_rate_hz is not None:
            sampling_rate = float(self.sampling_rate_hz)
            if not isfinite(sampling_rate) or sampling_rate <= 0:
                raise ContractValidationError("sampling_rate_hz must be positive when known")
            object.__setattr__(self, "sampling_rate_hz", sampling_rate)
        if self.subject_count is not None and (
            not isinstance(self.subject_count, int) or self.subject_count <= 0
        ):
            raise ContractValidationError("subject_count must be a positive integer when known")
        object.__setattr__(self, "label_schema", frozen_mapping(self.label_schema, "label_schema"))
        object.__setattr__(self, "canonicalization_rules", tuple(
            validate_non_empty(value, "canonicalization_rules entry")
            for value in self.canonicalization_rules
        ))
        object.__setattr__(self, "known_limitations", tuple(
            validate_non_empty(value, "known_limitations entry") for value in self.known_limitations
        ))


@dataclass(frozen=True, slots=True)
class ProtocolDefinition(RegistryDefinition):
    """A research protocol, distinct from a model configuration."""

    entity_type: str = field(init=False, default="protocol")
    name: str = ""
    version: str = ""
    modalities: tuple[str, ...] = ()
    split_strategy: str = ""
    train_validation_test_semantics: str = ""
    leakage_constraints: tuple[str, ...] = ()
    preprocessing: Mapping[str, Any] = field(default_factory=dict)
    feature_selection: Mapping[str, Any] = field(default_factory=dict)
    model_selection: Mapping[str, Any] = field(default_factory=dict)
    metrics: tuple[str, ...] = ()
    statistical_unit: StatisticalUnit = StatisticalUnit.SUBJECT
    seeds: tuple[int, ...] = ()
    hyperparameter_policy: str = ""
    status: ProtocolStatus = ProtocolStatus.DRAFT
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        RegistryDefinition.__post_init__(self)
        for field_name in ("name", "version", "split_strategy", "train_validation_test_semantics", "hyperparameter_policy"):
            object.__setattr__(self, field_name, validate_non_empty(getattr(self, field_name), field_name))
        modalities = tuple(validate_identifier(value.lower(), "modalities entry") for value in self.modalities)
        if not modalities:
            raise ContractValidationError("protocol modalities must not be empty")
        object.__setattr__(self, "modalities", tuple(dict.fromkeys(modalities)))
        constraints = tuple(validate_non_empty(value, "leakage_constraints entry") for value in self.leakage_constraints)
        if not constraints:
            raise ContractValidationError("protocol leakage_constraints must not be empty")
        object.__setattr__(self, "leakage_constraints", constraints)
        for field_name in ("preprocessing", "feature_selection", "model_selection"):
            object.__setattr__(self, field_name, frozen_mapping(getattr(self, field_name), field_name))
        metrics = tuple(validate_identifier(value, "metrics entry") for value in self.metrics)
        if not metrics:
            raise ContractValidationError("protocol metrics must not be empty")
        object.__setattr__(self, "metrics", tuple(dict.fromkeys(metrics)))
        if not isinstance(self.statistical_unit, StatisticalUnit):
            object.__setattr__(self, "statistical_unit", StatisticalUnit(self.statistical_unit))
        if not self.seeds or any(not isinstance(seed, int) or isinstance(seed, bool) or seed < 0 for seed in self.seeds):
            raise ContractValidationError("protocol seeds must contain one or more non-negative integers")
        object.__setattr__(self, "seeds", tuple(dict.fromkeys(self.seeds)))
        if not isinstance(self.status, ProtocolStatus):
            object.__setattr__(self, "status", ProtocolStatus(self.status))
        object.__setattr__(self, "limitations", tuple(
            validate_non_empty(value, "limitations entry") for value in self.limitations
        ))


@dataclass(frozen=True, slots=True)
class ModelDefinition(RegistryDefinition):
    """A model identity card, not a serialized model checkpoint."""

    entity_type: str = field(init=False, default="model")
    name: str = ""
    version: str = ""
    project_id: str = ""
    modalities: tuple[str, ...] = ()
    model_family: str = ""
    source_reference: str = ""
    intended_use: str = ""
    known_limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        RegistryDefinition.__post_init__(self)
        for field_name in ("name", "version", "project_id", "model_family", "intended_use"):
            object.__setattr__(self, field_name, validate_non_empty(getattr(self, field_name), field_name))
        object.__setattr__(self, "source_reference", validate_uri_or_path(self.source_reference, "source_reference"))
        modalities = tuple(validate_identifier(value.lower(), "modalities entry") for value in self.modalities)
        if not modalities:
            raise ContractValidationError("model modalities must not be empty")
        object.__setattr__(self, "modalities", tuple(dict.fromkeys(modalities)))
        object.__setattr__(self, "known_limitations", tuple(
            validate_non_empty(value, "known_limitations entry") for value in self.known_limitations
        ))


@dataclass(frozen=True, slots=True)
class ProjectDefinition(RegistryDefinition):
    """A mature-project or umbrella-project entry used to preserve ownership boundaries."""

    entity_type: str = field(init=False, default="project")
    name: str = ""
    role: str = ""
    repository_reference: str = ""
    license_id: str = ""
    independently_runnable: bool = True
    integration_boundary: str = ""

    def __post_init__(self) -> None:
        RegistryDefinition.__post_init__(self)
        for field_name in ("name", "role", "license_id", "integration_boundary"):
            object.__setattr__(self, field_name, validate_non_empty(getattr(self, field_name), field_name))
        object.__setattr__(self, "repository_reference", validate_uri_or_path(self.repository_reference, "repository_reference"))


@dataclass(frozen=True, slots=True)
class BenchmarkDefinition(RegistryDefinition):
    """A benchmark family definition with non-negotiable protocol identity."""

    entity_type: str = field(init=False, default="benchmark")
    name: str = ""
    protocol_id: str = ""
    dataset_ids: tuple[str, ...] = ()
    comparison_dimension: str = ""
    description: str = ""

    def __post_init__(self) -> None:
        RegistryDefinition.__post_init__(self)
        for field_name in ("name", "protocol_id", "comparison_dimension", "description"):
            object.__setattr__(self, field_name, validate_non_empty(getattr(self, field_name), field_name))
        ids = tuple(validate_identifier(value, "dataset_ids entry") for value in self.dataset_ids)
        if not ids:
            raise ContractValidationError("benchmark must reference at least one dataset")
        object.__setattr__(self, "dataset_ids", tuple(dict.fromkeys(ids)))


@dataclass(frozen=True, slots=True)
class ReportDefinition(RegistryDefinition):
    """A factual report reference generated from one or more registered runs."""

    entity_type: str = field(init=False, default="report")
    title: str = ""
    report_uri: str = ""
    run_ids: tuple[str, ...] = ()
    benchmark_id: str | None = None

    def __post_init__(self) -> None:
        RegistryDefinition.__post_init__(self)
        object.__setattr__(self, "title", validate_non_empty(self.title, "title"))
        object.__setattr__(self, "report_uri", validate_uri_or_path(self.report_uri, "report_uri"))
        run_ids = tuple(validate_identifier(value, "run_ids entry") for value in self.run_ids)
        if not run_ids:
            raise ContractValidationError("report must reference at least one run")
        object.__setattr__(self, "run_ids", tuple(dict.fromkeys(run_ids)))
        if self.benchmark_id is not None:
            object.__setattr__(self, "benchmark_id", validate_identifier(self.benchmark_id, "benchmark_id"))
