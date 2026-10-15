# P6 Decoder-Quality × Initial-State Extension Status — V2 Recovery R3

**Status:** **Not executed; hard stop remains active.**  
**Reason:** The required decoder-condition replay traces and their authoritative provenance are unavailable in the current evidence workspace.  
**Governing audit:** `audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md`.

## What R2 Actually Established

R2 established that the MyoSim simulator can produce a declared, seed-linked distribution of 20 distinct initial forearm states while preserving a fixed replay, controller, task geometry, and success rule. The R2 run records are reproducible and retain their all-failure result for the specified simulation integration fixture.

However, the replay file used by R2 identifies itself as `synthetic-demo` / `example-decoder-v1`. It contains no authenticated relationship to the frozen tiny-CNN/worst condition, no decoder score tier, no model artifact hash, and no subject/session provenance. Therefore, it must not be represented in R3 documents as a confirmed real decoder trace or as the worst/tiny-CNN condition.

| Requested R3 condition | Trace identity available? | Execution status |
|---|---|---|
| Claimed R2 worst/tiny-CNN condition | No; R2 input is only `example-decoder-v1` | Not eligible for decoder-quality labelling |
| Mid-tier decoder trace | No | Not executed |
| Best-performing decoder trace | No | Not executed |
| Three-condition decoder-quality comparison | No eligible condition set | Not executed |

## Permitted and Prohibited Wording

> **Permitted:** “R2 evaluated a fixed MyoSim example replay under a declared simulated initial-state distribution and found 0/20 task completions.”

> **Prohibited:** “R2 evaluated the worst/tiny-CNN decoder,” “R3 tested three decoder qualities,” or “decoder quality did or did not determine robustness.”

No confidence modification, label substitution, model-name assignment, or synthetic trace construction may be used to stand in for the missing frozen replay outputs.

## Reopening Requirement

R3 can be opened only after receipt of three immutable decoder traces or a verified manifest that maps the R2 trace and the two additional traces to worst/mid/best conditions. Each required trace must provide its checksum, model family/version, condition ordering, source stream identity, real-versus-synthetic origin, and MyoSim-compatible schema. Once available, R2_004 will be registered prospectively and the unchanged 20-state protocol will be applied to each newly identified trace.
