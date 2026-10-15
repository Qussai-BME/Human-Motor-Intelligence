> **HISTORICAL / SUPERSEDED RECORD:** This document records an earlier pre-reopening state. It is retained for provenance only. Current P6 disposition is documented in `P6_FINAL_STATUS.md` and `closure/10_FINAL_CLOSURE_REPORT.md`.

# CPU-First Q1 Upgrade Report
## Human Motor Intelligence — R3 Extension 001

## Executive interpretation

A small CPU-only extension was executed on the available derived caches without changing the frozen P4 R1 or P5 R2 namespaces. The extension answers two limited questions: whether a log-Euclidean covariance representation can be evaluated under the existing P4 subject-wise LOSO boundary, and whether entropy-confidence-weighted late fusion behaves differently from static mean fusion and unimodal controls in the amended P5 feature cache.

The results are **new extension evidence**, not replacements for the frozen primary papers and not pooled into their statistics.

## Executed conditions

| Extension | Subjects | Primary output | Independent rerun | Status |
|---|---:|---|---|---|
| P4 log-Euclidean covariance + shrinkage LDA | 54 | Subject-level and trial-level predictions | Exact byte match | Completed |
| P5 entropy-confidence-weighted late fusion | 24 | Subject-level and trial-level predictions, confidence weights | Exact byte match | Completed |
| P4 aligned log-Euclidean ablation | 54 intended | No valid result released | Not completed | Pending computational gate; no claim |
| P4 robustness perturbations/calibration | — | Not executed | — | Requires separate amendment |
| P5 modality corruption/missing-modality fallback/calibration | — | Not executed | — | Requires separate amendment |

## P4 result

The new log-Euclidean covariance representation with shrinkage LDA produced mean subject-level macro-F1 **0.35408 (SD 0.04930)** across 54 OpenBMI subjects. Mean accuracy and balanced accuracy were both **0.50065 (SD 0.00721)** under the stored binary-label evaluation. The primary and independent rerun subject-level JSON files have identical SHA-256:

`bb4073e93e95e00494ad900a2e9dbd31d0cd05e111ec86d81baa6c02e5b416fc`

This is not a direct comparison against the frozen P4 classifier ranking because the representation, feature construction, and extension protocol differ. It is evidence that a CPU-only covariance-geometry baseline can be executed under the declared LOSO boundary; it does not establish superiority or explain all cross-subject failure.

## P5 result

The new entropy-confidence-weighted fusion produced mean subject-level macro-F1 **0.08021 (SD 0.03033)** across 24 retained subjects. The corresponding new-run controls were EEG-only **0.08140 (SD 0.02511)**, EMG-only **0.04844 (SD 0.02574)**, and static mean fusion **0.08051 (SD 0.03155)**. The weighted fusion did not outperform EEG-only or static fusion in this extension. It was higher than EMG-only in the paired Wilcoxon comparison, with raw p = 0.000205; this is a within-extension exploratory comparison and was not used to claim general fusion benefit.

The exact primary/rerun subject-level SHA-256 is:

`a6c4cc7ea57d2fc9d5265a804ff836c75ee030fdc67d85e808b617147429b0a6`

The primary/rerun trial-prediction files also matched byte-for-byte. The result is consistent with the existing careful P5 interpretation: transparent fusion did not establish benefit over EEG-only in this amended cohort. The confidence rule did not change that conclusion.

## Non-executed extensions

The aligned P4 condition was registered but not released because its fold-local covariance transformation required repeated eigendecomposition over the full 54-subject epoch cache and exceeded the available execution window. No partial result was promoted. A future implementation may use a validated batch or compiled implementation, but it must preserve fold-local fitting and receive a new execution record.

Calibration metrics were not calculated for the frozen outputs because their per-trial probabilities were not preserved there. The new P5 extension stores trial-level predictions and confidence weights, but a calibration analysis requires its own prespecified binning/ECE/Brier protocol. P4 robustness perturbations, P5 modality corruption, and missing-modality fallback were not executed because their perturbation semantics and acceptance thresholds require separate amendments. Cross-dataset evaluation remains blocked by the absence of an authenticated compatible second dataset.

## Claim boundary

The extension supports a narrow methodological statement: interpretable CPU-only representation and reliability-rule experiments can be added without GPU training or alteration of the frozen evidence. It does **not** support claims that Riemannian alignment improves generalization, that confidence weighting improves fusion, that fusion is universally useful, or that any intervention is clinically effective.

P3 is integrated as qualified external archived evidence; it was not independently rerun in this umbrella. P6 R3 remains blocked pending authentic provenance-linked decoder traces and has no relation to these P4/P5 CPU extensions.

## Reproducibility pointers

The runner is `scripts/run_cpu_q1_upgrade_r3_001.py`; analysis is `scripts/analyze_cpu_q1_upgrade_r3_001.py`; the governing amendment is `audit/V2_PROTOCOL_AMENDMENT_CPU_Q1_UPGRADE_R3_001.md`; cache schema inspection is recorded in `audit/cpu_upgrade_cache_schema_r3.json`. Primary and independent extension outputs are under `results/extensions/v2-cpu-q1-upgrade-r3-001/` and `results/extensions/v2-cpu-q1-upgrade-r3-001-independent-rerun/`.

## References

[1]: ../audit/CPU_FIRST_Q1_UPGRADE_MATRIX_R3.md "CPU-First Q1 Upgrade Matrix"
[2]: ../audit/V2_PROTOCOL_AMENDMENT_CPU_Q1_UPGRADE_R3_001.md "CPU Q1 Upgrade Protocol Amendment"
[3]: ../papers/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md "Frozen P4 Q1 manuscript"
[4]: ../papers/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md "Frozen P5 Q1 manuscript"

This report follows the extension matrix, amendment, and frozen paper boundaries.[1] [2] [3] [4]

## P5 corruption and missing-modality extension

A second registered extension applied deterministic feature-group dropout to the 24-subject amended Jeong cache at 0%, 10%, and 20% in separate EEG and EMG arms, and evaluated two explicit missing-modality fallback states. This is a **feature-group perturbation study**, not a raw-channel hardware robustness experiment.

The confidence-weighted fusion macro-F1 means were 0.08040 at 0% EEG feature-group dropout, 0.07658 at 10%, and 0.07540 at 20%. In the EMG dropout arm they were 0.08040, 0.08037, and 0.08037, respectively. In the missing-modality fallback states, the weighted-fusion rule reduced to an available-modality behavior: 0.08127 when EMG was missing and 0.04844 when EEG was missing. These values are descriptive extension outcomes; they do not establish a general degradation law, hardware robustness, or physiological mechanism.

The primary and independent rerun subject-level JSON files matched byte-for-byte with SHA-256:

`d26729f05110a8cc5e22143b080b38b7f76739cd48a349edc31a5a2e1429588a`

The primary and rerun trial-prediction files also matched byte-for-byte. The exact arm/level summaries and paired contrasts are in `audit/p5_corruption_statistics_r3_002.json` and the corresponding extension result directories.

## Updated scope decision

The CPU-first proposal is now partially executed in two defensible increments: P4 log-Euclidean baseline, P5 entropy-confidence-weighted fusion, and P5 feature-group corruption/missing-modality fallback. P4 fold-local alignment remains registered but not released because the current uncompiled implementation exceeded the available CPU execution window. P4 calibration/robustness, P5 calibration, raw-signal perturbation, cross-dataset evaluation, and Paper 2 kernel-reduction remain separate gates. No result from an incomplete process is included in any summary.
