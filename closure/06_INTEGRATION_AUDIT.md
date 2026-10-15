# Integration Audit — P6 R3 Reconciled

## Verified from retained artifacts
`EEGMMIDB R03 motor-execution recording → held-out decoder → provenance-linked trace → abstract OPEN/CLOSE intent mapping → MyoSim offline replay → task metrics`.

## Limitations
- This is motor execution, not motor imagery.
- The class-to-command mapping is an abstract software integration mapping, not a validated semantic mapping.
- No task reached `COMPLETE`.
- Per-run rerun artifacts are absent; only aggregate equality is visible.
- The command-release metric was reconciled from transition records.

The verified path is an offline simulator integration record, not closed-loop real-time control, hardware validation, or clinical evidence.
