# Reproducibility Matrix — V2 Recovery R1

| Component | Inputs | Command / verification | Expected output | Status |
|---|---|---|---|---|
| Baseline recovery | User-delivered archive | Archive SHA-256 in `audit/V2_SANDBOX_RESET_RECOVERY.md` | Restored baseline worktree | Documented recovery event |
| P1/P2 source text | Two user DOCX files | `PYTHONPATH=src python3 scripts/extract_docx_text.py <input.docx> <output.txt>` | manuscript source text (not distributed), `P2_source_extracted.txt` | Re-extracted |
| P5 event audit | Official NEMAR TSV sidecars only | `python3 scripts/audit_jeong_event_inventory.py` | `audit/jeong_ses0_event_inventory.json` | Complete; source gate fails |
| P4 cache extraction | NEMAR OpenBMI v1.0.5, external BDF/TSV | `PYTHONPATH=src python3 scripts/run_v2_external_validation.py extract-p4` | 54 NPZ caches + 54 provenance JSON outside repository; temporary raw cleanup | Complete |
| P4 D1 manifest | P4 derived cache | `PYTHONPATH=src python3 scripts/run_v2_external_validation.py manifest-p4` | `datasets/manifests/nemar_nm000338_openbmi_v2_recovery_r1.json` | Pass |
| P4 primary LOSO | D1 cache and lock | `PYTHONPATH=src python3 scripts/run_v2_external_validation.py run-p4` | Immutable primary directory with protocol, validation, manifest, environment, CSV, results | Complete |
| P4 statistics | Primary CSV | `PYTHONPATH=src python3 scripts/analyze_subject_level_statistics.py <primary-result-dir>` | `statistics_macro_f1.json` | Complete |
| P4 figure | Primary CSV/statistics | `PYTHONPATH=src python3 scripts/plot_p4_external_validation.py` | `p4_openbmi_subject_level_macro_f1.png` | Complete and visually checked |
| P4 independent rerun | Same derived cache/lock | `PYTHONPATH=src python3 scripts/run_v2_external_validation.py rerun-p4` | Separate immutable rerun result directory | Complete; exact CSV match |
| P4 reproducibility check | Primary and rerun CSV | `cmp -s <primary>/subject_level_results.csv <rerun>/subject_level_results.csv` and `sha256sum` | Exact identity; expected SHA-256 `ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8` | Pass |
| P5 external fusion | Would require complete all-11-class/25-subject source | No permitted analysis command | No cache, manifest, score, statistics, or rerun | Hard stop |
| P6 repeat cohort | Would require validated seed-to-state/task distribution | No permitted repeat command | No repeat outcome artefacts | Hard stop |

## Required Environment

The Recovery R1 execution recorded its environment in the P4 primary and rerun `environment.json` files. The required Python components include NumPy, SciPy, scikit-learn, MNE, and PyTorch. MyoSim V1.1 was restored from the user-provided release only to inspect/run the existing integration boundary; P6 was not rerun or modified.

## Integrity Constraints

Raw recordings must not be written to the repository. P4 temporary raw recordings belong only under `<LOCAL_WORKSPACE>/hmi_data/raw/v2_recovery_r1_openbmi_nm000338` and must be removed after cache generation. P4 recovery result paths are immutable. P5 and P6 must not gain synthetic or pseudo-repeat outputs merely to populate this matrix.
