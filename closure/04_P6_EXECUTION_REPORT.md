# P6 C1 Execution and Closure Report

## Current status

**C1 is scientifically complete under the registered protocol `P6-C1-MI-R04-v1.0`.** The active experiment used PhysioNet EEGMMIDB R04 unilateral motor imagery for S001–S020 under strict LOSO, with frozen M1/M2/M3 quality ordering, a fixed abstract T1/T2 control mapping, a model-independent MyoSim fixture gate, primary replay, and rerun replay.

The raw R04 EDF files are external and are not redistributed in this release. Their source-file SHA-256 provenance is retained in `p6/c_mi_r04_primary/audit/DATASET_MANIFEST.json`.

## Retained R03 engineering baseline

The earlier R03 experiment is preserved as engineering/preflight evidence only. R03 is motor execution and is not used as the scientific primary for C1.

## Completed evidence

- 20 held-out subjects × 3 frozen model configurations.
- 60 primary decoder-conditioned traces and 60 primary MyoSim task artifacts.
- 60 rerun decoder-conditioned traces and 60 rerun MyoSim task artifacts.
- Model-independent MyoSim fixture: 1/1 `COMPLETE`.
- Rerun integrity: distinct run IDs and distinct artifact SHA-256 values; deterministic decoder traces reproduce byte-for-byte and task metrics reproduce exactly.
- Subject-level paired statistical analysis with degenerate-success handling.
- Canonical manuscript, claim/evidence matrices, provenance, release manifest, and reproducibility report.

## Primary outcome

Decoder-conditioned task success was 0/60 for M1, M2, and M3 in both primary and rerun. The registered binary success endpoint is therefore non-discriminative. Continuous downstream metrics are retained as exploratory, subject-level analyses.

## Scientific interpretation

The study supports a negative/non-discriminative downstream result under one fixed R04 cohort, one abstract command mapping, one controller, and one deterministic MyoSim task. It does not establish a general law that decoder quality determines control utility, and it does not constitute clinical, prosthetic, or online human validation.

## Re-execution boundary

A fresh end-to-end reproduction still requires external retrieval of the R04 EDF files and a compatible MyoSim/MuJoCo runtime. The release is therefore artifact-auditable and protocol-complete without redistributing the raw EEG data.
