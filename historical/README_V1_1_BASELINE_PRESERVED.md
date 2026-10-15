# Human Motor Intelligence Research Stack

## Purpose

This repository is a **thin, local-first integration layer** for mature research systems in human motor intelligence. It preserves the independent execution and ownership of **BioSignal-FM V4**, **MyoAdapt v2**, **MyoControl**, and **MyoSim V1.1**. It does not vendor, rebuild, or merge those systems.

The umbrella layer provides versioned interchange contracts, local research registries, provenance manifests, protocol-governed benchmark infrastructure, mapping-only adapters, a replay-first MyoSim demonstrator, EEG/multimodal study scaffolds, and a local Research-OS command-line MVP.

> **Evidence boundary:** The included end-to-end demonstrator is a synthetic, deterministic integration fixture. It is not a real biosignal benchmark, a decoder validation result, a clinical claim, or a live-hardware demonstration.

## Quick Start

```bash
cd human-motor-intelligence
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local seed
PYTHONPATH=src pytest -q
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local integrity
PYTHONPATH=src python3 scripts/verify_integrated_demo.py \
  --root artifacts/integrated_demo --registry-dir registry/local
```

## Architecture

```text
Mature systems (remain independent)
  BioSignal-FM ─┐
  MyoAdapt ────┼─ public exports / artifact references / explicit mapping
  MyoControl ──┤
  MyoSim ──────┘
               ↓
  Human Motor Intelligence umbrella layer
  ├── versioned contracts
  ├── local registry and provenance
  ├── protocol/benchmark safeguards
  ├── thin adapters
  ├── EEG/fusion preparation
  ├── replay-first demonstrator evidence
  └── local Research-OS CLI
```

The complete boundary diagram and ownership rules are in [ARCHITECTURE.md](../ARCHITECTURE.md); the repository audit is in [REPOSITORY_AUDIT.md](../REPOSITORY_AUDIT.md).

## Key Documents

| Document | Contents |
|---|---|
| [../CONTRACTS.md](../CONTRACTS.md) | Versioned signal, representation, intent, control, artifact, and experiment record schemas. |
| [RESEARCH_PROTOCOLS.md](../RESEARCH_PROTOCOLS.md) | Dataset cards, protocol governance, benchmark eligibility, and Paper 3 protection. |
| [../INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md) | BioSignal-FM, MyoAdapt, MyoControl, and MyoSim public-boundary adapters. |
| [BENCHMARK_GUIDE.md](../BENCHMARK_GUIDE.md) | Subject-level aggregation, statistical safeguards, reports, and reproducibility manifests. |
| [DEMONSTRATOR_GUIDE.md](../DEMONSTRATOR_GUIDE.md) | Synthetic replay-to-MyoSim execution and verification path. |
| [EEG_RESEARCH_TRACK.md](../EEG_RESEARCH_TRACK.md) | EEG foundation and EEG–EMG fusion preparation status. |
| [RESEARCH_OS_MVP.md](../RESEARCH_OS_MVP.md) | Local command-line operational workflow. |
| [../IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md) | Live project status, constraints, limitations, and next actions. |

## What Is Included

The deterministic seed catalog contains five project cards, six dataset cards, five protocols, three model cards, and three benchmark-family cards. The local registry then adds the synthetic end-to-end demonstration’s experiment/run/artifact references. The registry never stores raw biosignal data.

The current demonstrator converts synthetic MyoControl-shaped predictions into validated `IntentRecord` values, maps them explicitly to MyoSim’s V1 intent labels, then invokes MyoSim’s documented CSV replay/task path. The finalized fixture includes simulator-owned reports, metrics, transitions, GIF recordings, and an umbrella manifest that verifies the copied artifact hashes.

## What Is Not Included

No real NinaPro, BCI Competition IV-2a, WAY-EEG-GAL, MIT-BIH, or Paper 3 data/manifests were supplied. Consequently, this project does not include or claim real EMG/EEG/ECG benchmarks, cross-modal representation transfer, EEG–EMG fusion benefit, clinical safety, or commercial deployment. EEG and fusion components are intentionally protocol/adapter scaffolds pending authorized real-data work.

## Development

The project has no mandatory third-party runtime dependency. Optional runtimes remain localized: MyoSim is required only for live construction of its public `IntentEvent` or task execution; MNE is required only when an authorized researcher invokes the optional EEG edge adapter. The full umbrella suite is run with:

```bash
PYTHONPATH=src pytest -q
```

The package metadata declares the `hmi` CLI entry point. Use `PYTHONPATH=src python3 -m research_core.cli.main --help` from an uninstalled source tree, or install the package in a controlled environment to expose `hmi`.

## License

The umbrella layer is declared Apache-2.0. Each mature child repository retains its own license and operating conditions; consult its original repository before use.
