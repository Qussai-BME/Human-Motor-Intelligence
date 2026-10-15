# Research Gate Preparation — Post-V2 Recovery R1

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


## Purpose

This document specifies the next admissible decisions for the Human Motor Intelligence programme. It is not a request to add datasets or models for quantity. Each gate exists to protect the core question from sample-count inflation, target leakage, unsupported claims, and uncontrolled scope expansion.

## Current Gate Status

| Gate | Evidence required | Current status | Required action |
|---|---|---|---|
| P1/P2 source grounding | Author manuscript and extracted audit text | Pass | Preserve source statements and caveats; do not rewrite without authorization. |
| P3 integration | Author-supplied P3 package with methods/results/limitations | **Blocked** | Retain **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`**. |
| P4 external validation | D1–D5, subject outputs, statistics, independent rerun | Pass | Integrate only as harmonized OpenBMI external validation with no direct-replication language. |
| P5 external fusion | Complete, uniformly sourced cohort compatible with all-11-class MI LOSO | **Blocked** | Do not extract/model a 24-subject subset or use nine labels. Reopen only with pre-execution amendment and authoritative complete source. |
| P6 repeated real replay | Exposed independent initial/task state factor preserving replay/policy question | **Blocked** | Do not create seed-labelled duplicates. Reopen only with simulator-supported variation and precision protocol. |
| Synthetic/real separation | Origin/eligibility tags and separate paths | Required continuously | Audit before any programme-level release. |
| Manuscript integration | Claim-to-artifact traceability and cross-reference audit | Conditionally pass for P1/P2/P4 | Integrate P5/P6 as documented stops, not outcomes. |

## Reopening Requirements

### P3

P3 may be added only after the author supplies the complete evidence package. At minimum this must contain the exact title, research question, datasets and participant counts, split policy, preprocessing, model conditions, results, statistical analysis, limitations, artefacts/versions, and any causal claims. Until then, all fields remain **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`**.

### P5

A P5 reopening proposal must predate any BDF extraction and answer the source problem first. It must document either a complete authoritative replacement/access path for the missing `sub-23` imagery run or a formally new data-availability cohort that is scientifically justified rather than outcome-selected. It must specify license/provenance, all-class event coverage, MI/ME boundary, deterministic equalization policy if required, D1–D5, four transparent fusion conditions, subject-level inference, multiplicity plan, and independent rerun. It cannot turn into a deep-fusion paper by default.

### P6

A P6 reopening proposal must identify a simulator-exposed factor with a mechanistic reason to vary. It must supply the exact state distribution and seed-to-state map; preservation of replay trace, decoder mapping, controller, and task policy; a 20-run precision rationale; success/latency/failure endpoints; per-run provenance; and validation that different seeds produce different declared initial/task states. A hidden patch or changed policy cannot retroactively create this factor.

## Manuscript Gate

Before a programme-level manuscript claim is released, verify the following conditions.

| Check | Pass criterion |
|---|---|
| Artifact linkage | Every exact number links to a source extract, manifest, result CSV, statistics file, or frozen historical artefact. |
| Protocol identity | Dataset version, subject cohort, metric policy, split, pre-processing and model scope are stated. |
| Claim class | Each claim is marked supported, descriptive-only, blocked, pending, or prohibited. |
| Comparative language | No cross-dataset raw ranking without explicit comparability qualification. |
| Negative/blocked results | Retained prominently and not reframed as model failure/success without evidence. |
| P3 | No fill-in language, table values, or inferred narrative. |
| P5/P6 | Stops are described as source/capability gates, not completed null experiments. |
| Reproducibility | P4 primary/rerun checksum agreement and D1–D5 are included. |

## High-Value Next Work

The highest-value next action is integration and review of genuine P3 evidence when it arrives. Until then, the appropriate work is to maintain reproducibility, transparently report P4, and retain P5/P6 stop conditions. More datasets, architecture families, transformers, or synthetic perturbations are not automatically high-value and require a new question-specific audit.
