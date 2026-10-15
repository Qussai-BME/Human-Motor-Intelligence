# Final Project Report — V2 Recovery R3 Addendum

## Relationship to the Legacy Report

This addendum updates the programme’s **current-state evidence and release posture** after the legacy master-stack report. It does not replace or edit `FINAL_PROJECT_REPORT.md`, which remains the historical account of the baseline thin-integration implementation. The architecture, child-project boundaries, contracts, local registry, and synthetic-demonstrator scope remain unchanged.[1]

## What Was Implemented After the Baseline Report

| Area | Current addition | Verification status |
|---|---|---|
| P4 external EEG evidence | OpenBMI 54-subject binary-MI zero-calibration LOSO validation with five fixed models | D1–D5, subject-level statistics, figure, exact rerun |
| P5 external multimodal evidence | Amended Jeong 24-subject MI-only EEG/EMG transparent LDA study | Source audit, amendments, D1–D5, statistics, figure, exact rerun |
| P6 systems methodology | Minimal inert-by-default MyoSim initial-state perturbation patch; 20 locked initial-state records | Baseline compatibility, capability tests, exact rerun |
| P6 evidence governance | Replay identity inventory and hard stop before a false decoder-quality comparison | R3 hard-stop audit, no unauthorised execution |
| Q1 integration | Full P4/P5/P6 manuscripts, appendices, reviews, evidence-gap audits, programme synthesis and matrices | R3 integration validation passed |
| Phase S readiness | Current real-data, benchmark, reproducibility, child validation, limitations, roadmap, release, and red-team records | Current all-specification completion matrix |

## Current Evidence State

P4 is a reproducible external OpenBMI validation and P5 is a reproducible amended Jeong external validation. These reports extend the baseline programme from infrastructure-only status to source-bound real-data evidence for their declared tasks. Neither result permits a general clinical, cross-dataset, or product claim. P6 confirms a simulation methodology and negative fixture outcome under state perturbation, not a decoder-quality relationship.

## What Was Reused, Adapted, and Not Changed

The original thin umbrella layer and four child repositories remain separate. The R2 P6 initial-state capability is a patch retained outside the programme repository against user-provided MyoSim V1.1; the programme contains its patch and test evidence, not a replacement MyoSim source tree. No raw data are included. Paper 3 remains untouched and un-reconstructed.

## Tests and Runtime State

The main programme suite has 28 passing tests. The P4/P5 and P6 primary/rerun hashes pass current validation. The applicable MyoSim MuJoCo-capable selection yielded 62 passing tests; optional PyBullet remains unverified because the dependency is unavailable in the Python 3.12 environment. The test execution record reports the exact limitation rather than treating it as a pass.[2]

## Remaining Evidence Gates

The programme is not final-authoritative because P3 material is pending and P6 has no authentic three-condition decoder trace package. The next valid work is governed by `ROADMAP.md` and the P6 trace gate; it is not additional narrative or retrospective condition assignment.

## References

[1]: FINAL_PROJECT_REPORT.md "Legacy Final Project Report"
[2]: audit/V2_R3_TEST_EXECUTION_LOG.md "R3 Test Execution Log"
[3]: audit/SPECIFICATION_COMPLETION_MATRIX_ALL_SPECS_R3.md "All-Specification Completion Matrix"
[4]: papers/Q1_EVIDENCE_EXPANSION_MASTER_AUDIT_RECOVERY_R3.md "R3 Master Evidence Audit"

This addendum summarizes the verified R3 current-state records without changing the baseline report.[1] [2] [3] [4]
