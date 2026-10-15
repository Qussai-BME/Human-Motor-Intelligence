# P6 — Decoder Quality versus Control Utility

P6 has four evidence layers.

| Directory | Layer | Role |
|---|---|---|
| `exploratory_r03_primary/`, `exploratory_r03_rerun/` | R03 engineering baseline | Motor-execution preflight; provenance and failure analysis only |
| `c_mi_r04_primary/`, `c_mi_r04_rerun/` | **C1** registered replay | R04 motor imagery, M1–M3, 60 + 60 MyoSim runs; success 0/60 (archived, unchanged) |
| `c1_audit/` | Post-hoc audit of C1 | Re-execution, oracle, timeline, timeout-removed sensitivity; shows the C1 endpoint was unreachable by design |
| `c2_episode/` | **C2** registered follow-up | Episode-level interface, emulated ladder, real decoders (105 subjects), sensitivity, raw archives, verification |

The scientific completion record is `../P6_FINAL_STATUS.md`; the manuscript text is not distributed in this archive. The C1 completion gate is defined in `../closure/P6_C1_EXECUTION_GATE.md`.
