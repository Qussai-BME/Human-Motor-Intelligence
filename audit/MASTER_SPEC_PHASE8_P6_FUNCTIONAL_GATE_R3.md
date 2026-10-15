# Master Specification Phase 8 — Functional Decoder-Quality Gate
## V2 Recovery R3 Current-State Hard Stop

## Decision

> **Phase 8 is BLOCKED before execution.** The programme has a deterministic MyoSim integration fixture and frozen R2 initial-state systems evidence, but it does not have authenticated decoder replay inputs for the required worst/mid-tier/best-performing conditions. Consequently it has no valid three-condition functional benchmark, no effect estimate, no task-success comparison across decoder quality, and no decoder-quality statistical test.

## Evidence Boundary

| Available item | Permitted interpretation | Prohibited interpretation |
|---|---|---|
| R2 initial-state primary/rerun records | Deterministic bounded-state systems stress-test outcomes under a packaged example intent replay | Evidence of a biomedical decoder, tiny-CNN/worst condition, or decoder-quality response |
| MyoSim patch and integration tests | Software integration and bounded reset capability | Human/prosthetic efficacy or functional superiority of an upstream model |
| `pick_place_replay.csv` metadata: `synthetic-demo` / `example-decoder-v1` | Integration fixture provenance | A trace mapped to worst, mid-tier, or best model quality |
| P6 R3 hard-stop/status documents | Research-governance correction and exact intake requirements | A negative or null decoder-quality result |

## Required Trace Acceptance Manifest

Each of the three conditions must arrive as an immutable file plus an authoritative manifest containing: condition label; SHA-256; source project/dataset/subject/session; model family, checkpoint and version; offline performance context; trace serialization/time semantics; intent-label mapping; controller-facing compatibility; and permission to use. The manifest must support an explicit condition mapping without inference from filenames, ordering, or developer recollection.

## Required Reopening Sequence

1. Verify file identities and manifest completeness without modifying the files.
2. Decide whether any previously run system fixture can be reused **only if** its SHA-256 and provenance map exactly to one authenticated condition. Otherwise start all conditions in a new namespace.
3. Register a prospective amendment defining condition order, fixed 20-state protocol, endpoints, exclusions, missing/invalid rules, and statistical plan.
4. Execute deterministic runs and independent rerun only after acceptance.
5. Report task metrics and statistics with the decoder trace provenance at the same evidence tier as the outcomes.

## Forbidden Shortcuts

No synthetic confidence editing, guessed trace naming, fixture relabelling, model-score inference, condition imputation, Cochran Q/Fisher/other comparison, or publication statement about decoder quality may occur before the above acceptance sequence is complete.

## References

[1]: V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Replay Identity Hard Stop"
[2]: ../papers/P6_DECODER_QUALITY_EXTENSION_STATUS_V2_RECOVERY_R3.md "P6 Decoder-Quality Extension Status"
[3]: ../papers/RESEARCH_GATE_PREPARATION_RECOVERY_R3.md "P6 Research-Gate Preparation"
[4]: ../patches/README_MYOSIM_INITIAL_STATE_RECOVERY_R2.md "MyoSim Initial-State Recovery R2 Patch Guide"

This functional gate follows the replay-identity, P6 status, research-gate, and MyoSim patch records.[1] [2] [3] [4]
