# Real-Replay Control Robustness Under Declared Initial-State Variation: A Reproducible MyoSim Systems Study

**Version:** V2 Recovery R2 manuscript revision  
**Evidence identity:** `origin=real_replay_initial_state_variation`; simulation systems evidence; `benchmark_eligible=false`  
**Protocol ID:** `p6-real-replay-initial-state-repeats-recovery-r2`

## Abstract

Time-bin decoder accuracy alone does not determine whether a downstream motor-control task succeeds. However, repeated simulator executions are not independent evidence unless a declared factor produces distinct physical states or task conditions. We first reproduced the preserved MyoSim pick-place benchmark exactly with an unperturbed real replay. We then added a minimal, explicit, seed-linked initial-state capability that perturbs only two named forearm slider positions within predeclared ranges, records the realized state per run, and leaves replay input, decoder stream, controller, task geometry, object/target state, timing, and success rule fixed. Twenty predeclared seed-state realizations yielded 20 distinct initial qpos vectors and no invalid simulation states. None completed the task: success 0/20 (Wilson 95% CI 0.000–0.161), failure 20/20 (0.839–1.000), with all runs ending in `TRANSPORT`. The independent rerun reproduced the full run record byte-for-byte. This negative result demonstrates a control-margin limitation under the specified simulator distribution. It does not estimate human performance, clinical robustness, a physical mechanism, or a decoder-quality dose response.

## Introduction

Closed-loop motor-control evaluation needs task-level outcomes such as success, latency, failure state, final error, and correction burden in addition to classifier summary metrics. This motivation does not permit pseudo-replication: a simulator with a fixed task and a seed that changes no physical state can reproduce an implementation but cannot yield an outcome distribution.

The R1 audit found precisely this limitation in the supplied MyoSim V1.1 runtime. `run.seed` was recorded but did not alter joint qpos, qvel, object/target state, replay, controller, or task policy. R2 therefore used a registered minimal implementation extension rather than relabelling deterministic duplicates as replicates. The extension is intentionally a systems tool, not a biomedical data generator.

## Baseline and Capability Gates

The unperturbed benchmark replay was executed before modification and reproduced the preserved endpoint exactly: success `true`, final state `COMPLETE`, completion time 3.22 s, final error 0.04985601966004137 m, path length 0.9678159612131996 m, 14 grasp-stability steps, 3 command corrections, and no invalid state. The same output was verified again after the extension when perturbation was disabled.

The extension adds an `initial_state` configuration section that defaults to inert. When explicitly enabled with `uniform_forearm_xy_v1`, it samples only two offsets from `numpy.random.default_rng(run.seed)` after MuJoCo reset and before task/controller construction. It validates named joints and joint ranges, calls `mj_forward`, and records the actual offsets, qpos, qvel, named positions, configured range, seed, replay checksum, code fingerprint, configuration, and task result.

| Declared variable | Distribution | Safety envelope |
|---|---|---|
| `forearm_x` qpos offset | Uniform [0.000, 0.020] m | Within model range [0.000, 0.460] m |
| `forearm_y` qpos offset | Uniform [−0.015, +0.015] m | Within model range [−0.120, +0.150] m |

A two-seed preflight demonstrated distinct recorded state vectors within the allowed ranges, with unchanged undeclared named joint positions and no invalid state. The initial probe task outcomes were retained but did not alter the range, seeds, replay, controller, or endpoint hierarchy.

## Methods

### Fixed Components

The CSV replay is `pick_place_replay.csv` (SHA-256 `a94e59e30e2599eb92517198739dff96aa40b01f3bf6777756722e09960e09f3`). The fixed MuJoCo task is pick-place, and the fixed controller settings include a 0.75 confidence threshold, three confirmation windows, 0.20 s hold duration, 0.10 s release duration, and 2.0 rad/s command rate limit. Object and target state, replay event times, control mapping, decoder stream, and task success definition were unchanged.

### Cohort and Endpoints

