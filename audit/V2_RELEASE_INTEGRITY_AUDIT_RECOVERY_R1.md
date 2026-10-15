# V2 Recovery R1 Release Integrity Audit

**Release scope:** Human Motor Intelligence V2 evidence expansion after sandbox recovery  
**Audit status:** Pass with documented scientific stop conditions

## Technical Verification

| Check | Outcome | Evidence |
|---|---|---|
| Python compilation | Pass | `python3 -m compileall -q src scripts` |
| Baseline regression tests | 28 passed | `audit/v2_final_regression_tests.log` |
| Raw signal files in repository | 0 | Final raw-exclusion check |
| Temporary P4 raw files after extraction | 0 | `<LOCAL_WORKSPACE>/hmi_data/raw/v2_recovery_r1_openbmi_nm000338` check |
| P4 cache manifest D1 | Pass; 108 artefacts; 933,572,109 bytes | `datasets/manifests/nemar_nm000338_openbmi_v2_recovery_r1.json` |
| P4 D2–D5 | Pass | P4 primary `validation.json` |
| P4 subject coverage | 54 subjects × 5 fixed conditions = 270 rows | Primary `subject_level_results.csv` |
| P4 independent rerun | Exact byte-identical subject-level CSV | SHA-256 `ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8` |
| P5 | No cache/manifest/result created after source coverage failure | `V2_P5_JEONG_AVAILABILITY_HARD_STOP.md` |
| P6 | No repeat result created after deterministic capability failure | `V2_P6_REPLAY_VARIABILITY_CAPABILITY_HARD_STOP.md` |

## Scientific Integrity Verification

P4 is labelled external validation and not direct replication. Its OpenBMI binary metrics are not numerically ranked against frozen BCI IV-2a four-class results. The highest condition mean is not called a confirmed winner because no pairwise comparison survives Holm. P5/P6 stops are presented as availability/capability limitations, not as null outcomes. P3 retains **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** in all new programme records.

## Release Contents

The release package contains protocol/configuration, source validation code, P4 primary and rerun result artefacts, statistics, figure, audit records, manuscript-status revisions, source extracts, and reproducibility documentation. It excludes BDF/EDF/GDF/VHDR/EEG raw recording files and external derived cache arrays.

## Final Release Decision

**Pass for evidence-governed internal/research use.** The release is suitable for review of P4 external validation and programme-level auditing. It is not a clinical validation package, does not contain a P5 external fusion outcome or P6 repeat distribution, and cannot replace pending P3 source evidence.
