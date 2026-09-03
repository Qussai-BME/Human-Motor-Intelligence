from __future__ import annotations

import pytest

from research_core.contracts import EvidenceClass, RepresentationRecord, SignalProvenanceRecord
from research_core.protocols import (
    FusionPreparationError,
    FusionStrategy,
    FusionStudyPlan,
    MissingModalityCondition,
    ModalityRepresentationReference,
    bci_iv_2a_baseline_plans,
    validate_fusion_pair,
)


def representation(modality: str, identifier: str) -> RepresentationRecord:
    return RepresentationRecord(
        representation_id=identifier,
        modality=modality,
        encoder_id=f"{modality}-encoder",
        model_version="test-v1",
        dimension=2,
        input_signal_ids=(f"{modality}-signal",),
        provenance=SignalProvenanceRecord(
            origin=EvidenceClass.SYNTHETIC,
            fallback_reason="fusion scaffold unit fixture",
        ),
        values=(0.1, 0.2),
    )


def fusion_plan() -> FusionStudyPlan:
    return FusionStudyPlan(
        plan_id="fusion-plan-v1",
        protocol_id="emg-eeg-fusion-v1",
        strategy=FusionStrategy.EARLY_CONCATENATION,
        task_id="grasp-lift",
        alignment_tolerance_seconds=0.01,
        missing_modality_conditions=(
            MissingModalityCondition.BOTH_PRESENT,
            MissingModalityCondition.EEG_MISSING,
            MissingModalityCondition.EMG_MISSING,
        ),
    )


def test_fusion_scaffold_validates_matched_metadata_without_claiming_result() -> None:
    eeg = ModalityRepresentationReference(representation("eeg", "eeg-repr"), "subject-01", "session-01", 1.0, 2.0)
    emg = ModalityRepresentationReference(representation("emg", "emg-repr"), "subject-01", "session-01", 1.005, 2.005)
    result = validate_fusion_pair(fusion_plan(), eeg, emg, MissingModalityCondition.BOTH_PRESENT)

    assert result["alignment_checked"] is True
    assert result["representation_ids"] == {"eeg": "eeg-repr", "emg": "emg-repr"}
    assert "no fusion performance" in result["claim_boundary"]


def test_fusion_scaffold_rejects_misalignment_and_undeclared_missing_conditions() -> None:
    eeg = ModalityRepresentationReference(representation("eeg", "eeg-repr"), "subject-01", "session-01", 1.0, 2.0)
    emg = ModalityRepresentationReference(representation("emg", "emg-repr"), "subject-01", "session-01", 1.2, 2.2)
    with pytest.raises(FusionPreparationError, match="alignment tolerance"):
        validate_fusion_pair(fusion_plan(), eeg, emg, MissingModalityCondition.BOTH_PRESENT)
    with pytest.raises(FusionPreparationError, match="requires only an EMG"):
        validate_fusion_pair(fusion_plan(), eeg, emg, MissingModalityCondition.EEG_MISSING)


def test_eeg_baseline_plan_starts_with_simple_comparators() -> None:
    plans = bci_iv_2a_baseline_plans()
    assert [plan.baseline_id for plan in plans[:3]] == ["eeg-linear-v1", "eeg-lda-v1", "eeg-spectral-v1"]
    assert plans[3].readiness == "deferred_until_simple_baselines"
    assert all("No result exists" in plan.evidence_boundary for plan in plans)
