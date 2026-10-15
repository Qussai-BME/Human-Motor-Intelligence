# MyoSim Initial-State Recovery R2 Patch

## Purpose

`myosim_v1_1_initial_state_recovery_r2.patch` is the minimal source extension used by P6 Recovery R2. It is derived against the user-provided archive `MyoSim_V1.1_Public_Release_0.1(1).zip`, source root `MyoSim_V1.1_Public_Release_0.1.3`.

**Patch SHA-256:** `8f07a68f903c5aa749798016e1ea70ac24d337e8d6fff24681dea069bdf91fe2`

The patch modifies only three MyoSim files:

| File | Change |
|---|---|
| `src/myosim/core/config.py` | Adds an inert-by-default, validated `initial_state` configuration section. |
| `src/myosim/simulation/mujoco_backend.py` | Adds named-joint reset offsets with MuJoCo joint-range validation and actual initial-state metadata. |
| `src/myosim/experiments/task_runner.py` | Samples the declared state factor from the run seed and records realized state metadata in task artefacts. |

It does **not** change the CSV replay, decoder stream, controller parameters, task geometry, object/target state, success rule, or default deterministic execution path. The default `initial_state` configuration is disabled and requires zero offset ranges.

## Application

Apply only to a clean unpacking of the declared MyoSim release:

```bash
cd MyoSim_V1.1_Public_Release_0.1.3
patch -p1 < /path/to/myosim_v1_1_initial_state_recovery_r2.patch
PYTHONPATH=src pytest -q -o addopts='' \
  tests/integration/test_initial_state_perturbation.py \
  tests/integration/test_pick_place_benchmark.py
```

The R2 release separately includes `tests/integration/test_initial_state_perturbation.py`; copy it to the corresponding test path before running the final command if it is not present in the original release tree.

## Audit Boundary

This patch enables only the registered P6 `uniform_forearm_xy_v1` initial-state factor. Applying it does not grant permission to alter the R2 state ranges, replay, controller, task, seed cohort, or study endpoints. Any such change requires a new protocol and evidence namespace.
