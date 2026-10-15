# Q1 Evidence Expansion Master Audit — V2 Recovery R1

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


**Programme:** Human Motor Intelligence  
**Version:** V2.0 Recovery R1  
**Purpose:** Evidence-governance audit for the six-paper programme  
**Core question:** How can biomedical AI decode human motor intent robustly across individuals without subject-specific calibration?

## Executive Status

The V2 programme proceeded under a two-tier evidence model. Frozen V1/V1.1 evidence is not overwritten, re-run into legacy paths, or silently reinterpreted. The sandbox reset required a separately identified Recovery R1 execution namespace. The new P4 external validation completed with D1–D5, subject-level statistics, an exact independent rerun, and a protocol-qualified negative pairwise result. P5 is stopped at the source-coverage gate, and P6 is stopped at the simulator-independence gate. Neither stop is a missing result disguised as a null result.

| Paper | Research identity | V2 status | Evidence classification |
|---|---|---|---|
| P1 | Rest-class metric inflation in cross-subject sEMG | Source integrated; manuscript not rewritten | Author-supplied, source-grounded |
| P2 | MiniROCKET/domain-adaptation mechanism analysis | Source integrated; manuscript not rewritten | Author-supplied, source-grounded |
| P3 | Companion EMG work | Awaiting package | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** |
| P4 | Strict zero-calibration cross-subject EEG MI | Completed external OpenBMI validation | V2 Recovery R1, externally validated and reproducibility-verified |
| P5 | Transparent EEG–EMG fusion under LOSO | Halted before model run | Source coverage insufficient for locked 25-subject cohort |
| P6 | Decoder-quality/control replay relationship | Halted before repeat cohort | Deterministic runtime lacks a valid independent variation factor |

## Evidence Tiers and Preservation

| Tier | Status | Rule |
|---|---|---|
| Tier A — V1/V1.1 | Frozen historical evidence | Do not overwrite result paths, rerun them into legacy locations, or upgrade claims without a new separately labelled study. |
| Tier B — V2 Recovery R1 | New external/protocol evidence | Carry protocol, manifest, validation, environment, subject outputs, statistics, rerun record, and explicit origin labels. |
| Synthetic controls | Non-biomedical sensitivity evidence | Must remain `origin=synthetic_controlled_corruption` and `benchmark_eligible=false`; never pool with real biomedical evidence. |

## Dataset-Decision Audit

| Candidate / action | Scientific value | Availability/protocol decision | Final status |
|---|---|---|---|
| OpenBMI/NEMAR `nm000338` | Independent, larger binary MI cohort for P4; strict subject-level evaluation feasible | 54 subjects, event/label/channel checks completed; GPL-3.0 and provenance documented | **Executed as harmonized external validation** |
| Jeong/NEMAR `nm000311` | Independent synchronized EEG–EMG setting for P5 | `sub-23/ses-0` lacks run-2 and twist labels; locked 25-subject all-11-class cohort fails | **Hard stop; no P5 score** |
| BCI IV-2b expansion | Limited statistical and modality value for the stated P4 question | Additional scope without commensurate gain | Rejected for current scope |
| Deep/representation fusion | Would change P5’s transparent-fusion scientific identity | Not required to answer the stated question | Rejected for current scope |
| Repeated real P6 replay | Highest priority only if independent variation exists | Seed does not perturb MuJoCo initial/task/replay state | **Hard stop; no pseudo-replication** |

## P4 Final Evidence Audit

P4 used NEMAR `nm000338` v1.0.5 as an external dataset source. Each of 54 subjects contributed 200 binary MI trials from the declared `ses-1` train/test acquisitions; 62 channels were retained after exact EMG exclusion. The analysis used 8–30 Hz filtering, 0.5–3.5 s epoching, factor-8 decimation, and predeclared subject-level LOSO. The cache manifest contains 108 derived cache/provenance artefacts totaling 933,572,109 bytes and passed D1. D2–D5 passed before model fitting.

