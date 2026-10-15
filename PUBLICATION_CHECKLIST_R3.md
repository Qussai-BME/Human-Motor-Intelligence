# Publication / Upload Checklist — Human Motor Intelligence 1.2.0

## Required package gates

| Gate | Required state |
|---|---|
| Canonical README | Present and current. |
| Author/citation metadata | Qussai Adlbi + actual repository URL. |
| License/notice | Present. |
| Canonical release manifest | `release/RELEASE_MANIFEST.json` with SHA-256 values. |
| Core test suite | Pass, with optional MyoSim integration clearly skipped when unavailable. |
| No self-hash placeholders | None. |
| No workstation-specific required paths | P6 runners use CLI arguments or environment variables (`MYOSIM_DIR`, `EEGMMIDB_DIR`, `C2_OUT`, `C2_RAW`). |
| P6 scientific status | C1 + audit + C2 complete; R03 retained as engineering baseline. |
| Raw dataset governance | Raw EDF recordings excluded. |

## Public description

> Human Motor Intelligence 1.2.0 is a public research archive and thin integration layer containing cross-subject biosignal evidence, reproducibility records, and the executed P6 studies: the C1 registered EEG-to-MyoSim replay (0/60), its post-hoc audit, and the C2 registered episode-level follow-up with 19,750 real-decoder and 27,000 emulated episodes. R03 is retained only as engineering/preflight evidence.

## Claims prohibited by this release

Do not describe P6 as clinical validation, prosthetic validation, online human BCI evaluation, or a general proof that decoder quality does or does not determine control utility. The supported claims are limited to the registered EEGMMIDB cohorts, the fixed MyoSim configuration and interface, and are listed in `papers/paper_6/CLAIM_EVIDENCE_MATRIX.md`.

## Final external check

Confirm that upstream dataset and dependency terms are still current at the time of publication. The repository should be published only after the generated release ZIP and its SHA-256 are recorded by the uploader.
