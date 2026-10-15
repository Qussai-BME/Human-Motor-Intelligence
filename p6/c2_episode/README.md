# P6 C2 — Episode-level replay study

Protocol `P6-C2-EPISODE-v1.0` (frozen 2026-10-07 23:46 UTC, before any emulated or real-decoder outcome). Executed by an autonomous software agent under the frozen protocol; verified independently (see `verification/`).

## Layout

| Path | Content |
|---|---|
| `PROTOCOL_C2.md`, `c2_design.yaml`, `config/p6_c2_mysim.yaml` | Frozen protocol, design, controller configuration (numerically identical to C1) |
| `registry/` | `FREEZE_MANIFEST.json` (hashes), `ENVIRONMENT.json`, `CONFIG_DIFF.txt`, subject exclusions, EEGMMIDB source-file hashes (relative paths), output manifest (`OUTPUT_MANIFEST.json.gz`, 146,006 files), `frozen/` = byte-identical frozen originals (`*.py.frozen`) |
| `scripts/` | Agent execution scripts and portable reference code (`c2_runner.py` etc.; only path constants differ from the frozen copies) |
| `results/` | Episode tables (`emulator_episodes.csv`, `real_episodes.csv`, `sensitivity_episodes.csv`), `ANALYSIS.json`, `PREFLIGHT.json`, WP5 status and quality records |
| `raw_archives/` | Compressed replay CSVs, per-episode run JSONs, event logs (146k files) and the derived WP5 decoder caches (`.npz` features/predictions, kept out of the browsable tree by repository policy) with `SHA256SUMS.txt` |
| `figures/` | Agent-generated figures F1–F8 |
| `posthoc/` | Post-hoc analyses added after outcomes (chance-matched floor, gate sweep, recomputed statistics, manuscript figures) with `outputs/` |
| `verification/` | Independent re-execution of sampled episodes; lookup validation; sizing pilot |
| `REPORT_C2_agent_original.md` | The agent’s original report (see `../../papers/paper_6/RESULTS_SUMMARY.md` and the manuscript for corrected interpretation) |

## Arms
X0 regression control (100); E emulated ladder (54 cells × 500 = 27,000); S controller sensitivity (25,600); R0 C1 decoders + oracle (560); R1 real decoders D1–D5, 105 subjects (19,750).

## Reproduce

```bash
export MYOSIM_DIR=/path/to/myosim_repo          # MyoSim v0.1.5, commit 67ee74e3230b068b5db760efa15da3669e315eb3
export EEGMMIDB_DIR=/path/to/EEGMMIDB           # only for re-running WP5 from raw EDF (runs R04, R08, R12)
python p6/c2_episode/scripts/run_preflight.py   # WP0–WP1 + freeze (writes into $C2_OUT, default this directory)
python p6/c2_episode/scripts/run_main_arms.py   # WP2–WP4, WP7
python p6/c2_episode/scripts/run_wp5.py         # WP5 (to reuse the archived decoder caches, first extract raw_archives/P6_C2_wp5_decoder_caches.tar.gz into results/)
python p6/c2_episode/scripts/analyze_c2.py      # ANALYSIS.json (reproduces the recorded file)
```
Set `C2_OUT` to a scratch directory to avoid overwriting the archived record. Quick integrity check: `pytest tests/test_p6_c2_episode.py`.

## Headline results
Oracle 100/100 (C1-format oracle 0/100). Emulator: logit slope 14.8 per unit accuracy; over-confident chance-level decoder 23.0% success; calibration crossover near q = 0.8. Real zero-calibration decoders (balanced accuracy 0.53–0.60): success followed gate passage (ρ = 0.95), not accuracy (ρ = 0.24); at most +0.4 percentage points above a chance-matched floor at the registered gate.

## Caveats
Scheduled REST and sample-and-hold interface; deterministic physics; parametric emulator; one dataset; no real decoder above balanced accuracy 0.61; D5 evaluated on run R12 only. See `../../SCIENTIFIC_LIMITATIONS.md`.
