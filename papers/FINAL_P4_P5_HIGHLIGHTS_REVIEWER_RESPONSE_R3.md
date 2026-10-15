# Final P4/P5 Highlights, Reviewer Reports, and Response Strategy — R3

## P4 Highlights

1. A strict zero-calibration LOSO protocol was externally validated across 54 OpenBMI subjects.
2. Representation choice was tested directly under identical subject partitions.
3. Temporal and spectral representations exceeded the tested covariance-only log-Euclidean representation in paired subject-level analysis.
4. The conclusion is scoped to the evaluated cohort, feature family, classifier protocol, and external-validation design.
5. No universal claim about Riemannian methods or clinical performance is made.

## P5 Highlights

1. A 24-subject amended Jeong2020 MI-only cohort was evaluated under strict zero-calibration LOSO.
2. Transparent EEG–EMG fusion did not establish a clean-data advantage over EEG-only.
3. Under 20% EEG feature-group zeroing, fusion did not provide measurable robustness beyond EEG-only.
4. Confidence-aware fusion was not validated as a reliability-aware improvement.
5. Missing-modality handling is retained as engineering graceful degradation, not as clinical robustness evidence.

## Reviewer 1 — Machine Learning

**Objections:** novelty may be routine benchmarking; covariance comparison may be incomplete; test-subject leakage and model selection require inspection; confidence fusion may be uncalibrated; the degradation model may be artificial.

**Response disposition:** RESOLVED BY EXISTING EVIDENCE for strict LOSO, fixed protocols, reruns, and scope-controlled representation comparison. RESOLVED BY NEW LOW-COST ANALYSIS for paired Holm statistics and P5 clean-train/corrupted-test analysis. ACKNOWLEDGED AS LIMITATION for the restricted representation family, lack of P4 probability artifacts, and feature-level rather than physical corruption.

## Reviewer 2 — Biomedical Engineering

**Objections:** EMG ordering may be overinterpreted physiologically; robustness may be presented as hardware resilience; clinical or prosthetic relevance may be overstated.

**Response disposition:** ACKNOWLEDGED AS LIMITATION. No mechanism is claimed for EMG ordering. MI is separated from motor execution. Feature-cache degradation is not called electrode failure, and no clinical, prosthetic, safety, or human-factors validation is claimed.

## Reviewer 3 — Statistics

**Objections:** trial-level pseudo-replication; missing Holm correction; misuse of non-significance; retention treated as inferential; bootstrap uncertainty unclear.

**Response disposition:** RESOLVED BY NEW LOW-COST ANALYSIS. Subject is the inferential unit. P4 paired comparisons use bootstrap CIs, Wilcoxon tests, and Holm correction. P5 degradation drop and retention are reported descriptively, while degraded condition contrasts use paired subject-level tests. Non-significance is not described as equivalence.

## Response strategy

The papers should be positioned as evidence-governed external validations rather than universal algorithmic claims. Requests for transformers, adversarial adaptation, self-supervised learning, large hyperparameter searches, or extensive seed grids are outside the stated minimum-evidence objective and are not validity blockers for the current questions. The highest-value future improvement is to persist fold-local probabilities for P4 and evaluate calibrated reliability on a new external cohort with a preregistered physical degradation protocol.
