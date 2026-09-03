"""Protocol-facing study preparation components."""

from .eeg import EEGBaselineFamily, EEGBaselinePlan, bci_iv_2a_baseline_plans
from .fusion import (
    FusionPreparationError,
    FusionStrategy,
    FusionStudyPlan,
    MissingModalityCondition,
    ModalityRepresentationReference,
    validate_fusion_pair,
)

__all__ = [
    "EEGBaselineFamily",
    "EEGBaselinePlan",
    "bci_iv_2a_baseline_plans",
    "FusionPreparationError",
    "FusionStrategy",
    "FusionStudyPlan",
    "MissingModalityCondition",
    "ModalityRepresentationReference",
    "validate_fusion_pair",
]
