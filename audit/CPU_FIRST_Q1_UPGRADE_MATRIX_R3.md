# CPU-First Minimal Q1 Upgrade Matrix
## V2 Recovery R3 — Prospective Extension, Frozen Baselines Preserved

## Status and governing rule

This document registers a prospective CPU-first extension. It does **not** overwrite, relabel, or recompute the frozen P4/P5 R1/R2 result namespaces. Any extension result must receive a new versioned namespace, protocol, environment record, provenance manifest, subject-level output, and independent rerun before it can modify a manuscript claim.

> The objective is not to maximize model count. It is to answer reviewer-relevant mechanism and reliability questions with the smallest defensible experiment set.

## Evidence-eligibility matrix

| Proposed extension | Required evidence | Current evidence status | Decision |
|---|---|---|---|
| P4 Riemannian/tangent-space baseline | Epoch arrays with valid channel/time structure; covariance regularization rule; fixed LOSO protocol; CPU implementation | Executed as log-Euclidean covariance + shrinkage LDA in R3-001; 54 subjects; primary/rerun exact | **COMPLETE FOR LOG-EUCLIDEAN BASELINE**; not pooled with frozen P4 |
| P4 Euclidean alignment ablation | Same P4 epochs; alignment fit only on training subjects/folds; frozen transform and leakage audit | Fold-local aligned implementation registered but exceeded current CPU execution window; no result released | **PENDING COMPUTATIONAL GATE** |
| P4 Riemannian alignment | Same as above plus declared manifold/regularization implementation | Epoch cache is available; implementation and numerical stability tests are required | **Eligible**, pending implementation tests |
| P4 cross-dataset evaluation | Authenticated second dataset, compatible labels/tasks/channels or a declared harmonization protocol | No approved second dataset is registered in the current programme | **Blocked externally**; do not infer from OpenBMI alone |
| P4 channel dropout/noise/temporal-shift robustness | Stored epochs; deterministic perturbation protocol; perturbation applied after fold separation; best model declared before perturbation | P4 epochs available; exact perturbation protocol not yet registered | **Eligible after amendment**, no post hoc best-model selection |
| P4 calibration/ECE/Brier | Per-trial probabilities or decision scores from a newly executed frozen protocol; subject-level aggregation rule | Frozen P4 release stores subject-level metrics, not per-trial predictions/probabilities | **Blocked for frozen outputs**; requires new registered execution |
| P5 confidence-weighted fusion | Per-subject/per-trial EEG and EMG posterior probabilities or scores under a fixed evaluation protocol | Executed in R3-001; 24 subjects; trial probabilities/confidences stored; primary/rerun exact | **COMPLETE FOR NEW EXTENSION**; no universal fusion claim |
| P5 modality corruption | Features or trial-level signals; deterministic corruption applied without label leakage; fixed corruption grid | Executed in R3-002 as feature-group dropout at 0/10/20% for EEG and EMG; primary/rerun exact | **COMPLETE AS FEATURE-GROUP PERTURBATION**; not raw hardware robustness |
| P5 missing-modality fallback | Separate modality predictions and a prespecified fallback/adaptive rule; no imputation claim unless implemented | Executed in R3-002 with missing EEG and missing EMG states; fallback is explicit and non-imputing; primary/rerun exact | **COMPLETE AS FALLBACK RULE STUDY**; no physiology/robustness upgrade claim |
| P5 calibration/confidence | Per-trial probabilities/scores from each modality and fusion rule | Not preserved in frozen result artefacts | **Blocked for frozen outputs**; new execution required |
| Paper 2 kernel-reduction/CORAL proposal | Authenticated Paper 2 code/data/results and exact protocol | Not part of the currently validated P4/P5 evidence namespace | **Not started; separate intake required** |

## Minimum extension set

The preferred first execution is deliberately small. For P4, begin with one Riemannian baseline and one alignment ablation, followed by a prespecified robustness study using the declared best model only after the baseline comparison is complete. Calibration and cross-dataset evaluation remain separate gates because their required artefacts or datasets are absent.

For P5, begin with confidence-weighted fusion only if trial-level posterior generation is implemented and registered from the available feature caches. Then evaluate a fixed modality-corruption grid and a missing-modality fallback rule. The result must answer **when fusion is useful**, not claim that fusion is universally superior.

## Prohibited shortcuts

No GPU model, transformer, foundation model, adversarial network, large hyperparameter search, synthetic confidence editing, reconstruction of probabilities from aggregate F1, or cross-dataset claim may be introduced under this extension. No perturbation may be fit using held-out subjects, and no extension may reuse a frozen result path.

## Reopening and release requirements

Every eligible extension requires: a versioned amendment before execution; fixed seed and fold policy; explicit channel/label/task mapping; environment fingerprint; D1–D5-style validation where applicable; subject-level primary output; independent rerun; raw-data exclusion; and claim-safe manuscript addendum. A failed or blocked gate remains visible and is not converted into a null result.

## Current decision

The extension programme is **registered but not yet executed**. The next technical action is to inspect the P4/P5 cache schemas and implement only the smallest validated CPU pipeline. The existing P4/P5/P6 frozen evidence remains unchanged, and P3/P6 R3 external gates remain independent.