| P4 condition | Mean subject-level macro-F1 | SD | 95% bootstrap CI |
|---|---:|---:|---:|
| Linear | 0.5962 | 0.1050 | 0.5694–0.6253 |
| LDA | 0.5980 | 0.1059 | 0.5708–0.6278 |
| Linear SVM | 0.6123 | 0.1218 | 0.5806–0.6446 |
| Spectral | 0.6130 | 0.1226 | 0.5809–0.6459 |
| Compact CNN | 0.6364 | 0.1654 | 0.5929–0.6800 |

The Friedman test across five fixed conditions was χ²=16.16, *p*=0.00281. Nevertheless, no one of the ten predeclared pairwise Wilcoxon comparisons survived Holm correction (minimum adjusted *p*=0.1042). The correct summary is therefore that the condition means differed at omnibus level but the fixed study did not establish a Holm-surviving pairwise superiority claim. The entire subject-level CSV matched byte-for-byte across an independent rerun: SHA-256 `ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8`.

> P4 supports the existence of protocol-locked subject-independent binary MI decoding on a second external EEG cohort. It does not provide a direct numerical replication of BCI IV-2a or establish universal zero-calibration performance.

## P5 and P6 Stop-Condition Audit

P5 did not proceed because the selected official derivative fails the locked cohort boundary, not because of model outcome. The all-subject event audit found 24 complete subjects and `sub-23` with only two of three `ses-0` runs (450 observed events; two twist classes absent). Silently omitting this subject, narrowing to nine classes, mixing data sources, or calling a 24-subject subset the originally locked study would be protocol drift. The evidence stop is documented in `audit/V2_P5_JEONG_AVAILABILITY_HARD_STOP.md`.

P6 did not proceed because the seed is not an exposed biological or simulation-state variability factor in the inspected runtime. `MujocoBackend.reset(seed)` sets NumPy’s global seed and then calls `mj_resetData`/`mj_forward`; no perturbation is applied to joint state, target/object state, replay input, mapping, or task policy. Producing seed-labelled duplicate executions would be pseudo-replication. The evidence stop is documented in `audit/V2_P6_REPLAY_VARIABILITY_CAPABILITY_HARD_STOP.md`.

## Required Artefact Checklist

| Requirement | P4 Recovery R1 | P5 | P6 |
|---|---|---|---|
| Protocol | Pass | Stop record | Stop record |
| Dataset/source manifest | Pass | Source audit, no scientific manifest | Not applicable to repeat cohort |
| D1–D5 | Pass | Gate fails before data cache/model run | Capability gate fails before run |
| Subject outputs | 270 rows (54×5) | None | None |
| Statistics | Subject-level, bootstrap/Friedman/Wilcoxon/Holm | None by design | None by design |
| Environment fingerprint | Pass | Not applicable | Runtime source audit |
| Independent rerun | Exact pass | Not applicable | Not applicable |
| Claim status | Integrable with limits | Do not claim external fusion outcome | Do not claim repeat/control distribution |

## P4 Traceability Map

| Claim element | Supporting artefact |
|---|---|
| Source/version/license/protocol | `configs/experiments/v2_external_validation_recovery_r1.json`; `audit/V2_PROTOCOL_LOCK_RECOVERY_R1.md` |
| Raw-to-cache provenance | `<LOCAL_WORKSPACE>/hmi_data/derived/v2_recovery_r1_openbmi_nm000338_p4/sub-*.provenance.json` |
| D1 integrity | `datasets/manifests/nemar_nm000338_openbmi_v2_recovery_r1.json` |
| D2–D5 | Primary result `validation.json` |
| Subject-level outcome | Primary `subject_level_results.csv` |
| Statistics | Primary `statistics_macro_f1.json` |
| Reproducibility | Independent rerun directory and `audit/V2_PROTOCOL_AMENDMENT_RECOVERY_R1_001.md` |
| Visual asset | `p4_openbmi_subject_level_macro_f1.png` |

## Readiness Decision

P1/P2 evidence records and P4 may be incorporated into programme-level synthesis with their explicit limitations. P3 remains pending. P5 and P6 should be represented as **blocked evidence-expansion attempts with documented scientific stop conditions**, not as absent sections or as negative results. Any future reopening must create a new protocol amendment and evidence namespace before execution.
