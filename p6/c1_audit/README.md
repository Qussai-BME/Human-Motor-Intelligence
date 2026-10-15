# C1 post-hoc audit

Post-hoc, descriptive diagnostics defined after the C1 outcome (0/60) was known. They never alter archived C1 results.

| Item | Script | Output |
|---|---|---|
| D1 re-execution, D2 oracle, D3 event timeline (instrumented runner, 80 runs) | `scripts/rerun_diag.py` | `outputs/diag_runs.json` |
| S1 timeout removed (80 runs) | `scripts/rerun_notimeout.py` | `outputs/diag_runs_notimeout.json` |
| Statistics reported in the manuscript | `scripts/stats_all.py` | `outputs/numbers.json` (and temporary `.pkl` files) |
| Figures | `scripts/fig_a2.py`, `fig_a3.py`, `fig_b.py`, `fig_c.py`, `fig_d.py` | `outputs/figs/` |

Requirements: MyoSim v0.1.5 at commit `67ee74e3230b068b5db760efa15da3669e315eb3` (`MYOSIM_DIR=/path/to/myosim_repo`), MuJoCo ≥ 3.3, numpy, scipy, pandas, matplotlib, pyyaml. Re-running reproduces the recorded outputs (checked at release).

Key findings: oracle 0/20; 2 of 15 outputs inside the 8.0-s task window; 171/207 controller transitions after failure; all 64 command corrections after failure; no run completes even without timeout (an executing command can end only via REST).
