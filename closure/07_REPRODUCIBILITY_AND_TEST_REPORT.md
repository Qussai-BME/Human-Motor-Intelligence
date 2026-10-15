# Reproducibility and Test Report — C1 (updated 2026-10-06)

## P6 C1
- Active protocol: `p6/c_mi_r04_primary/`
- R04 acquisition code: present; raw EDF files intentionally not redistributed.
- Decoder trace generation: executed; 60 primary and 60 rerun decoder-conditioned runs.
- MyoSim fixture gate: executed; passed 1/1.
- Required full rerun: executed; run-level artifacts present (60/60). Task success 0/60 in both primary and rerun.

## Retained R03
- Primary trace CSVs: 60.
- Primary MyoSim per-run JSON files: 60.
- Original aggregate preserved: PASS.
- Reconciled aggregate: PASS.
- Rerun aggregate record count: 60.
- Independent rerun per-run audit: NOT VERIFIED; individual rerun MyoSim JSON artifacts are missing.

## Fresh umbrella test run
Command: `PYTHONPATH=src pytest -q`  
Result: **31 passed, 1 skipped**. The skipped test requires the separately maintained `myosim` runtime, which is not installed in the current environment.

## Scope
P6 C1 is complete under its registered protocol with a non-discriminative primary endpoint (see `P6_FINAL_STATUS.md`). R03 remains an engineering baseline.
