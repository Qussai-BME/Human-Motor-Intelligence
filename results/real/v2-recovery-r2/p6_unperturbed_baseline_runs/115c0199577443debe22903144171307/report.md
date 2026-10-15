# MyoSim V1 Pick-and-Place Run Report

## Run identity

| Field | Value |
|---|---|
| Run ID | `115c0199577443debe22903144171307` |
| Created (UTC) | `2026-08-23T15:52:04+00:00` |
| Git commit | `unavailable` |
| Config hash | `87e03b74bbfca74ee99a159e1818a622dd921573be639b37f35eac3203b9a74f` |
| Physics backend | `mujoco` |
| Model | `<LOCAL_WORKSPACE>/dependencies/myosim_v1_1/assets/models/hand.xml` (`myosim-hand-task-mjcf-v1`) |
| Intent source | `csv-replay:pick_place_replay.csv:a94e59e30e25` |
| Seed | `20260822` |

## Task outcome

| Metric | Value |
|---|---:|
| Task | pick_place |
| Success | True |
| Final state | COMPLETE |
| Completion time (s) | 3.22 |
| Path length (m) | 0.967816 |
| Final target error (m) | 0.049856 |
| Grasp-active steps | 14 |
| Command corrections | 3 |

## Control outcome

| Metric | Value |
|---|---:|
| Input events | 33 |
| Released commands | 1 |
| False activations (synthetic/replay definition) | 0 |
| False activation rate | 0.000000 |
| Unintended transitions | 0 |
| Mean confirmation latency (s) | 0.30000000000000004 |
| State transitions | 5 |

## Interpretation boundary

This file reports a deterministic software simulation under the exact source, model,
configuration, and seed listed above. It is not a clinical validation, medical-device
claim, patient-specific result, biomechanical validation, or evidence of safety in
physical deployment. The replay input must be interpreted according to its own
provenance; packaged examples are synthetic.

## Associated machine-readable artifacts

`provenance.json`, `control_metrics.json`, `task_metrics.json`,
`control_transitions.json`, `task_transitions.json`, and `summary.json` in this
directory preserve the underlying evidence.
