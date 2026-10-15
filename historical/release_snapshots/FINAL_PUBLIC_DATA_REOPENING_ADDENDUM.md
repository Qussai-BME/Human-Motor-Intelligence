# Final Public-Data Reopening Addendum

**Responsible author:** Qussai Adlbi

## Disposition

P6 R3 now has a separate, executed public-data reopening based on 20 real PhysioNet EEGMMIDB subjects and 900 held-out decoder events. It produced 60 raw traces, 60 quality-stratum aliases, paired subject-level statistics, and three successful MyoSim/MuJoCo replay-contract runs.

The historical P6 R3 namespace is not overwritten. Its original missing-authentic-trace hard stop remains retained for provenance. The new evidence supports authenticated offline decoder-to-replay integration, not clinical performance, universal cross-subject decoding, or a monotonic quality-to-task-success law.

## Final values

- `quality_worst`: mean held-out balanced accuracy 0.4540
- `quality_middle`: mean held-out balanced accuracy 0.4379
- `quality_best`: mean held-out balanced accuracy 0.4969
- 20 held-out subjects per stratum; 15 trials per subject
- 900 total trace events; no synthetic trace rows
- MyoSim replay: 15 events per S001 trace, no invalid state, zero released commands under the fixed temporal gate

## Reproduction entry points

1. `p6_public_reopening/scripts/run_public_p6.py` — CPU-first LOSO decoder run.
2. `p6_public_reopening/results/QUALITY_MAPPING.json` — prospective source-only quality mapping.
3. `p6_public_reopening/results/PAIRED_STATISTICS.json` — paired tests and bootstrap intervals.
4. `p6_public_reopening/results/MYOSIM_REPLAY_VALIDATION.json` — replay provenance and outcomes.
