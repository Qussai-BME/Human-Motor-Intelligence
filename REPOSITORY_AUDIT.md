# Phase A — Repository Audit and Architecture Map

> **Audit purpose.** This assessment maps the supplied mature repositories at their documented/public boundaries. It does not alter, vendor, or merge their source code. The umbrella layer described in the master specification will exchange validated records and artifact references with these projects; it will not depend on their internal implementation modules as a shared framework.

## Audit Method and Scope

The supplied archives were extracted into a separate, non-product audit workspace. The audit reviewed top-level package metadata, documented architecture, command-line entry points, declared licenses, test layouts, stable contract types where present, and reproducibility primitives. An initial baseline test invocation was attempted for all four repositories. It was blocked by the audit environment rather than treated as a source failure: `pytest` was absent initially; after its installation, MyoControl lacked `scipy`, while MyoAdapt, BioSignal-FM, and MyoSim lacked the declared `pytest-cov` plugin. No source modification was made to resolve those environment gaps.

| System | Supplied version / identity | Declared license | Primary role in ecosystem | Independently runnable surface | Audit result |
|---|---|---:|---|---|---|
| **MyoControl** | `myocontrol-main`; README describes v0.5 | MIT | EMG feature-based motor-intent decoding | Python package, Streamlit application, FastAPI service, ONNX/realtime paths | Decoder output type identified; baseline test collection blocked by missing `scipy`. |
| **MyoAdapt** | `myoadapt` v2.0.0 | Apache-2.0 | EMG cross-subject generalisation, adaptation, statistics, reproducibility | `myoadapt` CLI, optional REST/WebSocket/UI, local JSON tracking | Manifest and public CLI mapped; baseline test runner blocked by missing `pytest-cov`. |
| **BioSignal-FM V4** | Pre-publication V4 release | Apache-2.0 | Canonical multimodal biosignal representation, modality-aware research workflows | `bsfm` / `biosignal-fm` CLI, optional service/UI, core Python contracts | Canonical `Signal` contract and modality registry mapped; baseline test runner blocked by missing `pytest-cov`. |
| **MyoSim** | V1.1 public release 0.1.3 | Apache-2.0 | Intent replay to bounded virtual prosthetic control and task outcomes | `myosim` CLI, local deterministic replay/tasks/benchmarks | Stable `IntentEvent` and control types mapped; baseline test runner blocked by missing `pytest-cov`. |

## Architectural Roles and Dependency Direction

The four repositories already form complementary research capabilities. The appropriate integration is a **hub-and-spoke, artifact-oriented layer**. The umbrella repository owns contract schemas, registries, adapter logic, orchestration manifests, benchmark aggregation, reports, deterministic demonstration configuration, and documentation. It does not own raw data, platform-internal algorithms, model-training implementations, physics backends, or a shared all-purpose runtime.

```text
                                 ┌──────────────────────────────────────┐
                                 │ human-motor-intelligence (new)        │
                                 │ contracts • registry • benchmarks     │
                                 │ adapters • provenance • reports       │
                                 └─────────────┬────────────────────────┘
                                               │ versioned public records
          ┌───────────────────┬────────────────┼─────────────────┬───────────────────┐
          │                   │                │                 │                   │
          ▼                   ▼                ▼                 ▼                   ▼
  BioSignal-FM V4         MyoAdapt        MyoControl          MyoSim          External datasets
  represent / transfer    generalise      decode              act / simulate  stay external
```

The permitted dependency direction is from the umbrella layer toward **exported artifacts, declared CLI commands, public service endpoints, or documented stable types**. The child repositories must never import the umbrella layer to remain independently runnable. The umbrella package must not reach into a child repository’s private feature extractors, training loops, or backend implementations merely for convenience.

| From | To | Permitted integration form | Explicitly prohibited |
|---|---|---|---|
| BioSignal-FM V4 | Umbrella | Canonical signal/representation exports, run manifests, registered modality metadata, documented service/CLI outputs | Copying modality preprocessing, encoders, or foundation-model internals into umbrella code. |
| MyoAdapt | Umbrella | Result tables, signed manifests, model/dataset cards, locally exported metrics/artifacts | Moving Paper 3 or importing adaptation/training internals into the umbrella package. |
| MyoControl | Umbrella | Structured decoder prediction record or exported inference output | Rewriting its feature/training/deployment stack. |
| Umbrella | MyoSim | Validated intent-event interchange record rendered to MyoSim’s documented `IntentEvent` boundary in an optional adapter environment | Bypassing confidence gating, temporal logic, state machine, or safety layers; emitting joint targets directly. |

## Repository Boundary Map

### BioSignal-FM V4 — Representation and Multimodal Baseline

