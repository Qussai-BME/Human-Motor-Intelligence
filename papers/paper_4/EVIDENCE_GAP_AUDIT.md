# P4 Evidence-Gap Audit — V2 Recovery R3

## Current Evidence Is Sufficient For

P4 supports a reproducible, external, zero-calibration binary MI LOSO evaluation on 54 OpenBMI subjects. It supports descriptive comparison of five predeclared pipelines and the corrected conclusion that no individual pairwise superiority claim survived Holm adjustment.

## Gaps That Remain

| Gap | Why R1 cannot answer it | Required future evidence | Current status |
|---|---|---|---|
| Second external EEG cohort | One cohort cannot quantify source-to-source robustness | New source selection matrix, license/provenance checks, prospectively locked protocol | YELLOW |
| Cross-session robustness | R1 uses declared `ses-1` acquisitions only | Session-transfer protocol with leakage safeguards | YELLOW |
| Clinical population relevance | OpenBMI cohort is healthy | Approved patient/clinical study with distinct endpoints | RED |
| Calibration trade-off | No target calibration was permitted | Separate prospective calibration-ablation study | YELLOW |
| Broad architecture comparison | Five models are intentionally limited | New registered benchmark; no post-hoc additions to R1 | YELLOW |
| Online/device control relevance | Offline epoch outcomes only | Real-time hardware or validated closed-loop study | RED |

## Non-Remedies

No gap may be addressed by reselecting OpenBMI subjects, retuning models, changing epoch bands, adding an architecture, or reusing the held-out data under the P4 R1 namespace. Such actions would be post-result scope drift, not evidence expansion.
