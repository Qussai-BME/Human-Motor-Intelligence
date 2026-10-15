# Integrated Replay Demonstration

> **Evidence status:** synthetic deterministic integration fixture. This is not a biosignal benchmark, decoder validation, clinical result, or hardware demonstration.

## Flow

Serialized synthetic MyoControl-shaped prediction → `IntentRecord` → explicit MyoSim label map → MyoSim CSV replay → MyoSim control/safety/task pipeline → simulator-owned metrics and recordings.

## MyoSim-Reported Outcomes

| Metric | Value |
|---|---:|
| Task | pick_place |
| Success | True |
| Completion time (s) | 3.22 |
| Final state | COMPLETE |
| False activation rate | 0.0 |
| Mean confirmation latency (s) | 0.30000000000000004 |

## Reproducibility

The replay bundle and copied MyoSim artifacts are hashed in `umbrella_reproducibility_manifest.json`. The registered run ID is `1f79effb6d464da69da43b114ae74010`.
