# Research Registry and Protocol Guide

## Registry Purpose

The local registry answers a narrow, auditable question:

> **What experiment was run, on which declared dataset version, under which protocol, with which model/configuration, producing which metrics and artifacts?**

It is a metadata system of record, not a raw-data warehouse, model store, cloud service, or an attempt to replace the existing tracking/manifests in MyoAdapt, BioSignal-FM, or MyoSim. All raw datasets remain at licensed external/local locations. The registry only saves their dataset card, access/citation context, canonicalization rules, and run/artifact references.

## Persistent Layout

```text
registry/
└── local/
    ├── registry.json   # Atomically written normalized metadata entries
    └── events.jsonl    # Append-only registration/replacement event log
```

The initial catalog is seeded through the committed script below. It is deterministic for the current catalog release.

```bash
PYTHONPATH=src python3 scripts/seed_registry.py --registry-dir registry/local
```

A repeated invocation of the unchanged catalog is idempotent. A material change to a registered entry is rejected unless an explicit replacement is requested by code with documented event context. The event log records the replacement so metadata changes cannot silently rewrite history.

## Seeded Entity Types

| Entity type | Initial entries | Function |
|---|---:|---|
| Project | 5 | Establish ownership boundaries for the umbrella layer and four mature systems. |
| Dataset | 6 | NinaPro DB2/DB3/DB7; BCI Competition IV-2a; WAY-EEG-GAL; MIT-BIH Arrhythmia v1.0.0. |
| Protocol | 5 | EMG LOSO, EEG LOSO, EEG motor imagery, EMG–EEG fusion, and intent-to-control replay. |
| Model | 3 | Reference cards for MyoControl, MyoAdapt, and BioSignal-FM reusable model paths. |
| Benchmark | 3 | Protocol-identified EMG, EEG, and fusion benchmark families with no implied results. |
| Experiment / Run | 0 | Populated only after a validated external result or demonstrator execution exists. |
| Artifact / Report | 0 | Populated only with external output references and factual generated reports. |

The dataset source checks and access notes are preserved in `docs/DATASET_SOURCE_NOTES.md`. They support registry metadata only; researchers remain responsible for checking the exact access terms and data release used in every experiment.

## Dataset Card Governance

A dataset card must specify a modality, source/citation, access condition, available sampling/channel information, task, participant/session context, label schema, canonicalization rules, known limitations, and external version. Where the source collection is insufficiently specific for a chosen release—for example, the WAY-EEG-GAL rate/item metadata—the card says so explicitly and blocks an execution from pretending this is resolved.

| Dataset | Registry status | Execution condition |
|---|---|---|
| NinaPro DB2/DB3/DB7 | Cataloged as externally accessed sEMG sources | Researcher obtains authorized data and registers exact source version/local authorized path. |
| BCI Competition IV-2a | Cataloged as externally accessed EEG source | Researcher agrees to the source’s citation/access terms and provides an authorized local copy. |
| WAY-EEG-GAL | Cataloged for future EEG–EMG work | A chosen release item, sampling metadata, alignment semantics, and protocol must be confirmed before execution. |
| MIT-BIH Arrhythmia v1.0.0 | Cataloged ECG reference path | No umbrella ECG benchmark is part of the MVP scope. |

## Protocol Governance

A protocol is not a model configuration. It freezes the scientific conditions under which comparison may occur: split strategy, train/validation/test semantics, leakage restrictions, preprocessing/feature-selection fit scope, model-selection policy, metrics, statistical unit, seed policy, and limitations.

| Protocol | Status | Valid use |
|---|---|---|
| `emg-loso-v1` | Active | Generic EMG cross-subject benchmark scaffold with subject-level inference and training-only fitting. |
| `eeg-loso-v1` | Draft | EEG foundation scaffold; it becomes operational only after a validated BCI adapter and authorized data execution. |
| `eeg-mi-v1` | Draft | Dataset-specific subject-aware motor-imagery research scaffold. |
| `emg-eeg-fusion-v1` | Draft | Matched unimodal/fusion/missing-modality research scaffold. |
| `intent-to-control-v1` | Active | Deterministic, replay-first MyoSim demonstration path. |

### Paper 3 Protection

**Paper 3 is intentionally not represented as an editable protocol entry in this repository.** Its execution-locked protocol remains external. The umbrella layer may later import a completed exported manifest/result by reference, preserving its original identifiers and protocol text. It must not recreate, revise, or use `emg-loso-v1` as a substitute for Paper 3.

## Creating a Valid Run

A valid `ExperimentRecord` requires an experiment/run ID, project, protocol, dataset/version, modality, subject split, model/version, seed, SHA-256 configuration hash, environment, status, metrics, and artifact references. A terminal run requires a completion timestamp. A failed run requires an error. The registry refuses implicit duplicate overwrites and detects manual modification to a stored document by recomputing its content hash.

> **A matching metric name is not sufficient for comparison.** The benchmark engine will require the same `protocol_id` before aggregation. LOSO statistics use the subject, not individual windows, as the default unit of inference.

## Current Evidence Boundary

The seeded catalog contains **no benchmark results**. It records available research infrastructure, not measured model performance. Synthetic fixtures may validate contract/registry/demo plumbing but are marked ineligible for real-data benchmark aggregation. This prevents a development smoke run from becoming a scientific claim.
