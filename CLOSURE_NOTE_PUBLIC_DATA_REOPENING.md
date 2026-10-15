> **Current P6 state (2026-10-06): P6 C1 (PhysioNet EEGMMIDB R04 motor imagery, S001–S020, strict LOSO) was executed under the frozen protocol. The MyoSim control fixture passed 1/1; decoder-conditioned task success was 0/60 for every model in both the primary run and the rerun, so the primary task-success endpoint is non-discriminative. R03 is retained as an engineering baseline only. See `P6_FINAL_STATUS.md`.**

# Closure Note — P6 Public-Data Reopening

This note is superseded by the canonical P6 R03 exploratory report. Earlier reopening/fixture records are retained under `historical/` for provenance and must not be interpreted as a separate current experiment.

The current public evidence is the executed PhysioNet EEGMMIDB **R03 motor-execution** study under `p6/exploratory_r03_primary/` and its aggregate-only rerun under `p6/exploratory_r03_rerun/`. The current record contains 60 primary traces, 60 primary per-run MyoSim task artefacts, 0/60 `COMPLETE` tasks, and paired secondary-endpoint statistics.

The original motor-imagery decoder-quality-to-task-utility question remains unresolved. A future confirmatory answer would require a new motor-imagery execution under a new frozen experiment namespace; this archive does not relabel R03 to meet that requirement.
