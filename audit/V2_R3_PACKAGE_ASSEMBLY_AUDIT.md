# V2 Recovery R3 Interim Package Assembly Audit

## Package Identity

The deliverable is named `human-motor-intelligence-v2-recovery-r3-q1-interim-current-state.zip`. Its name and release notes intentionally state **interim current-state**, not final authoritative. The package contains the programme tree under one root directory and includes `RELEASE_CONTENTS_MANIFEST_R3_INTERIM.txt` generated during assembly.

## Assembly Acceptance Matrix

| Requirement | Evidence included in package | Status |
|---|---|---|
| P4/P5/P6 R3 Q1 manuscripts | Three R3 Q1 manuscript files under `papers/` | PASS |
| Complete appendices/reviews/gap audits | `papers/paper_4/`, `paper_5/`, and `paper_6/` | PASS |
| R3 P6 identity correction/hard stop | `audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md` and P6 R3 status | PASS |
| Programme-level integration | R3 master audit, synthesis, cross-reference audit, claim and reproducibility matrices | PASS |
| Verification evidence | Integration validation, main test log, MyoSim execution log | PASS with explicit PyBullet limitation |
| Frozen evidence preservation | V1/V1.1/R1/R2 tree remains included without overwriting/relabeling | PASS |
| Raw biosignal exclusion | Packaging rule excludes BDF/EDF/GDF/SET/FIF; integration audit confirms none in tree | PASS |
| Derived-cache exclusion | Packaging rule excludes NPZ; integration audit confirms none in tree | PASS |
| R3 decoder-quality completeness | Not included because no authentic three-trace provenance set exists | BLOCKED, correctly visible |
| P3 completion | Not included because no P3 evidence package was supplied | PENDING, correctly visible |

## Final Assembly Rules

The archive must pass ZIP integrity testing and contain no raw biosignal or cache extensions. Its contents must include the current `FINAL_PROGRAM_RELEASE_NOTES.md`, `V2_R3_INTEGRATION_VALIDATION.md`, and `V2_R3_TEST_EXECUTION_LOG.md`. The package must not contain `R2_004`, an R3 P6 result folder, fabricated replay traces, or a decoder-condition comparison table, because none exists in the retained evidence.

## References

[1]: V2_R3_INTEGRATION_VALIDATION.md "R3 Integration Validation"
[2]: V2_R3_TEST_EXECUTION_LOG.md "R3 Test Execution Log"
[3]: ../papers/CROSS_REFERENCE_AUDIT_RECOVERY_R3.md "R3 Cross-Reference Audit"
[4]: ../papers/REPRODUCIBILITY_MATRIX_V2_RECOVERY_R3.md "R3 Reproducibility Matrix"
[5]: V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Replay Identity Hard Stop"

The package’s interim status and inclusion rules follow the R3 validation, test, cross-reference, reproducibility, and hard-stop records.[1] [2] [3] [4] [5]
