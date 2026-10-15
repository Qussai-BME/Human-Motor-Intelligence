# Final P4/P5 Q1 Hardening Dossier — R3

## Executive scientific disposition

This dossier implements the supplied final hardening specification without expanding the project into expensive model families or large experimental grids. The analysis reuses frozen subject-level artifacts whenever valid. P4 representation comparisons are completed with paired subject-level inference and Holm correction. P4 calibration is explicitly marked non-estimable from the retained hard-label prediction artifacts; no confidence values are reconstructed from labels. P4 robustness is skipped after a documented CPU gate, as permitted by the specification.

P5 clean-train/corrupted-test evidence is available from the strict R3 run. The final specification's required comparison is restricted here to 0% clean and 20% EEG feature-group zeroing for EEG-only, static fusion, and the best confidence-based method. Models were fit on clean training subjects and frozen before corrupted-test evaluation. This intervention is feature-cache degradation, not electrode failure or clinical hardware robustness.

## P4 final representation evidence

| Paired comparison | Mean macro-F1 difference | Median difference | Bootstrap 95% CI | Holm-adjusted Wilcoxon p | Paired effect size |
|---|---:|---:|---:|---:|---:|
| Temporal − spectral | 0.035040 | 0.034236 | 0.017260–0.053382 | 0.000749 | 0.517 |
| Temporal − covariance log-Euclidean | 0.245420 | 0.238368 | 0.206567–0.284604 | <0.001 | 1.671 |
| Spectral − covariance log-Euclidean | 0.210381 | 0.203006 | 0.178665–0.242577 | <0.001 | 1.743 |

The P4 evidence supports a protocol-qualified representation finding: under the evaluated 54-subject OpenBMI strict zero-calibration LOSO protocol, temporal and spectral representations retained more discriminative information than the tested covariance-only log-Euclidean representation. It does not establish that Riemannian methods fail generally, that covariance representations are universally inferior, or that EEG transfer is fundamentally non-geometric.

P4 calibration is not estimable from the retained outputs because the relevant P4 artifacts contain hard predictions and labels but no probability or decision-score output. This is a reproducibility limitation, not a license to derive artificial confidence from correctness. A future P4 calibration analysis must store fold-local probabilities or decision scores at execution time.

## P5 clean-to-degraded robustness evidence

| Condition | Clean mean macro-F1 | 20% EEG-degraded mean macro-F1 | Mean drop | Mean relative retention |
|---|---:|---:|---:|---:|
| EEG-only | 0.081397 | 0.017279 | 0.064118 | 0.2290 |
| Static-mean fusion | 0.080506 | 0.017154 | 0.063352 | 0.2417 |
| Confidence-selective fusion | 0.081174 | 0.017279 | 0.063895 | 0.2357 |

At 20% EEG feature-group zeroing, static fusion was numerically higher than EEG-only by 0.000125 macro-F1 in the aggregated subject mean, but the paired Wilcoxon comparison was non-significant (*p*=0.715) with a small negative effect size for static fusion relative to EEG-only (−0.180). Confidence-selective fusion exactly matched EEG-only at the degraded aggregate and at every paired subject-level comparison in the retained output. Therefore, Outcome A is not supported. The appropriate conclusion is: under this corruption model and strict zero-calibration protocol, multimodal fusion did not provide measurable robustness beyond EEG-only. Relative retention is descriptive and is not treated as an inferential endpoint.

The confidence-based method also did not provide a robustness advantage. This supports the bounded interpretation that uncalibrated entropy-derived confidence was insufficient as a modality-reliability estimator in this setting. It does not prove that calibrated reliability-aware fusion cannot work.

## P5 calibration evidence

The independent P5 calibration analysis evaluated EEG-only, EMG-only, static fusion, confidence-weighted fusion, and confidence-selective fusion. Static fusion had Brier 0.919149 and ECE 0.044729. Confidence-weighted fusion had Brier 0.938161 and ECE 0.085202. Confidence-selective fusion had Brier 0.948498 and ECE 0.106809. Their accuracies were 0.114318, 0.112727, 0.110909, and 0.110909 for EEG-only, static fusion, confidence-weighted fusion, and confidence-selective fusion respectively. Confidence–correctness associations were near zero for fusion conditions. The primary and independent rerun probability files were byte-identical.

