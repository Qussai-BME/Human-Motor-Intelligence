# Cross-Reference Audit — V2 Recovery R2

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


## Purpose

This audit prevents the six-paper programme from turning distinct evidence sources into an implicit pooled benchmark. Every cross-reference must retain the source, task, cohort, modality, class policy, endpoint, and evidence tier.

| Source paper/result | Correct cross-reference | Forbidden shortcut |
|---|---|---|
| P1 rest-class audit | Cite when motivating active-class metrics and class-policy transparency in sEMG | Do not use P1 accuracy values to characterize P2, P4, or P5 macro-F1. |
| P2 MiniROCKET mechanism | Cite when discussing its tested PPV representation/conditioning diagnosis | Do not call it proof that all adaptation, CORAL, TCA, SA, or deep adaptation fails. |
| P3 | State **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** | Do not populate an inferred title, result, dataset, or comparison. |
| P4 OpenBMI | Describe as 54-subject external binary EEG MI LOSO validation | Do not average or rank its macro-F1 with BCI IV-2a or P5 Jeong values. |
| P5 Jeong | Describe as amended 24-subject, all-11-class, MI-only external EEG–EMG LDA validation | Do not call it direct Cho2017 replication, a general fusion verdict, or a motor-execution finding. |
| P6 R2 | Describe as 20 declared simulator initial states under one fixed replay/controller | Do not use it as biomedical evidence, a decoder-quality relation, or a synthetic-corruption result. |

## Metric and Chance Language

| Context | Permitted wording | Prohibited wording |
|---|---|---|
| P4 binary MI | “Binary macro-F1 under the declared subject-held-out OpenBMI protocol.” | “The programme’s universal binary chance-corrected EEG score.” |
| P5 all-11-class MI | “Held-out-subject macro-F1 in the balanced 11-class Jeong cohort.” | “Macro-F1 chance is exactly 1/11.” |
| P5 accuracy/balanced accuracy | “1/11 is a nominal uniform-class reference for accuracy/balanced accuracy.” | “1/11 proves macro-F1 statistical significance.” |
| P6 success | “0/20 simulated declared initial states completed the task.” | “The decoder fails in 100% of people/patients.” |
| P6 baseline | “A single unperturbed compatibility control completed the benchmark.” | “The baseline is a randomized control cohort.” |

## Required Linking Language

P4-to-P5 transitions must say that both are external validations but differ in source, modality, label cardinality, processing, and model family. P5-to-P6 transitions must say that P5 is biomedical data analysis while P6 is simulator systems evidence. P1/P2-to-P5 transitions must preserve that P1/P2 are author-supplied sEMG manuscripts with distinct datasets/protocols. Any statement about fusion must name the fixed LDA pipelines and external Jeong cohort. Any statement about control robustness must name the declared MyoSim initial-state distribution.

## Artefact Link Map

| Claim cluster | Canonical R2 artefact |
|---|---|
| P4 external EEG result | `audit/V2_P4_OPENBMI_EXTERNAL_VALIDATION_AUDIT_RECOVERY_R1.md` |
| P5 source amendment | `audit/V2_P5_SUB23_SECOND_SOURCE_CHECK.md`; `audit/V2_PROTOCOL_AMENDMENT_RECOVERY_R2_001.md` |
| P5 model result | `audit/V2_P5_JEONG_EXTERNAL_VALIDATION_AUDIT_RECOVERY_R2.md`; `statistics_macro_f1.json` |
| P6 baseline/capability | `audit/V2_P6_UNPERTURBED_BASELINE_MATCH_RECOVERY_R2.md`; `audit/V2_P6_INITIAL_STATE_CAPABILITY_PREFLIGHT_RECOVERY_R2.md` |
| P6 model/system result | `audit/V2_P6_REAL_REPLAY_INITIAL_STATE_REPEAT_AUDIT_RECOVERY_R2.md`; `statistics_initial_state_repeats.json` |
| P1/P2/P3 scope | `papers/EMG_SERIES_MASTER_EVIDENCE.md` |
| Programme integration | `papers/Q1_EVIDENCE_EXPANSION_MASTER_AUDIT_RECOVERY_R2.md` |

## Audit Decision

All R2 cross-references must retain the above qualifiers. If a proposed sentence cannot identify its source/protocol boundary, it must be rewritten or removed.
