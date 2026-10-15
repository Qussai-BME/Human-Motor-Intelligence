# Six-Paper Claim Audit — Public Release 1.1.0

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `papers/P2_SUPERSESSION_NOTICE.md`.


**Date:** 2026-10-05  
**Purpose:** one authoritative public statement of the strongest defensible interpretation of each paper record.

| Paper | Current evidence status | Strongest supported public statement | Not supported by this release |
|---|---|---|---|
| P1 | Frozen/submitted record | Rest-inclusive metrics can obscure active-gesture performance in its declared NinaPro benchmark. | Universal rest-inflation effect across datasets/tasks. |
| P2 | Manuscript/evidence record at documented supervisory stage | Alignment behaviour is representation/protocol dependent in the declared MiniROCKET study. | Pooled generalization beyond the declared protocol. |
| P3 | Qualified external evidence archive | Lite-DAN and controls were evaluated across the declared NinaPro cohorts with mixed results. | A universal adaptation winner or umbrella-level superiority claim. |
| P4 | Complete protocol-specific external validation | Strict zero-calibration external EEG validation was performed under the declared OpenBMI LOSO protocol; no Holm-surviving universal pairwise winner is established. | Universal decoder superiority or clinical efficacy. |
| P5 | Complete protocol-specific external validation | The amended Jeong2020 cohort did not establish a Holm-supported EEG-EMG fusion gain over EEG-only under the tested rules. | General failure of multimodal fusion or hardware/clinical claims. |
| P6 | **Exploratory/inconclusive R03 evidence** | Three decoder configurations generated 60 held-out traces and were replayed through one deterministic MyoSim configuration; all 60 tasks failed to reach `COMPLETE`, and the continuous endpoints showed no detectable omnibus differences. | Motor-imagery confirmation, decoder-quality dose-response, equivalence/no-effect claim, human/online control, prosthetic readiness, clinical efficacy, or hardware safety. |

## P6 governing limitation

The released P6 execution uses PhysioNet EEGMMIDB **R03**, which is motor execution. It must not be described as motor imagery. The source T1/T2 labels are retained and mapped to generic OPEN/CLOSE simulator intents through an explicitly named abstract software-interface mapping; that mapping is not a validated physiological or prosthetic semantic mapping.

The supplied rerun matches the primary aggregate, but its individual 60 per-run MyoSim JSON task artefacts are absent. The public claim is therefore aggregate equality only, not fully auditable run-by-run independent rerun execution.

Publication status is separate from evidence status. No journal acceptance, peer review outcome, or supervisor approval is asserted by this archive.
