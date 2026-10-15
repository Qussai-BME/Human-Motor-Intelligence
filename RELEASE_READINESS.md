# Release Readiness — 1.2.0

| Gate | Status |
|---|---|
| P6 C1 R04 decoder execution, strict LOSO, frozen quality mapping | PASS |
| Model-independent MyoSim fixture (C1) | PASS (1/1) |
| C1 primary and rerun run-level artifacts (60 + 60) | PASS |
| C1 post-hoc audit (re-execution, oracle, timeline, sensitivity) | PASS (reproducible from `p6/c1_audit`) |
| C2 protocol frozen before outcomes (hash manifest) | PASS |
| C2 pre-flight validity checks | PASS (oracle 100/100; X0 0/100; truth table 16/16) |
| C2 episodes (emulator 27,000; sensitivity 25,600; R0 560; R1 19,750) with raw archives and SHA-256 | PASS |
| Independent verification of C2 (300 re-run episodes; recomputed statistics) | PASS (0 mismatches) |
| Automated tests | PASS (44 passed, 2 optional MyoSim tests skipped without MyoSim) |
| Raw EEG excluded | PASS |
| R03 role | Engineering/preflight baseline only |

Scientific disposition: C1 is a complete, honest null whose endpoint was unreachable by design; C2 shows that control success follows confidence-gate passage rather than accuracy. No clinical, prosthetic or online-BCI claim is made.
