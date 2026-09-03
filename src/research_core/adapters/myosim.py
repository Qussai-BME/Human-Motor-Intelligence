"""Thin intent-to-MyoSim V1 adapter.

The adapter terminates at MyoSim's documented ``IntentEvent`` boundary. It
never generates commands, joint targets, controller state transitions, or
physics operations; those remain owned by MyoSim.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from research_core.contracts import IntentRecord
from research_core.contracts.base import validate_identifier

from .common import AdapterError


ADAPTER_ID = "myosim-intent-event"
ADAPTER_VERSION = "1.0.0"
MYOSIM_V1_LABELS = frozenset({"REST", "OPEN", "CLOSE", "PINCH"})


@dataclass(frozen=True, slots=True)
class MyoSimIntentPayload:
    """Dependency-free representation exactly sufficient to create a MyoSim V1 IntentEvent."""

    timestamp_s: float
    label: str
    confidence: float
    source_subject: str | None
    modality: str
    model_version: str
    window_id: str | None
    source_intent_id: str


def intent_to_myosim_payload(
    intent: IntentRecord,
    *,
    label_map: Mapping[str, str],
    default_stream_time_seconds: float | None = None,
) -> MyoSimIntentPayload:
    """Validate and map an umbrella discrete intent to MyoSim's V1 vocabulary.

    Mapping is mandatory. No attempt is made to infer that a decoder label such
    as ``grip`` means ``CLOSE`` or that a continuous vector should become a
    discrete command. A missing replay timestamp is rejected unless a fixed,
    explicit default is supplied by the deterministic replay configuration.
    """
    if intent.label is None:
        raise AdapterError("MyoSim V1 requires a discrete IntentRecord label")
    if not label_map:
        raise AdapterError("MyoSim label_map must be explicit and non-empty")
    if intent.label not in label_map:
        raise AdapterError(f"no MyoSim V1 label mapping configured for intent label '{intent.label}'")
    mapped_label = str(label_map[intent.label]).upper()
    if mapped_label not in MYOSIM_V1_LABELS:
        raise AdapterError(
            f"mapped label '{mapped_label}' is unsupported; MyoSim V1 supports {sorted(MYOSIM_V1_LABELS)}"
        )
    timestamp = intent.stream_time_seconds
    if timestamp is None:
        timestamp = default_stream_time_seconds
    if timestamp is None:
        raise AdapterError("MyoSim V1 requires stream_time_seconds or an explicit replay default")
    if timestamp < 0:
        raise AdapterError("MyoSim replay timestamp must be non-negative")
    modality = "+".join(intent.modalities)
    return MyoSimIntentPayload(
        timestamp_s=float(timestamp),
        label=mapped_label,
        confidence=intent.confidence,
        source_subject=intent.subject_id,
        modality=modality,
        model_version=intent.model_version,
        window_id=intent.window_id,
        source_intent_id=intent.intent_id,
    )


def payload_to_myosim_event(payload: MyoSimIntentPayload) -> Any:
    """Construct a real MyoSim V1 ``IntentEvent`` using its stable public type.

    MyoSim remains an optional runtime dependency. Import happens only at this
    boundary; callers can validate payloads and generate replay bundles without
    it. If MyoSim is unavailable, no substitute control implementation is used.
    """
    try:
        from myosim.core.types import IntentEvent, IntentLabel  # type: ignore[import-not-found]
    except ImportError as exc:
        raise AdapterError(
            "MyoSim is not available in this runtime. Install/run MyoSim independently and retry the public IntentEvent bridge."
        ) from exc
    try:
        return IntentEvent(
            timestamp_s=payload.timestamp_s,
            label=IntentLabel(payload.label),
            confidence=payload.confidence,
            source_subject=payload.source_subject,
            modality=payload.modality,
            model_version=payload.model_version,
            window_id=payload.window_id,
        )
    except (TypeError, ValueError) as exc:
        raise AdapterError(f"MyoSim rejected the mapped intent payload: {exc}") from exc


def intent_to_myosim_event(
    intent: IntentRecord,
    *,
    label_map: Mapping[str, str],
    default_stream_time_seconds: float | None = None,
) -> Any:
    """Map and instantiate a real MyoSim event when MyoSim is installed."""
    return payload_to_myosim_event(
        intent_to_myosim_payload(
            intent,
            label_map=label_map,
            default_stream_time_seconds=default_stream_time_seconds,
        )
    )
