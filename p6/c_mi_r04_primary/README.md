# P6 — C: Motor-Imagery Primary Experiment

This is the active P6 scientific protocol. It replaces the current R03 motor-execution experiment as the primary P6 evidence while **retaining R03 as an engineering/preflight baseline**.

## Evidence roles

- `../exploratory_r03_primary/` — retained R03 motor-execution integration baseline; historical engineering evidence, not motor-imagery evidence.
- `./` — P6 primary C experiment using R04 motor-imagery data.

## Scientific question

> Do frozen cross-subject EEG decoder-quality differences translate into downstream simulated control utility under a fixed, valid control task?

## Run order

1. Acquire the official R04 EDF files externally.
2. Run the dataset/provenance preflight.
3. Run `run_p6_mi_r04.py` to generate the 60 held-out EEG traces and freeze the source-only quality ranking.
4. Run the model-independent control-fixture validation with the external MyoSim checkout.
5. Replay all 60 decoder traces through the fixed MyoSim configuration.
6. Repeat the full run to obtain a run-level auditable rerun.
7. Run `analyze_p6_mi_r04.py` to generate the paired subject-level statistics and final claim matrix.
8. Only after all gates pass should the manuscript be promoted from `READY_PENDING_EXTERNAL_DATA` to `SCIENTIFICALLY_COMPLETE`.

No scientific result is fabricated when the raw R04 files or MyoSim runtime are absent.
