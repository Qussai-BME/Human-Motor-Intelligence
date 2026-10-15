# Reproducibility Matrix — V2 Recovery R2

| Study | Identity and input | Primary command | Required primary outputs | Independent rerun criterion | Boundary |
|---|---|---|---|---|---|
| P4 R1 | NEMAR OpenBMI derived cache; 54 subjects; external binary MI | `PYTHONPATH=src python3 scripts/run_v2_external_validation.py run-p4` | `subject_level_results.csv`, validation/protocol/manifest/environment, statistics, figure | Byte-identical subject-level CSV | External validation, not direct replication |
| P5 R2 extraction | NEMAR Jeong cache; amended 24-subject cohort; sequential raw cleanup | `PYTHONPATH=src python3 scripts/run_v2_p5_jeong_r2.py extract-p5-r2` | 24 `.npz`, 24 provenance files, raw cleanup pass | Manifest checksum validation | No raw BDF in repository |
| P5 R2 evaluation | P5 derived cache and locked JSON config | `PYTHONPATH=src python3 scripts/run_v2_p5_jeong_r2.py run-p5-r2` | 96-row subject result, D2–D5 validation, protocol/manifest/environment | `rerun-p5-r2`; CSV SHA-256 `a35b1cb5daa2cdae2078e7668eb1b028e4613c99e062df2b941183c7b971e36b` | External validation; amended 24-subject cohort |
| P5 R2 statistics | P5 primary result directory | `PYTHONPATH=src python3 scripts/analyze_p5_r2_subject_level_statistics.py <result_dir>` | `statistics_macro_f1.json` | Same CSV required before analysis | Subject is inference unit |
| P6 baseline | MyoSim replay + inert R2 baseline config | `PYTHONPATH=<LOCAL_WORKSPACE>/dependencies/myosim_v1_1/src python3 -m myosim.cli.main benchmark --config configs/experiments/p6_baseline_recovery_r2.yaml --file <LOCAL_WORKSPACE>/dependencies/myosim_v1_1/examples/intents/pick_place_replay.csv` | New baseline run; fixed benchmark endpoints | Exact metrics against preserved benchmark | Compatibility control, not cohort |
| P6 R2 cohort | MyoSim source extension, fixed replay, seeds 20260901–20260920 | `PYTHONPATH=<LOCAL_WORKSPACE>/dependencies/myosim_v1_1/src python3 scripts/run_p6_initial_state_repeats_r2.py --mode primary --seeds $(seq 20260901 20260920) --output results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2` | 20 per-run JSONs, records, protocol, environment, code fingerprint | Same command with `--mode independent-rerun`; exact `run_records.json` | Simulation systems evidence; real replay but not biomedical benchmark |
| P6 R2 statistics | P6 primary cohort records | `PYTHONPATH=<LOCAL_WORKSPACE>/dependencies/myosim_v1_1/src python3 scripts/analyze_p6_initial_state_repeats_r2.py results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2` | `statistics_initial_state_repeats.json` | Cohort must have 20 expected seeds and 20 distinct qpos states | No decoder-quality inference |

## Environment and Source Fingerprints

P5 stores its environment, protocol, manifest, validation, and cache provenance in its result directory. P6 stores `environment.json`, `code_fingerprint.json`, `protocol.json`, per-run configuration/result records, and replay SHA-256 in the primary and independent rerun directories. The P6 extension is tested by the MyoSim integration tests including inert default compatibility and distinct-state checks.

## Interpretation of Reproducibility

Exact reruns test artefact determinism and provenance completeness. They are not additional subjects, new simulated state draws, or independent biological replicates. Reproducibility does not broaden the scope of a claim beyond its protocol-defined cohort.
