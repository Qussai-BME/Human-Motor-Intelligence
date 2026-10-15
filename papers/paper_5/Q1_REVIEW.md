# P5 Q1 Review — V2 Recovery R3

## Disposition

**Overall: GREEN for a transparently amended external-validation manuscript; YELLOW for general fusion claims.**

| Dimension | Status | Basis |
|---|---|---|
| Source and availability audit | GREEN | The `sub-23` limitation was independently checked and documented before amendment/extraction. |
| Cohort amendment | GREEN | 24-subject list, all 11 MI labels, and cap rule were prospectively locked. |
| LOSO/no-calibration safety | GREEN | D5 records held-out exclusion from both scalers and all classifiers. |
| Reproducibility | GREEN | Primary/rerun 96-row CSVs are byte-identical. |
| Statistics | GREEN | Subject inference, six predeclared contrasts, Holm family, bootstrap, and Friedman are recorded. |
| Fusion-over-EEG claim | YELLOW | No early/late fusion contrast survives Holm against EEG-only. |
| EMG interpretation | RED | No physiological mechanism, microactivation assay, or execution evidence exists. |
| Cross-source fusion conclusion | RED | Cho2017 and Jeong differ in source, task, labels, pipeline, and cohort. |

## Reviewer-Facing Determination

The manuscript is ready for review if it calls the analysis an **amended 24-subject external MI-only validation** and states that the transparent fusion rules did not establish a Holm-supported gain over EEG-only. The reported EEG/early/late versus EMG-only comparisons are permitted only inside this fixed Jeong/LDA protocol. The paper must cite contrasting fusion literature as methodological context, not as a conflict resolvable by raw metric comparison.

## Required Submission Checks

Include the second-source record, both protocol amendments, D1–D5 validation, exact rerun checksum, `APPENDIX.md`, and raw-data exclusion note. Do not add deep fusion, target adaptation, or selected labels as a “revision” of this completed study.
