# V2 Recovery R2 Release Integrity Audit

**Release target:** Human Motor Intelligence V2 Recovery R2  
**Decision:** **Releaseable with a documented optional PyBullet test-environment limitation.**  
**Date:** 2026-08-23 (GMT+3)

## Evidence Integrity

| Check | Result | Evidence |
|---|---|---|
| V1/V1.1 legacy results overwritten | Pass | R2 uses separate `v2-recovery-r2` namespaces only. |
| P4 retained as R1 external evidence | Pass | R1 artefacts/manuscript remain distinct and unchanged. |
| P5 cohort amendment predated extraction | Pass | `V2_PROTOCOL_AMENDMENT_RECOVERY_R2_001.md` and `_002.md` precede P5 R2 cache/model execution. |
| P5 D1 | Pass | 48 observations; 8,188,646 bytes; no checksum failures. |
| P5 D2–D5 | Pass | `validation.json`: schema, labels, protocol, and leakage all pass. |
| P5 result completeness | Pass | 24 subjects × 4 fixed models = 96 rows; independent rerun exact. |
| P6 baseline compatibility | Pass | Unperturbed benchmark endpoints match preserved values before and after extension. |
| P6 state capability | Pass | 20 expected seeds, 20 distinct qpos states, bounded declared offsets, no invalid state. |
| P6 outcome integrity | Pass | All 20 predeclared runs retained despite all-failure result; no parameter/seed retuning. |
| P6 independent rerun | Pass | Primary and rerun `run_records.json` are byte-identical; code fingerprint matches. |
| Synthetic separation | Pass | P6 R2 identifies `origin=real_replay_initial_state_variation`; no synthetic artefact is used in its result. |

## Raw-Data Boundary

The repository contains zero `.bdf`, `.edf`, `.gdf`, or `.vhdr` raw-signal files. The temporary P5 raw workspace contains zero files after sequential extraction. The P5 derived cache contains 24 `.npz` files and 24 provenance JSON files outside the repository. No raw biomedical recording is included in the release package.

## Test Results

| Test surface | Result | Qualification |
|---|---|---|
| Human Motor Intelligence repository | 28 passed | `audit/v2r2_repository_full_test.log` |
| MyoSim MuJoCo/P6-capable suite | 62 passed, 3 deselected | `audit/v2r2_myosim_mujoco_complete_test.log` |
| New P6 integration tests | Included in the 62 passing MyoSim tests | Inert default, distinct bounded states, original benchmark |
| Full MyoSim suite with PyBullet | Not executable in this sandbox | PyBullet is optional, absent for Python 3.12; pip build failed and Ubuntu package was unavailable. PyBullet-specific tests and three backend-availability assertions were excluded, not silently passed. |

The R2 study uses the MuJoCo backend, which was exercised by the baseline, probes, 20-run cohort, independent rerun, and MyoSim test suite. The optional PyBullet limitation does not alter P5 or P6 outcome artefacts, but it remains a release-environment limitation.

## Release Package Verification

The final package is:

```text
<LOCAL_WORKSPACE>/human_motor_workspace/releases/human-motor-intelligence-v2-recovery-r2.zip
```

The final archive checksum is supplied in the adjacent external `.zip.sha256` file after final packaging. The internal file inventory is `FILE_CHECKSUMS.sha256`.

Archive verification passed (`unzip -t`). The archive contains two P5 subject-result CSV entries (primary plus independent rerun), the P6 statistics artefact, the MyoSim R2 patch, and the internal `FILE_CHECKSUMS.sha256` inventory. It contains zero raw-signal entries with `.bdf`, `.edf`, `.gdf`, or `.vhdr` suffixes.

## Release Contents Requirement

The release must include P5/P6 primary and rerun artefacts, protocols, audits, scripts, figures, the MyoSim R2 source patch and test file, documentation, and checksum inventory. It must exclude the derived caches and all raw BDF/TSV data. The final release notes must report P5 and P6 negative findings prominently and preserve P3 pending-status language.
