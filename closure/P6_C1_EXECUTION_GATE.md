# P6 C1 Execution Gate — Closed

**Gate disposition: PASS / SCIENTIFICALLY COMPLETE**

All registered C1 gates are satisfied by the archived execution artifacts and audit records in this release.

1. **R04 source provenance:** 20/20 required source-file records are present in `audit/DATASET_MANIFEST.json`, with SHA-256 values; raw EDF files are intentionally not redistributed.
2. **Dataset semantics:** R04 is the unilateral motor-imagery condition used for the active C1 study.
3. **Decoder stage:** 60 LOSO traces were generated and the source-only quality order was frozen before downstream analysis.
4. **Fixture stage:** the model-independent control fixture reached `COMPLETE` (1/1).
5. **Primary replay:** 60 decoder-conditioned MyoSim per-run JSON artifacts are present and internally valid.
6. **Primary analysis:** subject-level statistics and claim boundaries are recorded in the release.
7. **Rerun:** 60 rerun traces and 60 rerun MyoSim per-run JSON artifacts are present.
8. **Reproduction:** rerun run IDs and artifact hashes are distinct; deterministic decoder traces and task metrics reproduce exactly.
9. **Manuscript:** current Results/Discussion/Abstract are derived from archived C1 result files.
10. **Release verification:** public-release doctor PASS, project tests 31 passed / 1 skipped, manifest/hash integrity PASS, and public-tree hygiene PASS.

## Re-execution boundary

A fresh end-to-end reproduction still requires retrieval of the external PhysioNet R04 EDF files and a compatible MyoSim/MuJoCo environment. This does not reopen the scientific closure of the archived C1 experiment; it is the expected source-access boundary of a public release that does not redistribute raw biosignals.
