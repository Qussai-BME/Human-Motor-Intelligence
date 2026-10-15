# V2 P6 Replay-Variability Capability Audit: Hard Stop

**Recorded:** 2026-08-23 (GMT+3)  
**Component:** P6 real replay strengthening  
**Decision:** **STOP — no repeated-real-replay cohort is authorized in the current MyoSim V1.1 runtime.**

## Required Capability

The V2 specification permits repeated real replay only if a valid, predeclared source of independent variation exists, such as seed-driven initial-state variation or an equivalent task variation that does not alter the mapping, replay trace, or policy merely to manufacture a distribution. Repeated execution of an unchanged deterministic simulation is **not** an independent sample and cannot be relabelled as `n=20`.

## Inspected Runtime Evidence

The audit inspected the user-supplied MyoSim V1.1 source extracted at `<LOCAL_WORKSPACE>/dependencies/myosim_v1_1`, specifically the publicly packaged implementation used by the existing Human Motor integration.

| Code path | Observed implementation | Consequence |
|---|---|---|
| `SyntheticExperimentRunner.run` | Loads model then calls `backend.reset(seed=config.run.seed)` | Seed is passed to backend. |
| `PickPlaceExperimentRunner.run` | Loads model then calls the same `backend.reset(seed=config.run.seed)` | Real task replay uses the same reset path. |
| `MujocoBackend.reset` | If a seed is supplied, calls `np.random.seed(seed)`; then calls `mujoco.mj_resetData(model, data)` and `mujoco.mj_forward(model, data)` | No sampled perturbation is applied to `qpos`, `qvel`, object pose, target pose, event trace, controller policy, or task parameters. |
| `PickPlaceExperimentRunner` task setup | Instantiates fixed `PickPlaceTask` from config and reads static model body positions | No exposed random initial state or task distribution. |
| Task YAML files | Record a fixed `run.seed`; define fixed model, timestep, timeout, radius, and control values | Seed metadata exists, but no meaningful seed-dependent variation is exposed. |

The implementation labels the adapter itself “Deterministic” and documents replay consistency under fixed configuration and seed. The seed is useful provenance, but in the inspected code it does not instantiate a new initial-state draw. Replacing only its value would therefore generate deterministic reruns of effectively identical conditions, not independent repeats.

## Decision and Boundary

> The programme will not perform pseudo-replication by rerunning the same replay with seed labels, averaging duplicated outputs, adding synthetic perturbations, or changing the decoder mapping/task/controller solely to obtain variance.

No new P6 numeric endpoint, confidence interval, task-success rate, latency distribution, failure distribution, or quality-dose relationship is created under this audit. The prior real replay evidence remains frozen and must not be overwritten; the prior controlled synthetic corruption sweep remains separate and must retain `origin=synthetic_controlled_corruption` and `benchmark_eligible=false`.

## What Would Be Needed to Reopen P6

A later P6 amendment must precede execution and identify a valid exposed factor, its scientific rationale, exact distribution, seed-to-state mapping, 20-run precision rationale, per-run provenance, and a verification that it preserves the intended replay/decoder-policy research question. Examples could include a simulator-supported, documented initial pose/object/target-state distribution, but no such mechanism was found in the inspected V1.1 path. It would require a separate versioned implementation and protocol review, not a hidden local patch.

## Status

`P6_repeated_real_replay_v2`: **blocked by deterministic-runtime limitation; no replicate results were generated.**
