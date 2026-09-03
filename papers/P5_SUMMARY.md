# P5 — Transparent Cross-Subject EEG–EMG Fusion in Motor Imagery

**Authors:** Qussai Adlbi¹,²
¹ Al-Andalus University for Medical Sciences, Syria — ² Pázmány Péter Catholic University, Budapest, Hungary

**Status:** Manuscript prepared for peer-reviewed journal submission. Full text withheld pending journal decision; code, configuration, and result artefacts for this study are provided in this repository for reproducibility.

## Abstract (summary)
An amended 24-subject external validation on the Jeong2020 synchronized EEG–EMG cohort (NEMAR nm000311), evaluating four predeclared transparent LDA pipelines (EEG-only, EMG-only, early fusion, late fusion). EEG-only, early fusion, and late fusion each exceed EMG-only after Holm correction, but no fusion variant establishes a Holm-supported improvement over EEG-only in this cohort.

## Highlights
- Four fixed, transparent LDA conditions on an amended MI-only cohort
- Fusion did not establish a Holm-supported gain over EEG-only
- Sensitivity/power analysis confirms well-powered EMG-only contrasts
- Exploratory robustness check under graded feature dropout

Reproducibility code, frozen configs, and result artefacts: see `src/research_core/`, `configs/`, and `results/real/v2-recovery-r2*`.
