# Research-Gate Preparation — V2 Recovery R3

## Gate Decision

The programme is **not authorized** to execute the P6 decoder-quality experiment yet. The hard stop occurred before a new protocol amendment, before simulation runs, and before a condition-comparison statistic. This preserves the validity of any future experiment.

## Required Trace Package

| Required item | Acceptance requirement | Reason |
|---|---|---|
| Three trace files | One immutable file per declared worst/mid/best condition, or three explicitly named quality levels agreed prospectively | Prevents condition invention |
| Manifest | CSV/JSON/Markdown manifest mapping filename to condition, model/version/checkpoint, subject/source, decoding task, and date frozen | Makes condition identity auditable |
| SHA-256 | Digest for every trace, recorded before computation | Detects silent file changes |
| Producer provenance | Model repository/commit or checkpoint hash, inference config, data split/source, decoding label semantics | Establishes scientific lineage |
| Serialization detail | Sampling interval, timestamps, columns, units, class/probability encoding, replay parser version | Enables input validation and replay fidelity checks |
| Permission/licensing | User authority to run and redistribute metadata | Enables legitimate evidence packaging |

## Pre-Execution Acceptance Gates

1. Confirm that all three checksums match the manifest and files parse deterministically.
2. Confirm each trace represents a distinct declared model-quality condition without using synthetic confidence editing or a generic fixture.
3. Confirm task/context compatibility with the existing MyoSim replay reader; otherwise create a separate trace-adaptation protocol without changing original evidence.
4. Register `V2_PROTOCOL_AMENDMENT_RECOVERY_R2_004.md` with condition order, 20 locked initial-state seeds, primary endpoint, missing-data rules, and planned exact/paired statistical test.
5. Create a fresh R3 results namespace. The old R2 fixture results must never be relabelled as one of the three conditions.
6. Conduct primary runs and an independent rerun only after gates 1–5 pass.

## P3 Gate

P3 is integrated as qualified external evidence; no umbrella rerun is claimed. A future P3 package should include its explicit research question, source data/repository rights, protocol, code, frozen results or reproducibility route, and a statement of how it relates to—rather than numerically combines with—P1/P2/P4/P5/P6.

## References

[1]: ../audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Hard Stop"
[2]: P6_DECODER_QUALITY_EXTENSION_STATUS_V2_RECOVERY_R3.md "P6 R3 Status"
[3]: CLAIM_EVIDENCE_MATRIX_V2_RECOVERY_R3.md "R3 Claim–Evidence Matrix"

The gating requirements operationalize the evidence boundary established by the R3 status records.[1] [2] [3]
