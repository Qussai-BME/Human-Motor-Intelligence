# Data, Licences, and Reuse Boundary

## Human Motor Intelligence code

The umbrella code is distributed under Apache-2.0 as specified by `LICENSE` and `pyproject.toml`.

## PhysioNet EEGMMIDB

P6 (C1 and C2) uses the public PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0 as an **external input** (C1: run R04, S001–S020; C2: runs R04, R08, R12, 105 subjects after an integrity check). This release does not redistribute the raw EDF recordings. The authoritative dataset page and DOI are recorded in the P6 manifests and protocol files.

Dataset reference: https://physionet.org/content/eegmmidb/1.0.0/  
DOI: 10.13026/C28G6P

Before reuse, obtain the dataset directly from the authoritative source and follow its current attribution/licensing terms.

## External MyoSim runtime

P6 simulator execution depends on an external MyoSim checkout. The release scripts require `--myosim-root`; they do not embed a developer workstation path. MyoSim licensing and version compatibility remain governed by that separate project.

## C2 derived artefacts

`p6/c2_episode` redistributes only derived artefacts: decoder feature/prediction caches (`WP5_*.npz`), replay CSVs and run JSONs (compressed archives with SHA-256 in `p6/c2_episode/raw_archives/`), per-episode result tables, and source-file hashes (`registry/EEGMMIDB_MANIFEST.csv`, relative paths). No raw EDF recordings are included. Obtain the dataset from PhysioNet and follow its attribution terms; the derived feature caches are not a substitute for the source data.

## What is not included

No raw EEG recordings, private model checkpoints, or hidden workstation-specific datasets are distributed by this release.
