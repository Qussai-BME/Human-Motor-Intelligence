# P4 — Strict Zero-Calibration Cross-Subject EEG Motor-Imagery Decoding

**Authors:** Qussai Adlbi¹,²
¹ Al-Andalus University for Medical Sciences, Syria — ² Pázmány Péter Catholic University, Budapest, Hungary

**Status:** Manuscript prepared for peer-reviewed journal submission. Full text withheld pending journal decision; code, configuration, and result artefacts for this study are provided in this repository for reproducibility.

## Abstract (summary)
An external validation of five zero-calibration EEG motor-imagery decoders on 54 independent OpenBMI subjects (NEMAR nm000338), using a strict leave-one-subject-out protocol. Every statistic (Friedman, Holm-corrected Wilcoxon, bootstrap CIs, standardized effect sizes) was independently reproduced via a byte-identical rerun with SHA-256-verified artefacts. The study explicitly separates external validation from replication and reports an exploratory representation audit (temporal vs. spectral features).

## Highlights
- 54-subject harmonized external validation, zero-calibration, strict LOSO
- Fully reproduced statistics with independent, byte-identical rerun
- Post hoc sensitivity/power analysis within the predeclared comparison scope
- Explicit external-validation framing (not a BCI-IV-2a replication)

Reproducibility code, frozen configs, and result artefacts: see `src/research_core/`, `configs/`, and `results/real/v2-recovery-r1*`.
