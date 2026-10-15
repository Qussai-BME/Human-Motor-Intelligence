# V2 Recovery R3 P6 Replay-Identity Audit and Hard Stop

**Date:** 2026-08-23 (GMT+3)  
**Requested extension:** Two additional decoder-quality conditions (`mid-tier` and `best-performing`) across the fixed 20-state R2 protocol.  
**Decision:** **Hard stop before R2_004 registration, before any R3 run, and before any decoder-quality comparison.**

## Audit Question

The requested R3 extension presupposes three traceable decoder conditions: a previously used worst/tiny-CNN trace, a mid-tier trace, and a best-performing trace. The audit asked whether the retained P6 R2 replay can be identified as one of those traces and whether the other two replay artefacts are locally available with sufficient provenance to reproduce the same task/control protocol.

## Findings

The exact R2 input was:

```text
<LOCAL_WORKSPACE>/dependencies/myosim_v1_1/examples/intents/pick_place_replay.csv
SHA-256: a94e59e30e2599eb92517198739dff96aa40b01f3bf6777756722e09960e09f3
```

Its CSV metadata identifies every event as:

| CSV field | Recorded value |
|---|---|
| `source_subject` | `synthetic-demo` |
| `modality` | `emg-replay` |
| `model_version` | `example-decoder-v1` |
| Label/confidence pattern | Fixed demonstration sequence: `REST` 0.99 and repeated `PINCH` 0.95 |

The source file contains **no** decoder family ID, training artifact hash, held-out subject identity, cross-subject score, quality tier, tiny-CNN identifier, or linkage to the frozen P6 decoder conditions. The repository’s own integration-replay generator likewise labels its deterministic stream as `synthetic`, `benchmark_eligible=false`, and “not a real decoder output.”

A read-only inventory of the user-provided Human Motor Intelligence delivery archive, Recovery R1/R2 archives, MyoSim package, MyoAdapt package, and myocontrol package found no pair of usable, provenance-linked `mid-tier` and `best-performing` decoder replay CSV/JSON traces. No locally available file permits a defensible mapping from `example-decoder-v1` to `tiny_cnn`, worst, mid-tier, or best-performing performance conditions.

## Consequence for R2 and R3

The R2 initial-state experiment remains a reproducible **simulation integration-fixture stress test** with declared physical states. Its run records and all-failure result are retained as historical R2 artefacts. However, its replay identity cannot support the prior label “real decoder replay” or the new requested assertion that it is the frozen tiny-CNN/worst condition. That identity claim is **not established** by the preserved R2 input.

> No R2 artefact is deleted or overwritten. This R3 correction record supersedes only the unsupported replay-identity interpretation in programme-level integration. It does not convert R2 into biomedical evidence, a decoder-quality experiment, or a synthetic corruption sweep.

Because the necessary condition identity is absent, the following R3 actions are prohibited:

| Prohibited action | Reason |
|---|---|
| Registering R2_004 with guessed decoder labels | Would fabricate trace provenance. |
| Treating `example-decoder-v1` as tiny-CNN/worst | No evidence supports this mapping. |
| Constructing new “mid” or “best” traces by modifying confidence/labels | Would create synthetic conditions, not the requested real decoder outputs. |
| Testing Cochran’s Q/Fisher across guessed conditions | Condition labels and decoder-quality ordering would be invalid. |
| Updating P6 to claim decoder-quality robustness | The required decoder-quality factor is absent. |

## Required User-Supplied Inputs to Reopen R3

Provide the three frozen replay inputs or, at minimum, the two missing inputs plus an authoritative manifest mapping the existing one. Every trace must include or be accompanied by the following fields:

1. Immutable file path/name and SHA-256.
2. Decoder condition ID and ordering (`worst`, `mid-tier`, `best-performing`).
3. Model family/version and the originating frozen P6 result artefact.
4. Subject/session or source-stream identity and a statement of whether it is real recorded-decoder output or a declared synthetic control.
5. Exact CSV schema compatible with MyoSim, including timestamps, labels, confidences, and any required label map.
6. Confirmation that task, controller, and timing compatibility match the fixed R2 P6 protocol.

After these items are available, R2_004 can be registered prospectively, the two missing conditions can be evaluated across the unchanged 20-state seed set, and a valid three-condition success-proportion analysis can be performed. Until then, the requested final authoritative package is blocked because P6 R3 cannot be truthfully completed.