## Leakage, inference, and reproducibility audit

| Audit item | Result | Evidence |
|---|---|---|
| Held-out subject excluded from P4 model fitting | PASS | P4 representation runner constructs train subjects as all subjects except `held` and fits only on `xtr, ytr` |
| Held-out subject excluded from P5 fitting | PASS | P5 strict runner fits EEG and EMG LDA models on clean training subjects only |
| Corruption applied only after clean fitting | PASS | P5 strict protocol explicitly records `training_is_clean_for_all_test_variants=true` |
| Subject as inferential unit | PASS | P4 uses 54 subject rows per representation; P5 uses 24 subject rows per condition/variant |
| P4 representation rerun | PASS | Primary/rerun subject-level JSON SHA-256 `cd7f8df8926316d9107834efea9806f93adc915d20786ccd8b42aee8ec723bd1` |
| P5 calibration rerun | PASS | Primary/rerun trial-probability SHA-256 `9d454e309e6c529bc1466f155884bba7566d4616cdc95db9935e7374782d0378d` |
| P3/P6 boundary | PASS | No P3 reconstruction and no authenticated P6 R3 decoder-quality traces |

## Required claim-evidence matrix

| Claim | Class | Evidence | Disposition |
|---|---|---|---|
| Representation family materially affects P4 zero-calibration cross-subject performance under the evaluated OpenBMI protocol | A — directly demonstrated | P4 representation subject-level outputs and paired Holm analysis | Retain with protocol scope |
| Covariance-only log-Euclidean geometry is universally inferior | E — unsupported | No cross-protocol evidence | Remove |
| Static fusion provides conditional robustness at 20% EEG feature zeroing | C — plausible but not demonstrated | Small descriptive difference; non-significant paired comparison | Do not claim; report as non-confirmatory numerical pattern |
| Multimodal fusion provides measurable robustness beyond EEG-only under the tested corruption | E — unsupported | Static fusion did not significantly exceed EEG-only; selective matched EEG-only | Remove |
| Confidence weighting is a successful contribution | E — unsupported | P5 calibration and clean/degraded results | Remove; retain as negative ablation |
| Uncalibrated confidence is insufficient as a reliability estimator in this cohort | B — strongly supported | Near-zero confidence–correctness association; worse calibration for confidence variants | Retain cautiously and cohort-qualify |
| P5 missing-modality logic demonstrates graceful engineering fallback | A — directly demonstrated | Existing explicit EEG-only/EMG-only fallback states | Retain as engineering robustness, not scientific novelty |
| P4 calibration quality is known | E — unsupported | No retained P4 probability/score artifact | Remove; state not estimable |

## Internal Reviewer 1 — Machine Learning

**Likely objections.** The reviewer will ask whether the representation result is a classifier artifact, whether the covariance implementation is competitive, whether preprocessing or model selection leaked across folds, whether the confidence heuristic was calibrated, and whether the P5 degradation intervention is sufficiently realistic.

**Disposition.** The classifier-leaderboard framing is rejected. The P4 claim is restricted to the tested representation family, fixed LDA protocol, and OpenBMI cohort. The leakage audit shows held-out subjects are excluded from fitting. The covariance result is not rescued with a method grid. P5 reports confidence calibration as a negative result and states that feature-group zeroing is not physical sensor failure. The objection is **resolved by existing evidence and acknowledged limitation** where realism cannot be claimed.

## Internal Reviewer 2 — Biomedical Engineering

**Likely objections.** The reviewer will challenge physiological interpretations of the EMG ordering, clinical or prosthetic extrapolation, the practical significance of synthetic corruption, and the relationship between multimodality and hardware reliability.

**Disposition.** No causal physiological explanation is asserted. MI and motor execution remain distinct. P5 degradation is labelled feature-cache intervention rather than electrode or hardware robustness. No clinical, prosthetic, safety, or human-factors claim is made. The objection is **acknowledged as limitation** and bounded by the engineering-fallback analysis.

## Internal Reviewer 3 — Statistics

**Likely objections.** The reviewer will inspect the subject-level unit, paired structure, Holm correction, bootstrap logic, non-significance interpretation, and whether retention is incorrectly treated as an inferential endpoint.

