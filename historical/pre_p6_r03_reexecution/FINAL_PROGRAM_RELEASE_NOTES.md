# Human Motor Intelligence — V2 Recovery R3 Q1 Integration
## Interim Current-State Release Notes

> **Release status: INTERIM — NOT the final authoritative all-complete R3 release.** The requested P6 three-decoder-quality study remains unexecuted because the authentic, provenance-linked worst/mid/best replay traces have not been supplied. P3 material also remains pending.

## Purpose

This interim release preserves the complete frozen programme record while providing the R3 correction, Q1-standard integration documents, full appendices, paper-level reviews, evidence-gap audits, and programme-level governance documents. It does **not** manufacture missing evidence, rename the P6 fixture, or present a package as final before its central blocked requirement is satisfied.

## Included Evidence

| Area | Included material | Release interpretation |
|---|---|---|
| Historical programme | Frozen V1, V1.1, R1, and R2 artefacts present in the project tree | Preserved; not overwritten or silently relabelled |
| P4 | R1 OpenBMI source/protocol/manifest/D1–D5/statistics/figure, exact rerun, R3 Q1 manuscript, appendix, review, evidence-gap audit | Completed external binary-MI validation, not direct replication |
| P5 | R2 amendments, source check, result/statistics/figure, exact rerun, R3 Q1 manuscript, appendix, review, evidence-gap audit | Completed amended external MI-only validation; no general fusion claim |
| P6 R2 | Initial-state patch, compatibility/capability materials, 20 repeat records, statistics, exact rerun | Reclassified in R3 as an integration-fixture systems test |
| P6 R3 | Hard-stop audit, status paper, Q1 manuscript, appendix/review/gap audit, future research gate | No decoder-quality execution or model comparison |
| Programme integration | Master audit, synthesis, cross-reference audit, claim matrix, reproducibility matrix | Current authoritative interpretation of retained evidence |

## Material R3 Correction

The R2 replay input is the MyoSim packaged `pick_place_replay.csv`. Its own records identify `source_subject=synthetic-demo` and `model_version=example-decoder-v1`. It is not provenanced as a tiny-CNN/worst decoder trace. No valid mid-tier or best trace was found. Therefore, this release contains **no** `R2_004` amendment, no P6 R3 run records, no 2×20 or 3×20 decoder condition table, and no Cochran Q/Fisher/other between-condition test.[1]

## Evidence Dispositions

| Paper/area | Disposition | Essential caveat |
|---|---|---|
| P4 | GREEN/YELLOW | Reproducible external validation; external generalisation and clinical scope remain limited |
| P5 | GREEN/YELLOW | Audited amended-cohort fusion comparison; no general or mechanistic conclusion |
| P6 R2 mechanics | GREEN/YELLOW | Robust simulator fixture methods and rerun; not a real-decoder study |
| P6 decoder quality | RED/BLOCKED | Authentic condition traces and provenance are required |
| P3 | PENDING | Required research package/evidence has not been provided |

## Exclusions

No raw BDF, EDF, or related raw biosignal data is included. The Jeong derived cache remains external to the repository and release. No synthetic trace, edited confidence stream, guessed model label, or reconstructed confusion matrix has been inserted. The interim release never replaces historical R2 artefacts with R3 prose.

## Required Author Input for Final Authoritative R3 Release

Supply the P6 trace package described in `papers/RESEARCH_GATE_PREPARATION_RECOVERY_R3.md`: three frozen decoder outputs, one authoritative condition mapping per trace, SHA-256 values, model/version/checkpoint/source provenance, parsing/serialization details, and permission to use the material. On acceptance, the programme will register the prospective amendment, execute in a new R3 namespace, verify/repeat the runs, and then produce the final authoritative release. Supply the P3 package if it is intended to be part of the six-paper completion.

## References

[1]: audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Replay Identity Hard Stop"
[2]: papers/Q1_EVIDENCE_EXPANSION_MASTER_AUDIT_RECOVERY_R3.md "R3 Q1 Master Audit"
[3]: papers/CLAIM_EVIDENCE_MATRIX_V2_RECOVERY_R3.md "R3 Claim–Evidence Matrix"
[4]: papers/RESEARCH_GATE_PREPARATION_RECOVERY_R3.md "R3 Research-Gate Preparation"

The release status and trace requirements are governed by the retained R3 hard stop and integration audit.[1] [2] [3] [4]
