# P5 Appendix — V2 Recovery R3 Q1 Standard

## A. Scope and Evidence Boundary

P5 is a 24-subject amended external MI-only validation. It is not a direct replication of frozen Cho2017 and no score may be pooled across sources.

This appendix is rendered from the locked primary artefacts. It does not rerun a model, modify a cohort, or calculate a new result. The primary and independent rerun are separate reproducibility executions, not pooled evidence.

## B. Protocol, Validation, and Reproducibility Record

| Gate | Status | Failure count | Failure detail |
|---|---|---|---|
| D1_file_integrity | pass | 0 | — |
| D2_schema | pass | 0 | — |
| D3_labels | pass | 0 | — |
| D4_protocol | pass | 0 | — |
| D5_leakage_audit | pass | 0 | — |

| Artefact | Primary location | Rerun / check |
|---|---|---|
| Protocol | `protocol.json` | Protocol ID: `nemar-nm000311-jeong-p5-external-loso-24subject-r2` |
| Manifest | `manifest.json` | Manifest ID: `nemar-nm000311-jeong-p5-v2-recovery-r2` |
| Environment | `environment.json` | Captured with primary execution |
| Results | `subject_level_results.csv` | 96 observations; rerun at `results/real/v2-recovery-r2-independent-rerun/nemar-nm000311-jeong-p5-external-loso-24subject-r2` |
| Statistics | `statistics_macro_f1.json` | subject is the inference unit |

## C. Full Subject-Level Result Table

