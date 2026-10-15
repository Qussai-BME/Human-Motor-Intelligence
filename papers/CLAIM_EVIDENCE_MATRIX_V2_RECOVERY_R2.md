# Claim–Evidence Matrix — V2 Recovery R2

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


| Claim ID | Claim text permitted in R2 | Evidence tier | Canonical numeric/source artefact | Scope condition | Status |
|---|---|---|---|---|---|
| E1 | P1 reports rest-class metric inflation in its stated databases. | Author-supplied | `EMG_SERIES_MASTER_EVIDENCE.md`; extracted P1 source text | P1 protocols and populations only | Integrated context |
| E2 | P2 reports a MiniROCKET PPV-conditioning diagnosis in its stated adaptation analysis. | Author-supplied | `EMG_SERIES_MASTER_EVIDENCE.md`; extracted P2 source text | Tested representation/adaptation path only | Integrated context |
| E3 | P3 has a programme result. | Pending | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** | No source package | Not admissible |
| E4 | P4 compact CNN mean macro-F1 is 0.6364 on external OpenBMI. | V2 R1 external | `results/real/v2-recovery-r1/.../statistics_macro_f1.json` | 54-subject binary MI OpenBMI LOSO; fixed CNN | Admissible with limits |
| E5 | P4 has no Holm-surviving pairwise superiority claim. | V2 R1 external | P4 `statistics_macro_f1.json` and P4 audit | Five fixed models; 10 paired contrasts | Admissible |
| E6 | P5 EEG-only mean macro-F1 is 0.0813. | V2 R2 external | `results/real/v2-recovery-r2/nemar-nm000311-jeong-p5-external-loso-24subject-r2/statistics_macro_f1.json` | Amended 24-subject, MI-only, all-11-class Jeong cohort | Admissible with limits |
| E7 | P5 early and late fusion do not exceed EEG-only after Holm. | V2 R2 external | P5 `statistics_macro_f1.json`, pairwise entries | Transparent LDA features/fusion only | Admissible with limits |
| E8 | P5 EEG/early/late conditions exceed EMG-only after Holm. | V2 R2 external | P5 `statistics_macro_f1.json`, pairwise entries | Same cohort/pipeline; not a mechanism claim | Admissible with limits |
| E9 | P5 result reruns exactly. | V2 R2 reproducibility | Primary/rerun `subject_level_results.csv`; SHA-256 in P5 audit | Same cache/environment/config path | Admissible |
| E10 | P6 has 0/20 task successes under declared state variation. | V2 R2 systems | `results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2/statistics_initial_state_repeats.json` | Fixed replay/controller; declared MyoSim state distribution | Admissible with limits |
| E11 | P6 is reproducible and had 20 distinct qpos states. | V2 R2 systems | P6 `run_records.json`, rerun `run_records.json`, P6 audit | Deterministic rerun; not an independent second cohort | Admissible |
| E12 | P6 failures were caused by decoder quality or predict human outcomes. | None | No eligible artefact | Decoder held fixed; simulator-only state factor | Prohibited |

## Citation Rule

Any manuscript sentence that reports an E4–E11 value must cite its result artefact and the corresponding audit. Dataset landing pages, prose reviews, and figures can provide context but cannot replace the numeric source artefact.
