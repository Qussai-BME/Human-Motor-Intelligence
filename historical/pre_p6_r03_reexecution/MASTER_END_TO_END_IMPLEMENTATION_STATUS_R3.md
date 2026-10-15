# Master End-to-End Implementation Status
## Human Motor Intelligence — V2 Recovery R3 Current State

> **Status convention:** `COMPLETE` denotes a verified repository capability or retained evidence stream. `BLOCKED` denotes a required external evidence input that is absent and will not be substituted. `DEFERRED` denotes an explicitly out-of-scope future product/research phase.

## Current System Surface

| System component | Status | Current implementation |
|---|---|---|
| Versioned contracts | COMPLETE | Metadata-only signal/provenance, representation, intent, control, artifact, and experiment contracts with validation and compatibility support |
| Local research registry | COMPLETE | Dataset, protocol, model, project, benchmark, report, experiment/run, and artifact identities in a hash-guarded local JSON registry plus append-only event log |
| Protocol governance | COMPLETE | Split, preprocessing, leakage, metric, inference-unit, seed, selection-policy, status, and limitation metadata preserved in typed definitions |
| Benchmark/report engine | COMPLETE | Subject-level aggregation, comparability safeguards, conservative optional omnibus test, machine-readable summaries, tables, SVG asset, and factual report assets |
| P4/P5 real-data streams | COMPLETE within registered protocols | Frozen external-validation code, manifests, D1–D5 gates, outputs, statistics, figures, independent reruns, and Q1 deliverables |
| P6 R2 systems stream | COMPLETE within systems scope | MyoSim patch/test, bounded state variation, records, rerun, and systems-evidence reporting |
| P6 R3 decoder-quality stream | BLOCKED | No authenticated condition traces; no amendment/execution/statistic exists |
| P3 stream | BLOCKED | Original author package has not been supplied |
| Research-OS CLI navigation | COMPLETE | `doctor`, typed `dataset/protocol/experiment/benchmark/artifact/report` read-only navigation, integrity, run query, manifest verification, and controlled external-manifest import |
| Product/discovery layer | DEFERRED | No billing, telemetry, cloud, multi-tenancy, subscription, or traction claim |

## Stable CLI Workflows

```bash
# Local preflight: registry integrity, publication/document status, data-governance scan, P3/P6 gates.
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local doctor

# Read-only registry navigation.
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local dataset list
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local protocol list
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local protocol validate <protocol-id>
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local experiment list
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local artifact list
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local report list

# Integrity and provenance checks.
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local integrity
PYTHONPATH=src python3 -m research_core.cli.main verify-manifest <path/to/manifest.json>
```

The CLI intentionally does **not** expose a generic `experiment run`, `experiment reproduce`, `benchmark run`, `demo control`, or cloud command. Such operations would be unsafe or misleading without a registered source-specific protocol, external runtime/data availability, and complete provenance. The existing P4/P5 and P6 runners remain versioned research scripts tied to their explicit protocol namespaces rather than being disguised as generic CLI actions.

## Definition-of-Done Reconciliation

The end-to-end platform definition is met for contracts, local registry, protocol governance, benchmark/report infrastructure, reproducibility records, controlled simulation integration, real EEG evidence, public-review documentation, and limitation controls. The broader programme definition remains open only where external inputs are genuinely absent: P3 evidence and P6 authentic decoder traces. These are not engineering omissions and must remain visible.

## References

[1]: audit/MASTER_END_TO_END_SPEC_COMPLIANCE_AUDIT_R3.md "Master End-to-End Specification Compliance Audit"
[2]: PUBLIC_REVIEW_DISCLOSURE_R3.md "Public Review Disclosure"
[3]: audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Replay Identity Hard Stop"
[4]: papers/RESEARCH_GATE_PREPARATION_RECOVERY_R3.md "P6 R3 Research-Gate Preparation"

The implementation status follows the master-spec audit, public disclosure, hard-stop, and research-gate records.[1] [2] [3] [4]