**Disposition.** P4 uses paired subject-level differences with bootstrap CIs, Wilcoxon tests, and Holm adjustment across three representation comparisons. P5 reports clean-minus-degraded drops and descriptive retention but does not treat retention as confirmatory. Non-significant fusion-versus-EEG differences are not labelled equivalent. The objection is **resolved by new low-cost analysis** and explicit terminology.

## Response strategy

The response letter should state that the papers are not presented as universal algorithmic victories. The contribution is protocol-specific evidence about transfer under strict zero-calibration and about the failure of simple confidence weighting to establish clean-data or degraded-data benefit in the evaluated cohort. Reviewer requests for a larger representation grid, GPU models, transformers, adversarial adaptation, or broad transfer benchmarking should be declined as outside the minimum-evidence objective unless a reviewer identifies a specific validity blocker.

## Q1 readiness scorecard

| Dimension | P4 score /10 | P5 score /10 | Basis |
|---|---:|---:|---|
| Scientific significance | 7.0 | 7.0 | Non-trivial cross-subject representation/fusion questions with bounded negative evidence |
| Novelty | 6.5 | 6.5 | Protocol-specific evidence rather than a new universal method |
| Methodological rigor | 8.5 | 8.5 | Strict LOSO, external cohorts, fixed protocols, fold-local fitting |
| Statistical rigor | 8.0 | 8.0 | Subject-level paired inference, bootstrap CIs, Holm correction; P5 retention remains descriptive |
| Reproducibility | 8.5 | 8.5 | Independent reruns, hashes, manifests, source code, machine-readable outputs |
| Biomedical relevance | 6.5 | 7.0 | Clear motor-intent relevance; no clinical endpoint claimed |
| Generalizability | 6.0 | 6.0 | External validation exists, but cohort/task/representation scope remains narrow |
| Writing quality | 8.0 | 8.0 | Q1-style structure with explicit evidence boundaries |
| Journal fit | 7.0 | 7.0 | Suitable for methods/BCI/biomedical AI venues subject to editor scope |
| Q1 readiness | 7.5 | 7.5 | Strong submission candidate after normal journal-specific formatting; not guaranteed acceptance |

## Final scorecard narrative

**Strongest contribution.** P4 provides a reproducible subject-level demonstration that representation choice is materially associated with zero-calibration cross-subject EEG performance under a fixed external protocol. P5 provides a transparent negative result showing that simple confidence-aware fusion did not add clean-data or tested degraded-data value beyond EEG-only.

**Biggest weakness.** P4 lacks retained probability/decision-score outputs for a defensible calibration analysis, and P5's corruption model is a feature-cache intervention rather than a physical sensor-failure study.

**Strongest likely reviewer objection.** The observed representation and robustness patterns may depend on the particular cohorts, feature definitions, classifier family, and synthetic degradation model.

**Highest-value remaining improvement.** Add prospective fold-local probability storage and learned calibration, then evaluate a preregistered physically grounded modality-degradation protocol on a new external cohort.

**Lowest-cost path to improvement.** Preserve the current experiments, add probability outputs to the existing P4 runner, and perform one predeclared 0%/20% degradation analysis with the same subject-level pipeline; do not add a large model or representation grid.

## Experiment cost accounting

| Experiment | Cost disposition |
|---|---|
| P4 paired representation analysis | Low; subject-level JSON reuse only, no feature extraction or model rerun |
| P4 calibration | Not run; retained artifacts lack probability/score outputs |
| P4 robustness | Skipped after CPU gate; no result artifact released |
| P5 0%/20% corrupted-test analysis | Low; existing strict R3 outputs subsetted and reanalyzed |
| P5 calibration | Low; existing probabilities analyzed and independently rerun |
| Deep learning, transformers, adaptation, adversarial, self-supervised, large grids | Not run by design |

## Stop decision

The final hardening stop condition is met for the internally actionable evidence: P4 representation findings are statistically documented; P5 clean and degraded analyses are documented; calibration interpretation is complete; reviewer objections are resolved or explicitly limited; and reproducibility artifacts are retained. No further experiments should be added before manuscript submission unless a specific reviewer or data gate creates a new validity requirement.
