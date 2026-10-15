# Reproducibility Report
## V2 Recovery R3 Current-State Addendum

## Scope

This report consolidates the current reproducibility evidence across the umbrella repository and the executed P4–P6 recovery studies. It differentiates exact result reproduction, exercised runtime checks, and environment-limited components. It does not interpret an unavailable optional backend as having passed.

## Exact Research-Result Reproductions

| Study | Primary artefact | Independent rerun result | SHA-256 / equivalence | Status |
|---|---|---|---|---|
| P4 R1 | `subject_level_results.csv`, 270 subject-model rows | Byte-identical CSV | `ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8` | PASS |
| P5 R2 | `subject_level_results.csv`, 96 subject-model rows | Byte-identical CSV | `a35b1cb5daa2cdae2078e7668eb1b028e4613c99e062df2b941183c7b971e36b` | PASS |
| P6 R2 | `run_records.json`, 20 locked-seed simulation records | Byte-identical aggregate record | `2edaa2a7d8a1e0448dc9f5742190a736a2877eb20c65395d60d65dd019cad120` | PASS |

The P4/P5 reruns reproduce the locked subject-level CSVs exactly rather than merely matching rounded summaries. P6 reproduces the seed-to-state mapping, outcomes, errors, and aggregate run record exactly. These checks confirm reproducibility of the retained studies, subject to their stated evidence boundaries.[1]

## Repository and Runtime Verification

| Surface | Current result | Interpretation |
|---|---|---|
| Main programme repository | 28 tests passed in 0.86 s | PASS |
| P4/P5/P6 R3 document/evidence validator | Required documents, result-rerun checksums, raw/cache exclusion, figure targets, and R3 terminology checks passed | PASS |
| MyoSim MuJoCo-capable selection | 62 applicable tests passed | PASS for exercised MuJoCo-capable path |
| MyoSim optional PyBullet backend | Not fully executable on this Python 3.12 environment | Not certified; limitation documented |
| Default MyoSim pytest configuration | Requests unavailable `pytest-cov` | Environment configuration limitation |

The MyoSim suite has a transparent limitation: PyBullet-dependent test files or parametrizations require the absent optional dependency. The release log records the exact cases and avoids an unsupported full-suite claim.[2]

## Environment and Retention Controls

P4 and P5 record their execution environment in each primary result directory. P6 records its patch/source fingerprint and simulation environment. The project contains no raw BDF/EDF/GDF/SET/FIF files and no NPZ derived cache in the release tree; these files are excluded deliberately to preserve data restrictions. Historical V1/V1.1/R1/R2 paths are retained rather than recomputed or relabelled.[1] [3]

## What This Report Does Not Establish

Reproducible reruns do not establish clinical validity, cross-source generalisation, an EEG–EMG fusion mechanism, direct BCI IV-2a replication, or P6 decoder-quality response. R3 P6 remains unexecuted because authentic condition traces are absent; there is no valid three-condition reproducibility test to report.

## References

[1]: papers/REPRODUCIBILITY_MATRIX_V2_RECOVERY_R3.md "R3 Reproducibility Matrix"
[2]: audit/V2_R3_TEST_EXECUTION_LOG.md "R3 Test Execution Log"
[3]: audit/V2_R3_INTEGRATION_VALIDATION.md "R3 Integration Validation"
[4]: audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Replay Identity Hard Stop"

The exact-rerun and environment statements are governed by the retained validation, test, and hard-stop records.[1] [2] [3] [4]
