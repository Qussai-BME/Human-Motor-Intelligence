# Lite-DAN: Cross-Subject sEMG Domain Adaptation (Protocol v1.1)

Code and results for:

> Q. Adlbi and M. A. Darwich, "Adversarial Domain Confusion and Feature-Covariance Alignment Do Not Close the Cross-Subject Generalization Gap in Surface EMG Gesture Recognition: A Systematic Zero-Calibration LOSO Study Across Three NinaPro Cohorts," submitted for publication, 2026.

This repository accompanies a systematic, zero-calibration leave-one-subject-out (LOSO) evaluation of adversarial domain adaptation (a lightweight domain-adversarial neural network, "Lite-DAN") and covariance-alignment domain adaptation (CORAL) for surface EMG (sEMG) gesture recognition, compared against classical baselines (LDA, Random Forest, XGBoost), across three NinaPro cohorts: DB2 (40 intact-limbed subjects), DB3 (11 trans-radial amputees), and DB7 (22 mixed intact/amputee subjects).

It is the direct successor to [MiniROCKET-sEMG-CrossSubject-DomainAdaptation](https://github.com/Qussai-BME/MiniROCKET-sEMG-CrossSubject-DomainAdaptation), which tested classical (non-adversarial) domain adaptation methods on a different feature representation.

## Headline results

27 experiments (9 modeling conditions x 3 cohorts), 657 individual LOSO model fits. Full numbers are in the paper's Table 2 and reproduced exactly in [`results_v1_1/*/aggregate/summary.csv`](results_v1_1/).

- Disabling the adversarial signal in Lite-DAN (no-GRL) matched or significantly outperformed the full adversarial model on every cohort, and trained several times faster than the XGBoost-family baselines it matched or exceeded.
- Multi-source, zero-target-information CORAL alignment significantly *degraded* accuracy on the mixed cohort (DB7), converging with an independent finding from the predecessor study on a different feature representation.
- Classical linear/tree models significantly outperformed Lite-DAN on the small amputee cohort (DB3), despite a fold-by-fold training-loss audit finding no evidence of an optimization failure.
- Which individual subjects are hardest to classify is highly consistent across all nine modeling approaches (mean pairwise Spearman r = 0.65-0.80), consistent with a strongly subject-dependent component of cross-subject variance.

## Repository structure

```
configs/            Protocol configuration (feature schema, model hyperparameters, LOSO settings)
src/litedan_p3/      Package: data loading, feature extraction, models, evaluation pipeline, CLI
scripts/             Data provisioning, feature-cache auditing, and experiment-registry tooling
registry_v1_1/       Experiment tracking: plan, per-fold registry, status log
results_v1_1/        Per-fold results (657 fold_S##.json files), aggregated summaries, confusion matrices
tests/               Unit tests for the experiment registry
docs/                Data provenance notes
```

Raw NinaPro archives and the extracted per-subject feature caches (`artifacts_v1_1/features/`, `.npz`, several GB) are **not included** in this repository due to size and NinaPro's redistribution terms. See [Reproducing this study](#reproducing-this-study) below for how to regenerate them.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Everything runs on CPU; no GPU is required or used.

## Reproducing this study

1. **Obtain NinaPro data.** Register and download DB2, DB3, and DB7 from the [official NinaPro site](https://ninapro.hevs.ch/). `scripts/staged_prepare_ninapro.py` (with `scripts/chunked_official_download_v1_1.py` / `scripts/segmented_official_download.py` as transport helpers for unreliable connections) downloads, validates, and caches each subject's features under `artifacts_v1_1/features/<DB>/`.

2. **Validate the feature caches.**
   ```bash
   python -m litedan_p3.cli validate-data --db DB2 --config configs/protocol_v1_1.yaml
   ```

3. **Run a LOSO experiment** (one dataset x condition at a time; conditions are `lda`, `random_forest`, `xgb`, `coral_xgb`, `litedan`, `litedan_fixed_0p1`, `litedan_fixed_0p5`, `litedan_fixed_1p0`, `litedan_no_grl`):
   ```bash
   export PYTHONPATH=src   # Windows: $env:PYTHONPATH = "src"
   python -m litedan_p3.cli run-loso --db DB2 --condition litedan_no_grl --config configs/protocol_v1_1.yaml
   ```
   Runs resume automatically from any completed per-subject folds under `results_v1_1/<DB>/<condition>/`.

4. **Sync the experiment registry** after each run:
   ```bash
   python scripts/experiment_registry_v1_1.py --config configs/protocol_v1_1.yaml --artifact-root artifacts_v1_1 --results-root results_v1_1 --registry-root registry_v1_1 sync
   ```

5. **Aggregate results:**
   ```bash
   python -m litedan_p3.cli aggregate --db DB2 --results-root results_v1_1
   ```

`activate_env.ps1` and `sync.ps1` wrap steps used repeatedly on Windows during this study.

## Method summary

- **Features:** 618-dimensional hybrid time-domain / autoregressive / histogram / Hjorth / frequency descriptors per window (46 features x 12 channels, plus 66 inter-channel correlations), reduced to 308 by a leakage-safe, per-LOSO-fold ANOVA F-test selector.
- **Protocol:** strict zero-calibration LOSO — the held-out subject contributes no data to feature selection, alignment, or model fitting at any stage.
- **Models:** LDA, Random Forest, XGBoost, a zero-target-information multi-source CORAL variant applied to XGBoost, and Lite-DAN (a ~52.5-53.4K-parameter domain-adversarial network) in five gradient-reversal-layer (GRL) configurations: gradual schedule, three fixed-lambda schedules, and a no-GRL ablation.
- **Statistics:** paired Wilcoxon signed-rank tests, Benjamini-Hochberg FDR correction across a single 12-comparison family (6 primary pre-specified, 6 bounded exploratory), rank-biserial correlation and Cohen's dz effect sizes.

Full methodological detail is in the paper (Section 3); `configs/protocol_v1_1.yaml` is the single source of truth for every numeric setting.

## Citation

If you use this code or these results, please cite the paper above. A citable archive of this exact repository state is available via Zenodo: **[DOI to be added after archival]**.

## License

Code is released under the MIT License (see [LICENSE](LICENSE)). NinaPro data is subject to its own terms at [ninapro.hevs.ch](https://ninapro.hevs.ch/); this repository contains no NinaPro data.

## Notes on this repository

Portions of this project's code, data-pipeline engineering, and analysis were developed with the assistance of AI coding tools, under the direction and review of the authors, who verified the experimental results reported here and in the accompanying paper. We note this for transparency; see [`docs/DATA_PROVENANCE.md`](docs/DATA_PROVENANCE.md) for the data-integrity checks performed on the released results.
