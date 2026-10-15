> **Current P6 state (2026-10-11: C1 + audit + C2 complete; see `P6_FINAL_STATUS.md`). Earlier note (2026-10-06): P6 C1 (PhysioNet EEGMMIDB R04 motor imagery, S001–S020, strict LOSO) was executed under the frozen protocol. The MyoSim control fixture passed 1/1; decoder-conditioned task success was 0/60 for every model in both the primary run and the rerun, so the primary task-success endpoint is non-discriminative. R03 is retained as an engineering baseline only. See `P6_FINAL_STATUS.md`.**

# Master End-to-End Implementation Status — Human Motor Intelligence 1.2.0

> This is the current release status. Earlier R3 hard-stop and interim-state documents have been moved under `historical/pre_p6_r03_reexecution/` and remain provenance records only.

| Surface | Status | Current evidence |
|---|---|---|
| Versioned contracts | COMPLETE | `src/research_core/contracts/` + tests |
| Registry/provenance | COMPLETE | `registry/local/` + integrity workflows |
| Benchmark/report infrastructure | COMPLETE | `src/research_core/benchmarks/`, protocols, result records |
| P4/P5 evidence | RELEASED WITH PAPER-SPECIFIC LIMITS | Frozen source/protocol/result/rerun records |
| P6 R2 systems stream | RELEASED WITH SYSTEMS LIMITS | MyoSim fixture and initial-state evidence |
| P6 R03 decoder/control stream | RELEASED AS ENGINEERING BASELINE | 60 traces + 60 primary MyoSim run artifacts + paired statistics |
| P6 C1 motor-imagery study | COMPLETE | R04 LOSO, frozen quality gate, fixture gate, primary/replay/rerun artifacts; success 0/60 (endpoint non-discriminative; unreachable by design per audit). |
| P6 C1 audit and C2 follow-up | COMPLETE | `p6/c1_audit`, `p6/c2_episode`; protocol frozen before outcomes; independently verified. |
| P3 | QUALIFIED EXTERNAL EVIDENCE | External archive preserved; umbrella does not claim independent rerun |
| Public packaging | COMPLETE | Canonical release manifest + release-readiness gate |
| Optional MyoSim integration | EXTERNAL DEPENDENCY | Core tests remain runnable without it |

## P6 current evidence boundary

P6 is complete as three stages: C1 (registered R04 motor-imagery replay, 60 + 60 runs, task success 0/60), a post-hoc audit of C1 (endpoint unreachable by design) and the C2 registered episode-level follow-up (27,000 emulated, 19,750 real-decoder and 25,600 sensitivity episodes). See `P6_FINAL_STATUS.md`, `papers/paper_6/RESULTS_SUMMARY.md` and `p6/c2_episode/README.md`.

The retained R03 experiment (PhysioNet EEGMMIDB run R03, motor execution, 60 traces and 60 primary MyoSim artefacts) is engineering baseline evidence only; its T1/T2 events are mapped to generic commands through an explicit abstract mapping and it is not motor-imagery evidence.
