# P6 C1 — Statistical Analysis Report

## Unit and design
The inferential unit is subject. The three decoder conditions are paired within each of 20 LOSO-held-out subjects. Trial/event rows are descriptive only and are never used as independent observations.

## Decoder quality freeze
Source-training 3-fold balanced accuracy was frozen before task analysis: M2 low (0.465274), M3 mid (0.465607), M1 high (0.505179).

## Endpoints
The primary endpoint was MyoSim pick-and-place task success. It was 0/20 for each model in both primary and rerun, hence it is degenerate and no inferential success test was performed. Secondary endpoints were final error, path length, command corrections, and grasp-stability steps. Completion time was unavailable for failed decoder-conditioned runs.

## Statistics
For continuous endpoints, paired Friedman tests, Kendall's W, paired Cohen's dz, and deterministic subject-level bootstrap 95% CIs are stored in `p6/c_mi_r04_primary/results/FINAL_STATISTICS.json`. These are exploratory because the primary success endpoint was non-discriminative. The rerun reproduces the primary numerical summaries.

## Disposition
The fixture capability claim is supported. A decoder-quality-to-task-success claim is not supported under this fixed simulator/task boundary.


---
## Addendum (v1.2.0): audit and C2

**Withdrawn interpretation.** Section "exploratory continuous endpoints" above reports a significant omnibus difference in command corrections. The audit (`p6/c1_audit`) shows all 64 corrections occurred after the task had already failed (0 before task end); per run they correlate with the number of confident events (Spearman ρ = 0.51), not with held-out balanced accuracy (ρ = −0.03). Final-error and path-length differences between decoders are floating-point level (< 1e-12 m) and determined by the first-event onset (η² = 1.00 and 0.94). None of these may be cited as evidence about decoder-to-control transfer.

**C2 statistics.** Confirmatory tests (Holm over H-E1…H-R1) are in `p6/c2_episode/results/ANALYSIS.json` and were recomputed independently in `p6/c2_episode/posthoc/verify_stats.py` (identical). Post-hoc analyses (chance-matched floor, gate sweep, lookup validation) are in `p6/c2_episode/posthoc/` and are labelled post-hoc in the manuscript.
