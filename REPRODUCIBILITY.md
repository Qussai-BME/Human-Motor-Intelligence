# Reproducibility Guide
## Current-State V2 Recovery R3

## Reproducibility Contract

The project separates immutable historical evidence from new versioned recovery outputs. Never overwrite V1, V1.1, R1, or R2 result paths. R3 documents correct the interpretation of P6 replay identity without modifying the historical bytes or filenames. Raw biosignal data and external derived caches are not bundled; reproduction requires a properly authorized local source path where applicable.

## Reproducing the Retained Evidence Checks

| Goal | Canonical record | Expected observation |
|---|---|---|
| Main repository verification | `pytest -q` from repository root with `PYTHONPATH=src` | 31 passed in the current recorded environment |
| P4 result equivalence | Primary and independent-rerun `subject_level_results.csv` files | Identical SHA-256 `ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8` |
| P5 result equivalence | Primary and independent-rerun `subject_level_results.csv` files | Identical SHA-256 `a35b1cb5daa2cdae2078e7668eb1b028e4613c99e062df2b941183c7b971e36b` |
| P6 record equivalence | Primary and independent-rerun `run_records.json` files | Identical SHA-256 `2edaa2a7d8a1e0448dc9f5742190a736a2877eb20c65395d60d65dd019cad120` |
| R3 integration validation | `scripts/validate_r3_interim_release.py` | Required files, checksums, exclusions, image targets, and terminology audit pass |

## Study-Specific Entry Points

P4 uses `configs/experiments/v2_external_validation_recovery_r1.json` and `scripts/run_v2_external_validation.py`. P5 uses `configs/experiments/v2_p5_jeong_recovery_r2.json` and `scripts/run_v2_p5_jeong_r2.py`. P6 uses the separately retained MyoSim patch and `scripts/run_p6_initial_state_repeats_r2.py`. Executing a new run is not the same action as verifying retained evidence: any data/model/protocol change requires a new registered namespace rather than overwriting results.

## Environment Notes

The captured study environments reside in each primary result directory. The current main repository test suite passes. MyoSim’s MuJoCo-capable selection has 62 applicable passing tests; full PyBullet backend confirmation is outside the recorded environment because the optional dependency is unavailable under Python 3.12, and the default test configuration also requests `pytest-cov`. These constraints are recorded, not suppressed.[1]

## P6 R3 Reopening Rule (resolved in 1.1.0/1.2.0)

The R3 rule required authentic frozen trace files and a registered amendment before any decoder-quality study. That requirement was met by C1 (registered protocol, frozen traces and hashes) and C2 (registered follow-up, frozen before outcomes). Do not rerun P6 R2 as an imagined decoder condition. Any further study requires a new registered namespace; never overwrite C1 or C2 results.[2]

## P6 C1/C2 reproduction

See `papers/paper_6/REPRODUCIBILITY_REPORT.md` (addendum) and `p6/c2_episode/README.md`: scripts take `MYOSIM_DIR`, `EEGMMIDB_DIR`, `C2_OUT` and `C2_RAW` from the environment; re-running the C1 audit and the C2 analysis reproduces the recorded outputs, and `p6/c2_episode/verification/verify_c2.py` re-executes sampled episodes.

## References

[1]: REPRODUCIBILITY_REPORT.md "R3 Reproducibility Report"
[2]: papers/RESEARCH_GATE_PREPARATION_RECOVERY_R3.md "P6 R3 Research Gate"
[3]: patches/README_MYOSIM_INITIAL_STATE_RECOVERY_R2.md "MyoSim Patch Guide"

The guide is governed by the current reproducibility, trace-provenance, and patch records.[1] [2] [3]
