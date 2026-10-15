# Does Decoder Quality Predict Control Outcome? Real-Replay Evidence Status, Synthetic Boundary, and Repeatability Gate Report

**Version:** V2 Recovery R1 manuscript-status revision  
**Evidence boundary:** Frozen real replay remains separate from synthetic controlled corruption  
**V2 outcome:** Repeated-real-replay extension blocked before pseudo-replication

## Abstract

**Background.** Classifier time-bin accuracy is not by itself a control-system endpoint. Task success, completion time, failure, and correction burden can be essential when an intent stream is mapped into a control simulation. The frozen programme evidence contains a real replay-only systems study and a separate synthetic decoder-quality corruption sweep; these origins must never be pooled.

**V2 objective.** The primary V2 priority was not another biomedical dataset but repeated real replay or wider measured decoder-quality coverage. Repeated execution was permitted only if the simulator exposed a valid independent variation factor such as a seed-linked initial-state distribution.

**Capability result.** Inspection of the user-supplied MyoSim V1.1 runtime found that the runner passes `run.seed` to `MujocoBackend.reset`, which calls `np.random.seed(seed)` followed by `mj_resetData` and `mj_forward`. No seed-dependent perturbation is applied to joint state, object/target state, replay trace, controller policy, or task configuration. The task runner otherwise constructs a fixed task from configuration and static model positions.

**Conclusion.** No valid independent repeat cohort, confidence interval, failure-rate distribution, or decoder-quality dose-response estimate was generated. Changing seed labels on deterministic reruns would be pseudo-replication. The frozen real replay and frozen synthetic sensitivity evidence remain distinct.

## Motivation

Closed-loop evaluation requires endpoints that retain task context. Recent work on myocontrol and human-in-the-loop systems supports considering success, time, and failure-related outcomes rather than treating classifier accuracy as a sufficient proxy [1,2]. This motivates P6 but does not license unvalidated repetition or causal extrapolation from a simulator to clinical control.

The V2 specification ranked repeated real replay and measured decoder-quality coverage ahead of expanding biomedical dataset count. The necessary condition was an honest source of run-to-run independence. A deterministic simulator can be valuable for exact reproducibility, but identical reruns do not estimate variability.

## Frozen Evidence Boundary

| Evidence category | Status | Permitted use | Prohibited use |
|---|---|---|---|
| Frozen V1.1 real replay-only study | Historical real systems evidence | Describe only through its frozen provenance and task/control artefacts | Do not overwrite, rerun into legacy paths, or add V2 repeat labels retrospectively |
| Frozen V1.1 synthetic corruption sweep | Controlled sensitivity study | Study designed corruption-response patterns under explicit synthetic origin | Do not call biomedical validation, real replay evidence, or benchmark eligible |
| V2 repeated real replay | Not run | Report source/capability hard stop | Do not construct synthetic replicates or claim a repeat distribution |

Any synthetic artefact must retain `origin=synthetic_controlled_corruption` and `benchmark_eligible=false`.

## Runtime Capability Audit

The audit examined the installed source path for MyoSim V1.1. The `SyntheticExperimentRunner` and the real `PickPlaceExperimentRunner` both load the model and call `backend.reset(seed=config.run.seed)`. The backend implementation validates a non-negative seed, sets NumPy’s global RNG state, then uses `mujoco.mj_resetData(model, data)` and `mujoco.mj_forward(model, data)`. No sampling operation consumes the seeded RNG to vary the simulator’s initial physical state. The pick-and-place task takes fixed timeout/radius values from YAML and reads body locations from the static model.

| Candidate variation | Evidence in inspected runtime | P6 eligibility |
|---|---|---|
| Seed-dependent joint position/velocity | None | Not available |
| Seed-dependent object or target pose | None | Not available |
| Seed-dependent replay event trace | None | Not available |
| Seed-dependent controller/mapping policy | None | Not available |
| Fixed seed provenance | Present | Reproducibility metadata only |
| Exact deterministic rerun | Available | Useful for engineering replay, not independent replication |

## Decision

The programme stopped before repeat execution. The following actions are prohibited under the current implementation: creating 20 seed-labelled duplicates; averaging duplicate outputs; applying unregistered perturbations; altering controller or decoder mapping to induce variability; or mixing synthetic corruption outputs into real replay evidence.

> A deterministic run may demonstrate repeatability of an implementation, but it cannot serve as a sample of independent task outcomes without a declared mechanism generating distinct states or conditions.

## Reopening Criteria

P6 may be reopened only under a new pre-execution amendment. The amendment must identify a simulator-supported state or task distribution, exact seed-to-state mapping, rationale for retaining the replay/decoder-policy question, anticipated 20-run precision, per-run provenance, success/latency/failure endpoints, and a test showing that seeds produce genuinely different declared states. A hidden local patch does not satisfy this requirement.

## Conclusion

V2 contributes a reproducibility/capability finding rather than a new P6 outcome estimate. The current MyoSim path is deterministic with respect to the inspected seed/reset interface. The scientifically correct action is to preserve real and synthetic evidence boundaries and decline pseudo-replication until valid independent variation can be declared and audited.

## References

[1] [Pan et al. (2024), *Frontiers in Human Neuroscience*](https://doi.org/10.3389/fnhum.2024.1429130)  
[2] [Skomrock et al. (2018), *Frontiers in Neuroscience*](https://doi.org/10.3389/fnins.2018.00763)
