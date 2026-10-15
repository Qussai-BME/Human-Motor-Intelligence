# Public-Release Audit — P4/P5 Only
## V2 Recovery R3 Public Package Decision Record

> **Decision:** **CONDITIONALLY APPROVED FOR PUBLIC REPOSITORY UPLOAD** as a P4/P5-only research code-and-evidence archive, provided the publisher confirms that they hold authority to release the programme-owned code under Apache-2.0 and preserves the included attribution/data notice. The package must not be represented as a clinical, general-purpose, or P6 decoder-quality release.

## Completeness Assessment

| Surface | Public-package status | Verification basis |
|---|---|---|
| P4 implementation | Included | Experiment module, runner, analyzer, plotter, fixed config, manifest, primary result, and independent rerun |
| P5 implementation | Included | Experiment module, runner, analyzer, plotter, amended-cohort config, manifest, primary result, and independent rerun |
| Research-core imports | Included | `src/research_core/` is included with `pyproject.toml`; public requirements record observed P4/P5 dependencies |
| Result artefacts | Included | Subject-level CSVs, statistics, D1–D5 validation, protocols, environments, figures, and exact rerun artefacts |
| Manuscripts | Included | P4/P5 Markdown, appendix, review, evidence-gap audit, and standalone DOCX |
| Raw source recordings | Excluded by design | P4/P5 raw data must be acquired from authoritative sources; no BDF/MAT/BrainVision recordings are redistributed |
| Derived participant cache | Excluded by design | No NPZ cache is published |
| P6 | Excluded by package rule | No P6 paper, fixture, patch, result, audit, state-run record, or decoder-quality claim appears in the public archive |
| P3 | Included as qualified external evidence | Zenodo archive preserved; not independently rerun |
| Credentials/secrets | No detected text-pattern hit in reviewed program text | Public-package staging also excludes environment and key files |
| Medical/product claims | Prohibited | README and manuscript framing retain research-only limitation |

## Dataset and Attribution Controls

| Study | Authoritative source used by retained run | Recorded source version/license | Public-package treatment |
|---|---|---|---|
| P4 OpenBMI | NEMAR `nm000338`; supporting data DOI `10.5524/100542` | v1.0.5; NEMAR page currently labels dataset GPL-3.0 | Do not bundle raw source data; cite source DOI, publication, and source terms |
| P5 Jeong2020 | NEMAR `nm000311`; supporting data DOI `10.5524/100788` | v1.0.2; NEMAR page currently labels dataset CC0-1.0 | Do not bundle raw source data in this archive; cite source DOI/publication and check current terms |

The P4/P5 source pages were checked on 2026-08-26. Source terms can change or include record-specific constraints, so a public uploader should verify the authoritative record again at the time of publication.[1] [2]

## Mandatory Public-Release Statements

The public repository description should state that P4 is an external OpenBMI validation and **not** a BCI IV-2a replication. It should state that P5 is an amended Jeong MI-only external validation; its transparent fixed fusion rules did not establish improvement over EEG-only in this cohort. It must state that source data are **not included** and must be acquired independently. It must not mention P6 as a completed public result.

## Residual Publication Risk

No automated audit can establish that the uploader owns every line of programme-authored code or has satisfied every upstream term. The actual published code tree is declared Apache-2.0 by its `pyproject.toml`; this public package supplies the matching license text. Third-party source repositories, raw data, and external software are **not sublicensed** by this package. The publisher remains responsible for confirming rights and preserving required attribution.

## References

[1]: https://nemar.org/dataset/nm000338 "NEMAR nm000338 — OpenBMI"
[2]: https://nemar.org/dataset/nm000311 "NEMAR nm000311 — Jeong2020"
[3]: ../papers/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md "P4 Q1 Manuscript"
[4]: ../papers/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md "P5 Q1 Manuscript"

This audit uses the retained P4/P5 evidence and the official source records cited above.[1] [2] [3] [4]
