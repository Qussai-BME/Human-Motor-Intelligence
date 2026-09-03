from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from research_core.contracts import (
    ArtifactRecord,
    ArtifactRole,
    ContractValidationError,
    EvidenceClass,
    ExperimentRecord,
    IntentRecord,
    RunStatus,
    SignalProvenanceRecord,
    SignalRecord,
    ensure_real_benchmark_records,
)


def real_provenance() -> SignalProvenanceRecord:
    return SignalProvenanceRecord(
        origin=EvidenceClass.REAL,
        source_dataset_id="ninapro-db7",
        dataset_version="2026-accessed",
        license_id="credentialed-research-access",
        adapter_id="biosignal-fm-emg-export",
        adapter_version="4.0.0",
        details={"benchmark_eligible": True},
    )


def test_signal_record_is_immutable_json_safe_and_tracks_provenance() -> None:
    signal = SignalRecord(
        signal_id="emg-window-0001",
        modality="EMG",
        sampling_rate_hz=2000,
        channel_names=("ch1", "ch2"),
        units=("mV",),
        sample_count=400,
        provenance=real_provenance(),
        subject_id="subject-01",
        session_id="session-01",
        window_id="window-0001",
    )

    serialized = signal.to_dict()
    assert serialized["contract_kind"] == "signal"
    assert serialized["modality"] == "emg"
    assert serialized["provenance"]["origin"] == "real"
    assert len(signal.content_hash()) == 64
    with pytest.raises(FrozenInstanceError):
        signal.modality = "eeg"  # type: ignore[misc]


def test_synthetic_provenance_requires_explicit_reason_and_is_not_benchmark_eligible() -> None:
    with pytest.raises(ContractValidationError, match="requires fallback_reason"):
        SignalProvenanceRecord(origin=EvidenceClass.SYNTHETIC)

    provenance = SignalProvenanceRecord(
        origin=EvidenceClass.SYNTHETIC,
        fallback_reason="deterministic contract smoke fixture",
        details={"benchmark_eligible": False},
    )
    assert provenance.benchmark_eligible is False


def test_intent_requires_single_semantic_output_and_normalized_probabilities() -> None:
    provenance = real_provenance()
    record = IntentRecord(
        intent_id="intent-001",
        confidence=0.91,
        source_model_id="myocontrol-xgb",
        model_version="0.5.0",
        modalities=("emg",),
        provenance=provenance,
        label="OPEN",
        probabilities={"OPEN": 0.91, "REST": 0.09},
        stream_time_seconds=1.25,
        subject_id="subject-01",
        window_id="window-001",
    )
    assert record.label == "OPEN"
    assert record.stream_time_seconds == 1.25
    assert record.to_dict()["probabilities"] == {"OPEN": 0.91, "REST": 0.09}

    with pytest.raises(ContractValidationError, match="exactly one"):
        IntentRecord(
            intent_id="invalid-intent",
            confidence=0.5,
            source_model_id="decoder",
            model_version="1.0.0",
            modalities=("emg",),
            provenance=provenance,
        )
    with pytest.raises(ContractValidationError, match="sum to one"):
        IntentRecord(
            intent_id="invalid-probabilities",
            confidence=0.5,
            source_model_id="decoder",
            model_version="1.0.0",
            modalities=("emg",),
            provenance=provenance,
            label="OPEN",
            probabilities={"OPEN": 0.8},
        )


def test_terminal_experiment_requires_completion_and_benchmark_guard_rejects_synthetic() -> None:
    common = dict(
        experiment_id="exp-emg-smoke",
        run_id="run-emg-smoke",
        project_id="myoadapt",
        protocol_id="emg-loso-v1",
        dataset_id="ninapro-db7",
        dataset_version="credentialed",
        modality="emg",
        subject_split="leave-one-subject-out",
        model_id="xgboost",
        model_version="1.0.0",
        seed=42,
        configuration_hash="a" * 64,
    )
    with pytest.raises(ContractValidationError, match="completed_at_utc"):
        ExperimentRecord(status=RunStatus.SUCCEEDED, **common)

    synthetic = ExperimentRecord(
        status=RunStatus.SUCCEEDED,
        completed_at_utc="2026-08-22T12:00:00+00:00",
        metadata={"synthetic": True, "benchmark_eligible": False},
        **common,
    )
    with pytest.raises(ContractValidationError, match="ineligible"):
        ensure_real_benchmark_records((synthetic,))


def test_artifact_rejects_secret_bearing_uri() -> None:
    with pytest.raises(ContractValidationError, match="credentials"):
        ArtifactRecord(
            artifact_id="artifact-001",
            role=ArtifactRole.MANIFEST,
            uri="https://token@example.invalid/manifest.json",
            producing_run_id="run-001",
        )
