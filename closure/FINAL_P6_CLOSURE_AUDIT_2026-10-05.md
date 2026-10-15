# Final P6 Closure Audit — 2026-10-05

| Gate | Status | Evidence |
|---|---|---|
| Authentic source data | PASS | PhysioNet EEGMMIDB R04, S001–S020; raw EDF excluded from release |
| R03 retained as baseline | PASS | `p6/exploratory_r03_primary/`; engineering/preflight only |
| Authentic trace provenance | PASS | 60 primary + 60 rerun decoder traces with hashes |
| Quality assignment independent of task outcomes | PASS | Source-only frozen mapping M2 low, M3 mid, M1 high |
| Control fixture | PASS | 1/1 model-independent fixture reached COMPLETE |
| Full chain execution | PASS | EEG → decoder → contract → controller → safety → MyoSim → task → metrics |
| Primary execution | PASS | 60 task runs and 60 per-run artifacts; 0 successes |
| Independent rerun | PASS | 60 traces and 60 per-run artifacts; numerical summaries reproduced |
| Final statistics | PASS | Subject-level paired statistics, effect sizes, bootstrap CIs; success test skipped as degenerate |
| Public documentation | PASS | Manuscript, claims, protocol, status, provenance and closure reconciled |

## Scientific disposition
**Negative/non-discriminative downstream systems evidence under the locked R04/MyoSim configuration.** The fixture passed, but decoder-conditioned task success was 0/60 for M1, M2, and M3 in both primary and rerun. Therefore no decoder-quality-to-task-success claim is made; continuous endpoints remain exploratory.
