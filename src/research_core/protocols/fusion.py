"""Validated preparation contracts for future EEG–EMG fusion studies.

This module deliberately does not implement a fusion model. It makes the study
conditions required to test fusion explicit: independently produced
representations, alignment metadata, a declared strategy, and planned
missing-modality conditions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Any

from research_core.contracts import RepresentationRecord
from research_core.contracts.base import ContractValidationError, validate_identifier, validate_non_empty


class FusionPreparationError(ValueError):
    """Raised when a future fusion study lacks explicit, comparable inputs."""


class FusionStrategy(StrEnum):
    """Declared strategy family; performance remains an empirical question."""

    EARLY_CONCATENATION = "early_concatenation"
    LATE_SCORE_FUSION = "late_score_fusion"
    LEARNED_CROSS_MODAL = "learned_cross_modal"


class MissingModalityCondition(StrEnum):
    """Conditions which must be considered before a robustness claim is made."""

    BOTH_PRESENT = "both_present"
    EEG_MISSING = "eeg_missing"
    EMG_MISSING = "emg_missing"


@dataclass(frozen=True, slots=True)
class ModalityRepresentationReference:
    """One time-aligned representation reference with participant/session context."""

    representation: RepresentationRecord
    subject_id: str
    session_id: str
    window_start_seconds: float
    window_end_seconds: float

    def __post_init__(self) -> None:
        if self.representation.modality not in {"eeg", "emg"}:
            raise FusionPreparationError("fusion scaffold currently accepts EEG and EMG representation records only")
        object.__setattr__(self, "subject_id", validate_identifier(self.subject_id, "subject_id"))
        object.__setattr__(self, "session_id", validate_identifier(self.session_id, "session_id"))
        start, end = float(self.window_start_seconds), float(self.window_end_seconds)
        if not all(isfinite(value) for value in (start, end)) or start < 0 or start >= end:
            raise FusionPreparationError("window bounds must be finite, non-negative, and strictly increasing")
        object.__setattr__(self, "window_start_seconds", start)
        object.__setattr__(self, "window_end_seconds", end)


@dataclass(frozen=True, slots=True)
class FusionStudyPlan:
    """Protocol-facing fusion study declaration, not a result-producing model config."""

    plan_id: str
    protocol_id: str
    strategy: FusionStrategy
    task_id: str
    alignment_tolerance_seconds: float
    missing_modality_conditions: tuple[MissingModalityCondition, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "plan_id", validate_identifier(self.plan_id, "plan_id"))
        object.__setattr__(self, "protocol_id", validate_identifier(self.protocol_id, "protocol_id"))
        object.__setattr__(self, "task_id", validate_non_empty(self.task_id, "task_id"))
        if not isinstance(self.strategy, FusionStrategy):
            object.__setattr__(self, "strategy", FusionStrategy(self.strategy))
        tolerance = float(self.alignment_tolerance_seconds)
        if not isfinite(tolerance) or tolerance < 0:
            raise FusionPreparationError("alignment_tolerance_seconds must be finite and non-negative")
        object.__setattr__(self, "alignment_tolerance_seconds", tolerance)
        conditions = tuple(
            condition if isinstance(condition, MissingModalityCondition) else MissingModalityCondition(condition)
            for condition in self.missing_modality_conditions
        )
        required = {
            MissingModalityCondition.BOTH_PRESENT,
            MissingModalityCondition.EEG_MISSING,
            MissingModalityCondition.EMG_MISSING,
        }
        if not required.issubset(set(conditions)):
            raise FusionPreparationError(
                "fusion plan must declare both_present, eeg_missing, and emg_missing conditions"
            )
        object.__setattr__(self, "missing_modality_conditions", tuple(dict.fromkeys(conditions)))


def validate_fusion_pair(
    plan: FusionStudyPlan,
    eeg: ModalityRepresentationReference | None,
    emg: ModalityRepresentationReference | None,
    condition: MissingModalityCondition,
) -> dict[str, Any]:
    """Validate one planned fusion condition and return factual alignment metadata.

    This function never produces an output embedding, prediction, or metric. It
    only proves that a proposed experimental sample satisfies its declared
    condition and alignment metadata requirements.
    """
    if not isinstance(condition, MissingModalityCondition):
        condition = MissingModalityCondition(condition)
    if condition not in plan.missing_modality_conditions:
        raise FusionPreparationError("condition was not declared in the fusion study plan")
    if condition is MissingModalityCondition.BOTH_PRESENT:
        if eeg is None or emg is None:
            raise FusionPreparationError("both_present condition requires EEG and EMG references")
    elif condition is MissingModalityCondition.EEG_MISSING:
        if eeg is not None or emg is None:
            raise FusionPreparationError("eeg_missing condition requires only an EMG reference")
    else:
        if eeg is None or emg is not None:
            raise FusionPreparationError("emg_missing condition requires only an EEG reference")
    present = tuple(reference for reference in (eeg, emg) if reference is not None)
    if len(present) == 2:
        first, second = present
        if first.subject_id != second.subject_id or first.session_id != second.session_id:
            raise FusionPreparationError("EEG and EMG references must have identical subject and session IDs")
        start_delta = abs(first.window_start_seconds - second.window_start_seconds)
        end_delta = abs(first.window_end_seconds - second.window_end_seconds)
        if start_delta > plan.alignment_tolerance_seconds or end_delta > plan.alignment_tolerance_seconds:
            raise FusionPreparationError("EEG and EMG windows exceed declared alignment tolerance")
    reference = present[0]
    return {
        "plan_id": plan.plan_id,
        "protocol_id": plan.protocol_id,
        "condition": condition.value,
        "subject_id": reference.subject_id,
        "session_id": reference.session_id,
        "representation_ids": {item.representation.modality: item.representation.representation_id for item in present},
        "alignment_checked": len(present) == 2,
        "claim_boundary": "validated study-input metadata only; no fusion performance or robustness result",
    }
