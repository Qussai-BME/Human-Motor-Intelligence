# Real-Data Validation and Evidence Report — Human Motor Intelligence 1.2.0

## Executed real-data studies

| Study | Evidence status | Interpretation |
|---|---|---|
| P4 | Complete registered external validation | OpenBMI binary-MI LOSO evidence; scope remains cohort/protocol specific. |
| P5 | Complete registered amended external validation | Jeong2020 MI-only EEG/EMG comparison; no Holm-supported fusion gain under tested rules. |
| P6 C1 | Complete registered downstream-control study | PhysioNet EEGMMIDB R04 motor-imagery decoder → MyoSim; 60 primary + 60 rerun runs; fixture passed; 0/60 task success in every model; endpoint non-discriminative. |
| P6 audit of C1 | Post-hoc, reproducible | `p6/c1_audit`: oracle 0/20, 2 of 15 outputs inside the task window, 171/207 transitions after failure → C1 endpoint unreachable by design. |
| P6 C2 | Complete registered follow-up | EEGMMIDB R04/R08/R12, 105 subjects; episode-level replay; oracle 100/100; 27,000 emulated + 19,750 real-decoder + 25,600 sensitivity episodes; independently verified. |
| P6 R03 | Engineering baseline | PhysioNet EEGMMIDB R03 motor-execution decoder traces replayed to MyoSim; retained as systems/preflight evidence only. |

## P6 R03 facts

20 subjects × 3 model configurations produced 60 primary held-out traces and 60 primary MyoSim per-run task artefacts. All 60 tasks ended without `COMPLETE`; no invalid simulator state was detected. Paired Friedman tests were used for continuous downstream endpoints because the three model conditions are repeated within subject.

The R03 source run is motor execution. The T1/T2-to-OPEN/CLOSE mapping is explicitly abstract and cannot support a motor-imagery semantic claim. The supplied rerun matches the primary aggregate but does not include individual rerun MyoSim JSON task artefacts.

## Non-executed or external tracks

Direct BCI IV-2a replication, new Paper 3 umbrella rerun, ECG/ECoG studies, and other extensions remain outside the current evidence package. Results are not inferred from existing R03 data.
