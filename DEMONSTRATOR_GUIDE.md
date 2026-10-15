# Deterministic Intent-to-Control Demonstrator

## Scope

The demonstrator proves the **integration path**, not scientific efficacy:

```text
Synthetic MyoControl-shaped prediction
        ↓
IntentRecord v1
        ↓
Explicit configured label map
        ↓
MyoSim V1 IntentEvent / documented CSV replay contract
        ↓
MyoSim confidence, temporal, state-machine, safety, task, and physics stack
        ↓
MyoSim-owned task/control artifacts
        ↓
Umbrella registry entry and reproducibility manifest
```

> **Evidence status:** The supplied run is a deterministic **synthetic integration fixture**. It is not an EMG benchmark, a validated decoder result, a clinical result, a hardware demonstration, or evidence that one decoder is superior to another.

## Boundary Discipline

The MyoSim adapter consumes an `IntentRecord` and ends at MyoSim’s documented `IntentEvent` boundary. It requires a discrete label, confidence, non-negative replay timestamp, provenance metadata, and an explicit map to the MyoSim V1 vocabulary: `REST`, `OPEN`, `CLOSE`, or `PINCH`. Unsupported labels, continuous intents, guessed mappings, and missing time bases are rejected.

The adapter does **not** create `CommandRequest`, `JointTargets`, control states, safety outcomes, or physics commands. Those remain under MyoSim’s existing controller/safety/simulation ownership.

## Reproducing the Integrated Fixture

The following commands are local-only. They require the independently installed MyoSim runtime and do not modify its repository source.

```bash
# 1. Generate the synthetic upstream prediction → intent → replay bundle.
PYTHONPATH=src python3 scripts/generate_intent_replay.py \
  --output-dir artifacts/integrated_demo

# 2. Run the replay through MyoSim's public pick-and-place CLI from the MyoSim workspace.
myosim run-task --task pick_place \
  --file /absolute/path/to/human-motor-intelligence/artifacts/integrated_demo/adapter_generated_intent_replay.csv \
  --config configs/demo.yaml --record

# 3. Preserve/registry-register the simulator-owned outputs.
PYTHONPATH=src python3 scripts/finalize_integrated_demo.py \
  --myosim-output artifacts/integrated_demo/myosim_task_output.json \
  --replay-bundle artifacts/integrated_demo/replay_bundle.json \
  --output-dir artifacts/integrated_demo \
  --registry-dir registry/local --repo-root .

# 4. Verify the umbrella provenance bundle and every copied artifact hash.
PYTHONPATH=src python3 scripts/verify_manifest.py \
  artifacts/integrated_demo/myosim/<RUN_ID>/umbrella_reproducibility_manifest.json
```

## Verified Integration Run

The generated bundle is stored under `artifacts/integrated_demo/myosim/1f79effb6d464da69da43b114ae74010/`. Its synthetic replay included 33 mapped intent events. MyoSim’s public CLI produced a successful `pick_place` task response and simulator-owned report/metric/transition/GIF artifacts. The umbrella manifest verification checked nine copied artifacts with no hash mismatches.

| Evidence item | Recorded value |
|---|---:|
| MyoSim run ID | `1f79effb6d464da69da43b114ae74010` |
| Evidence class | Synthetic, non-benchmark |
| Replay event count | 33 |
| MyoSim task | `pick_place` |
| MyoSim task success | `true` |
| Completion time | 3.22 s |
| False activation rate | 0.0 |
| Mean confirmation latency | 0.3 s |
| Reproducibility verification | 9 artifacts checked; verified |

These values are **simulator outputs for the documented synthetic fixture only**. They should not be generalized to real subjects, real EMG signals, clinical control, or external task performance.

## Independent Runtime Checks

MyoSim’s strict MuJoCo environment check succeeded, including headless model load/reset/step. The adapter runtime bridge constructs a real MyoSim public `IntentEvent` in the installed MyoSim runtime. With MyoSim 0.1.6 installed, the umbrella test suite has 32 passing tests, including the public intent-event bridge and the reproducibility-path regression test. MyoSim’s own suite (207 tests, both backends, 93.13% coverage) is verified in MyoSim’s release notes; running it requires the optional PyBullet extra.

## Safety and Product Boundary

The demonstrator is replay-first and software-only. It introduces no live hardware connection, no actuation, no patient data, no clinical calibration, no cloud service, and no commercial telemetry. Moving from this fixture to a real decoder output requires an externally run, registered, protocol-compliant study with explicit label mapping, timing semantics, safety review, and reproducibility evidence.
