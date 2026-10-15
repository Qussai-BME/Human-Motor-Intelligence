# Versioned Cross-Project Contracts

## Purpose and Scope

The contract layer is the **only durable cross-project language** in the Human Motor Intelligence Research Stack. It describes records exchanged among independent systems and records the provenance required to interpret them. It is not a shared signal-processing library, model interface, physics API, or a replacement for the mature platforms.

All records are immutable Python dataclasses with deterministic JSON serialization, strict `major.minor.patch` schema versions, and content hashing. The current supported schema is **v1.0.0**. A record with an unsupported major schema version is rejected. New optional fields require a minor version increment; a meaning-changing field, removal, or incompatible validation change requires a major increment.

| Design decision | Rationale |
|---|---|
| JSON-safe metadata plus artifact references | Keeps raw datasets and large arrays external, local, licensed, and out of Git. |
| Immutable value records | Prevents post-validation mutation from silently invalidating provenance. |
| Explicit evidence class | Stops synthetic smoke fixtures from entering real-data benchmark summaries. |
| Explicit protocol/run identity | Prevents protocol-free leaderboards and ambiguous comparisons. |
| Content SHA-256 where material is available | Allows report and manifest verification without introducing remote artifact storage. |
| Project-neutral names | Avoids embedding any child repository’s internal implementation details in the umbrella layer. |

## Contract Inventory

| Contract | Stable kind | Required core semantics | Primary producer examples | Primary consumer examples |
|---|---|---|---|---|
| `SignalProvenanceRecord` | `signal_provenance` | Evidence class, dataset/version, license, adapter, source, creation time | BioSignal-FM or an edge dataset adapter | Every signal, representation, and intent record |
| `SignalRecord` | `signal` | Modality, sampling rate, channels, sample count, optional external data reference, participant/session/task/window context | BioSignal-FM / EEG adapter | representation workflows, registry |
| `RepresentationRecord` | `representation` | Encoder/model identity/version, dimensions, input signals, provenance, values or external tensor reference | BioSignal-FM model export | task/fusion research records, registry |
| `IntentRecord` | `intent` | Time, confidence, one discrete label or one continuous vector, source model/version, modalities, subject/session provenance | MyoControl prediction adapter, representation task head, replay bundle | MyoSim adapter, registry |
| `ControlCommandRecord` | `control_command` | Timestamp, mode, originating intent, targets, validity and provenance | MyoSim result import | registry / downstream report |
| `ArtifactRecord` | `artifact` | Role, producer run, location, optional hash, evidence class, media metadata | Every adapter or registry action | provenance / reporting |
| `ExperimentRecord` | `experiment` | Dataset/protocol/model/version/split/seed/config hash/environment/status/metrics/artifacts | registry / MyoAdapt and BioSignal-FM manifest adapters | benchmark and reporting engines |

## Core Invariants

### Evidence and Data Governance

`EvidenceClass` is one of `real`, `synthetic`, or `unknown`. A synthetic provenance record must carry a reason, and a `synthetic` run is not benchmark-eligible. Raw signal/tensor content is not serialized into the registry. `SignalRecord.data_uri` and `RepresentationRecord.tensor_uri` are local or permitted URI references only; they reject URI userinfo to avoid committing credentials.

| Evidence state | Permitted use | Prohibited use |
|---|---|---|
| `real` | Registered real-data experiment or benchmark input when the associated protocol/license is complete | Interpreting without its dataset card, protocol, and provenance. |
| `synthetic` | Unit tests, smoke tests, contract demonstrations, deterministic development paths | Benchmark, baseline, scientific inference, clinical-performance or generalisation claim. |
| `unknown` | Incomplete import awaiting governance review | Benchmark aggregation and unqualified report claims. |

### Signal and Representation Semantics

A `SignalRecord` has a positive sampling rate, nonempty unique channels, positive sample count, and explicit `SignalProvenanceRecord`. It can reference external raw data but does not contain data arrays. A `RepresentationRecord` references one or more input signal IDs and must contain either a finite inlined small vector matching its declared dimension or a tensor artifact reference. This mirrors BioSignal-FM’s explicit separation of signal, representation, modality, and provenance without recreating its processing implementation.

