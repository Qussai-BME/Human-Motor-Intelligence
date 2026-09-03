"""EEG research-track baseline planning without a claim-producing training implementation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from research_core.contracts.base import validate_identifier, validate_non_empty


class EEGBaselineFamily(StrEnum):
    """Baseline families required to test whether complexity adds value."""

    LINEAR = "linear"
    LDA = "lda"
    SPECTRAL = "spectral"
    LIGHTWEIGHT_CNN_TCN = "lightweight_cnn_tcn"
    LIGHTWEIGHT_TRANSFORMER = "lightweight_transformer"
    DOMAIN_GENERALISATION = "domain_generalisation"


@dataclass(frozen=True, slots=True)
class EEGBaselinePlan:
    """A registered baseline definition with a clear scientific role and readiness state."""

    baseline_id: str
    family: EEGBaselineFamily
    protocol_id: str
    input_description: str
    selection_policy: str
    readiness: str
    evidence_boundary: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "baseline_id", validate_identifier(self.baseline_id, "baseline_id"))
        object.__setattr__(self, "protocol_id", validate_identifier(self.protocol_id, "protocol_id"))
        if not isinstance(self.family, EEGBaselineFamily):
            object.__setattr__(self, "family", EEGBaselineFamily(self.family))
        for field_name in ("input_description", "selection_policy", "readiness", "evidence_boundary"):
            object.__setattr__(self, field_name, validate_non_empty(getattr(self, field_name), field_name))


def bci_iv_2a_baseline_plans() -> tuple[EEGBaselinePlan, ...]:
    """Return an ordered baseline plan for the BCI IV-2a research track.

    This is a planning artifact only. It does not represent model training,
    cross-subject performance, or a validated preprocessing choice.
    """
    protocol_id = "eeg-loso-v1"
    boundary = "No result exists until authorized data, a registered run, and protocol-compliant analysis are available."
    return (
        EEGBaselinePlan(
            baseline_id="eeg-linear-v1",
            family=EEGBaselineFamily.LINEAR,
            protocol_id=protocol_id,
            input_description="Training-only normalized epoch features under registered preprocessing.",
            selection_policy="Predeclare linear feature representation and fit all transforms on training participants only.",
            readiness="planned",
            evidence_boundary=boundary,
        ),
        EEGBaselinePlan(
            baseline_id="eeg-lda-v1",
            family=EEGBaselineFamily.LDA,
            protocol_id=protocol_id,
            input_description="Protocol-declared spectral or spatial features; appropriateness reviewed per task.",
            selection_policy="Use only training-side validation for any component selection.",
            readiness="planned",
            evidence_boundary=boundary,
        ),
        EEGBaselinePlan(
            baseline_id="eeg-spectral-v1",
            family=EEGBaselineFamily.SPECTRAL,
            protocol_id=protocol_id,
            input_description="Registered spectral/time-frequency representation of declared EEG epochs.",
            selection_policy="Lock frequency/window settings before held-out participant evaluation.",
            readiness="planned",
            evidence_boundary=boundary,
        ),
        EEGBaselinePlan(
            baseline_id="eeg-lightweight-cnn-tcn-v1",
            family=EEGBaselineFamily.LIGHTWEIGHT_CNN_TCN,
            protocol_id=protocol_id,
            input_description="Raw or registered time-frequency epoch tensors with explicit split and seed controls.",
            selection_policy="Run only after simple baselines are registered under matching protocol conditions.",
            readiness="deferred_until_simple_baselines",
            evidence_boundary=boundary,
        ),
        EEGBaselinePlan(
            baseline_id="eeg-lightweight-transformer-v1",
            family=EEGBaselineFamily.LIGHTWEIGHT_TRANSFORMER,
            protocol_id=protocol_id,
            input_description="Protocol-declared EEG epochs and positional/time representation.",
            selection_policy="Requires documented justification after simpler matched baselines.",
            readiness="deferred_until_justified",
            evidence_boundary=boundary,
        ),
        EEGBaselinePlan(
            baseline_id="eeg-domain-generalisation-v1",
            family=EEGBaselineFamily.DOMAIN_GENERALISATION,
            protocol_id=protocol_id,
            input_description="Participant-domain-aware training data under strict held-out-participant constraints.",
            selection_policy="No held-out participant labels or unlabeled exposure unless a separately named protocol permits it.",
            readiness="planned_after_unimodal_baselines",
            evidence_boundary=boundary,
        ),
    )
