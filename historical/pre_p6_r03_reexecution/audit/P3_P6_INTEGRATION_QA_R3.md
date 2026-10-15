> **HISTORICAL / SUPERSEDED RECORD:** This document records an earlier pre-reopening state. It is retained for provenance only. Current P6 disposition is documented in `P6_FINAL_STATUS.md` and `closure/10_FINAL_CLOSURE_REPORT.md`.

# P3/P6 Integration and Release QA — R3

**Responsible author:** Qussai Adlbi

## Results

- P3 external archive accepted: PASS
- P3 fold inventory: DB2 = 360, DB3 = 99, DB7 = 198; total = 657: PASS
- P3 planned experiment coverage: 27 condition/cohort summaries: PASS
- P3 raw-recording/cache exclusion: PASS
- P3 headline summary values cross-checked against the supplied manuscript: PASS
- P3 Word manuscript opens and carries controlled author metadata: PASS
- P6 Markdown updated with explicit P3 upstream evidence boundary: PASS
- P6 Word export opens and carries controlled author metadata: PASS
- P6 R3 hard stop remains visible: PASS
- Core umbrella test suite: 28 passed, 1 environment-dependent failure.

The single failing test is `test_myosim_runtime_bridge_constructs_public_intent_event`; it requires the separately maintained `myosim` package, which is intentionally not vendored in this release. The failure is an environment dependency report, not a P3/P6 content or provenance failure.

## Scientific boundary

P3 is accepted as externally archived EMG evidence and is not represented as an independently rerun umbrella benchmark. P3 does not supply three immutable MyoSim intent traces mapped to worst/mid/best decoder conditions. Therefore P6 R3 remains blocked before decoder-quality execution.

## Provenance

The upstream P3 repository's provenance notes and disclosure metadata are retained. The release does not remove or falsify upstream authorship, data provenance, or tool-use disclosure. Programme-controlled metadata uses **Qussai Adlbi**.
