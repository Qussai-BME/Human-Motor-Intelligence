# Data Provenance and Integrity Checks

## Source

All sEMG data used in this study come from the public [NinaPro](https://ninapro.hevs.ch/) repository: DB2, DB3, and DB7. Archives were downloaded directly from the official NinaPro hosting (`https://ninapro.hevs.ch/files/...`), verified against the advertised byte count and a SHA-256 checksum of each downloaded archive, and extracted only after that verification passed. Raw archives and extracted feature caches are not redistributed in this repository (see `.gitignore`); they must be regenerated locally with `scripts/staged_prepare_ninapro.py`.

The official host serves large archives slowly and occasionally unreliably. `scripts/segmented_official_download.py` and `scripts/chunked_official_download_v1_1.py` implement retry-hardened, ranged HTTP transport for exactly this situation. Neither script changes the archive URL, the advertised byte count, ZIP validation, or any downstream feature-extraction or modeling step — they only make the download itself more robust to a slow or interrupted connection. Feature construction was run at 6 parallel workers per subject with native BLAS threading pinned to 1 thread per worker, which was the fastest setting that consistently produced a validated cache; one subject archive was processed at a time when the connection was unstable.

## Per-subject label coverage

A formal audit (`scripts/audit_feature_caches_v1_1.py`, results in `results_v1_1/audits/feature_cache_audit_v1_1.json`) enumerated which of the 41 class labels (40 gestures + rest) were actually present in each subject's cached windows, for all three cohorts. Every DB2 subject has complete 41-class coverage. Two subjects have partial coverage:

- **DB3, subject S01** is missing 11 of the 40 gesture classes (label indices 30-40).
- **DB7, subject S21** is missing 2 gesture classes. This matches the official NinaPro DB7 documentation, which states that Subject 21 did not perform the final two functional movements of Exercise 2.

Both subjects were retained in the LOSO evaluation reported in the paper; all metrics are computed only over each held-out subject's observed labels, so no fabricated or imputed labels are used anywhere in the pipeline. This is disclosed in the paper's Methods section (3.2).

## Feature-cache integrity

Each subject's cached feature file is paired with a metadata sidecar recording the source archive's byte count and SHA-256, the feature-extraction schema version (`current_618_v1`), and a cache-input hash (a hash of the data root, dataset entry, protocol, and feature configuration — see `cache_input_hash` in `src/litedan_p3/config.py`) that must match the current configuration before a fold will use the cache. Per-dataset manifests aggregate these into a single manifest-level SHA-256. This is what `validate-data` and `run-loso` check automatically before any model is fit; a fingerprint mismatch raises an error rather than silently using stale or incompatible features.

## Results-to-paper consistency

Every accuracy and macro-F1 value in the paper's Table 2 was cross-checked programmatically against `results_v1_1/<DB>/aggregate/summary.csv` in this repository (27/27 conditions, exact match to the precision reported). The full per-fold evidence behind every aggregate number is the corresponding `results_v1_1/<DB>/<condition>/fold_S##.json` file.
