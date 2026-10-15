# All-Specification Package Assembly Audit
## V2 Recovery R3 Interim Current-State Release

## Package Identity

The revised deliverable is a single ZIP named `human-motor-intelligence-v2-recovery-r3-all-specs-interim-current-state.zip`. It is **interim current-state**, not final authoritative all-complete, because P3 source evidence and P6 authentic three-condition decoder traces remain unavailable.

## Inclusion Matrix

| Required component | Inclusion decision | Evidence location |
|---|---|---|
| Preserved governing specifications | Include unchanged copies | `specifications/` |
| Frozen baseline and Recovery evidence | Include project paths without deleting/relabeling historical artefacts | `results/`, `papers/`, `audit/`, patches/code/docs |
| P4/P5/P6 Q1 Markdown manuscripts and appendices | Include | `papers/` |
| P4/P5/P6 standalone Word manuscripts | Include | `deliverables/` |
| Phase S current-state reports | Include | Top-level reports plus `audit/` |
| All-specification completion/red-team/validation/test/QA records | Include | `audit/` |
| Verified artifact manifest | Include | `VERIFIED_ARTIFACT_MANIFEST.md` |
| Raw biosignal recordings and derived cache | Exclude | BDF/EDF/GDF/SET/FIF/NPZ prohibited by packaging rule |
| Runtime cache and repository metadata | Exclude | `__pycache__`, `.pytest_cache`, `.git`, `.pyc` excluded |
| P6 R2_004/R3 decoder-quality run record | Not included because it does not exist | Hard-stop enforcement record included instead |

## Package Acceptance Checks

Before delivery, the archive must pass ZIP integrity testing; contain all required Word documents and current release records; contain no raw/cache extension; contain no `V2_PROTOCOL_AMENDMENT_RECOVERY_R2_004.md` or `results/real/v2-recovery-r3` execution directory; and have a verified SHA-256 calculated after final assembly. The ZIP’s internal contents manifest is generated from its staged package tree.

## Interpretation

Packaging should preserve the distinction between **complete documentation/readiness work** and **unavailable experimental evidence**. The package is professionally complete for its present evidence state, but its title and top-level release notes must continue to state the two open gates: P3 input and P6 authentic trace provenance.

## References

[1]: SPECIFICATION_COMPLETION_MATRIX_ALL_SPECS_R3.md "All-Specification Completion Matrix"
[2]: ALL_SPECS_RED_TEAM_AUDIT_RECOVERY_R3.md "All-Specification Red-Team Audit"
[3]: ALL_SPECS_RELEASE_VALIDATION_R3.md "All-Specification Release Validation"
[4]: V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Replay Identity Hard Stop"

The assembly criteria follow the all-specification completion, red-team, validation, and hard-stop records.[1] [2] [3] [4]
