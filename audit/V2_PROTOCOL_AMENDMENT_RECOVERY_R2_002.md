# V2 Protocol Amendment Recovery R2 002

**Protocol ID:** `nemar-nm000311-jeong-p5-external-loso-24subject-r2`  
**Registered:** 2026-08-23 (GMT+3), before any P5 signal extraction, model fit, score, or statistical analysis.

## Reason

The completed official sidecar audit shows that 22 retained participants have 50 events in every MI class, while `sub-14` has 100 and `sub-16` has 101 `grasp_cup` events. All other required label counts are 50. The original R2 amendment requires all 11 labels for every retained subject but did not yet specify the deterministic handling of these extra event rows.

## Locked Equalization Rule

For every retained subject and each of the eleven predeclared labels, use the **first 50 valid event rows in original TSV order**. Reject a subject if any label has fewer than 50 valid extractable epochs after boundary/channel checks. Discard later same-label rows only for labels with more than 50 sidecar events; record the discarded row count and source event order in subject provenance.

This rule fixes each retained subject at 550 trials, preserves all eleven labels, is defined before signal extraction and model fitting, and does not inspect signal values, predictions, or outcomes. It neither restores `sub-23` nor modifies the source-availability exclusion.

## Scope and Impact

The amendment changes neither modality/channel policy, timing, LOSO split, classifiers, statistics, seed, external-validation label, nor independent-rerun requirement. It only resolves a deterministic source-event multiplicity difference detected in the pre-model availability audit.
