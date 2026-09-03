from __future__ import annotations

import json

import pytest

from research_core.contracts import ExperimentRecord, RunStatus
from research_core.registry import (
    DatasetAccess,
    DatasetDefinition,
    LocalResearchRegistry,
    ProtocolDefinition,
    ProtocolStatus,
    RegistryError,
    StatisticalUnit,
)


def dataset_card() -> DatasetDefinition:
    return DatasetDefinition(
        entity_id="ninapro-db7",
        name="NinaPro DB7",
        modality="emg",
        source_url="https://ninapro.hevs.ch/",
        citation="Atzori et al.; dataset access page recorded by registry maintainer.",
        license_access=DatasetAccess.REGISTRATION_REQUIRED,
        sampling_rate_hz=2000.0,
        channel_description="Dataset-defined sEMG channels; see source documentation.",
        task_description="Gesture classification research.",
        subject_count=22,
        session_description="Dataset-defined sessions.",
        label_schema={"source_of_truth": "dataset documentation"},
        canonicalization_rules=("Use externally documented subject identifiers.",),
        known_limitations=("Raw data remains external and requires authorized access.",),
        version="external-accessed-2026",
    )


def protocol_card() -> ProtocolDefinition:
    return ProtocolDefinition(
        entity_id="emg-loso-v1",
        name="EMG LOSO",
        version="1.0.0",
        modalities=("emg",),
        split_strategy="leave-one-subject-out",
        train_validation_test_semantics="Held-out subject is never used for train, selection, or fitting.",
        leakage_constraints=(
            "Fit scaling using training data only.",
            "Fit feature selection using training data only.",
            "Aggregate statistical inference at subject level.",
        ),
        preprocessing={"owner": "external project configuration"},
        feature_selection={"owner": "external project configuration"},
        model_selection={"owner": "external project configuration"},
        metrics=("accuracy", "macro_f1", "active_only_f1", "rest_recall"),
        statistical_unit=StatisticalUnit.SUBJECT,
        seeds=(42,),
        hyperparameter_policy="Select using training-side validation only.",
        status=ProtocolStatus.ACTIVE,
    )


def completed_experiment() -> ExperimentRecord:
    return ExperimentRecord(
        experiment_id="exp-001",
        run_id="run-001",
        project_id="myoadapt",
        protocol_id="emg-loso-v1",
        dataset_id="ninapro-db7",
        dataset_version="external-accessed-2026",
        modality="emg",
        subject_split="leave-one-subject-out",
        model_id="xgboost",
        model_version="1.0.0",
        seed=42,
        configuration_hash="c" * 64,
        status=RunStatus.SUCCEEDED,
        completed_at_utc="2026-08-22T12:00:00+00:00",
        metrics={"accuracy": 0.0},
        metadata={"benchmark_eligible": False, "fixture": True},
    )


def test_registry_persists_typed_metadata_without_raw_data(tmp_path) -> None:
    registry = LocalResearchRegistry(tmp_path / "registry")
    card = dataset_card()
    stored = registry.register(card)
    repeated = registry.register(card)

    assert stored.entity_type == "dataset"
    assert repeated.content_hash == stored.content_hash
    document = json.loads((tmp_path / "registry" / "registry.json").read_text())
    persisted = document["entities"]["dataset"]["ninapro-db7"]["document"]
    assert "data" not in persisted
    assert persisted["source_url"] == "https://ninapro.hevs.ch/"


def test_registry_rejects_undocumented_entity_replacement(tmp_path) -> None:
    registry = LocalResearchRegistry(tmp_path / "registry")
    registry.register(dataset_card())
    baseline = dataset_card()
    revised = DatasetDefinition(
        entity_id=baseline.entity_id,
        name=baseline.name,
        modality=baseline.modality,
        source_url=baseline.source_url,
        citation=baseline.citation,
        license_access=baseline.license_access,
        sampling_rate_hz=baseline.sampling_rate_hz,
        channel_description=baseline.channel_description,
        task_description=baseline.task_description,
        subject_count=baseline.subject_count,
        session_description=baseline.session_description,
        label_schema=baseline.label_schema,
        canonicalization_rules=baseline.canonicalization_rules,
        known_limitations=("Different limitation.",),
        version=baseline.version,
        created_at_utc=baseline.created_at_utc,
        metadata=baseline.metadata,
    )
    with pytest.raises(RegistryError, match="already exists"):
        registry.register(revised)
    replaced = registry.register(revised, replace=True, event_context={"reason": "source correction"})
    assert replaced.entity_id == "ninapro-db7"


def test_protocol_requires_subject_level_leakage_controls_and_run_is_queryable(tmp_path) -> None:
    registry = LocalResearchRegistry(tmp_path / "registry")
    protocol = registry.register(protocol_card())
    experiment_entry, run_entry = registry.register_experiment_run(completed_experiment())

    assert protocol.entity_id == "emg-loso-v1"
    assert experiment_entry.entity_type == "experiment"
    assert run_entry.entity_type == "run"
    assert registry.query_runs(protocol_id="emg-loso-v1") == (run_entry,)
    assert registry.query_runs(model_id="unregistered") == ()


def test_registry_detects_manual_document_tampering(tmp_path) -> None:
    registry = LocalResearchRegistry(tmp_path / "registry")
    registry.register(dataset_card())
    path = tmp_path / "registry" / "registry.json"
    document = json.loads(path.read_text())
    document["entities"]["dataset"]["ninapro-db7"]["document"]["name"] = "tampered"
    path.write_text(json.dumps(document), encoding="utf-8")

    with pytest.raises(RegistryError, match="integrity failure"):
        registry.get("dataset", "ninapro-db7")
