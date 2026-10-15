# Release Changelog — Human Motor Intelligence

## 2026-10-11 — v1.2.0: P6 audit and C2 follow-up

- Added `p6/c1_audit` (post-hoc audit of C1): oracle negative control, event-timeline accounting, timeout-removed sensitivity, re-execution; withdrew the exploratory command-correction interpretation. Archived C1 results are unchanged.
- Added `p6/c2_episode`: registered protocol `P6-C2-EPISODE-v1.0` (frozen before outcomes), episode-level interface with cue-correct endpoint, emulated decoder ladder (27,000 episodes), real decoders D1–D5 on 105 EEGMMIDB subjects (19,750 episodes), controller sensitivity (25,600), R0 (560) and X0 (100); raw archives with SHA-256; independent verification and post-hoc analyses.
- New P6 manuscript (text not distributed in this archive; its 14 figures are in `papers/paper_6/figures/`); C1-only drafts marked superseded (`papers/P6_SUPERSESSION_NOTICE.md`).
- Full texts of the P1–P6 manuscripts are not distributed in this archive (withheld pending peer review, as in v1.0.0); their evidence records remain.
- Rewrote `SCIENTIFIC_LIMITATIONS.md` (it previously described only R03), updated README, status, readiness, notice, licences, checklist and closure records; added `closure/11_P6_C2_CLOSURE_REPORT.md`.
- Added 13 tests (`tests/test_p6_c2_episode.py`, plus one optional MyoSim integration test); extended `scripts/public_release_doctor.py` to check C2 integrity; added `scripts/build_release_manifest.py`.
- Made all C2/audit scripts portable (environment variables instead of workstation paths).
- Version bumped to 1.2.0 (supersedes v1.1.0, which contained C1 only, and v1.0.0).

## 2026-10-06 — P6 C1 results, Paper 3 integration, status unification

- Executed P6 C1 under `P6-C1-MI-R04-v1.0`: fixture 1/1; decoder-conditioned task success 0/60 for M1/M2/M3 in both primary run and rerun; primary endpoint non-discriminative; run-level artifacts present (60 + 60).
- Replaced every "execution pending" statement about P6 C1 with the executed status; historical R3 audit documents under `audit/` keep their dated wording.
- Synchronized Paper 2 with its revised manuscript and with MiniROCKET v2.0.0 (corrected CORAL; see `papers/EMG_SERIES_MASTER_EVIDENCE.md`).
- Version scheme aligned with the public record: the previous public release is v1.0.0 (Zenodo 22288272); this release is 1.1.0.

## 2026-10-05 — Public release reconciliation

- Established one canonical public-release narrative and moved the former P4/P5-only `public_release/` snapshot to `historical/`.
- Renamed current P6 paths from `confirmatory` to `exploratory_r03` to match the actual R03 motor-execution evidence.
- Removed the impossible self-referential `trace_sha256` CSV column and moved file hashing to external trace manifests.
- Added explicit source-event labels and the abstract T1/T2-to-OPEN/CLOSE mapping identifier to P6 traces.
- Made P6 runners portable by replacing workstation-specific paths with explicit CLI arguments.
- Standardized current P6 manifests, experiment status, model version, and result filenames.
- Corrected citation metadata and package authorship to Qussai Adlbi with the actual repository URL.
- Marked the MyoSim integration test as optional when the external MyoSim runtime is not installed.
- Added a public release index, release-readiness gate, data/licence boundary, and current implementation status.
- Preserved raw evidence and historical snapshots rather than silently deleting them.
- Reopened P6 under registered C1: R04 motor-imagery is now the scientific primary; R03 is retained strictly as an engineering baseline.
- Added the C1 execution runbook, fixture gate, full rerun gate, subject-level analysis path, and result-population safeguards.
- Declared C1 numerical results pending until the R04 data were processed and executed in a compatible MyoSim/MuJoCo environment, rather than fabricating or reusing R03 numbers (executed later; see the 2026-10-06 entry).
