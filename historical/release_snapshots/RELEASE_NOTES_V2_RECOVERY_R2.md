# Human Motor Intelligence — V2 Recovery R2 Release Notes

## Release Scope

V2 Recovery R2 extends the audited Recovery R1 programme without modifying frozen V1/V1.1 evidence. It adds one completed external multimodal validation (P5) and one completed declared-state simulator robustness study (P6), along with source checks, protocol amendments, exact independent reruns, programme documentation, figures, and a minimal reproducible MyoSim patch.

## Headline Results

| Study | Result | Required qualification |
|---|---|---|
| P4 retained R1 OpenBMI EEG validation | Five fixed model means range from 0.5962 to 0.6364 macro-F1 over 54 subjects; no pairwise contrast survives Holm | External validation, not direct BCI IV-2a replication or cross-dataset ranking |
| P5 R2 Jeong MI fusion validation | EEG-only 0.0813, late fusion 0.0805, early fusion 0.0754, EMG-only 0.0484 mean subject macro-F1; no fusion-over-EEG Holm result | Amended 24-subject all-11-class MI-only cohort; not direct Cho2017 replication or general fusion verdict |
| P6 R2 real-replay state robustness | 0/20 declared simulator initial states completed task; all ended in `TRANSPORT`; 0 invalid states | Fixed replay/controller, declared MyoSim state distribution; not a biomedical or decoder-quality causal result |

## Evidence and Reproducibility

P5 passed D1–D5, contains 96 subject-model observations, and reproduced with an exact independent CSV match. P6 first matched the preserved unperturbed benchmark, then passed declared-state preflight; 20 seeds produced 20 distinct state vectors and the independent rerun reproduced `run_records.json` exactly. P3 remains **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`**.

## Package Contents

The package includes R2 code, configurations, P5/P6 results and statistics, primary and rerun artefacts, audits, manuscripts, figures, programme matrices, MyoSim patch/test materials, and checksums. It excludes raw BDF/TSV files and derived caches outside the repository.

## Known Environment Limitation

The MuJoCo test path used by P6 passed. Optional PyBullet tests could not run in this Python 3.12 sandbox because PyBullet was unavailable and could not be built/installed; the release integrity audit documents the exact affected tests. This does not affect the MuJoCo P6 execution artefacts but remains an explicit environment limitation.

## Recommended Reading Order

1. `papers/Q1_EVIDENCE_EXPANSION_MASTER_AUDIT_RECOVERY_R2.md`
2. `audit/V2_P5_JEONG_EXTERNAL_VALIDATION_AUDIT_RECOVERY_R2.md`
3. `audit/V2_P6_REAL_REPLAY_INITIAL_STATE_REPEAT_AUDIT_RECOVERY_R2.md`
4. `papers/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R2.md`
5. `papers/P6_REAL_REPLAY_INITIAL_STATE_ROBUSTNESS_V2_RECOVERY_R2.md`
6. `audit/V2_RELEASE_INTEGRITY_AUDIT_RECOVERY_R2.md`
