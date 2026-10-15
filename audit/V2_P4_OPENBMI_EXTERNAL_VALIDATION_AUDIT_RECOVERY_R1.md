# P4 OpenBMI Harmonized External Validation Audit — Recovery R1

**Status:** Completed, independently rerun, and reproducibility-verified  
**Evidence tier:** **V2 Recovery R1 external validation**  
**Identity:** `external_validation: true`; `direct_replication: false`  
**Primary result directory:** `results/real/v2-recovery-r1/nemar-nm000338-openbmi-p4-external-loso-recovery-r1/`

## Scope and Claim Boundary

This audit records a newly acquired **harmonized external validation** of a strict, zero-calibration, subject-level LOSO EEG motor-imagery analysis on NEMAR OpenBMI/KU-MI derivative `nm000338` v1.0.5. The dataset derivative is identified by DOI `10.82901/nemar.nm000338`; the underlying OpenBMI supporting data are identified by DOI `10.5524/100542`; its source descriptor is Lee et al. (2019) [1] [2] [3]. The derivative is recorded under GPL-3.0 in the locked protocol.

> This analysis is **not** a direct replication of the frozen BCI Competition IV-2a result. It has a binary target, a different cohort, recording setting, channel montage, task structure, and pre-processing implementation. It therefore does not rank OpenBMI scores numerically against BCI IV-2a scores. Any programme-level synthesis may compare only carefully qualified qualitative patterns.

## Locked Cohort and Data Boundary

| Field | Verified value |
|---|---:|
| Held-out inference unit | Subject |
| Cohort | 54 named OpenBMI subjects (`sub-1`–`sub-54`) |
| Source recordings per subject | `ses-1`, `acq-train_run-1` and `acq-test_run-4` |
| Labels | `left_hand`, `right_hand` |
| Source events | 50 trials/label/recording; 200 trials/subject after merge |
| Signal selection | 62 named channels; exact exclusion of `EMG1`–`EMG4` |
| Source / derived rate | 1000 Hz / 125 Hz |
| Fixed preprocessing | 8–30 Hz bandpass; 0.5–3.5 s epoch; factor-8 deterministic decimation |
| Derived cache shape | `(200, 62, 375)` per subject |
| Target-subject calibration | None |
| Fit scope for scaler/classifier | Training subjects only |
| Raw-data policy | Sequential external BDF acquisition; checksum receipt; derived cache outside repository; temporary raw BDF/TSV deletion |

All 54 subject caches completed. D1 verified 108 cache/provenance artefacts totaling **933,572,109 bytes**, with recomputed SHA-256 hashes, no missing artefacts, and no raw BDF/EDF-like files retained in the derived cache. D2 confirmed the locked schema; D3 confirmed both labels in every subject; D4 confirmed the 54-subject LOSO/no-calibration protocol; and D5 recorded affirmative fold-isolation and raw-boundary checks. The machine-readable record is `datasets/manifests/nemar_nm000338_openbmi_v2_recovery_r1.json`.

## Subject-Level Results

The primary endpoint is macro-F1. Bootstrap intervals are 10,000-resample percentile intervals across the 54 held-out subjects; they are descriptive uncertainty intervals and are not population guarantees.

| Predeclared condition | Mean macro-F1 | SD | Bootstrap 95% CI for mean | Mean accuracy | Mean balanced accuracy |
|---|---:|---:|---:|---:|---:|
| `eeg-linear-v1` | 0.5962 | 0.1050 | 0.5694–0.6253 | 0.6074 | 0.6074 |
| `eeg-lda-v1` | 0.5980 | 0.1059 | 0.5708–0.6278 | 0.6096 | 0.6096 |
| `eeg-linear-svm-v1` | 0.6123 | 0.1218 | 0.5806–0.6446 | 0.6257 | 0.6257 |
| `eeg-spectral-v1` | 0.6130 | 0.1226 | 0.5809–0.6459 | 0.6262 | 0.6262 |
| `eeg-lightweight-cnn-tcn-v1` | 0.6364 | 0.1654 | 0.5929–0.6800 | 0.6667 | 0.6667 |

