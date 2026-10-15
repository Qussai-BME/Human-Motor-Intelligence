# V2 P5 Jeong2020 Availability Gate: Hard Stop

**Recorded:** 2026-08-23 (GMT+3)  
**Study component:** P5 external multimodal validation  
**Dataset derivative:** NEMAR `nm000311` v1.0.2, `ses-0`  
**Decision:** **STOP — no P5 model extraction, LOSO fit, or manuscript result is authorized under the locked 25-subject cohort.**

## Why This Audit Was Required

The P5 recovery protocol inherited a locked cohort of 25 named subjects, all three `ses-0` imagery runs, all 11 motor-imagery labels, and a subject-level LOSO inference unit. Before downloading high-volume BDF recordings, the programme audited the official event sidecars for all subjects. This is a source-availability and label-coverage check, not a model-selection step.

## Observed Availability

The complete sidecar audit is retained in `audit/jeong_ses0_event_inventory.json` and its execution log. Twenty-four subjects have all three expected runs and all 11 locked labels. However, the public derivative directory for `sub-23/ses-0/eeg/` contains event/BDF files only for runs 0 and 1. Run 2 returns HTTP 404 from the selected source. Consequently, `sub-23` has 450 events and lacks both twist labels.

| Cohort rule | Required | Observed | Gate result |
|---|---:|---:|---|
| Named subjects | 25 | 25 listed | Not sufficient alone |
| Imagery runs per subject | 3 | `sub-23`: 2 | **Fail** |
| MI labels per subject | 11 | `sub-23`: 9 | **Fail** |
| All-class balanced analysis feasible under locked cohort | Yes | No | **Fail** |
| Subject-level LOSO on the original cohort | Yes | Not valid with incomplete held-out subject | **Fail** |

The audit also found that `sub-14` has 600 events and `sub-16` has 601 events, owing to extra `grasp_cup` events. For the 24 complete subjects, every class has at least 50 events; a possible later amendment could predeclare a deterministic first-50-per-class rule. That potential remedy does **not** fix the absent twist classes for `sub-23` and is not enacted here.

## Decision Boundary

The V2 specification requires stopping when source accessibility, subject coverage, LOSO compatibility, or label integrity fails. Therefore the project will **not** silently omit `sub-23`, use only a nine-class subset, substitute another session, mix a source for one participant, or treat the 24-subject technical subset as an external scientific result.

> No P5 score, effect estimate, null claim, or fusion conclusion may be generated from this derivative under the locked 25-subject protocol.

A future P5 amendment would need to be a separately justified, pre-execution decision supported by authoritative proof of a complete, uniformly licensed source for the missing recording or a newly predeclared 24-subject dataset-availability cohort. It must not retrofit an outcome-bearing selection and would require a new protocol identifier, manifest, and independent audit. This record makes no such amendment.

## Evidence Sources

| Evidence | Location |
|---|---|
| Full all-subject sidecar inventory | `audit/jeong_ses0_event_inventory.json` |
| Reproducible sidecar audit code | `scripts/audit_jeong_event_inventory.py` |
| Audit log | `audit/jeong_ses0_event_inventory.log` |
| Direct `sub-23` directory/source-status diagnosis | Execution record `v2_jeong_sub23_source_diagnosis` |
| Direct `sub-23` class inventory | Execution record `v2_jeong_sub23_class_inventory` |

## Status

`P5_external_Jeong2020_nm000311_v1.0.2`: **blocked by source coverage; no model run performed.**
