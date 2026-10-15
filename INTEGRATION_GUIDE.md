# Integration Guide

## Integration Model

The umbrella layer integrates mature systems through **public serialized outputs, artifact references, documented command surfaces, and minimal value translations**. It does not vendor source repositories, reach into private module implementations, or require a child repository to install/import the umbrella package. This preserves independent execution, release cadence, and scientific ownership.

| Integration | Adapter | Input boundary | Output boundary | Deliberate exclusion |
|---|---|---|---|---|
| BioSignal-FM V4 signal | `signal_from_biosignal_fm_export` | JSON-like canonical signal metadata export | `SignalRecord` | No preprocessing/modality registry/encoder import. |
| BioSignal-FM V4 representation | `representation_from_biosignal_fm_export` | JSON-like representation export | `RepresentationRecord` | No encoder/fusion/task-head import. |
| MyoControl | `intent_from_myocontrol_prediction` | Serialized `predicted_class`, confidence, optional probabilities plus caller timing/context | `IntentRecord` | No feature, training, ONNX, realtime, or UI import. |
| MyoAdapt | `import_myoadapt_manifest` | Exported JSON run manifest and referenced output paths | `ExperimentRecord` plus `ArtifactRecord` references | No adaptation/evaluation implementation import; no Paper 3 modification. |
| MyoSim | `intent_to_myosim_event` | Validated discrete `IntentRecord` and explicit label map | Optional MyoSim V1 `IntentEvent` at runtime | No controller/state/safety/physics/joint-target bypass. |

## BioSignal-FM V4

The BioSignal-FM adapter accepts a public mapping that describes a canonical signal or representation. It deliberately needs no installed BioSignal-FM dependency. At integration time, the external project can serialize its documented signal/metadata/provenance fields and write a small JSON export beside its own artifact. The umbrella adapter validates it into an immutable record.

```python
from research_core.adapters import signal_from_biosignal_fm_export

signal = signal_from_biosignal_fm_export({
    "signal_id": "eeg-window-0001",
    "sample_count": 1000,
    "data_uri": "authorized-data/eeg-window-0001.npy",
    "metadata": {
        "modality": "eeg",
        "sampling_rate_hz": 250,
        "channel_names": ["C3", "C4"],
        "provenance": {
            "origin": "real",
            "source_dataset_id": "bci-competition-iv-2a",
            "dataset_version": "operator-verified-release",
            "license_id": "operator-verified-terms",
            "details": {"benchmark_eligible": False},
        },
    },
})
```

The adapter intentionally defaults `benchmark_eligible` to `false` unless a validated ingest workflow states otherwise. A mapping’s mere existence does not establish that data access, protocol, or scientific conditions were satisfied.

## MyoControl

The MyoControl adapter consumes only the public prediction shape: a predicted class, confidence, and optional normalized class probabilities. The caller must supply the timestamp, model identifier/version, source subject/session/window context where available, and provenance. This is necessary because a standalone prediction is not a reproducible temporal/control event.

```python
from research_core.adapters import intent_from_myocontrol_prediction

intent = intent_from_myocontrol_prediction(
    {"predicted_class": "open_hand", "confidence": 0.91,
     "probabilities": {"open_hand": 0.91, "rest": 0.09}},
    intent_id="decoder-event-0001",
    timestamp_utc="2026-08-22T12:00:00+00:00",
    stream_time_seconds=0.0,
    source_model_id="myocontrol-classical-decoder",
    model_version="0.5",
    external_provenance={"origin": "synthetic", "fallback_reason": "integration smoke fixture"},
)
```

The result remains a prediction. An explicit configured label map is still needed before it can enter MyoSim’s small V1 intent vocabulary.

## MyoAdapt

MyoAdapt’s `RunManifest` remains the original provenance artifact. The importer receives its parsed JSON and the manifest path/URI, then produces an imported experiment record and separately registered artifact references. It preserves configuration hash evidence, environment/Git metadata, seed, outputs, and the source manifest location. It does not infer that the result is benchmark-eligible; the default is `false`.

```python
import json
from research_core.adapters import import_myoadapt_manifest

external = json.loads(open("external/myoadapt/manifest.json", encoding="utf-8").read())
bundle = import_myoadapt_manifest(
    external,
    manifest_uri="external/myoadapt/manifest.json",
    experiment_id="imported-exp-001",
    run_id="imported-run-001",
    protocol_id="emg-loso-v1",
    dataset_id="ninapro-db7",
    dataset_version="operator-verified-release",
    modality="emg",
    subject_split="leave-one-subject-out",
)
```

### Paper 3

Paper 3 is execution-locked and remains external. Do not use the generic `emg-loso-v1` scaffold to recreate it or change it. A future import must use the exact exported Paper 3 manifest/result and retain the source protocol identity. The initial implementation does not include a Paper 3 importer shortcut, deliberately avoiding accidental reinterpretation.

## Adapter Error Policy

| Condition | Adapter response |
|---|---|
| Missing required external field | Raises `AdapterError`; no partial contract is produced. |
| Invalid confidence, timestamp, probability sum, or ID | Raises `AdapterError` wrapping contract validation. |
| Invalid provenance origin or missing synthetic rationale | Raises `AdapterError`; synthetic evidence remains explicit. |
| External run lacks proof of benchmark eligibility | Imports with `benchmark_eligible: false`. |
| Unsupported/ambiguous MyoSim label mapping | Will raise a MyoSim adapter error; no command is guessed. |
| No installed optional child package | Mapping adapters still work; runtime-specific adapter reports an availability error. |

## Independence Check

The adapter package has no package dependency on BioSignal-FM, MyoAdapt, MyoControl, or MyoSim. It can be tested with JSON-like fixtures. Optional runtime interoperation, where necessary, is localized to an adapter function and does not alter a child repository. This ensures that deleting the umbrella project cannot prevent any mature repository from running on its own.