| Subject | Condition | Fold | Seed | Macro-F1 | Accuracy | Balanced accuracy |
|---|---|---|---|---|---|---|
| sub-1 | EEG-only LDA | 0 | 20260824 | 0.099042 | 0.156364 | 0.156364 |
| sub-1 | EMG-only LDA | 0 | 20260825 | 0.114339 | 0.163636 | 0.163636 |
| sub-1 | Early-fusion LDA | 0 | 20260826 | 0.111778 | 0.130909 | 0.130909 |
| sub-1 | Late-fusion LDA | 0 | 20260827 | 0.105693 | 0.136364 | 0.136364 |
| sub-2 | EEG-only LDA | 1 | 20260925 | 0.068365 | 0.103636 | 0.103636 |
| sub-2 | EMG-only LDA | 1 | 20260926 | 0.038706 | 0.063636 | 0.063636 |
| sub-2 | Early-fusion LDA | 1 | 20260927 | 0.067884 | 0.094545 | 0.094545 |
| sub-2 | Late-fusion LDA | 1 | 20260928 | 0.059244 | 0.094545 | 0.094545 |
| sub-3 | EEG-only LDA | 2 | 20261026 | 0.095329 | 0.141818 | 0.141818 |
| sub-3 | EMG-only LDA | 2 | 20261027 | 0.077282 | 0.136364 | 0.136364 |
| sub-3 | Early-fusion LDA | 2 | 20261028 | 0.125983 | 0.165455 | 0.165455 |
| sub-3 | Late-fusion LDA | 2 | 20261029 | 0.096863 | 0.147273 | 0.147273 |
| sub-4 | EEG-only LDA | 3 | 20261127 | 0.081250 | 0.103636 | 0.103636 |
| sub-4 | EMG-only LDA | 3 | 20261128 | 0.030905 | 0.069091 | 0.069091 |
| sub-4 | Early-fusion LDA | 3 | 20261129 | 0.098941 | 0.118182 | 0.118182 |
| sub-4 | Late-fusion LDA | 3 | 20261130 | 0.075864 | 0.105455 | 0.105455 |
| sub-5 | EEG-only LDA | 4 | 20261228 | 0.080214 | 0.105455 | 0.105455 |
| sub-5 | EMG-only LDA | 4 | 20261229 | 0.046439 | 0.105455 | 0.105455 |
| sub-5 | Early-fusion LDA | 4 | 20261230 | 0.087567 | 0.125455 | 0.125455 |
| sub-5 | Late-fusion LDA | 4 | 20261231 | 0.072511 | 0.105455 | 0.105455 |
| sub-6 | EEG-only LDA | 5 | 20261329 | 0.052820 | 0.107273 | 0.107273 |
| sub-6 | EMG-only LDA | 5 | 20261330 | 0.043681 | 0.101818 | 0.101818 |
| sub-6 | Early-fusion LDA | 5 | 20261331 | 0.050096 | 0.105455 | 0.105455 |
| sub-6 | Late-fusion LDA | 5 | 20261332 | 0.051800 | 0.100000 | 0.100000 |
| sub-7 | EEG-only LDA | 6 | 20261430 | 0.098958 | 0.130909 | 0.130909 |
| sub-7 | EMG-only LDA | 6 | 20261431 | 0.060573 | 0.125455 | 0.125455 |
| sub-7 | Early-fusion LDA | 6 | 20261432 | 0.032621 | 0.100000 | 0.100000 |
| sub-7 | Late-fusion LDA | 6 | 20261433 | 0.079515 | 0.134545 | 0.134545 |
| sub-8 | EEG-only LDA | 7 | 20261531 | 0.105269 | 0.160000 | 0.160000 |
| sub-8 | EMG-only LDA | 7 | 20261532 | 0.016170 | 0.074545 | 0.074545 |
| sub-8 | Early-fusion LDA | 7 | 20261533 | 0.052567 | 0.110909 | 0.110909 |
| sub-8 | Late-fusion LDA | 7 | 20261534 | 0.070775 | 0.118182 | 0.118182 |
| sub-9 | EEG-only LDA | 8 | 20261632 | 0.061674 | 0.067273 | 0.067273 |
| sub-9 | EMG-only LDA | 8 | 20261633 | 0.002009 | 0.003636 | 0.003636 |
| sub-9 | Early-fusion LDA | 8 | 20261634 | 0.003418 | 0.005455 | 0.005455 |
| sub-9 | Late-fusion LDA | 8 | 20261635 | 0.028783 | 0.029091 | 0.029091 |
| sub-10 | EEG-only LDA | 9 | 20261733 | 0.097026 | 0.118182 | 0.118182 |
| sub-10 | EMG-only LDA | 9 | 20261734 | 0.040093 | 0.087273 | 0.087273 |
| sub-10 | Early-fusion LDA | 9 | 20261735 | 0.116846 | 0.149091 | 0.149091 |
| sub-10 | Late-fusion LDA | 9 | 20261736 | 0.119285 | 0.138182 | 0.138182 |
| sub-11 | EEG-only LDA | 10 | 20261834 | 0.063283 | 0.150909 | 0.150909 |
| sub-11 | EMG-only LDA | 10 | 20261835 | 0.034052 | 0.094545 | 0.094545 |
| sub-11 | Early-fusion LDA | 10 | 20261836 | 0.064633 | 0.132727 | 0.132727 |
| sub-11 | Late-fusion LDA | 10 | 20261837 | 0.050552 | 0.132727 | 0.132727 |
| sub-12 | EEG-only LDA | 11 | 20261935 | 0.132815 | 0.156364 | 0.156364 |
| sub-12 | EMG-only LDA | 11 | 20261936 | 0.039923 | 0.100000 | 0.100000 |
| sub-12 | Early-fusion LDA | 11 | 20261937 | 0.142012 | 0.169091 | 0.169091 |
| sub-12 | Late-fusion LDA | 11 | 20261938 | 0.132381 | 0.149091 | 0.149091 |
| sub-13 | EEG-only LDA | 12 | 20262036 | 0.078405 | 0.100000 | 0.100000 |
| sub-13 | EMG-only LDA | 12 | 20262037 | 0.034332 | 0.103636 | 0.103636 |
| sub-13 | Early-fusion LDA | 12 | 20262038 | 0.080191 | 0.114545 | 0.114545 |
| sub-13 | Late-fusion LDA | 12 | 20262039 | 0.079319 | 0.105455 | 0.105455 |
| sub-14 | EEG-only LDA | 13 | 20262137 | 0.067132 | 0.085455 | 0.085455 |
| sub-14 | EMG-only LDA | 13 | 20262138 | 0.055086 | 0.103636 | 0.103636 |
| sub-14 | Early-fusion LDA | 13 | 20262139 | 0.051696 | 0.092727 | 0.092727 |
| sub-14 | Late-fusion LDA | 13 | 20262140 | 0.067713 | 0.101818 | 0.101818 |
| sub-15 | EEG-only LDA | 14 | 20262238 | 0.065967 | 0.090909 | 0.090909 |
| sub-15 | EMG-only LDA | 14 | 20262239 | 0.012636 | 0.020000 | 0.020000 |
| sub-15 | Early-fusion LDA | 14 | 20262240 | 0.048564 | 0.089091 | 0.089091 |
| sub-15 | Late-fusion LDA | 14 | 20262241 | 0.064005 | 0.087273 | 0.087273 |
| sub-16 | EEG-only LDA | 15 | 20262339 | 0.056509 | 0.087273 | 0.087273 |
| sub-16 | EMG-only LDA | 15 | 20262340 | 0.067422 | 0.120000 | 0.120000 |
| sub-16 | Early-fusion LDA | 15 | 20262341 | 0.063378 | 0.114545 | 0.114545 |
| sub-16 | Late-fusion LDA | 15 | 20262342 | 0.067037 | 0.100000 | 0.100000 |
| sub-17 | EEG-only LDA | 16 | 20262440 | 0.062794 | 0.103636 | 0.103636 |
| sub-17 | EMG-only LDA | 16 | 20262441 | 0.057572 | 0.085455 | 0.085455 |
| sub-17 | Early-fusion LDA | 16 | 20262442 | 0.077733 | 0.098182 | 0.098182 |
| sub-17 | Late-fusion LDA | 16 | 20262443 | 0.068359 | 0.100000 | 0.100000 |
| sub-18 | EEG-only LDA | 17 | 20262541 | 0.102119 | 0.112727 | 0.112727 |
| sub-18 | EMG-only LDA | 17 | 20262542 | 0.083357 | 0.116364 | 0.116364 |
| sub-18 | Early-fusion LDA | 17 | 20262543 | 0.088507 | 0.120000 | 0.120000 |
| sub-18 | Late-fusion LDA | 17 | 20262544 | 0.101693 | 0.114545 | 0.114545 |
| sub-19 | EEG-only LDA | 18 | 20262642 | 0.143579 | 0.176364 | 0.176364 |
| sub-19 | EMG-only LDA | 18 | 20262643 | 0.025773 | 0.065455 | 0.065455 |
| sub-19 | Early-fusion LDA | 18 | 20262644 | 0.113609 | 0.120000 | 0.120000 |
| sub-19 | Late-fusion LDA | 18 | 20262645 | 0.168930 | 0.189091 | 0.189091 |
| sub-20 | EEG-only LDA | 19 | 20262743 | 0.054593 | 0.085455 | 0.085455 |
| sub-20 | EMG-only LDA | 19 | 20262744 | 0.053905 | 0.129091 | 0.129091 |
| sub-20 | Early-fusion LDA | 19 | 20262745 | 0.068953 | 0.125455 | 0.125455 |
| sub-20 | Late-fusion LDA | 19 | 20262746 | 0.064215 | 0.092727 | 0.092727 |
| sub-21 | EEG-only LDA | 20 | 20262844 | 0.068490 | 0.112727 | 0.112727 |
| sub-21 | EMG-only LDA | 20 | 20262845 | 0.078040 | 0.123636 | 0.123636 |
| sub-21 | Early-fusion LDA | 20 | 20262846 | 0.041295 | 0.090909 | 0.090909 |
| sub-21 | Late-fusion LDA | 20 | 20262847 | 0.066845 | 0.103636 | 0.103636 |
| sub-22 | EEG-only LDA | 21 | 20262945 | 0.046983 | 0.056364 | 0.056364 |
| sub-22 | EMG-only LDA | 21 | 20262946 | 0.079647 | 0.110909 | 0.110909 |
| sub-22 | Early-fusion LDA | 21 | 20262947 | 0.051309 | 0.076364 | 0.076364 |
| sub-22 | Late-fusion LDA | 21 | 20262948 | 0.048932 | 0.061818 | 0.061818 |
| sub-24 | EEG-only LDA | 22 | 20263046 | 0.104028 | 0.129091 | 0.129091 |
| sub-24 | EMG-only LDA | 22 | 20263047 | 0.032585 | 0.101818 | 0.101818 |
| sub-24 | Early-fusion LDA | 22 | 20263048 | 0.121275 | 0.180000 | 0.180000 |
| sub-24 | Late-fusion LDA | 22 | 20263049 | 0.125984 | 0.165455 | 0.165455 |
| sub-25 | EEG-only LDA | 23 | 20263147 | 0.063833 | 0.100000 | 0.100000 |
| sub-25 | EMG-only LDA | 23 | 20263148 | 0.037966 | 0.083636 | 0.083636 |
| sub-25 | Early-fusion LDA | 23 | 20263149 | 0.048909 | 0.090909 | 0.090909 |
| sub-25 | Late-fusion LDA | 23 | 20263150 | 0.066096 | 0.092727 | 0.092727 |

