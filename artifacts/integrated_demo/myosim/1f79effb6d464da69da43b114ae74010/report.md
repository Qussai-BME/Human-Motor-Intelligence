# MyoSim V1 Pick-and-Place Run Report

## Run identity

| Field | Value |
|---|---|
| Run ID | `1f79effb6d464da69da43b114ae74010` |
| Created (UTC) | `2026-08-22T17:51:17+00:00` |
| Git commit | `unavailable` |
| Config hash | `ac74a486ddad14ee5bc343afb1cd091451d0ef32344c4333a8d2406d27aada89` |
| Physics backend | `mujoco` |
| Model | `/usr/local/lib/python3.12/dist-packages/myosim/resources/assets/models/hand.xml` (`myosim-hand-task-mjcf-v1`) |
| Intent source | `csv-replay:adapter_generated_intent_replay.csv:8cebfaf08d92` |
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
