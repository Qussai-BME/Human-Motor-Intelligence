# Research Gate Preparation — V2 Recovery R2

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


## Current Integration Decision

| Evidence item | Integration status | Required wording / action |
|---|---|---|
| P1 author manuscript | Ready as source-grounded context | Retain its rest-class metric and database-specific caveats. |
| P2 author manuscript | Ready as source-grounded context | Retain representation-specific mechanism boundary. |
| P3 | Not ready | Use **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** only. |
| P4 R1 OpenBMI | Ready with external-validation limits | Report five fixed models, non-null omnibus, and no Holm-surviving pairwise result. |
| P5 R2 Jeong | Ready with amended-cohort limits | State 24-subject all-11-class MI-only external validation; no fusion-over-EEG Holm result. |
| P6 R2 | Ready as simulation systems evidence | State fixed replay/control and declared state distribution; no biomedical/decoder causal extension. |

## Closed Decisions

The P5 R2 feature set, LDA model family, source cohort, label cap, subject list, statistics, and seed-independent rerun are closed. No new model, deep fusion architecture, feature selection, trial exclusion, or cohort substitution may be used to pursue a different result in this namespace.

The P6 R2 replay, controller, task, perturbation range, 20 seeds, endpoints, and code fingerprint are closed. The all-failure result is final for the stated distribution. No range retuning or controller change may be labelled a follow-up analysis of this study.

## Gates for Future Work

| Candidate next step | Minimum entry requirement | Disallowed shortcut |
|---|---|---|
| Integrate P3 | Author-supplied manuscript/result package and source extraction | Filling placeholders from project narrative or expectation |
| New P5 external source | License/provenance/subject identity, full cohort availability, pre-execution selection matrix and protocol | Using a partial or source-mixed cohort without amendment |
| Different P5 model family | New paper/protocol explaining why transparent LDA scope changes | Adding deep fusion to R2 after results |
| P5 mechanism study | Independently measured microactivation/strategy/hardware evidence | Inferring mechanism from macro-F1 ordering |
| P6 decoder-quality study | A declared decoder-quality factor, fixed state distribution, condition identifiers, and real/synthetic origin policy | Calling state-only R2 a quality dose response |
| Simulator-to-human claim | Appropriate empirical human/device study and safety review | Generalizing from MyoSim task outcomes |

## Release Gate

Before release, verify: source and cache manifests; D1–D5 for P4/P5; P6 baseline/preflight/run/rerun chain; exact rerun comparisons; code/environment fingerprints; raw-data exclusion; test results; checksums; and all R2 documentation links. Release notes must present P5/P6 negative results prominently rather than imply only positive evidence is included.
