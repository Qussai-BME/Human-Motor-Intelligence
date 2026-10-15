# V2 Protocol Amendment Recovery R2 003 — P6 Initial-State Repeat Study

**Protocol ID:** `p6-real-replay-initial-state-repeats-recovery-r2`  
**Registered:** 2026-08-23 (GMT+3), before the MyoSim patch, perturbed-run generation, or outcome analysis.  
**Scope:** New V2 Recovery R2 real-replay systems evidence only.  
**Does not modify:** Frozen V1/V1.1 P6 real replay, frozen synthetic controlled-corruption sweep, P4/P5 results, task/replay/decoder mappings, or historical result paths.

## Reopening Basis

The R1 capability audit correctly stopped P6 because `run.seed` was not consumed to vary state. The current R2 unperturbed baseline now reproduces the preserved pick-place endpoints exactly (`audit/V2_P6_UNPERTURBED_BASELINE_MATCH_RECOVERY_R2.md`). This amendment therefore adds the smallest auditable capability sufficient for an independent *simulated initial-state* cohort. It does not pretend that deterministic seed labels alone are replicates.

## Fixed Variation Factor

After `mj_resetData`, and before task/controller construction, each run will draw two independent initial joint-position offsets using `numpy.random.default_rng(run.seed)`:

| Joint | Offset distribution | Rationale |
|---|---|---|
| `forearm_x` | Uniform [0.000, 0.020] m | Keeps the initial slider state inside the model’s [0.000, 0.460] m range while producing a bounded starting-position displacement. |
| `forearm_y` | Uniform [−0.015, +0.015] m | Bounded lateral initial-state displacement within the model’s [−0.120, +0.150] m range. |

The base model qpos, object state, target state, CSV replay, decoder output stream, controller policy, timing, task geometry, success rule, and all other joint positions remain unchanged. The patch must set velocity and actuator-control state to the model reset values, set only the two declared qpos addresses, call `mj_forward`, and record every realized offset plus the observed initial qpos and named joint positions.

## Run Set and Precision Rationale

The study uses exactly 20 seeds: `20260901` through `20260920`, one task execution per seed. Twenty declared state realizations are sufficient to expose a failure distribution or a precision limitation without turning the programme into an unbounded simulation sweep. No seed may be replaced after observing outcomes. The baseline seed `20260822` remains a separate unperturbed validation and is not included in the 20-run cohort.

## Endpoint Hierarchy

| Tier | Endpoint | Interpretation boundary |
|---|---|---|
| Primary | Task success proportion | Success across the declared initial-state distribution; report exact count and Wilson 95% interval. |
| Primary | Completion time among successful runs | Descriptive median, mean, range, and bootstrap 95% CI for mean. |
| Primary | Final planar error | Descriptive across all valid runs. |
| Secondary | Failure proportion and final state | Separate from success; report exact count and Wilson 95% interval. |
| Secondary | Command corrections, grasp-stability steps, invalid-state count | Systems quality/context endpoints only. |
| Quality control | Realized offsets and initial-state summary | Must prove that the seeds create distinct declared initial states within range. |

The study will not estimate a decoder-quality dose response because the replayed decoder stream is fixed. It may only characterize task outcome sensitivity to the declared initial-state distribution under that one replay/control mapping.

## Required Acceptance and Stop Conditions

Before the 20-run analysis, execute at least two distinct-seed perturbation probes and stop if the recorded offsets or observed initial state do not differ, exceed configured ranges, affect undeclared joints, produce invalid state before task stepping, or alter the unperturbed baseline path when perturbation is disabled. Stop and document failure if tests fail, raw/replay identity changes, source code cannot record the realized state, or any run is missing its complete provenance/artifact.

Every run must include a deterministic seed, configured distribution ID/ranges, actual offsets, initial qpos summary, replay checksum, config hash, code commit/diff fingerprint, and task/control outputs. Real replay and synthetic controlled corruption remain separate: synthetic outputs retain `origin=synthetic_controlled_corruption` and `benchmark_eligible=false` and do not enter this cohort.

## Reproducibility Requirement

After the primary 20 runs, an independent rerun must regenerate the same seeds and reproduce per-run realized offsets and task/control outputs exactly before manuscript integration. It is an execution reproducibility check, not a second 20-run statistical cohort.
