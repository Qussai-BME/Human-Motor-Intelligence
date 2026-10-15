# Six-Paper Claim–Counterclaim Audit

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


**Rule:** A claim enters this audit only with an evidence tier, protocol boundary, and artefact. “Counterclaim” identifies a real qualification or external context, not a rebuttal invented to force symmetry.

| Paper / domain | Evidence-supported claim | Counterclaim or comparability limit | Status | Governing artefact |
|---|---|---|---|---|
| P1 — sEMG metrics | In the stated LOSO analyses, rest-inclusive aggregate reporting can diverge sharply from macro-F1/active performance, particularly in the reported DB3 result. | The magnitude is dataset/task/prevalence/model dependent; it does not establish inflation in all EMG benchmarks. | Supported within source scope | `EMG_SERIES_MASTER_EVIDENCE.md`; P1 DOCX extract |
| P1 — model comparison | P1 reports database-specific Friedman evidence and a transparent benchmark. | DB3 is small; EA/CNN and distributional caveats limit model-wide conclusions. | Qualified | Same |
| P2 — cross-subject gap | MiniROCKET raw LOSO results are far below the stated within-subject comparisons in P2. | Accuracy target policy differs from P1; no direct numerical merge is permitted. | Supported within source scope | `EMG_SERIES_MASTER_EVIDENCE.md`; P2 DOCX extract |
| P2 — adaptation mechanism | The diagnosed PPV conditioning problem explains behaviour in the tested representation/adaptation path. | It does not prove all domain adaptation approaches fail; representation and regularization differ across methods. | Mechanism-specific | Same; literature log L5–L7 context |
| P3 | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** | No counterclaim is appropriate when source evidence is absent. | Pending | `EMG_SERIES_MASTER_EVIDENCE.md` |
| P4 — external subject-independent MI | Under the Recovery R1 protocol, binary OpenBMI MI is decoded above a nominal binary accuracy reference across five fixed zero-calibration LOSO conditions. | This is not a direct replication of BCI IV-2a, not a universal claim, and performance is not numerically rankable across differing dataset protocols. | Reproducibility-verified external validation | P4 manifest, `statistics_macro_f1.json`, P4 audit |
| P4 — model ordering | Compact CNN has the highest descriptive mean macro-F1 (0.6364). | No pairwise model comparison survives Holm; no model is confirmed superior in the predeclared family. | Descriptive only | `statistics_macro_f1.json` |
| P4 — cross-subject limitation | Inter-subject variation is visible in subject-level distributions and the source literature identifies MI variability. | The current binary external validation has means materially above its nominal binary reference; it cannot be summarized as a universal “weak zero-calibration” finding. | Nuanced / protocol-specific | P4 figure and audit; literature log L1/L5/L6 |
| P5 — transparent fusion | Frozen Cho2017 evidence found no Holm-surviving transparent fusion advantage over EMG-only. | External Jeong validation did not run owing to source coverage failure. Contemporary fusion work uses differing architecture/task/selection settings, so no universal “fusion useless” conclusion follows. | Primary result frozen; V2 extension blocked | V2 master audit; P5 hard stop; literature log L7 |
| P6 — replay/system endpoint | Task success/time/failure are conceptually important endpoints beyond time-bin classification. | No V2 repeat distribution was generated because seed did not yield independent simulator variation. | Design context only; execution blocked | P6 hard stop; literature log L8/L9 |
| Programme integration | Auditable, protocol-specific negative and blocked results are informative and should be retained. | They do not collectively establish clinical utility, prosthesis readiness, causal mechanisms, or performance in patient populations. | Supported governance principle | Q1 master audit |

## Prohibited Claim Escalations

| Prohibited escalation | Reason |
|---|---|
| “All cross-subject EEG decoding is weak.” | P4 is binary OpenBMI only; literature and model/protocol differences matter. |
| “CNN wins P4.” | The highest mean did not yield Holm-surviving pairwise superiority. |
| “P5 externally replicated a null fusion finding.” | P5 had no valid external model run. |
| “Fusion is useless.” | Evidence is transparent-fusion/dataset/protocol-specific; counterexamples have different designs. |
| “P6 demonstrates replay robustness across repeats.” | No valid independent repeats were possible. |
| “P3 confirms the series conclusion.” | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`**. |
| “Synthetic corruption validates biomedical performance.” | Synthetic control is non-benchmark sensitivity material. |
