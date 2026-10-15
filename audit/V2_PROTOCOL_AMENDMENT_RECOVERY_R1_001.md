# V2 Protocol Amendment — Recovery R1.001

**Status:** Pre-execution operational amendment  
**Applies to:** P4 OpenBMI Recovery R1 independent rerun only  
**Does not change:** Dataset, cohort, labels, channels, preprocessing, cache, models, hyperparameters, seed schedule, metrics, statistics, or scientific question.

## Purpose

The locked Recovery R1 P4 protocol requires an independent rerun before manuscript integration. The initial implementation made result paths immutable and exposed only the primary result namespace. This amendment introduces a second, separately immutable result namespace solely for an exact reproducibility rerun from the same D1-verified derived cache.

| Item | Primary run | Independent rerun |
|---|---|---|
| Data/cache manifest | Same D1-verified P4 cache | Same D1-verified P4 cache |
| Protocol ID | `p4-openbmi-harmonized-zero-calibration-loso-recovery-r1` | Unchanged |
| Seed schedule | `20260823 + fold_index*101 + model_index` | Unchanged |
| Analytical code | Same committed recovery source | Same committed recovery source |
| Result namespace | `results/real/v2-recovery-r1/` | `results/real/v2-recovery-r1-independent-rerun/` |
| Acceptance criterion | Primary execution completed | Exact CSV checksum agreement with primary run; otherwise stop manuscript integration and investigate |

The rerun is not a new experiment and must not be pooled with the primary run, counted as additional subjects, or used to select a better result. It is an execution reproducibility check. A failure to agree exactly is a protocol-integrity failure, not a reason to average or choose a favourable output.
