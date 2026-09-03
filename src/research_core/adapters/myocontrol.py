"""Thin adapter from a serialized MyoControl prediction to an umbrella intent record."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from research_core.contracts import IntentRecord, SignalProvenanceRecord
from research_core.contracts.base import ContractValidationError

from .common import AdapterError, provenance_from_export, required, safe_metadata


ADAPTER_ID = "myocontrol-prediction"
ADAPTER_VERSION = "1.0.0"


def intent_from_myocontrol_prediction(
    prediction: Mapping[str, Any],
    *,
    intent_id: str,
    timestamp_utc: str,
    source_model_id: str,
    model_version: str,
    stream_time_seconds: float | None = None,
    subject_id: str | None = None,
    session_id: str | None = None,
    window_id: str | None = None,
    provenance: SignalProvenanceRecord | None = None,
    external_provenance: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> IntentRecord:
    """Convert MyoControl's public prediction fields into a validated intent.

    Expected public prediction keys are `predicted_class`, `confidence`, and
    optional `probabilities`. The adapter does not train, call, inspect, or
    import MyoControl internals. Timing and source context are explicit because
    a standalone class prediction does not contain them.
    """
    if provenance is not None and external_provenance is not None:
        raise AdapterError("provide either provenance or external_provenance, not both")
    resolved_provenance = provenance or provenance_from_export(
        external_provenance,
        adapter_id=ADAPTER_ID,
        adapter_version=ADAPTER_VERSION,
    )
    raw_probabilities = prediction.get("probabilities", {})
    if raw_probabilities is None:
        raw_probabilities = {}
    if not isinstance(raw_probabilities, Mapping):
        raise AdapterError("MyoControl prediction probabilities must be a mapping")
    caller_metadata = safe_metadata(metadata)
    caller_metadata.update(
        {
            "adapter_id": ADAPTER_ID,
            "adapter_version": ADAPTER_VERSION,
            "external_prediction_schema": "myocontrol-classification-result",
        }
    )
    try:
        return IntentRecord(
            intent_id=intent_id,
            timestamp_utc=timestamp_utc,
            confidence=float(required(prediction, "confidence")),
            source_model_id=source_model_id,
            model_version=model_version,
            modalities=("emg",),
            provenance=resolved_provenance,
            label=str(required(prediction, "predicted_class")),
            probabilities={str(label): float(value) for label, value in raw_probabilities.items()},
            stream_time_seconds=stream_time_seconds,
            subject_id=subject_id,
            session_id=session_id,
            window_id=window_id,
            metadata=caller_metadata,
        )
    except (ContractValidationError, TypeError, ValueError) as exc:
        raise AdapterError(f"invalid MyoControl prediction mapping: {exc}") from exc
