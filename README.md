# Human Motor Intelligence v1.2.0

[![Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.23406267.svg)](https://zenodo.org/records/23406267)

Public research archive and thin integration layer for the Human Motor Intelligence programme: a series of six papers on cross-subject EMG/EEG decoding and on the traceable path from decoded intent to simulated action. The archive holds the reproducibility infrastructure, the executed P6 studies (C1 registered replay, its post-hoc validity audit and the C2 registered follow-up) with their audit trails, and the evidence records of the programme. It is non-clinical research software and evidence, not a medical device.

Previous public release: v1.0.0 (Zenodo 22288272); v1.1.0 (C1-only) is superseded by this release. See `RELEASE_CHANGELOG.md`.

Zenodo archive of this release: 10.5281/zenodo.23406267.

## The six papers

| # | Topic | Status |
|---|---|---|
| P1 | Rest-class metric inflation in zero-calibration cross-subject sEMG (three-database LOSO benchmark) | Submitted |
| P2 | Reference MiniROCKET domain-adaptation benchmark (revised after supervisor review; archive v2.0.0 supersedes v1.0.0) | Supervisory review |
| P3 | Adversarial domain confusion and feature-covariance alignment (Lite-DAN) | Supervisory review; included as externally archived evidence |
| P4 | Strict zero-calibration cross-subject EEG motor-imagery decoding, external validation | Supervisory review |
| P5 | Transparent cross-subject EEG–EMG fusion, amended external validation | Supervisory review |
| P6 | Decoder accuracy versus control utility in simulated intent-to-action control (C1, audit, C2) | Manuscript v2 in preparation |

Authoritative per-paper evidence: `papers/EMG_SERIES_MASTER_EVIDENCE.md`. Statements about P2 in older audit documents describe its first version and are superseded: `papers/P2_SUPERSESSION_NOTICE.md`.

## P6 results at a glance

P6 is reported in three stages (the manuscript text is not distributed in this archive; see "Manuscript texts" below).

| Stage | Record | Outcome |
|---|---|---|
| **C1** registered replay (`p6/c_mi_r04_primary`, `p6/c_mi_r04_rerun`) | R04 motor imagery, S001–S020, strict LOSO, M1/M2/M3, 60 + 60 MyoSim runs | Fixture 1/1; task success **0/60** (primary and rerun). Decoders at chance (pooled accuracy 0.497–0.510). |
| **Audit** (`p6/c1_audit`, post-hoc) | Re-execution, oracle negative control, event-timeline accounting, timeout-removed sensitivity | The C1 endpoint was **unreachable by design**: an oracle stream also scored 0/20; 2 of 15 outputs reached the task before its 8.0-s clock ended; 171/207 controller transitions followed task failure. The C1 command-correction contrast is withdrawn as an artefact. |
| **C2** registered follow-up (`p6/c2_episode`) | Episode-level interface (oracle 100/100), emulated decoder ladder (27,000 episodes), real decoders on 105 EEGMMIDB subjects (19,750 episodes), controller sensitivity (25,600) | Control success follows **confidence-gate passing**, not accuracy: over-confident chance-level decoder 23.0%; real zero-calibration decoders (balanced accuracy 0.53–0.60) gain at most 0.4 percentage points above a chance-matched floor at the registered gate. |

Details: `P6_FINAL_STATUS.md`, `papers/paper_6/RESULTS_SUMMARY.md`, `p6/c2_episode/README.md`. Everything is non-clinical offline replay in a deterministic simulator.

The earlier R03 experiment is kept under `p6/exploratory_r03_primary/` as an engineering/preflight motor-execution baseline only. It is not motor-imagery evidence. Raw EEG is not redistributed; provenance and SHA-256 hashes are in the dataset manifests.

## Verify

```bash
pip install -e ".[dev,p6]"         # Python >= 3.11
pytest -q                          # 44 passed, 2 skipped without MyoSim (all passed with MyoSim installed)
python scripts/public_release_doctor.py   # checks status consistency and the SHA-256 release manifest
```

The two skipped tests need the separately maintained `myosim` package. The C2 results were produced with MyoSim v0.1.5 (commit `67ee74e`; see `p6/c2_episode/README.md`); with MyoSim 0.1.6 installed all 46 tests pass.

## Repository map

| Path | Content |
|---|---|
| `src/`, `tests/`, `scripts/` | Integration layer, tests, verification tools |
| `p6/` | P6: C1 protocol and results, `c1_audit/` (post-hoc audit), `c2_episode/` (C2 protocol, results, raw archives, verification) and the R03 baseline |
| `papers/` | Per-paper evidence records, claim–evidence matrices and audits |
| `external/` | Externally archived evidence (e.g. P3) |
| `closure/`, `audit/`, `historical/` | Closure records, dated audits and superseded materials |
| `release/` | SHA-256 manifest and verification records |

## Manuscript texts

The full texts of the manuscripts for P1–P6 are not distributed in this archive; they are withheld pending peer-review submission, as in v1.0.0. The archive holds the code, protocols, results, audits and evidence records on which they rest, plus the figures of P6 under `papers/paper_6/figures/`.

## Limits

Non-clinical, simulation-only and offline-replay evidence. Nothing here establishes real-time control, user benefit, hardware performance or clinical efficacy; see `SCIENTIFIC_LIMITATIONS.md`.

## Use of generative-AI tools

Generative-AI use is declared in the manuscripts. The P6 C2 experiment was executed by an autonomous software agent under a frozen protocol, with the agent's original report and the independent human-directed verification kept in `p6/c2_episode/` (see its README). The authors take responsibility for all content.

## Citation and licence

Cite with `CITATION.cff`. Code is released under Apache-2.0 (`LICENSE`); data licences are in `DATA_AND_LICENSES.md`.