The classes are exactly balanced in the derived subject cache. Accordingly, a **nominal binary reference** is appropriate for accuracy under an equal-class random-labeling thought experiment. Macro-F1 is reported as defined by the macro average over the two class-specific F1 values; this audit does **not** mechanically call 0.5 an exact macro-F1 chance value, nor conflate accuracy with macro-F1.

## Within-Dataset Inference

The five fixed conditions had a Friedman statistic of **16.16** across 54 paired subjects (*p* = **0.00281**). Nevertheless, the predeclared ten pairwise Wilcoxon tests had **no Holm-adjusted *p* value below 0.05**; the smallest adjusted value was 0.1042. The raw but multiplicity-unadjusted CNN-versus-linear comparison had a mean paired macro-F1 difference of 0.0402 (*p* = 0.0104), which becomes 0.1042 after Holm. This is reported as an observed descriptive ordering, not a confirmed pairwise superiority claim.

| Comparison (A − B) | Mean paired macro-F1 difference | Raw *p* | Holm-adjusted *p* | Interpretation boundary |
|---|---:|---:|---:|---|
| CNN − linear | 0.0402 | 0.0104 | 0.1042 | No pairwise result survives Holm. |
| CNN − LDA | 0.0384 | 0.0109 | 0.1042 | No pairwise result survives Holm. |
| spectral − linear | 0.0168 | 0.0223 | 0.1780 | No pairwise result survives Holm. |
| SVM − linear | 0.0161 | 0.0278 | 0.1947 | No pairwise result survives Holm. |
| spectral − LDA | 0.0150 | 0.0522 | 0.2609 | No pairwise result survives Holm. |

The full all-pairs table, effects, unadjusted tests, and bootstrap metadata are in `statistics_macro_f1.json`. No model selection, post-hoc tuning, target-domain adaptation, or cross-dataset pooling was performed.

## Independent Reproducibility Rerun

A second complete 54-fold execution was run in the separate immutable namespace `results/real/v2-recovery-r1-independent-rerun/` under the operational amendment `audit/V2_PROTOCOL_AMENDMENT_RECOVERY_R1_001.md`. It reused the same D1-verified cache, analysis code, protocol, and seed schedule solely as an execution reproducibility check.

| Check | Primary | Independent rerun | Result |
|---|---|---|---|
| Subject-level rows | 270 | 270 | Pass |
| `subject_level_results.csv` SHA-256 | `ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8` | Same | Exact pass |
| Byte-for-byte CSV comparison | — | — | Exact pass |
| Manifest SHA-256 | `3c99872b31f1a9d0e0051844bf64362cff7d656b8d2adec01a945d5aafa8d5ac` | Same | Exact pass |
| Protocol SHA-256 | `bb232d08e94beea14b6ccb3a050a376cccf1d50559320d18ec66810d860d4e9d` | Same | Exact pass |

The rerun is not an additional experiment, does not add subjects, and was not pooled with the primary run.

## Permitted and Prohibited Conclusions

| Statement | Status |
|---|---|
| Strict zero-calibration LOSO binary MI decoding was observed on a second, independently sourced EEG dataset under a protocol-locked evaluation. | **Permitted** |
| The condition means were above a nominal binary accuracy reference in this balanced task. | **Permitted with metric qualification** |
| One fixed condition was definitively superior to every other condition after multiplicity correction. | **Not supported** |
| This reproduces the BCI IV-2a result directly. | **Prohibited** |
| OpenBMI’s numerical macro-F1 proves the earlier four-class result weak/strong by comparison. | **Prohibited** |
| This establishes universal subject-independent EEG decoding performance. | **Prohibited** |

## References

[1] [NEMAR dataset `nm000338` v1.0.5](https://doi.org/10.82901/nemar.nm000338)  
[2] [OpenBMI supporting dataset](https://doi.org/10.5524/100542)  
[3] [Lee et al., *OpenBMI: a large-scale EEG database for three BCI paradigms*, GigaScience (2019)](https://doi.org/10.1093/gigascience/giz002)
