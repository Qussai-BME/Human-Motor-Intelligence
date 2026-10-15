# P6 C1 Reproducibility Report

P6 C1 is scientifically complete under the registered protocol. The release contains the run-level decoder and MyoSim outputs needed to audit the reported result, while the original R04 EDF files remain external and are therefore not redistributed.

## Evidence package
- 20 R04 source-file provenance records with SHA-256 hashes.
- 60 primary decoder traces.
- 60 primary MyoSim task JSON artifacts.
- 60 rerun decoder traces.
- 60 rerun MyoSim task JSON artifacts.
- Fixed configuration and source-only quality ranking.
- Model-independent fixture replay that completed successfully.
- Subject-level statistics in `results/FINAL_STATISTICS.json`.
- `audit/RERUN_INTEGRITY_CHECK.json` documenting distinct rerun run IDs and artifact hashes.

## Re-execution boundary
A fresh end-to-end reproduction still requires retrieval of the external PhysioNet R04 EDF files and a compatible MyoSim/MuJoCo environment. The release therefore supports **artifact-level audit and protocol-faithful re-execution**, but does not redistribute the raw EEG source files.

## Result
The primary task-success endpoint is non-discriminative: 0/60 for M1, M2, and M3. Continuous endpoint analyses are exploratory and paired at subject level.


---
## Addendum (v1.2.0): reproducing the audit and C2

```bash
export MYOSIM_DIR=/path/to/myosim_repo          # MyoSim v0.1.5, commit 67ee74e3230b068b5db760efa15da3669e315eb3
python p6/c1_audit/scripts/rerun_diag.py        # D1–D3: bit-identical to p6/c1_audit/outputs/diag_runs.json
python p6/c1_audit/scripts/stats_all.py         # C1 audit statistics -> numbers.json
python p6/c2_episode/scripts/analyze_c2.py      # recompute ANALYSIS.json from the episode tables
python p6/c2_episode/posthoc/verify_stats.py && python p6/c2_episode/posthoc/final_numbers.py && python p6/c2_episode/posthoc/excess.py && python p6/c2_episode/posthoc/build_paper_numbers.py
# independent re-execution of 300 sampled episodes (extract p6/c2_episode/raw_archives/*.tar.gz into C2_RAW first)
C2_RAW=/path/to/extracted python p6/c2_episode/verification/verify_c2.py
```
Checked at release: re-running the C1 audit and the C2 analysis from the repository reproduces the recorded outputs (`ANALYSIS.json` identical apart from a timestamp in a statsmodels summary); `verify_c2.py` reproduced 300/300 sampled episodes.
