from __future__ import annotations

import pytest

from research_core.adapters import AdapterError, intent_to_myosim_event, intent_to_myosim_payload
from research_core.contracts import EvidenceClass, IntentRecord, SignalProvenanceRecord


def source_intent(*, label: str | None = "open_hand", stream_time_seconds: float | None = 0.25) -> IntentRecord:
    kwargs = {"label": label} if label is not None else {"values": (0.1, 0.2)}
    return IntentRecord(
        intent_id="intent-001",
        timestamp_utc="2026-08-22T12:00:00+00:00",
        confidence=0.9,
        source_model_id="myocontrol-classical-decoder",
        model_version="0.5",
        modalities=("emg",),
        provenance=SignalProvenanceRecord(
            origin=EvidenceClass.SYNTHETIC,
            fallback_reason="adapter unit fixture",
        ),
        stream_time_seconds=stream_time_seconds,
        subject_id="subject-01",
        window_id="window-01",
        **kwargs,
    )


def test_myosim_payload_requires_explicit_mapping_and_retains_provenance() -> None:
    payload = intent_to_myosim_payload(
        source_intent(),
        label_map={"open_hand": "OPEN"},
    )
    assert payload.label == "OPEN"
    assert payload.timestamp_s == 0.25
    assert payload.source_subject == "subject-01"
    assert payload.window_id == "window-01"


def test_myosim_runtime_bridge_constructs_public_intent_event() -> None:
    pytest.importorskip("myosim")
    event = intent_to_myosim_event(
        source_intent(),
        label_map={"open_hand": "OPEN"},
    )
    assert event.label.value == "OPEN"
    assert event.timestamp_s == 0.25
    assert event.confidence == 0.9


def test_myosim_payload_rejects_guessed_labels_continuous_intents_and_missing_time() -> None:
    with pytest.raises(AdapterError, match="no MyoSim V1 label mapping"):
        intent_to_myosim_payload(source_intent(), label_map={"close_hand": "CLOSE"})
    with pytest.raises(AdapterError, match="requires a discrete"):
        intent_to_myosim_payload(source_intent(label=None), label_map={"anything": "OPEN"})
    with pytest.raises(AdapterError, match="requires stream_time_seconds"):
        intent_to_myosim_payload(
            source_intent(stream_time_seconds=None),
            label_map={"open_hand": "OPEN"},
        )
    with pytest.raises(AdapterError, match="unsupported"):
        intent_to_myosim_payload(source_intent(), label_map={"open_hand": "WAVE"})