### Intent-to-Control Semantics

An `IntentRecord` is always a **prediction**, never an actuator command. It has a timezone-aware timestamp, confidence in `[0,1]`, source model/version, and at least one modality. It holds exactly one semantic output: either a discrete `label` or continuous `values`. Class probabilities, when supplied, must sum to one.

MyoSim’s V1 intent vocabulary is intentionally narrower than upstream EMG classifiers. The MyoSim adapter accepts only explicitly configured mappings. It translates an `IntentRecord` to a MyoSim-compatible event only when all conditions below are satisfied.

| Requirement | Why it is required |
|---|---|
| Discrete upstream `label` is present | MyoSim V1 event interface is discrete. |
| Explicit mapping exists to `REST`, `OPEN`, `CLOSE`, or `PINCH` | Prevents a gesture label being guessed as a control command. |
| `stream_time_seconds` is present or deterministically derived by replay configuration | MyoSim requires a non-negative relative replay timestamp. |
| Model version, modality, source subject, and window ID are retained where available | Preserves MyoSim’s stable intent event provenance fields. |
| The event is handed to MyoSim control logic, not directly to physics/joint targets | Retains confidence gating, temporal logic, safety, and state-machine control. |

`ControlCommandRecord` is a **downstream evidence record** obtained from a MyoSim result. The umbrella layer does not create simulator joint targets or bypass MyoSim control safety.

### Experiment and Artifact Semantics

An `ExperimentRecord` declares the irreducible identity of a study execution. It requires experiment/run/project/protocol/dataset/model identifiers, dataset and model versions, modality, subject split, seed, configuration SHA-256, status, environment, metric mapping, and artifact IDs. Terminal statuses require a completion timestamp; failed runs require an error string. The record deliberately stores aggregate metrics as numbers but does not assume a metric is valid—its associated protocol determines which metrics and inference are appropriate.

`ArtifactRecord` references a producing run and its role. Its URI/path, optional SHA-256, media type, size, creation time, and metadata permit provenance without duplicated object storage. An external MyoAdapt/BioSignal-FM/MyoSim manifest always remains the source artifact; importing it never converts the umbrella registry into a replacement provenance engine.

## Existing-System Mapping

| Mature system | Existing public boundary | Umbrella contract mapping | Non-goal |
|---|---|---|---|
| BioSignal-FM V4 | Canonical signal/provenance and modality concepts; representation and run manifests | `SignalProvenanceRecord`, `SignalRecord`, `RepresentationRecord`, `ExperimentRecord`, `ArtifactRecord` | Copying preprocessors, modality registry internals, encoders, or fusion code. |
| MyoAdapt v2 | JSON `RunManifest`, result tables/artifacts, LOSO/LODO study outputs | `ExperimentRecord` and `ArtifactRecord`, with external manifest kept by reference | Altering or recreating adaptation methods, statistics, or Paper 3. |
| MyoControl | Serialized classification result: class, confidence, probabilities, feature context | `IntentRecord`, with timestamp/provenance supplied by adapter caller | Importing/rebuilding feature extraction, training, deployment, or explainability internals. |
| MyoSim V1.1 | `IntentEvent` and external replay/task artifacts | `IntentRecord` in; `ControlCommandRecord` and artifact/metric evidence out | Direct backend, state machine, command, safety, or target manipulation. |

## Compatibility and Persistence Rules

Records are persisted as canonical JSON after being validated in memory. Consumers must check `contract_kind` and `schema_version` before reading. Consumers may ignore unknown optional fields only where the schema major version is supported. The registry maintains a `content_hash` for each stored record to detect changes. Artifact content hashes remain distinct from record content hashes.

> **Protocol identity is mandatory for comparison.** Records from different `protocol_id` values must not appear in the same leaderboard or statistical comparison merely because their metric names match.

## Reference Implementation

The reference implementation resides in `src/research_core/contracts/`. Its focused test suite validates immutability, schema safeguards, synthetic-data rejection, deterministic serialization, experiment status invariants, confidence/probability semantics, and secret-bearing URI rejection. The contract package has no dependency on BioSignal-FM, MyoAdapt, MyoControl, MyoSim, external databases, or cloud services.
