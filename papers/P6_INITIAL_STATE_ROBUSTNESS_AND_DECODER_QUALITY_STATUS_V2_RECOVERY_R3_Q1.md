# Simulator Initial-State Robustness and Decoder-Quality Evidence Status for Motor-Intent Replay

**Author:** Qussai Adlbi  
**Version:** V2 Recovery R3 Q1-standard manuscript  
**Evidence identity:** R2 systems/integration-fixture stress test; `benchmark_eligible=false`  
**P3 upstream evidence:** Accepted from the external Lite-DAN v1.0.0 archive; it is not a MyoSim decoder-trace package.  
**R3 decoder-quality status:** Not executed; hard stop active pending authentic trace provenance  

## Abstract

**Background.** Downstream motor-control evaluation requires task success, failure state, timing, and error endpoints in addition to time-bin decoding metrics. Repeated simulations are only informative when a declared factor produces distinct states, and a decoder-quality comparison requires identifiable decoder traces.

**Methods.** R2 first reproduced an unperturbed MyoSim pick-place compatibility state. It then sampled 20 prespecified bounded initial forearm states while holding replay input, controller, task geometry, object/target state, timing, and success logic fixed. R3 audited the replay identity after the upstream P3 Lite-DAN package became available. The P3 package contains subject-level LOSO outputs and aggregate results, but no serialized MyoSim intent traces mapped to worst/mid/best decoder conditions.

**Results.** The 20 R2 seeds generated 20 distinct qpos vectors with no invalid state. All 20 runs ended in `TRANSPORT`; task success was 0/20 (Wilson 95% CI 0.000–0.161), and mean final planar error was 0.046650 m (bootstrap 95% CI 0.045621–0.047751 m). The independent rerun reproduced `run_records.json` byte-for-byte. R3 found that the input was `pick_place_replay.csv`, which labels all events `synthetic-demo` and `example-decoder-v1`; it contains no authenticated tiny-CNN/worst identity or decoder-quality tier. No mid-tier or best-performing provenance-linked trace is available locally.

**Conclusion.** R2 is a reproducible initial-state sensitivity test for a fixed simulation integration fixture. It is not a real-decoder, biomedical, or decoder-quality dose-response result. R3 decoder-quality evaluation, including all 2 × 20 additional runs and any three-condition statistical comparison, is stopped pending user-supplied immutable traces and their provenance.

**Keywords:** motor control; simulation; initial-state perturbation; reproducibility; task success; MyoSim; decoder provenance; evidence governance.

## Introduction

Classifier accuracy alone does not establish task-level control performance. In myoelectric and human-in-the-loop systems, success, failure, latency, correction burden, and endpoint error can add information that a time-bin label metric does not carry [1,2]. This motivates a systems analysis layer, but it does not permit causal claims from a simulator fixture or pseudo-replication from repeatedly executing an unchanged state.

R1 correctly stopped a proposed repeated-replay study because the supplied MyoSim seed was logged but did not alter physical state, task, replay, controller, or target. R2 introduced a minimal, inert-by-default initial-state mechanism so a seed could generate a declared bounded physical state. R3 was requested to cross the same 20-state distribution with two additional decoder-quality traces. Its first requirement was trace identity: a quality comparison is meaningful only if each input can be identified as a real or declared synthetic decoder output, mapped to an immutable model/version/quality condition, and reproduced under the same task/control protocol.

## Related Work

Task-oriented myoelectric-control research emphasizes that downstream interaction outcomes and user/task success cannot always be inferred from classifier accuracy alone [1]. Control-performance studies likewise motivate reporting task completion, time, and failure-related endpoints alongside label-level measures [2]. These methodological sources motivate P6’s outcome hierarchy; they do not validate the present MyoSim fixture as a clinical endpoint or establish a decoder-effect mechanism.

Multimodal and motor-intention studies sometimes report improved recognition under different signals, architectures, task windows, subject settings, or clinical populations. Such evidence does not substitute for a replay-provenance chain linking a frozen decoder model to a control trace. The separate programme synthetic corruption sweep remains a controlled sensitivity analysis and cannot be pooled with R2 state variation. A real decoder-quality study requires all condition inputs before outcome generation, not retrospective labelling of a generic example file.

## Data and Methods

### R2 unperturbed compatibility control

Before the initial-state extension, the fixed MyoSim pick-place benchmark was reproduced in a new namespace. The unperturbed compatibility control matched the preserved endpoint: `success=true`, final state `COMPLETE`, completion time 3.22 s, final error 0.04985601966004137 m, path length 0.9678159612131996 m, 14 grasp-stability steps, three command corrections, and no invalid state. The same compatibility condition was checked after the inert-by-default extension.

### Declared state factor and cohort

The enabled R2 factor `uniform_forearm_xy_v1` samples only named forearm slider offsets after MuJoCo reset. `forearm_x` is uniform in [0.000, 0.020] m and `forearm_y` is uniform in [−0.015, +0.015] m. Joint range is validated; actual qpos/qvel and named state values are recorded. Replay input, decoder stream, controller, task geometry, target/object states, event timing, and success rule are fixed. The cohort contains one execution for each predeclared seed `20260901`–`20260920`.

### Replay-identity audit and R3 stop condition

The R2 replay input is `<LOCAL_WORKSPACE>/dependencies/myosim_v1_1/examples/intents/pick_place_replay.csv`, SHA-256 `a94e59e30e2599eb92517198739dff96aa40b01f3bf6777756722e09960e09f3`. Its CSV metadata identifies `source_subject=synthetic-demo`, `modality=emg-replay`, and `model_version=example-decoder-v1`. Its fixed events are REST (0.99) and PINCH (0.95). It has no decoder-family ID, model artifact hash, subject/session identity, performance score, quality tier, or mapping to the purported tiny-CNN/worst condition.

