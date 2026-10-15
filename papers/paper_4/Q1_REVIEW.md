# P4 Q1 Review — V2 Recovery R3

## Disposition

**Overall: GREEN for an external-validation manuscript with explicit scope limits.**

| Dimension | Status | Basis |
|---|---|---|
| Dataset provenance and license | GREEN | NEMAR/OpenBMI version, source DOI, GPL-3.0 record, receipts, and manifest are retained. |
| Subject-held-out design | GREEN | 54-subject LOSO; target subject excluded from fit/selection/calibration. |
| Data integrity and leakage | GREEN | D1–D5 all pass; raw-data boundary audited. |
| Reproducibility | GREEN | Independent 270-row rerun is byte-identical. |
| Statistics | GREEN | Subject is inference unit; bootstrap, Friedman, Wilcoxon, and Holm are explicit. |
| Model-superiority claim | YELLOW | Omnibus test is non-null, but no pairwise contrast survives Holm. |
| External generalization | YELLOW | One independent OpenBMI cohort supports protocol-qualified validation only. |
| Clinical/real-world applicability | RED | Healthy binary MI cohort; no patient, online, or device-control outcome. |

## Reviewer-Facing Determination

The manuscript is ready for Q1-level review if it retains the terms **external validation**, **zero calibration**, and **no Holm-surviving pairwise superiority**. It should not describe the compact CNN as a confirmed winner, call the study a replication of BCI IV-2a, or compare raw scores across datasets. The Related Work section correctly distinguishes methods with target-data, subject selection, alternative modalities, or differing architectures.

## Required Submission Checks

The manuscript submission package should include `APPENDIX.md`, the P4 R1 result/statistics/validation files, the exact rerun evidence, source links, and raw-data exclusion note. Any future claim about a different patient population, session, class structure, or adaptation scheme requires a new study rather than a revision of this result.
