# Human Motor Intelligence Research Showcase
## Ten-Minute External Review Route — V2 Recovery R3 Current State

![Human Motor Intelligence master end-to-end architecture](figures/MASTER_END_TO_END_ARCHITECTURE_R3.png)

## Purpose

This guide gives a technically literate reviewer a direct route through the umbrella architecture, retained empirical evidence, reproducibility surface, and the two external evidence gates. It is designed for review, not for clinical, product, or decoder-quality marketing.

> **Current-state status:** P4 and P5 are completed external-validation studies within their declared protocols. P6 R2 is complete only as a simulator integration-fixture systems study. P3 and P6 R3 remain explicit external-input gates, not missing footnotes.

## Review Route

| Minute | Reviewer action | What can be verified | Evidence boundary |
|---:|---|---|---|
| 0–1 | Read [`../README.md`](../README.md) and [`../PUBLIC_REVIEW_DISCLOSURE_R3.md`](../PUBLIC_REVIEW_DISCLOSURE_R3.md) | Programme scope, independent-child-project architecture, current-state label | Not a final-authoritative all-complete release |
| 1–2 | Inspect this diagram and [`../audit/MASTER_END_TO_END_SPEC_COMPLIANCE_AUDIT_R3.md`](../audit/MASTER_END_TO_END_SPEC_COMPLIANCE_AUDIT_R3.md) | Ownership boundaries, contracts, registry, governance, benchmark engine, and gates | Child-project source is not vendored |
| 2–4 | Read [`../papers/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md`](../papers/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md) and its appendix | P4 OpenBMI LOSO evidence, D1–D5, subject-level inference, rerun | External validation; not direct BCI IV-2a replication |
| 4–6 | Read [`../papers/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md`](../papers/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md) and its appendix | P5 amended Jeong cohort, transparent fusion conditions, negative/limited conclusion, rerun | No general fusion or mechanism claim |
| 6–7 | Read [`../BENCHMARK_REPORT.md`](../BENCHMARK_REPORT.md) | Compatibility rules that prevent P4/P5 pooling or a false cross-study leaderboard | Metrics only compare within declared compatible protocols |
| 7–8 | Read [`../papers/P6_INITIAL_STATE_ROBUSTNESS_AND_DECODER_QUALITY_STATUS_V2_RECOVERY_R3_Q1.md`](../papers/P6_INITIAL_STATE_ROBUSTNESS_AND_DECODER_QUALITY_STATUS_V2_RECOVERY_R3_Q1.md), [`../audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md`](../audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md), and the integrated-demo artifacts | Deterministic systems integration, bounded-state test, identity correction, and nonexecution decision | No real decoder-quality comparison exists |
| 8–9 | Run the local checks in [`../REPRODUCIBILITY.md`](../REPRODUCIBILITY.md) or `hmi doctor` | Registry integrity, artifact hashes, protocol navigation, raw/cache exclusion checks | Raw source data and external child-project runtimes are deliberately external |
| 9–10 | Inspect [`../audit/MASTER_SPEC_PHASE_GATE_LEDGER_R3.md`](../audit/MASTER_SPEC_PHASE_GATE_LEDGER_R3.md) | Complete, blocked, and deferred phase gates | P3 and P6 R3 reopening requirements remain mandatory |

## Demonstrator Boundary

The MyoSim artefacts show a deterministic intent-contract-to-simulation integration route. They are a research demonstrator and virtual-control systems proof of concept; they are **not** clinical validation, a medical-device result, a prosthesis-effectiveness result, or evidence that better offline decoding has been functionally compared.[1]

## Reproduce the Local Infrastructure

```bash
cd human-motor-intelligence-v1_1
PYTHONPATH=src pytest -q
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local doctor
PYTHONPATH=src python3 -m research_core.cli.main --registry-dir registry/local protocol validate eeg-loso-v1
python3 scripts/validate_all_specs_release_r3.py
```

The first command validates the repository-level unit/integration suite. The diagnostic and protocol command expose only local registry/provenance information. The release validator checks documented artefacts and evidence boundaries; none of these commands recomputes frozen P4/P5/P6 outcomes.

## References

[1]: ../PUBLIC_REVIEW_DISCLOSURE_R3.md "Public Review Disclosure"
[2]: ../audit/MASTER_END_TO_END_SPEC_COMPLIANCE_AUDIT_R3.md "Master End-to-End Specification Compliance Audit"
[3]: ../audit/MASTER_SPEC_PHASE_GATE_LEDGER_R3.md "Master Specification Phase-Gate Ledger"
[4]: ../audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Replay Identity Hard Stop"

This showcase follows the public-review, master-spec audit, phase-gate, and P6 hard-stop records.[1] [2] [3] [4]