R3 inventory of the supplied Human Motor Intelligence, MyoSim, MyoAdapt, myocontrol, Recovery, and externally archived P3 Lite-DAN packages found no usable condition-mapped mid-tier or best-performing MyoSim replay trace. Consequently R2_004 was not registered, no additional trace was run, and no decoder-quality statistical test was performed. Constructing, relabelling, or confidence-editing traces would manufacture synthetic inputs rather than evaluate the requested frozen decoder outputs.

### Endpoints and analysis

For R2, task success/failure use Wilson 95% intervals. Continuous endpoints use 10,000-resample percentile bootstrap intervals across the 20 declared initial-state realizations. The unperturbed state is a compatibility control, not a randomized comparator cohort. No test of decoder quality is identified by R2 because the replay input remains constant; no test is identifiable in R3 because required condition identities are absent.

## Results

### R2 initial-state stress-test result

Twenty distinct initial qpos vectors were recorded, and no invalid state occurred. Realized `forearm_x` offsets spanned 0.000136–0.019980 m (mean 0.010071 m); realized `forearm_y` offsets spanned −0.012405–0.013199 m (mean 0.000901 m).

| Endpoint | R2 result |
|---|---:|
| Task success | 0/20; Wilson 95% CI 0.000–0.161 |
| Task failure | 20/20; Wilson 95% CI 0.839–1.000 |
| Final state | `TRANSPORT` in 20/20 |
| Completion time among successes | Undefined; no successful run |
| Final planar error | Mean 0.046650 m; bootstrap 95% CI 0.045621–0.047751 m |
| Path length | Mean 1.024690 m; bootstrap 95% CI 1.007466–1.042456 m |
| Grasp stability | Mean 15.15 steps; range 15–16 |
| Command corrections | 3.0 in every run |
| Invalid states | 0/20 |

![R2 declared initial states and descriptive final errors](../results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2/p6_initial_state_offsets_final_error.png)

The independent R2 rerun reproduced the full `run_records.json` byte-for-byte, including seed-to-offset mapping, actual states, outcomes, errors, and final states.

### R3 decoder-quality execution status: blocked before analysis

| Planned decoder condition | Eligible immutable trace present? | Execution | Statistical contribution |
|---|---|---|---|
| R2 presumed tiny-CNN/worst | No; only `example-decoder-v1` synthetic-demo fixture is known | Not eligible for quality label | None |
| Mid-tier | No | Not run | None |
| Best-performing | No | Not run | None |
| Three-condition success-proportion test | No eligible three-condition set | Not run | None |

## Discussion

Under the declared R2 simulator-state distribution, the fixed integration fixture did not complete the pick-place task in any of 20 states. This is a negative systems finding and should be retained rather than tuned away. It shows that a compatibility baseline at a single fixed state does not establish robustness over the declared state distribution.

The R3 audit changes the admissible interpretation of R2, while the newly accepted P3 package strengthens the upstream EMG evidence record without satisfying the downstream trace gate. The result cannot be attributed to tiny-CNN/worst decoder quality because the source file does not authenticate that identity. It is equally invalid to infer that a better decoder would—or would not—alter task success. The correct state of evidence is **inconclusive about decoder-quality-to-robustness**, not because a non-significant result was obtained, but because no valid condition contrast was available.

The absence of a trace provenance chain is itself a research-governance result. It prevents unsupported bridge claims between an upstream decoder benchmark and a downstream simulator. The highest-quality next step is not to synthesize plausible traces but to obtain immutable actual decoder outputs and an authoritative manifest. Only then can the locked 20-state design be repeated without moving any other parameter.

## Limitations

R2 uses a MyoSim example/integration fixture, not a real participant-decoder stream. The two-coordinate state factor is a narrow simulator perturbation and is not a clinical or human population distribution. The compatibility baseline is one fixed state, not a control cohort. The all-failure result does not identify a biomechanical/control mechanism. R3 is incomplete: two requested replay traces and a verifiable mapping of all three conditions are unavailable, so neither a Cochran’s Q/Fisher comparison nor an effect estimate of decoder quality exists.

## Conclusion

R2 provides reproducible systems evidence that a fixed MyoSim example replay fails under the specified 20-state perturbation distribution. R3 decoder-quality completion is explicitly blocked by missing trace identity/provenance. The programme therefore makes no claim that decoder quality is independent of, associated with, or causally related to initial-state robustness. This limitation must remain visible in all final programme documents until authentic frozen traces are supplied.

## Data and Code Availability

R2 artefacts are at `results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2/` with an exact independent rerun under `results/real/v2-recovery-r2-independent-rerun/`. The MyoSim source patch is `patches/myosim_v1_1_initial_state_recovery_r2.patch`. The governing R3 stop record is `audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md`. No R3 result directory exists because no R3 execution was authorized. The required trace specification is in `papers/P6_DECODER_QUALITY_EXTENSION_STATUS_V2_RECOVERY_R3.md`.

## References

[1] [Pan et al. (2024), task-level outcomes in myoelectric control, Frontiers in Human Neuroscience](https://doi.org/10.3389/fnhum.2024.1429130)  
[2] [Skomrock et al. (2018), control performance measures, Frontiers in Neuroscience](https://doi.org/10.3389/fnins.2018.00763)