## D. Descriptive and Pairwise Statistical Tables

| Condition A | Condition B | Wilcoxon W | Raw p | Holm p | Holm rank | Paired-sign effect |
|---|---|---|---|---|---|---|
| Early-fusion LDA | EEG-only LDA | 135.0 | 0.68398643 | 1.00000000 | 5 | 0.083333 |
| Early-fusion LDA | EMG-only LDA | 46.0 | 0.00200093 | 0.00800371 | 3 | 0.500000 |
| Early-fusion LDA | Late-fusion LDA | 117.0 | 0.35962629 | 1.00000000 | 4 | -0.083333 |
| EEG-only LDA | EMG-only LDA | 29.0 | 0.00020516 | 0.00102580 | 2 | 0.666667 |
| EEG-only LDA | Late-fusion LDA | 148.0 | 0.96644723 | 1.00000000 | 6 | 0.000000 |
| EMG-only LDA | Late-fusion LDA | 26.0 | 0.00012708 | 0.00076246 | 1 | -0.666667 |

Friedman omnibus: χ²=22.7390, df=4, p=0.0001428.

## E. Figures and Confusion-Matrix Availability

![Subject-level macro-F1 figure](../../results/real/v2-recovery-r2/nemar-nm000311-jeong-p5-external-loso-24subject-r2/p5_jeong_subject_level_macro_f1.png)

