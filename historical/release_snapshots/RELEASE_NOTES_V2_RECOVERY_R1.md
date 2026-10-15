# Human Motor Intelligence — V2 Recovery R1 Evidence Package

## Release Status

This package records V2 evidence expansion after a sandbox-reset recovery. It preserves the distinction between historical frozen evidence and new Recovery R1 evidence. It includes **no raw BDF/EDF recordings**.

## What Completed

P4 completed a 54-subject OpenBMI harmonized external binary MI validation under zero-calibration subject-level LOSO. The derived cache passed D1; D2–D5 passed before fitting; the primary metric was macro-F1; five fixed conditions were analysed with subject-level bootstrap, Friedman, Wilcoxon, and Holm procedures. An independent rerun produced an exact byte-identical 270-row result CSV.

P5 did not produce an external fusion result. The selected Jeong derivative failed the locked 25-subject/all-11-class coverage gate because `sub-23` lacks the third imagery run and twist labels. P6 did not produce repeat estimates. The inspected MyoSim V1.1 seed/reset path is deterministic and does not expose an independent initial/task/replay state factor.

## Essential Findings

| Component | Evidence outcome |
|---|---|
| P4 macro-F1 means | Linear 0.5962; LDA 0.5980; Linear SVM 0.6123; spectral 0.6130; compact CNN 0.6364 |
| P4 omnibus test | Friedman χ²=16.16, *p*=0.00281 |
| P4 pairwise conclusion | No predeclared pair survives Holm; minimum adjusted *p*=0.1042 |
| P4 reproducibility | Primary/rerun CSV byte-identical; SHA-256 `ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8` |
| P5 | Hard stop before model run; no external fusion claim |
| P6 | Hard stop before repeat run; no pseudo-replication |
| P3 | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** |

## Start Here

1. Read `papers/Q1_EVIDENCE_EXPANSION_MASTER_AUDIT.md` for programme-level status.
2. Read `audit/V2_P4_OPENBMI_EXTERNAL_VALIDATION_AUDIT_RECOVERY_R1.md` for P4 methods, results, gates, and reproducibility.
3. Read the P5/P6 hard-stop audits before interpreting their manuscript-status revisions.
4. Use `papers/REPRODUCIBILITY_MATRIX_V2_RECOVERY_R1.md` for exact execution/reproduction paths.

## Boundaries

OpenBMI is an **external validation**, not a direct replication of BCI Competition IV-2a. Its binary dataset metrics must not be directly ranked against the frozen four-class result. The high compact-CNN mean does not establish pairwise superiority after Holm correction. P5/P6 hard stops are not null outcomes. P1/P2 author manuscripts are contextual evidence records and have not been rewritten. P3 remains pending real source evidence.
