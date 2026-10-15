# Reproducibility Matrix — V2 Recovery R3

| Component | Protocol / evidence record | Result artefacts | Independent reproduction | Verification status | Boundary |
|---|---|---|---|---|---|
| P4 R1 OpenBMI | `v2_external_validation_recovery_r1.json`, protocol, manifest, D1–D5 | 270 subject-model rows, stats, figure, environment | 270-row CSV byte-identical; SHA-256 `ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8` | Reproducible | External validation only |
| P5 R2 Jeong | R2_001/R2_002, source check, protocol, manifest, D1–D5 | 96 subject-model rows, stats, figure, environment | 96-row CSV byte-identical; SHA-256 `a35b1cb5daa2cdae2078e7668eb1b028e4613c99e062df2b941183c7b971e36b` | Reproducible | Derived cache stays outside package; no raw BDF |
| P6 R2 state study | R2_003, patch, source fingerprint, capability/baseline records | 20 per-seed JSONs, aggregate records, stats, figure | `run_records.json` byte-identical | Reproducible as fixture systems study | R3 corrects replay identity; no decoder mapping |
| P6 R3 decoder-quality extension | No R2_004 because trace identity failed pre-execution | No new run folder, no inference | Not applicable | Blocked correctly | Requires authentic trace manifest before execution |
| Main repository tests | Repository test suite | `audit/test_logs/main_repo_pytest_r3.txt` | **28 passed** in 0.86 s | PASS | Does not validate unavailable source data |
| MyoSim MuJoCo-capable tests | Local patched MyoSim suite | `audit/test_logs/myosim_mujoco_capable_pytest_r3.txt`; `audit/V2_R3_TEST_EXECUTION_LOG.md` | **62 passed** in the applicable MuJoCo selection; PyBullet-dependent cases isolated | PASS for applicable suite | Full PyBullet collection unavailable under Python 3.12; default configuration also requests absent `pytest-cov` |

## Archive and Exclusion Rules

The interim package includes protocols, code, documents, patches, result metadata, statistical outputs, figures, and audit records. It excludes raw BDF/EDF and external derived cache data. Historical V1, V1.1, R1, and R2 artefacts retain their locations and filenames. The R3 package layers correction and integration records on top of, rather than altering, the frozen record.

## References

[1]: ../results/real/v2-recovery-r1/nemar-nm000338-openbmi-p4-external-loso-recovery-r1/statistics_macro_f1.json "P4 statistics"
[2]: ../results/real/v2-recovery-r2/nemar-nm000311-jeong-p5-external-loso-24subject-r2/statistics_macro_f1.json "P5 statistics"
[3]: ../audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Hard Stop"
[4]: ../patches/README_MYOSIM_INITIAL_STATE_RECOVERY_R2.md "MyoSim Patch Guide"

The checksums and P6 interpretation boundary are retained in the underlying result and audit records.[1] [2] [3] [4]