The primary cohort consists of 20 prespecified seeds `20260901`–`20260920`, one execution per seed. The primary endpoints are task success proportion, completion time among successful runs, and final planar error. Secondary endpoints are failure proportion, final state, path length, grasp-stability steps, command corrections, invalid-state count, and the realized offset/state record. Success/failure intervals use Wilson 95% intervals; continuous summaries use 10,000-resample percentile bootstrap intervals across the declared state realizations.

The replay decoder stream is fixed across all runs. Accordingly, the design does not identify a decoder-quality dose response and does not test a relationship between classifier accuracy and task outcome.

## Results

All 20 seeds produced distinct qpos vectors. Observed `forearm_x` offsets spanned 0.000136–0.019980 m (mean 0.010071 m), and observed `forearm_y` offsets spanned −0.012405–0.013199 m (mean 0.000901 m). No invalid state was observed.

| Endpoint | Result |
|---|---:|
| Success | 0/20; 0.000; Wilson 95% CI 0.000–0.161 |
| Failure | 20/20; 1.000; Wilson 95% CI 0.839–1.000 |
| Final state | `TRANSPORT` in 20/20 |
| Completion time among successes | Not defined; no successful runs |
| Final planar error | Mean 0.046650 m; SD 0.002513 m; bootstrap 95% CI 0.045621–0.047751 m |
| Path length | Mean 1.024690 m; SD 0.041596 m; bootstrap 95% CI 1.007466–1.042456 m |
| Grasp stability | Mean 15.15 steps; range 15–16 |
| Command corrections | 3 in every run |
| Invalid state | 0/20 |

![Declared initial states and descriptive final errors](../results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2/p6_initial_state_offsets_final_error.png)

## Discussion

The all-failure outcome is reported without seed deletion, range narrowing, controller adjustment, or post hoc scenario changes. Within this narrowly declared simulator distribution, the fixed real replay/control sequence did not complete the task. In contrast, the single unperturbed compatibility state did complete the benchmark. The appropriate conclusion is a **simulator control-margin limitation under the specified initial-state distribution**, not a claim about human motor behaviour or real prosthetic robustness.

The value of the negative finding is methodological. It demonstrates why fixed-state replay success should not be generalized automatically to a distribution of states, and why independent variability must be made explicit rather than inferred from arbitrary seed labels. It also demonstrates that final error alone does not capture task completion: all runs had final error values below the fixed 0.08 m target radius yet remained in the `TRANSPORT` state and did not complete the required release transition.

The study cannot explain which unmodelled physical or control factor creates the sensitivity. It also cannot establish whether improving the decoder would improve this outcome because the decoder replay is fixed. The frozen synthetic controlled-corruption study may explore a separate designed decoder-quality sensitivity question, but it must remain a separate synthetic evidence tier and cannot be pooled with this cohort.

## Limitations

The initial-state factor changes two simulator sliders only and is not a sample from a human or clinical population. Twenty seeds provide a limited empirical distribution, reflected by the Wilson interval. The task and replay are a simplified control scenario; object dynamics, actuator parameters, controller mapping, and perturbation ranges are specific to this model. The baseline is a compatibility control rather than a randomized comparator. Finally, the study does not evaluate a learned decoder or a range of decoder qualities.

## Reproducibility

Primary artefacts are in `results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2/`, including 20 per-run JSON records, `run_records.json`, `protocol.json`, `environment.json`, `code_fingerprint.json`, and `statistics_initial_state_repeats.json`. The independent rerun is under `results/real/v2-recovery-r2-independent-rerun/p6_real_replay_initial_state_repeats_r2/`. The primary and rerun `run_records.json` files are byte-identical.

## References

[1] [Pan et al. (2024), task-level outcomes in myoelectric control](https://doi.org/10.3389/fnhum.2024.1429130)  
[2] [Skomrock et al. (2018), control performance measures](https://doi.org/10.3389/fnins.2018.00763)
