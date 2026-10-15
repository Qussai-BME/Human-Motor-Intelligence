# V2 P6 Initial-State Capability Preflight — Recovery R2

**Protocol ID:** `p6-real-replay-initial-state-repeats-recovery-r2`  
**Status:** **Pass — the declared 20-seed cohort is authorized.**  
**Precondition records:** `V2_P6_UNPERTURBED_BASELINE_MATCH_RECOVERY_R2.md` and `V2_PROTOCOL_AMENDMENT_RECOVERY_R2_003_P6.md`.

## Checks Performed

| Check | Result | Evidence |
|---|---|---|
| Unperturbed baseline before modification | Pass | Exact endpoint match to preserved benchmark; `V2_P6_UNPERTURBED_BASELINE_MATCH_RECOVERY_R2.md` |
| Unperturbed baseline after modification | Pass | `v2r2_p6_postpatch_baseline.log`; success, `COMPLETE`, 3.22 s completion, 0.04985601966004137 m final error, 14 grasp-stability steps, and 3 corrections exactly match the preserved benchmark values |
| Unit/integration tests | Pass | `3 passed` for new initial-state tests plus existing deterministic pick-place benchmark |
| Probe seed 20260901 | Pass for state validity | `forearm_x=0.012643603681518822 m`; `forearm_y=0.002472205430941149 m`; no invalid state |
| Probe seed 20260902 | Pass for state validity | `forearm_x=0.018459270615720027 m`; `forearm_y=0.003767357688051722 m`; no invalid state |
| Distinct declared states | Pass | The two offsets and full initial qpos vectors differ; all nondeclared named joint positions are identical in the recorded probe summaries |
| Range enforcement | Pass | Both probes lie within `[0, 0.020] m` for `forearm_x` and `[−0.015, +0.015] m` for `forearm_y` |
| Replay/controller/task identity | Pass | Same replay SHA-256 `a94e59e30e2599eb92517198739dff96aa40b01f3bf6777756722e09960e09f3`; unchanged control/task settings in each run record |

## Interpretation Boundary

The probes establish **physical-state variation**, not biological variation and not decoder-quality variation. Both probe runs ended in `TRANSPORT` without invalid state. This early failure pattern is retained as an observed probe outcome but was **not** used to alter the predeclared perturbation range, seed set, replay, controller, decoder mapping, task geometry, or endpoints. The full 20-seed cohort will retain all declared seeds and quantify its failure distribution rather than tune it away.

The probe directory is a technical capability artefact, not part of the 20-run analytical cohort:

```text
results/real/v2-recovery-r2/p6_initial_state_variability_probes/
```

## Authorization

The implementation exposes an explicit, seed-linked `uniform_forearm_xy_v1` initial-state factor. Each run records the distribution ID, configured ranges, realized offsets, initial qpos, initial named joint positions, replay hash, configuration, code fingerprint, and task/control results. The conditions required by the amendment are met; the fixed seed cohort `20260901`–`20260920` may proceed without further protocol change.