Prediction-level true/predicted label arrays were not retained in the locked public result artefacts. Consequently, no post hoc confusion matrix is generated in this appendix. Recomputing predictions after lock would be a new computation and is not authorized for this integration step. The subject-level outcomes, validation, and statistics above are the complete retained primary evidence.

## F. Final Hardening Supplement — Conditional Robustness

The final analysis reused strict R3 clean-train/corrupted-test outputs and retained only 0% clean and 20% EEG feature-group zeroing for the prespecified final comparison. EEG-only, static-mean fusion, and confidence-selective fusion were compared after clean training. Mean macro-F1 values were 0.081397 to 0.017279 for EEG-only, 0.080506 to 0.017154 for static fusion, and 0.081174 to 0.017279 for confidence-selective fusion. Mean drops were 0.064118, 0.063352, and 0.063895, respectively; mean relative retentions were 0.2290, 0.2417, and 0.2357. Static fusion versus EEG-only at 20% degradation had mean difference -0.000125 for static fusion relative to EEG-only, *p*=0.715, effect size -0.180. Confidence-selective fusion matched EEG-only at degraded testing.

The machine-readable source is `results/extensions/v2-final-q1-hardening-r3-001/final_hardening_statistics.json`. This intervention is feature-cache zeroing and is not physical electrode failure, clinical hardware degradation, or physiological robustness evidence. Relative retention is descriptive, not a confirmatory endpoint.

## G. Calibration and Missing-Modality Supplement

Calibration values were: EEG-only Brier/ECE 0.944344/0.100162; static fusion 0.919149/0.044729; confidence-weighted fusion 0.938161/0.085202; confidence-selective fusion 0.948498/0.106809. Confidence–correctness associations were near zero for fusion conditions. Existing missing-modality outputs are retained as explicit EEG-only/EMG-only graceful-degradation states and are not presented as the primary scientific novelty.
