# Human Motor Intelligence — Public Reproduction Release
## P4 and P5 Evidence Package Only

> **Public-release status:** This package is designed for public upload as a **P4/P5 code-and-evidence release**. It excludes P6 experimental material, P3 unpublished material, all raw biosignal recordings, and all derived feature caches. It is research software and evidence documentation—not a medical device, clinical decision system, or general claim of decoder robustness.

## What the Public Archive Contains

| Component | Included | Purpose |
|---|---:|---|
| Research-core source code | Yes | Versioned contracts, validation, registry, and the P4/P5 experiment implementations |
| P4/P5 runners, analyzers, and plotting scripts | Yes | Code used for the recorded external-validation workflows |
| P4/P5 frozen configurations and manifests | Yes | Protocol, provenance, cohort, and source records |
| P4/P5 primary and independent-rerun result artefacts | Yes | Subject-level CSVs, statistics, figures, environments, protocol and validation records |
| P4/P5 manuscript summaries (abstract + highlights) | Yes | Full manuscript text withheld pending peer-review submission |
| Tests and dependency specification | Yes | Public reproduction and software-verification guidance |
| Raw BDF/MAT/BrainVision recordings | No | Download only from the authoritative source records |
| Derived NPZ feature cache | No | Excluded to avoid raw/derived participant data redistribution and archive bloat |
| P6 manuscript, code patch, data/results, fixture, or audit | No | Deliberately excluded from this P4/P5 public release |
| P3 material | No | Pending author-supplied original package |

## Evidence Scope

P4 is a **54-subject harmonized external validation** on OpenBMI binary motor imagery. It is not a direct replication or numerical ranking against BCI Competition IV-2a. P5 is a **24-subject amended external validation** on the Jeong MI-only cohort; it evaluates four predeclared transparent LDA conditions and does not establish a general claim about multimodal fusion. The complete boundaries and statistical interpretations are contained in the included manuscripts and audits.[1] [2]

## Recorded Environment and Installation

The primary P4/P5 executions recorded Python 3.12.3 with NumPy 1.26.4, SciPy 1.14.1, scikit-learn 1.9.0, and MNE 1.12.1. P4 additionally recorded PyTorch 2.13.0+cu130. The public requirements file records these evidence-grounded constraints. Use a virtual environment and select a PyTorch wheel appropriate for the host when reproducing P4.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
PYTHONPATH=src pytest -q
```

The source suite is expected to pass 28 tests in the documented current state. The public archive contains a verification record rather than promising bit-identical reruns on a different operating system or accelerator stack.

## Reproducing P4 and P5 with Authoritative Data

The archive deliberately contains **code and retained result artefacts, not source recordings**. Download data yourself from the cited authoritative records, preserve the source receipt/checksum/version, and comply with the current source terms before executing. P4 records the NEMAR OpenBMI v1.0.5 source (`10.82901/nemar.nm000338`), whose current dataset page identifies GPL-3.0. P5 records NEMAR Jeong v1.0.2 (`10.82901/nemar.nm000311`), whose current page identifies CC0-1.0.[3] [4]

The historic R1/R2 configurations preserve absolute project-workspace paths to protect the original evidence record. **Do not edit those frozen configurations in place.** For an independent rerun, copy the corresponding configuration to a newly named local experiment configuration, change only the local raw/cache roots and output namespace, record that change prospectively, and retain a new manifest. The historic stage commands are:

```bash
# P4: extract, manifest, primary run, then independent rerun
PYTHONPATH=src python scripts/run_v2_external_validation.py extract-p4
PYTHONPATH=src python scripts/run_v2_external_validation.py manifest-p4
PYTHONPATH=src python scripts/run_v2_external_validation.py run-p4
PYTHONPATH=src python scripts/run_v2_external_validation.py rerun-p4

# P5: extract, manifest, primary run, then independent rerun
PYTHONPATH=src python scripts/run_v2_p5_jeong_r2.py extract-p5-r2
PYTHONPATH=src python scripts/run_v2_p5_jeong_r2.py manifest-p5-r2
PYTHONPATH=src python scripts/run_v2_p5_jeong_r2.py run-p5-r2
PYTHONPATH=src python scripts/run_v2_p5_jeong_r2.py rerun-p5-r2
```

The public package contains the recorded output hashes so an independent rerun may be compared to, but never overwrite, the retained result namespaces.

## Publication and Attribution Rules

The source code in this public archive is distributed under Apache-2.0 as declared in `LICENSE`. This does **not** relicence external datasets, publications, data conversion tools, or unbundled child projects. Cite the NEMAR dataset DOI and the source publication for each dataset, cite this programme release using `CITATION.cff`, and preserve the P4/P5 external-validation framing. Do not redistribute source recordings simply because this archive references them; obtain and follow the authoritative source terms at the time of download.[3] [4]

## References

[1]: papers/P4_SUMMARY.md "P4 Summary"
[2]: papers/P5_SUMMARY.md "P5 Summary"
[3]: https://nemar.org/dataset/nm000338 "NEMAR nm000338 — OpenBMI"
[4]: https://nemar.org/dataset/nm000311 "NEMAR nm000311 — Jeong2020"

The public release boundary follows the retained P4/P5 evidence documents and the source dataset records.[1] [2] [3] [4]
