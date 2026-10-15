# Human Motor Intelligence Research Stack — Architecture

## Architectural Intent

The **Human Motor Intelligence Research Stack** is a local-first research integration layer. It connects mature, independently runnable research systems through minimal versioned records and reproducible artifact references. Its purpose is to make a research question traceable from declared dataset and protocol through model output, control outcome, benchmark analysis, and report—without rewriting the systems that already perform those duties.

> **Core research flow:** Biosignal → Representation → Generalisation → Motor Intent → Control → Physical Action → Measurable Outcome.

The umbrella repository is intentionally small. It must not become a shared dependency framework for BioSignal-FM, MyoAdapt, MyoControl, or MyoSim.

## System Context

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                   human-motor-intelligence (umbrella)                    │
│                                                                          │
│  contracts │ registries │ adapters │ orchestration │ benchmarks │ reports│
└───────┬────────────┬──────────────┬───────────────┬──────────────┬───────┘
        │            │              │               │              │
        │            │              │               │              │
        ▼            ▼              ▼               ▼              ▼
┌─────────────┐ ┌───────────┐ ┌─────────────┐ ┌───────────┐ ┌─────────────┐
│BioSignal-FM │ │ MyoAdapt  │ │ MyoControl  │ │  MyoSim   │ │ External    │
│represent /  │ │ generalise│ │ decode      │ │ act /     │ │ datasets    │
│multimodal   │ │ / evaluate│ │             │ │ simulate  │ │ and licenses│
└─────────────┘ └───────────┘ └─────────────┘ └───────────┘ └─────────────┘

No child repository imports this umbrella layer. No raw dataset is owned by it.
```

## Component Responsibilities

| Component | Owns | Does not own |
|---|---|---|
| `research_core.contracts` | Versioned JSON-safe research records and schema validation. | Signal preprocessing, learned encoders, model training, physics/control logic. |
| `research_core.registry` | Local structured metadata for datasets, protocols, models, experiments, runs, artifacts, reports, and benchmarks. | Raw datasets, artifact bytes, remote storage, multi-tenant access control. |
| `research_core.adapters` | Explicit record translation at a documented external boundary and external-manifest ingestion. | Platform-internal algorithms or private module imports as a durable dependency. |
| `research_core.provenance` | Configuration/environment fingerprints, artifact hashing, and reproducibility verification. | Replacing source-project provenance facilities. |
| `research_core.benchmarks` | Protocol-identified aggregation, subject-level summaries, optional valid statistics, and paper-asset generation. | Inventing statistical evidence, promoting synthetic results to benchmark status. |
| `research_core.reporting` | Factual reports and tables derived from registered data. | Scientific interpretation beyond measured outputs. |
| `research_core.orchestration` | Local command execution plans and structured run events. | A cloud scheduler, distributed compute fabric, or child-system implementation. |
| `research_core.cli` | Researcher-facing local workflow: register, validate, compare, report, demo. | Browser dashboard, billing, accounts, telemetry, or SaaS management. |

## Contracts as the Only Cross-System Language

The system has six first-class contracts. Each carries a schema version and is designed for JSON persistence and artifact interchange.

| Contract | Producer examples | Consumer examples | Invariants |
|---|---|---|---|
| `SignalRecord` | BioSignal-FM or an edge dataset adapter | representation pipeline / registry | Modality, time basis, channel metadata, provenance, real/synthetic evidence class are explicit. |
| `RepresentationRecord` | BioSignal-FM encoder export | task / fusion / registry | Encoder identifier/version, dimensions, input provenance, and timing/window mapping are explicit. |
| `IntentRecord` | MyoControl, BioSignal-FM task head, replay bundle | MyoSim adapter / registry | Timestamp, confidence, source model, modality provenance, subject/session provenance, label/vector are explicit. |
| `ControlCommandRecord` | MyoSim result adapter | registry / report | Originating intent, mode, actuator/joint targets, timestamp, and provenance are retained. It is output evidence, not an upstream control bypass. |
| `ExperimentRecord` | Registry, external-manifest adapters | benchmark / reporting | Protocol identity, dataset version, split, model/version, seed, config hash, code commit, environment, status, and referenced outputs are required. |
| `ArtifactRecord` | Registry, every adapter | provenance / reports | Role, URI/path, content hash, media type, producing run, and evidence class are explicit. |

Breaking contract changes require a major schema-version increment. Added optional fields require a minor schema-version increment. Patches clarify validation without changing serialization semantics.

## Explicit Integration Boundaries

### BioSignal-FM Boundary

BioSignal-FM remains the canonical multimodal representation platform. The integration layer accepts exported canonical signal/representation metadata and run artifacts. It may read package-level public contracts at runtime when the optional integration is installed, but all persistent exchange uses the umbrella JSON contract. Preprocessing, encoders, fusion implementation, and task heads remain inside BioSignal-FM.

### MyoAdapt Boundary

MyoAdapt remains the EMG domain-generalisation and evaluation implementation. The integration layer imports its exported run manifest, result tables, model card, dataset card, and artifacts. A MyoAdapt run is registered by reference; the umbrella registry neither changes its split semantics nor re-runs its adaptation methods internally. Paper 3 is an external, execution-locked source of future result manifests only.

### MyoControl Boundary

MyoControl remains the decoding implementation. Its adapter converts a serialized prediction plus caller-supplied timing/provenance context into `IntentRecord`. It never copies MyoControl’s feature engineering or training code. Label mapping to MyoSim’s deliberately smaller V1 vocabulary must be configured explicitly and rejected when ambiguous.

### MyoSim Boundary

The only upstream integration target is MyoSim’s documented intent event boundary. An umbrella `IntentRecord` translates to a MyoSim-compatible `IntentEvent`; MyoSim then retains control over confidence gating, temporal filtering, command state machine, safety, target generation, physics, and task metrics. The adapter never creates MyoSim joint targets or invokes a physics backend directly.

## Local-First Data Flow

```text
1. Register dataset metadata, access conditions, and citation — no dataset copy.
2. Register a protocol that freezes split, fitting scope, metrics, unit of inference, and seed policy.
3. Reference an external model/run or a replay fixture.
4. Validate/import its manifest and output artifacts.
5. Aggregate only records sharing an explicit protocol identity.
6. Produce verified tables, figures, report, and reproducibility bundle.
7. For the demonstrator, replay an intent stream through MyoSim and register generated control/task artifacts.
```

Synthetic fixtures are permitted only for unit, schema, adapter, and deterministic smoke tests. They carry `origin: synthetic` and `benchmark_eligible: false`; benchmark/report routines refuse them as scientific results.

## EEG and Multimodal Path

The EEG foundation path uses a dataset card and an edge adapter to render externally acquired BCI Competition IV-2a data into `SignalRecord` with the true license/access, channel names, sampling rate, epoch semantics, and participant split. It does not store the dataset. A baseline experiment requires actual data and a registered `EEG-LOSO-v1` or `EEG-MI-v1` protocol; therefore no real EEG performance result is present in the initial implementation.

The fusion layer is an interface and protocol scaffold. It requires separately identified encoder outputs, alignment metadata, a declared fusion strategy, and explicit missing-modality cases. It cannot claim cross-modal transfer, multimodal uplift, or missing-modality robustness until those experiments are executed and registered.

## Demonstrator Architecture

```text
Recorded EMG-origin or synthetic replay intent
               │
               ▼
        IntentRecord v1
               │   (configured label map + validation)
               ▼
     MyoSim intent adapter
               │
               ▼
  MyoSim confidence / temporal / safety control
               │
               ▼
 Virtual prosthetic task + native MyoSim metrics
               │
               ▼
 Umbrella ArtifactRecord / ExperimentRecord / factual report