BioSignal-FM already supplies the strongest canonical biosignal boundary. Its core `Signal` object is immutable, has `(channels, samples)` data, sampling rate, channel names, timestamps, annotations/events, missingness information, subject/session/task context, and explicit provenance. Its `SignalProvenance` identifies origin, dataset/version/license, adapter identity, and synthetic fallbacks. The modality registry declares EMG, EEG, ECG, experimental ECoG/iEEG, and compatibility fNIRS paths with explicit maturity and optional-dependency boundaries.

| Public capability | Existing component evidence | Umbrella reuse decision |
|---|---|---|
| Canonical signal semantics | `biosignal_fm.core.contracts` exposes `Signal`, `SignalMetadata`, `SignalProvenance`, `SignalEvent`, and `SignalBatch`. | The umbrella defines a JSON-safe contract aligned with these semantics; it does not duplicate signal-processing code. |
| Modality declarations | `biosignal_fm.modalities` includes explicit registry/adapters. | Dataset/protocol registry stores compatible modality and adapter metadata only. |
| EEG edge path | README states MNE/BIDS-facing adapters belong at the edge and MNE is optional. | EEG work is a separate adapter/protocol scaffold, with no synthetic benchmark claim. |
| Reproducibility | `RunManifest` records dataset/protocol/config/environment/output hashes. | An adapter maps external manifests into the umbrella experiment record. |
| Fusion | Explicit optional fusion after modality-specific encoders. | Only a fusion interface and missing-modality protocol scaffold will be built now; no performance claim. |

### MyoAdapt v2 — Generalisation, Evaluation, and Provenance Baseline

MyoAdapt already contains EMG loading/preprocessing, LOSO/LODO evaluation, feature paths, adaptation methods, model families, local tracking, statistics, paper assets, model cards, and run manifests. Its architecture is explicitly acyclic and its reproducibility layer exposes a stable JSON manifest with seed, configuration snapshot, environment hash, Git information, timestamps, and output hashes. It is therefore the primary **external EMG benchmark producer**, not a subsystem to be relocated.

| Public capability | Existing component evidence | Umbrella reuse decision |
|---|---|---|
| Subject-aware EMG experiments | `myoadapt` CLI offers train, eval, benchmark, export, audit and related commands; `evaluation` includes LOSO/LODO. | Registry imports exported experiment metadata and metrics. |
| Adaptation research | CORAL, TCA, Subspace Alignment, Euclidean Alignment, adversarial methods, Lite-DAN. | Models/adaptation strategies are referenced by immutable identifiers; implementations remain in MyoAdapt. |
| Statistics and paper assets | Built-in Friedman, Wilcoxon, correction/effect-size/CI and report utilities. | Umbrella adds a minimal, protocol-governed aggregator; it does not substitute or duplicate all MyoAdapt analyses. |
| Provenance | `myoadapt.reproducibility.RunManifest` v1.0 includes outputs with SHA-256 and environment fingerprint. | Adapter imports a normalized view while retaining the external manifest as the source artifact. |
| Paper 3 | Master specification defines Paper 3 as execution-locked. | **No import, move, modification, or protocol recreation.** Only a future exported manifest/result may be ingested. |

### MyoControl — Decoder Baseline

MyoControl is an established EMG decoder product/research artifact. Its public `ClassificationResult` carries the required minimum inference payload: predicted class, confidence, class probabilities, and feature-vector context. It also supports multiple model backends, optional ONNX/realtime inference, and UI/API presentation. Unlike BioSignal-FM and MyoSim, it does not expose a versioned cross-project interchange contract; the umbrella adapter must therefore treat a **serialized prediction result** as the boundary and add the missing timestamp/provenance through explicit caller-provided context.

| Public capability | Existing component evidence | Umbrella reuse decision |
|---|---|---|
| Discrete decoder output | `src.core.classifier.ClassificationResult` is serializable through `to_dict()`. | Wrap an exported/presented prediction into `IntentRecord` with validated timestamp, model provenance, modality provenance, and label mapping. |
| EMG models | `EMGClassifier` supports XGBoost, random forest, LDA, and linear SVC. | Reference by model identifier/version in registry; no model conversion/training rewrite. |
| Edge/realtime | Public ONNX and realtime modules are documented. | Deferred; live integration is outside replay-first demonstrator scope. |
| Explainability | Optional SHAP report generators are documented. | External report artifact may be registered without interpretation by umbrella reporting. |

### MyoSim V1.1 — Control and Simulation Baseline

MyoSim defines a deliberately small stable boundary between an upstream decoder and its control stack. `IntentEvent` requires non-negative timestamp, a constrained discrete intent label, calibrated confidence, source subject, modality, model version, and optional window identifier. It explicitly states that an event is a prediction rather than an actuator command. Control logic, safety, motion targets, physics backend, virtual hand/task, metrics, and provenance remain inside MyoSim. This is precisely the narrow boundary required by the master specification.

