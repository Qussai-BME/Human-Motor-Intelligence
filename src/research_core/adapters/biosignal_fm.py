"""Thin mapping adapters for BioSignal-FM public exports.

The adapter accepts JSON-like public export mappings. It intentionally does not
import BioSignal-FM package internals, preprocessing logic, encoders, fusion,
or task heads; this keeps the durable integration boundary artifact-based.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from research_core.contracts import RepresentationRecord, SignalRecord
from research_core.contracts.base import ContractValidationError

from .common import AdapterError, provenance_from_export, required, safe_metadata


SIGNAL_ADAPTER_ID = "biosignal-fm-signal-export"
REPRESENTATION_ADAPTER_ID = "biosignal-fm-representation-export"
ADAPTER_VERSION = "1.0.0"


def signal_from_biosignal_fm_export(export: Mapping[str, Any]) -> SignalRecord:
    """Convert a public canonical-signal export mapping to an umbrella record."""
    metadata = required(export, "metadata")
    if not isinstance(metadata, Mapping):
        raise AdapterError("BioSignal-FM signal export metadata must be a mapping")
    provenance = provenance_from_export(
        metadata.get("provenance"),
        adapter_id=SIGNAL_ADAPTER_ID,
        adapter_version=ADAPTER_VERSION,
    )
    try:
        return SignalRecord(
            signal_id=str(required(export, "signal_id")),
            modality=str(required(metadata, "modality")),
            sampling_rate_hz=float(required(metadata, "sampling_rate_hz")),
            channel_names=tuple(str(value) for value in required(metadata, "channel_names")),
            sample_count=int(required(export, "sample_count")),
            provenance=provenance,
            data_uri=export.get("data_uri"),
            data_sha256=export.get("data_sha256"),
            units=tuple(str(value) for value in metadata.get("units", ("unknown",))),
            timestamp_start_utc=export.get("timestamp_start_utc"),
            duration_seconds=export.get("duration_seconds"),
            subject_id=metadata.get("subject_id"),
            session_id=metadata.get("session_id"),
            recording_id=metadata.get("recording_id"),
            task_id=metadata.get("task_id"),
            window_id=metadata.get("window_id"),
            annotations=safe_metadata(export.get("annotations")),
        )
    except (ContractValidationError, TypeError, ValueError) as exc:
        raise AdapterError(f"invalid BioSignal-FM signal export: {exc}") from exc


def representation_from_biosignal_fm_export(export: Mapping[str, Any]) -> RepresentationRecord:
    """Convert a public representation export mapping to an umbrella record."""
    provenance = provenance_from_export(
        export.get("provenance"),
        adapter_id=REPRESENTATION_ADAPTER_ID,
        adapter_version=ADAPTER_VERSION,
    )
    values = export.get("values")
    if values is not None and (not isinstance(values, Sequence) or isinstance(values, (str, bytes))):
        raise AdapterError("representation values must be a numeric sequence when supplied")
    try:
        return RepresentationRecord(
            representation_id=str(required(export, "representation_id")),
            modality=str(required(export, "modality")),
            encoder_id=str(required(export, "encoder_id")),
            model_version=str(required(export, "model_version")),
            dimension=int(required(export, "dimension")),
            input_signal_ids=tuple(str(value) for value in required(export, "input_signal_ids")),
            provenance=provenance,
            values=tuple(float(value) for value in values) if values is not None else None,
            tensor_uri=export.get("tensor_uri"),
            tensor_sha256=export.get("tensor_sha256"),
            window_ids=tuple(str(value) for value in export.get("window_ids", ())),
            metadata=safe_metadata(export.get("metadata")),
        )
    except (ContractValidationError, TypeError, ValueError) as exc:
        raise AdapterError(f"invalid BioSignal-FM representation export: {exc}") from exc
