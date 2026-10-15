# P6 Appendix — V2 Recovery R3 Q1 Standard

## A. Scope and R3 Status

R2 is a 20-state MyoSim integration-fixture stress test. R3 decoder-quality comparison is **not executed** because the retained replay is `synthetic-demo` / `example-decoder-v1` and no immutable mid-tier/best trace with authoritative provenance is available. See `audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md`.

## B. Protocol and Reproducibility Record

| Artefact | Primary record | Rerun/interpretation |
|---|---|---|
| Protocol | `protocol.json` | Protocol ID: `p6-real-replay-initial-state-repeats-recovery-r2` |
| Replay | `pick_place_replay.csv` | R3 audit reclassifies identity as synthetic integration fixture; not decoder-quality condition |
| State factor | `uniform_forearm_xy_v1` | 20 prespecified seeds; 20 distinct qpos states |
| Primary records | 20 run JSON artefacts plus `run_records.json` | Exact rerun at `results/real/v2-recovery-r2-independent-rerun/p6_real_replay_initial_state_repeats_r2` |
| Statistics | `statistics_initial_state_repeats.json` | Wilson proportions and bootstrap continuous summaries |

## C. Full Per-Record Table

| Seed | x offset (m) | y offset (m) | Success | Final state | Completion time (s) | Final error (m) | Path length (m) | Stability steps | Corrections |
|---|---|---|---|---|---|---|---|---|---|
| 20260901 | 0.012644 | 0.002472 | False | TRANSPORT | — | 0.051861 | 0.958954 | 16 | 3 |
| 20260902 | 0.018459 | 0.003767 | False | TRANSPORT | — | 0.046348 | 0.992294 | 15 | 3 |
| 20260903 | 0.005115 | -0.004998 | False | TRANSPORT | — | 0.043468 | 1.022077 | 15 | 3 |
| 20260904 | 0.017118 | 0.010991 | False | TRANSPORT | — | 0.047939 | 1.049782 | 15 | 3 |
| 20260905 | 0.008896 | 0.013199 | False | TRANSPORT | — | 0.049346 | 1.052737 | 15 | 3 |
| 20260906 | 0.016252 | -0.001524 | False | TRANSPORT | — | 0.044050 | 0.981433 | 15 | 3 |
| 20260907 | 0.004074 | -0.000188 | False | TRANSPORT | — | 0.046483 | 1.036425 | 15 | 3 |
| 20260908 | 0.017497 | 0.004453 | False | TRANSPORT | — | 0.045578 | 0.982078 | 15 | 3 |
| 20260909 | 0.019980 | -0.001051 | False | TRANSPORT | — | 0.046720 | 1.016975 | 15 | 3 |
| 20260910 | 0.000136 | 0.012166 | False | TRANSPORT | — | 0.047879 | 1.070657 | 15 | 3 |
| 20260911 | 0.013265 | -0.002240 | False | TRANSPORT | — | 0.049936 | 0.950669 | 16 | 3 |
| 20260912 | 0.004415 | 0.012702 | False | TRANSPORT | — | 0.048212 | 1.057034 | 15 | 3 |
| 20260913 | 0.004289 | -0.004401 | False | TRANSPORT | — | 0.050825 | 0.983351 | 16 | 3 |
| 20260914 | 0.004153 | -0.001224 | False | TRANSPORT | — | 0.044274 | 1.096133 | 15 | 3 |
| 20260915 | 0.014869 | 0.002701 | False | TRANSPORT | — | 0.045749 | 1.005483 | 15 | 3 |
| 20260916 | 0.002964 | -0.005040 | False | TRANSPORT | — | 0.044489 | 1.051592 | 15 | 3 |
| 20260917 | 0.013061 | -0.010098 | False | TRANSPORT | — | 0.043836 | 1.024191 | 15 | 3 |
| 20260918 | 0.019212 | -0.012405 | False | TRANSPORT | — | 0.043459 | 1.013763 | 15 | 3 |
| 20260919 | 0.004143 | 0.010954 | False | TRANSPORT | — | 0.047707 | 1.055997 | 15 | 3 |
| 20260920 | 0.000875 | -0.012213 | False | TRANSPORT | — | 0.044850 | 1.092169 | 15 | 3 |

## D. Endpoint Table

| Endpoint | Result |
|---|---|
| Task success | 0/20; Wilson 95% CI 0.000000–0.161125 |
| Task failure | 20/20; Wilson 95% CI 0.838875–1.000000 |
| Final error mean | 0.046650 m; bootstrap 95% CI 0.045621–0.047751 |
| Path length mean | 1.024690 m; bootstrap 95% CI 1.007466–1.042456 |
| Final states | TRANSPORT: 20 |
| Invalid states | 0 |

## E. Figure, Validation, and Confusion-Matrix Availability

![Declared state offsets and descriptive final error](../../results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2/p6_initial_state_offsets_final_error.png)

The baseline compatibility check, post-patch inert-default check, bounded-state preflight, 20-run completeness record, and exact independent rerun are documented in the linked R2 audits. A class confusion matrix is not a meaningful retained endpoint for this simulator task: the locked P6 records task transitions/outcomes rather than a multi-class classifier prediction table. R3 decoder-condition tables do not exist because no valid R3 condition traces were supplied.
