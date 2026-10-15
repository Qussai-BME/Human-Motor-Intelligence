# P6 C1 External Execution Runbook

## Preconditions

- Python 3.10+ with the project dependencies installed.
- Network access to the official PhysioNet EEGMMIDB v1.0.0 source, or a local lawful copy of the 20 R04 EDF files.
- A compatible MyoSim checkout with its declared MuJoCo dependency installed.
- Do not place raw EDF files inside the public repository tree before release packaging.

## 1. Acquire R04

```bash
python p6/c_mi_r04_primary/scripts/acquire_r04.py --output-root /path/to/eegmmidb
```

Or provide an equivalent local dataset root containing `S001/S001R04.edf` … `S020/S020R04.edf`.

## 2. Run the complete C1 pipeline

```bash
python p6/c_mi_r04_primary/scripts/run_all_p6_c1.py \
  --data-root /path/to/eegmmidb \
  --myosim-root /path/to/MyoSim
```

The orchestrator executes decoder generation, ground-truth replay creation, the model-independent fixture gate, 60 primary decoder-conditioned MyoSim runs, a full 60-run decoder rerun, and the paired subject-level analysis in the registered order.

## 3. Required evidence before declaring C1 complete

- `audit/DATASET_MANIFEST.json` covers S001–S020 and records SHA-256 for every R04 source file.
- `results/QUALITY_MAPPING.json` exists and is frozen before task analysis.
- 60 primary trace CSVs exist.
- 60 primary MyoSim per-run JSON records exist.
- The model-independent fixture completes the declared task.
- 60 rerun trace CSVs and 60 rerun MyoSim per-run JSON records exist.
- `results/FINAL_STATISTICS.json` and the claim/evidence matrix are populated from those artifacts.
- Release doctor and the full test suite pass after results are written.

## Scientific stop conditions

Do not claim decoder-quality → control-utility translation if the control fixture cannot complete or if the primary success endpoint is non-discriminative. Report such a result as exploratory and preserve all failed runs.