```

The first demonstrator is replay-first, deterministic, local, and software-only. It is scientific communication infrastructure, not a hardware-control product and not a clinical demonstration.

## Quality and Security Rules

All orchestration runs carry a run identifier, stage, project, model, dataset, protocol, status, duration, errors, and artifact references through structured JSON logging. The registry defaults to local paths and SQLite/JSON files. It does not upload data, require credentials, provision cloud resources, or collect telemetry.

No raw clinical/private data, credentials, secret material, proprietary datasets, or false scientific results may enter this repository. Dataset cards record licensed access paths and limitations. Reports only summarize registered measured outputs and visibly distinguish synthetic smoke evidence from real-data results.

## Repository Layout

```text
human-motor-intelligence/
├── src/research_core/
│   ├── contracts/       # Versioned immutable record schemas
│   ├── registry/        # Local registry persistence and queries
│   ├── adapters/        # Thin external-boundary translators
│   ├── provenance/      # Hashes, manifests, reproducibility verification
│   ├── protocols/       # Protocol schema and registered definitions
│   ├── benchmarks/      # Aggregation, statistics, assets
│   ├── reporting/       # Factual reports and paper assets
│   ├── orchestration/   # Local plans/events only
│   └── cli/             # Researcher-facing commands
├── registry/            # Versioned dataset/protocol/model/project metadata
├── configs/             # Demonstration and benchmark configurations
├── examples/            # Replay-only examples; no private/clinical data
├── tests/               # Focused umbrella tests
└── docs/                # Usage, integration, governance, roadmap
```

The provided child repositories are deliberately excluded from this tree. Their independent source locations are supplied explicitly to adapter commands or referenced by artifact URI/path.