| Public capability | Existing component evidence | Umbrella reuse decision |
|---|---|---|
| Intent boundary | `myosim.core.types.IntentEvent`, with `REST`, `OPEN`, `CLOSE`, `PINCH` vocabulary. | Adapter validates/normalizes an umbrella `IntentRecord` and emits a MyoSim-compatible event only when runtime integration is available. |
| Controller command boundary | `CommandRequest` and `JointTargets` are controller/internal downstream values. | **Do not target directly.** The adapter ends at `IntentEvent`. |
| Deterministic replay | README documents local replay and deterministic task artifacts. | Demonstrator uses replayed intent events and records external artifact references. |
| Downstream metrics | Task/control metrics and provenance exist in MyoSim. | Import/attach their emitted metrics/artifact paths; avoid reimplementing simulator metrics. |
| Clinical scope | README states research-only, no medical device/clinical readiness. | All umbrella documentation preserves this non-clinical boundary. |

## Contract Recommendations Resulting from the Audit

The umbrella contract layer should use **immutable, JSON-serializable value records** with schema identifiers and strict semantic validation. It must deliberately use neutral, project-agnostic names and match only the intersection of existing public requirements.

| Umbrella record | Primary producer(s) | Primary consumer(s) | Compatibility anchor |
|---|---|---|---|
| `SignalRecord` | BioSignal-FM adapter; future EEG adapter | registry, representation adapter | BioSignal-FM `Signal` metadata/provenance semantics. |
| `RepresentationRecord` | BioSignal-FM or other model-export adapter | registry, fusion scaffold, decoder adapter | Modality/encoder/version/input-provenance fields from master specification. |
| `IntentRecord` | MyoControl adapter, BioSignal-FM task-head export, replay fixture | MyoSim adapter, registry, demonstration | MyoControl classification output plus MyoSim `IntentEvent` requirements. |
| `ControlCommandRecord` | MyoSim artifact adapter only | registry/reporting | MyoSim command/targets are captured as output evidence, not authored upstream. |
| `ExperimentRecord` | registry and external-manifest adapters | benchmark/reporting | MyoAdapt/BioSignal-FM reproducibility manifest fields. |
| `ArtifactRecord` | all adapters and registry | provenance/reporting | SHA-256, role, URI/path, producing run, media type. |

## Baseline Test and Environment Findings

The audit attempted each documented default test command from the isolated source extraction. These findings establish **environment verification status**, not quality claims about the repositories.

| Repository | Attempted command | Observed result | Correct next action |
|---|---|---|---|
| MyoControl | `pytest -q` | Collection reached project code but failed because `scipy` was unavailable. | Verify in its declared dependency environment or project virtual environment. |
| MyoAdapt | `pytest tests/ --no-cov -q` | Project configuration referenced `pytest-cov`, which was not installed in the audit environment. | Install declared dev/test extras in a clean isolated environment, then execute. |
| BioSignal-FM V4 | `pytest -q` | Project configuration referenced `pytest-cov`, which was not installed in the audit environment. | Install declared dev/test extras in a clean isolated environment, then execute. |
| MyoSim | `pytest -q` | Project configuration referenced `pytest-cov`, which was not installed in the audit environment. | Install declared dev/test extras in a clean isolated environment, then execute headlessly. |

The umbrella repository will not fix, hide, or patch any child-project test condition. It will provide its own focused contract, adapter, registry, reporting, reproducibility, and demonstration tests.

## Security, Data Governance, and License Compatibility

The three Apache-2.0 repositories and MyoControl’s MIT license permit a separate local-first umbrella repository, provided attribution/notices are maintained for any redistributed content. The umbrella code will not redistribute child source code, model weights, raw biosignal recordings, credentialed datasets, or secrets. Dataset registry entries contain source/licensing/access metadata only; they do not embed datasets. Synthetic fixtures carry explicit `synthetic` origin and are barred from benchmark reporting.

## Phase A Conclusion

The audit validates the master specification’s central architectural premise: the mature systems already expose enough capability for a thin connective layer. BioSignal-FM owns canonical multimodal representation semantics; MyoAdapt owns extensive EMG evaluation and reproducibility workflows; MyoControl produces decoder predictions; MyoSim owns control safety and simulation. The umbrella project can now proceed to versioned contracts without a monolith, shared giant framework, or scientific overclaim.

## Audit Evidence Files

The transient audit workspace contains the captured archive inventory, declared package metadata, public-surface inventory, and test logs. It is outside this repository and is not an implementation dependency. The durable conclusions are recorded in this document and in `ARCHITECTURE.md`.
