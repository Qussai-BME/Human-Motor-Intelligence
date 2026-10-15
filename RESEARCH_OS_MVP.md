# Research-OS MVP

## Purpose

The Research-OS MVP is a **local-first command-line workflow** for research metadata, artifact provenance, registry inspection, and controlled import. It deliberately avoids cloud hosting, user accounts, billing, telemetry, commercial infrastructure, and raw-data replication. The mature child repositories remain their own execution environments.

## Command Surface

The package declares an `hmi` command. During source-tree development, invoke the equivalent module command with `PYTHONPATH=src python3 -m research_core.cli.main`.

| Command | Purpose | Safety property |
|---|---|---|
| `hmi seed` | Initialize/update the deterministic catalog | Idempotent; catalog changes cannot silently replace stored records. |
| `hmi summary` | Display registry entity counts | Read-only. |
| `hmi integrity` | Recompute and validate every stored entry hash | Read-only; non-zero exit on a mismatch. |
| `hmi list <entity_type>` | List validated metadata/contract entries | Read-only. |
| `hmi show <entity_type> <entity_id>` | Display one validated record | Read-only. |
| `hmi runs [filters]` | Query protocol/dataset/model/status-matched runs | Read-only; preserves exact metadata filtering. |
| `hmi verify-manifest <path>` | Verify configuration/environment/artifact hashes | Read-only; non-zero exit on mismatch. |
| `hmi import-myoadapt ...` | Import an external MyoAdapt manifest by reference | Does not import MyoAdapt implementation or assert benchmark eligibility by default. |

## Typical Local Workflow

```bash
# Initialize the registry.
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local seed

# Inspect and validate it.
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local summary
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local integrity

# Verify a generated reproducibility bundle.
PYTHONPATH=src python3 -m research_core.cli.main verify-manifest \
  artifacts/integrated_demo/myosim/<RUN_ID>/umbrella_reproducibility_manifest.json

# Import a separately run MyoAdapt manifest only by reference.
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local import-myoadapt \
  external/myoadapt/manifest.json \
  --experiment-id imported-exp-001 --run-id imported-run-001 \
  --protocol-id emg-loso-v1 --dataset-id ninapro-db7 \
  --dataset-version operator-verified-release --subject-split leave-one-subject-out
```

The importer leaves `benchmark_eligible` false unless the caller explicitly supplies the flag. Supplying that flag is a governance action: it is appropriate only after a researcher has confirmed real-data status, dataset/version, protocol identity, split semantics, and provenance outside the CLI.

## Current Registry State

The finalized local registry contains the 22 deterministic catalog entries plus the synthetic end-to-end demonstration’s experiment/run and artifact references. The CLI integrity check verified all current entries. The demonstration remains synthetic and non-benchmark; it is visible for reproducibility traceability, not scientific aggregation.

## Non-Goals

| Out of scope | Rationale |
|---|---|
| Cloud database, SaaS, accounts, payments, or subscription controls | The specification requires thin local infrastructure and forbids unnecessary commercial/cloud work. |
| Raw biosignal storage | Dataset access, licensing, and privacy remain external/local to authorized researchers. |
| A universal training pipeline | Existing mature systems remain authoritative for their specialist workflows. |
| Paper 3 protocol editing | Paper 3 remains execution-locked and external. |
| Auto-publishing performance claims | The benchmark engine admits only registered real-data evidence and retains protocol constraints. |
| Clinical or live-hardware deployment | The implemented demonstrator is software-only replay infrastructure. |

## Test Evidence

The MVP command surface has focused tests for catalog seeding, summary, integrity verification, and reproducibility-manifest verification. The full umbrella suite currently contains 28 passing tests.
