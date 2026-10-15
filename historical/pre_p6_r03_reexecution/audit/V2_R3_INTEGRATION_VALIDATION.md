> **HISTORICAL / SUPERSEDED RECORD:** This document records an earlier pre-reopening state. It is retained for provenance only. Current P6 disposition is documented in `P6_FINAL_STATUS.md` and `closure/10_FINAL_CLOSURE_REPORT.md`.

# V2 Recovery R3 Interim Integration Validation

This validation checks release integrity and evidence boundaries only. It does not rerun scientific models or derive new performance measures.

## Artefact and Reproduction Checks

| Check | Status | Detail |
|---|---|---|
| Required R3 integration documents (23) | PASS | All required manuscript, appendix, review, audit, and release-note files exist |
| P4 primary/rerun CSV | PASS | `ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8` |
| P5 primary/rerun CSV | PASS | `a35b1cb5daa2cdae2078e7668eb1b028e4613c99e062df2b941183c7b971e36b` |
| P6 primary/rerun aggregate record | PASS | primary/rerun SHA-256 `2edaa2a7d8a1e0448dc9f5742190a736a2877eb20c65395d60d65dd019cad120` |
| Markdown appendix image targets | PASS | No unresolved targets |
| Raw biosignal exclusion | PASS | No .bdf/.edf/.gdf/.set/.fif in repository |
| Derived-cache exclusion | PASS | No .npz cache in repository |
| R3 terminology audit | PASS | No unqualified prohibited P6 terms in current R3 surfaces |

## Terminology Findings

No unqualified occurrence of `real decoder`, `tiny-CNN`, `worst decoder`, or `decoder-quality result` was found in non-historical R3 release surfaces.

## Mandatory Interpretation

P6 R3 is blocked and unexecuted. The R2 input is an example/integration fixture identified in the R3 replay-identity hard-stop record; it may not be mapped to a decoder-quality condition. This interim release is therefore not the requested final authoritative all-complete R3 package.

## References

[1]: V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "R3 P6 Replay Identity Hard Stop"
[2]: ../papers/CROSS_REFERENCE_AUDIT_RECOVERY_R3.md "R3 Cross-Reference Audit"
[3]: ../papers/REPRODUCIBILITY_MATRIX_V2_RECOVERY_R3.md "R3 Reproducibility Matrix"

The terminology and release status are governed by the retained hard-stop and R3 programme records.[1] [2] [3]
