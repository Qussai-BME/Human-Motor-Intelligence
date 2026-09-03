from __future__ import annotations

from research_core.adapters import (
    import_myoadapt_manifest,
    intent_from_myocontrol_prediction,
    representation_from_biosignal_fm_export,
    signal_from_biosignal_fm_export,
)
from research_core.contracts import EvidenceClass, RunStatus


def test_myocontrol_adapter_requires_explicit_context_and_preserves_public_prediction() -> None:
    intent = intent_from_myocontrol_prediction(
        {"predicted_class": "open_hand", "confidence": 0.8, "probabilities": {"open_hand": 0.8, "rest": 0.2}},
        intent_id="intent-001",
        timestamp_utc="2026-08-22T12:00:00+00:00",
        source_model_id="myocontrol-classical-decoder",
        model_version="0.5",
        stream_time_seconds=0.5,
        subject_id="subject-01",
        window_id="window-01",
        external_provenance={"origin": "synthetic", "fallback_reason": "adapter test fixture"},
    )
    assert intent.label == "open_hand"
    assert intent.modalities == ("emg",)
    assert intent.provenance.origin is EvidenceClass.SYNTHETIC
    assert intent.metadata["external_prediction_schema"] == "myocontrol-classification-result"


def test_biosignal_fm_adapters_map_public_export_without_package_import() -> None:
    signal = signal_from_biosignal_fm_export(
        {
            "signal_id": "signal-001",
            "sample_count": 100,
            "data_uri": "signals/signal-001.npy",
            "metadata": {
                "modality": "eeg",
                "sampling_rate_hz": 250,
                "channel_names": ["C3", "C4"],
                "units": ["uV"],
                "subject_id": "s01",
                "session_id": "train",
                "provenance": {"origin": "unknown"},
            },
        }
    )
    representation = representation_from_biosignal_fm_export(
        {
            "representation_id": "representation-001",
            "modality": "eeg",
            "encoder_id": "external-encoder",
            "model_version": "4",
            "dimension": 3,
            "input_signal_ids": ["signal-001"],
            "values": [0.1, 0.2, 0.3],
            "provenance": {"origin": "unknown"},
        }
    )
    assert signal.provenance.benchmark_eligible is False
    assert representation.dimension == 3
    assert representation.values == (0.1, 0.2, 0.3)


def test_myoadapt_manifest_import_retains_source_reference_but_defaults_to_nonbenchmark() -> None:
    bundle = import_myoadapt_manifest(
        {
            "schema_version": "1.0",
            "run_name": "external-run",
            "dataset": "NinaPro-DB7",
            "model": "xgboost",
            "seed": 42,
            "config": {"k_features": 308},
            "environment": {"python": "3.12"},
            "environment_hash_sha256": "external-hash",
            "git": {"commit": "abc123"},
            "outputs": [{"path": "results.csv", "role": "metrics", "sha256": "a" * 64, "size_bytes": 10}],
        },
        manifest_uri="external/myoadapt/manifest.json",
        experiment_id="experiment-001",
        run_id="run-001",
        protocol_id="emg-loso-v1",
        dataset_id="ninapro-db7",
        dataset_version="external-accessed-2026",
        modality="emg",
        subject_split="leave-one-subject-out",
    )
    assert bundle.experiment.status is RunStatus.IMPORTED
    assert bundle.experiment.benchmark_eligible is False
    assert bundle.artifacts[0].uri == "external/myoadapt/manifest.json"
    assert bundle.artifacts[1].sha256 == "a" * 64
