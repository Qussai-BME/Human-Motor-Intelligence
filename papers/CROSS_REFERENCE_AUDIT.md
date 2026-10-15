# Cross-Reference Audit — Human Motor Intelligence Six-Paper Programme

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


## Purpose

This audit prevents invalid cross-paper transfer of metrics, claims, or evidence tiers. A shared research trajectory does not make results numerically comparable by default.

## Citation and Evidence Links

| From | To | Valid relationship | Invalid shortcut prohibited |
|---|---|---|---|
| P1 | P2 | Both are author-supplied cross-subject sEMG studies; both motivate attention to target definition and representation. | Comparing P1 overall/rest-inclusive accuracy directly to P2 rest-excluded accuracy. |
| P1 | P3 | P1 provides a metric-audit context. | Inferring P3 dataset, values, or conclusion from P1. |
| P2 | P3 | P2 provides a representation-specific mechanism context. | Calling P3 an adaptation solution or failure without its source package. |
| P1/P2 | P4 | Cross-subject generalisation is a shared programme theme. | Treating sEMG and EEG outcomes as a common pooled benchmark. |
| P4 frozen BCI IV-2a | P4 V2 OpenBMI | Both address strict cross-subject EEG MI; V2 is a harmonized independent dataset check. | Calling V2 OpenBMI a direct replication or comparing raw macro-F1/accuracy rankings without the class/task/protocol caveats. |
| P5 frozen Cho2017 | P5 proposed Jeong validation | The latter was selected as an external synchronized multimodal setting. | Claiming an external replication or null result: Jeong stopped before valid model fitting. |
| P5 | P4 | Both examine zero-calibration EEG-related signals under LOSO. | Interpreting P4 EEG model means as an EMG-vs-EEG fusion conclusion. |
| P6 real replay | P6 synthetic corruption | Synthetic sweep may stress decoder-quality sensitivity under controlled corruption. | Using synthetic results as biomedical or real-replay evidence. |
| P6 | P4/P5 | System-level endpoints contextualize downstream control relevance. | Claiming that EEG/fusion classifier results caused real task outcomes without a valid linked experimental trace. |

## Metric Compatibility Audit

| Paper/evidence | Primary metric or endpoint | Directly comparable with | Required qualifier |
|---|---|---|---|
| P1 | Overall accuracy, macro-F1, active-only analyses | Only same target-policy/database-specific analyses | Rest prevalence/policy and participant cohort must be stated. |
| P2 | Rest-excluded accuracy, within/cross ratios, representation diagnostics | Only same rest-excluded protocol | Do not conflate accuracy with P1 macro-F1. |
| Frozen P4 BCI IV-2a | Four-class macro-F1, 9 subjects | Within its frozen result only | Nominal four-class language, not an exact universal chance equivalence. |
| V2 P4 OpenBMI | Binary macro-F1, accuracy, balanced accuracy, 54 subjects | Within Recovery R1 model conditions | Nominal binary accuracy reference; external validation not replication. |
| Frozen P5 Cho2017 | Macro-F1 for EEG/EMG/early/late transparent fusion, 52 subjects | Within frozen Cho2017 condition comparisons | MI setting and original preprocessing define scope. |
| Proposed P5 Jeong | No outcome | None | Hard stop means no metric exists. |
| P6 real replay | Existing frozen task/control endpoints | Its frozen replay protocol only | No V2 repeat estimate. |
| P6 synthetic control | Controlled sensitivity endpoints | Synthetic condition comparisons only | `benchmark_eligible=false`. |

## Terminology Audit

| Term | Approved usage | Prohibited usage |
|---|---|---|
| “external validation” | P4 OpenBMI Recovery R1; labelled `external_validation:true`. | As a synonym for direct replication. |
| “direct replication” | Not used for P4 OpenBMI or P5 Jeong. | Any statement that dataset/task/protocol differs yet calls it replication. |
| “zero calibration” | No target-subject labels, fitting, tuning, scaler fitting, or adaptation in the held-out fold. | Mere absence of a calibration UI while target data influence preprocessing/model choice. |
| “null result” | A completed registered comparison without a supported superiority effect. | P5/P6 source/capability hard stops. |
| “blocked” | A documented stop condition prior to a valid scientific outcome. | A hidden negative result or missing analysis. |
| “synthetic” | Controlled corruption/sensitivity only. | Biomedical validation or real replay evidence. |
| “P3 evidence” | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`**. | Any inferred numeric/mechanistic statement. |

## Required Cross-References in Revisions

P4 should cite the P1/P2 evidence record only for programme context, then state its independent EEG cohort/protocol. P5 should cite frozen Cho2017 findings and then state the Jeong availability stop, not a manufactured fusion result. P6 should cite the deterministic capability audit and retain a real-versus-synthetic boundary. Every programme-level synthesis must point readers to `Q1_EVIDENCE_EXPANSION_MASTER_AUDIT.md` for tier status.
