# Claim–Evidence Matrix — V2 Recovery R1

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


| ID | Claim or status statement | Classification | Evidence artefact(s) | Exact boundary |
|---|---|---|---|---|
| CE-01 | P1 observes rest-related metric divergence in its stated DB3 LOSO analysis. | Source-grounded | P1 DOCX; manuscript source text (not distributed); `EMG_SERIES_MASTER_EVIDENCE.md` | P1 data/model/policy only. |
| CE-02 | P2’s adaptation mechanism is MiniROCKET representation-specific. | Source-grounded | P2 DOCX; P2 extract; EMG master record | Do not generalize to all adaptation. |
| CE-03 | P3 evidence is pending. | Pending | `EMG_SERIES_MASTER_EVIDENCE.md` | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`**. |
| CE-04 | P4 uses 54 OpenBMI subjects, binary left/right labels, 62 named channels, and 200 derived trials/subject. | Verified external protocol | P4 `protocol.json`; cache provenance; P4 manifest/validation | External OpenBMI only; not BCI IV-2a. |
| CE-05 | P4 D1 passed for 108 artefacts and 933,572,109 bytes. | Verified integrity | `datasets/manifests/nemar_nm000338_openbmi_v2_recovery_r1.json` | Derived cache only; raw BDF excluded. |
| CE-06 | P4 D2–D5 passed before model fitting. | Verified validation | P4 primary `validation.json` | Recovery R1 implementation and cache only. |
| CE-07 | P4 macro-F1 means range from 0.5962 to 0.6364 across five conditions. | Result | P4 `subject_level_results.csv`; `results.json`; `statistics_macro_f1.json` | Subject-level OpenBMI binary MI only. |
| CE-08 | P4 Friedman χ²=16.16, *p*=0.00281. | Result | `statistics_macro_f1.json` | Five fixed within-OpenBMI conditions. |
| CE-09 | No P4 pairwise comparison survives Holm; minimum adjusted *p*=0.1042. | Result / negative conclusion | `statistics_macro_f1.json` | Does not negate omnibus difference or prove all models equal. |
| CE-10 | P4 primary and rerun subject-level CSV are byte-identical. | Reproducibility verified | Both CSVs; SHA-256 comparison; `V2_P4_OPENBMI_EXTERNAL_VALIDATION_AUDIT_RECOVERY_R1.md` | Execution reproducibility, not new biological cohort. |
| CE-11 | P4 is external validation, not direct replication. | Protocol identity | P4 protocol, manifest, audit | Do not cross-rank with BCI IV-2a. |
| CE-12 | P5 Jeong external analysis did not run. | Source gate | `V2_P5_JEONG_AVAILABILITY_HARD_STOP.md`; event inventory | Not a fusion null result. |
| CE-13 | `sub-23` lacks run-2 and twist labels in selected P5 derivative. | Verified source availability | `audit/jeong_ses0_event_inventory.json`; hard-stop audit | Selected NEMAR v1.0.2 `ses-0` source only. |
| CE-14 | Frozen Cho2017 transparent fusion has no Holm-surviving fusion advantage over EMG-only. | Frozen historical result | V1.1 provenance as described in master audit | Do not rewrite/recompute as V2 or generalize to all fusion. |
| CE-15 | P6 repeated real replay did not run. | Capability gate | `V2_P6_REPLAY_VARIABILITY_CAPABILITY_HARD_STOP.md` | Not a systems null result. |
| CE-16 | Current MyoSim seed/reset does not expose seed-dependent state/task/replay variation. | Source-code capability finding | Inspected MyoSim runner/backend paths; P6 audit | Applies to inspected V1.1 implementation. |
| CE-17 | Synthetic controlled corruption is non-benchmark evidence. | Governance rule | V2 master audit and frozen synthetic policy | Must retain origin/eligibility labels. |
