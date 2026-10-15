# EMG Series Master Evidence Record

**Scope:** P1–P3 programme context only. This record extracts and aligns evidence from the two author-supplied DOCX manuscripts. It does **not** revise P1 or P2, and it does not infer P3 content.

## Authoritative Inputs

| Paper | Author-supplied source | Extracted audit text | Evidence status |
|---|---|---|---|
| P1 | Manuscript submitted; text not distributed in this archive | Evidence recorded in the audits under `audit/` | Source-grounded |
| P2 | Revised manuscript (after supervisor review); text not distributed in this archive | Archived code and results: Zenodo 10.5281/zenodo.23136515 (v2.0.0) | Source-grounded in the archived results |
| P3 | Manuscript text not distributed; archived evidence in `external/p3_litedan_v1_0_0/` | `audit/P3_EXTERNAL_EVIDENCE_ACCEPTANCE_R3.md` | **Externally archived evidence accepted; not independently rerun** |

## P1 — Rest-Class Metric Inflation

**Title:** *Rest-Class Metric Inflation in Zero-Calibration Cross-Subject sEMG: A Three-Database LOSO Benchmark Across Intact-Limb and Transradial Amputee Populations*.

P1 asks whether conventional all-window performance reporting can be inflated by a dominant rest class in strict cross-subject sEMG recognition, including intact-limb and transradial-amputee populations. The source manuscript specifies NinaPro DB2 (*n*=40 intact), DB3 (*n*=11 transradial), and DB7 (*n*=22 mixed), for 73 participants in total. It describes 12-channel Delsys acquisition at 2000 Hz, strict LOSO, 400 ms windows with 50% overlap, 420 selected hand-engineered features, and XGBoost, LDA, LinearSVC, random forest, and naive CNN conditions.

| P1 XGBoost source result | Overall accuracy | Macro-F1 | Boundary |
|---|---:|---:|---|
| DB7 | 65.96 ± 6.01% | 27.14% | Intact/mixed source cohort as defined by P1 |
| DB2 | 54.64 ± 7.84% | 21.89% | Intact source cohort as defined by P1 |
| DB3 | 43.46 ± 10.73% | 4.01% | Small transradial cohort; interpretation must preserve its sample-size limitation |

The source reports a DB3 overall-versus-macro-F1 divergence of 39.45 percentage points and an active-only XGBoost figure of 3.6%, yielding 39.86 percentage points overall-minus-active inflation in that stated analysis. Its reported Friedman results are DB7 χ²=4.91, *p*=0.179; DB3 χ²=24.49, *p*<0.001; and DB2 χ²=39.69, *p*<0.001.

> P1 supports a metric-policy warning in its declared benchmark; it does not prove that every cross-subject EMG study is rest-inflated.

The source caveats must remain attached: EA was not ablated; the CNN has tuning/data asymmetry; *t*-CI may be fragile under non-normality; DB3 is small; and dataset/protocol differences constrain generalization.

## P2 — Reference MiniROCKET Domain-Adaptation Benchmark (revised, v2)

**Title:** *Cross-Subject sEMG Gesture Recognition with Reference MiniROCKET: a multi-seed benchmark of unsupervised domain adaptation* (see the manuscript file for the exact title).

> **Supersession notice.** The first version of P2 (archive v1.0.0) used a hand-written PPV transform and a CORAL implementation with two errors (extra re-coloring applied to the target, and a transposition error). Its headline claims — raw LOSO accuracy of 9.15% / 13.08% / 6.63% on DB7 / DB2 / DB3, CORAL significantly degrading accuracy, and a "PPV near-singularity" mechanism — are **withdrawn** and must not be cited. Version 2.0.0 of the archive corrects the implementation; v1.0.0 is superseded.

P2 v2 evaluates the reference multivariate MiniROCKET transform with a ridge classifier under subject-held-out evaluation on NinaPro DB2 (40 subjects), DB3 (11 amputees) and DB7 (22 subjects: 20 intact + 2 amputee): 73 held-out-subject folds, five seeds, 1,825 method–fold evaluations. Raw (inductive) is compared with CORAL, TCA and SA, which use unlabeled target repetitions for adaptation and disjoint repetitions for testing. Statistics are subject-level (Friedman, Holm–Šidák-corrected Wilcoxon). Rest is excluded from reported accuracies, so P2 accuracy must **not** be compared numerically with P1 all-window accuracy.

| P2 v2 quantity (from the manuscript abstract and Table 2) | Value |
|---|---|
| Raw accuracy | DB7 20.7%, DB3 8.9%, DB2 11.5% (chance 2.5%, 5.9%, 2.0%) |
| CORAL covariance-distance reduction | 81–90% in all 365 fold–seed evaluations |
| CORAL accuracy change at pre-specified default regularization | DB7 +1.4 pp (adjusted p = 0.041); DB2 +1.0 pp; DB3 not detectable |
| CORAL macro-F1 change | +2.5 pp and +1.8 pp (accompanied by a flatter predicted-class distribution) |
| TCA | no significant accuracy improvement |
| SA | accuracy reduced by 2.7–13.0 pp |
| Amputee accuracy (DB3) | 1.0–1.6 times chance |

The regularization sweep is single-seed, descriptive and did not identify an optimum. The results are specific to reference MiniROCKET features with a ridge classifier and these protocols; they are not a statement about all domain-adaptation methods.

## P3 — Learned Adaptation (Externally Archived Evidence)

P3 is accepted as an externally archived Lite-DAN study across DB2, DB3, and DB7. Its package contains 27 experiment summaries and 657 LOSO fold records, with source code, registry, and provenance documentation. It is not independently rerun in the umbrella environment and does not provide a MyoSim-compatible decoder trace.

## Cross-Paper Interpretation Rules

| Rule | Required treatment |
|---|---|
| Metric policy | Preserve P1 rest-inclusive versus P2 rest-excluded reporting boundary. |
| Unit and split | Do not combine counts or statistics across papers without a newly justified joint analysis. |
| Mechanism | P2 v2 makes no PPV near-singularity claim; its CORAL findings are specific to reference MiniROCKET features with a ridge classifier. |
| Clinical scope | Retain DB3 small-sample/participant-context limitations. |
| P3 | Use only the externally archived package with its qualified limitations; do not imply an umbrella rerun or P6 trace bridge. |
| V2 EEG/fusion papers | P1/P2 contextualize cross-subject research but do not supply a result for P4–P6. |
