#!/usr/bin/env python3
"""Generate a deterministic verified-artifact manifest for the R3 all-specs interim release."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path("<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1")
OUTPUT = ROOT / "VERIFIED_ARTIFACT_MANIFEST.md"

REQUIRED = [
    "README.md",
    "historical/README_V1_1_BASELINE_PRESERVED.md",
    "PUBLIC_REVIEW_DISCLOSURE_R3.md",
    "PUBLICATION_CHECKLIST_R3.md",
    "LICENSE",
    "NOTICE.md",
    "CITATION.cff",
    "specifications/MASTER_SPEC_ORIGINAL.md",
    "specifications/V1_VALIDATION_AND_COMPLETION_SPEC_ORIGINAL.md",
    "specifications/V2_R3_Q1_INTEGRATION_SPEC_ORIGINAL.md",
    "specifications/MASTER_END_TO_END_RESEARCH_BENCHMARK_INTEGRATION_PRODUCT_SPEC_2026-08-26.md",
    "FINAL_PROJECT_REPORT.md",
    "FINAL_PROJECT_REPORT_RECOVERY_R3_ADDENDUM.md",
    "MASTER_END_TO_END_IMPLEMENTATION_STATUS_R3.md",
    "docs/MASTER_END_TO_END_ARCHITECTURE_R3.mmd",
    "docs/figures/MASTER_END_TO_END_ARCHITECTURE_R3.png",
    "docs/RESEARCH_SHOWCASE_QUICKSTART_R3.md",
    "REAL_DATA_VALIDATION_REPORT.md",
    "BENCHMARK_REPORT.md",
    "REPRODUCIBILITY_REPORT.md",
    "CHILD_PROJECT_VALIDATION_MATRIX.md",
    "SCIENTIFIC_LIMITATIONS.md",
    "RELEASE_CHANGELOG.md",
    "RELEASE_NOTES_MASTER_END_TO_END_R3.md",
    "FINAL_PROGRAM_RELEASE_NOTES_R3_ALL_SPECS_INTERIM.md",
    "audit/SPECIFICATION_COMPLETION_MATRIX_ALL_SPECS_R3.md",
    "audit/ALL_SPECS_RED_TEAM_AUDIT_RECOVERY_R3.md",
    "audit/ALL_SPECS_RELEASE_VALIDATION_R3.md",
    "audit/ALL_SPECS_TEST_EXECUTION_LOG_R3.md",
    "audit/ALL_SPECS_PACKAGE_ASSEMBLY_AUDIT_R3.md",
    "audit/COMPREHENSIVE_PUBLIC_REVIEW_AUDIT_R3.md",
    "audit/MASTER_END_TO_END_SPEC_COMPLIANCE_AUDIT_R3.md",
    "audit/MASTER_END_TO_END_PACKAGE_ASSEMBLY_AUDIT_R3.md",
    "audit/MASTER_SPEC_PHASE_GATE_LEDGER_R3.md",
    "audit/MASTER_SPEC_PHASE4_P3_EVIDENCE_GATE_R3.md",
    "audit/MASTER_SPEC_PHASE8_P6_FUNCTIONAL_GATE_R3.md",
    "audit/MASTER_SPEC_PHASE10_PRODUCT_DISCOVERY_GATE_R3.md",
    "audit/MASTER_SPEC_PHASE_COMPLETION_DOSSIER_R3.md",
    "audit/FINAL_Q1_AUDIT_R3.json",
    "audit/P4_ROBUSTNESS_COMPUTATIONAL_GATE_R3_006.md",
    "audit/p5_calibration_statistics_r3_005.json",
    "audit/p5_calibration_statistics_r3_005_rerun.json",
    "audit/FINAL_HARDENING_REQUIREMENT_INVENTORY_R3.txt",
    "audit/FINAL_HARDENING_LEAKAGE_REPRODUCIBILITY_AUDIT_R3.jsonl",
    "audit/final_p4_p5_hardening_statistics_r3_001.json",
    "audit/p5_friedman_clean_subject_level_r3.json",
    "scripts/compute_p5_friedman_from_subject_results.py",
    "audit/FINAL_P4_P5_Q1_HARDENING_DOSSIER_R3.md",
    "papers/FINAL_P4_P5_HIGHLIGHTS_REVIEWER_RESPONSE_R3.md",
    "papers/CLAIM_EVIDENCE_MATRIX_V2_RECOVERY_R3.md",
    "papers/paper_4/APPENDIX.md",
    "papers/paper_5/APPENDIX.md",
    "results/extensions/v2-final-q1-hardening-r3-001/final_hardening_statistics.json",
    "results/extensions/v2-final-q1-hardening-r3-001/figures/p4_representation_paired_differences.png",
    "results/extensions/v2-final-q1-hardening-r3-001/figures/p5_clean_vs_degraded_robustness.png",
    "audit/test_logs/phase0_architecture_freeze_r3.txt",
    "audit/test_logs/phase1_contract_adapter_compatibility_r3.txt",
    "audit/test_logs/phase2_registry_workflow_r3.json",
    "audit/test_logs/phase2_registry_cli_tests_r3.txt",
    "audit/test_logs/phase3_benchmark_provenance_tests_r3.txt",
    "audit/test_logs/phase5_eeg_eegemg_validation_r3.txt",
    "audit/test_logs/phase6_multimodal_preparation_r3.txt",
    "audit/test_logs/phase7_myosim_integration_r3.txt",
    "audit/test_logs/phase8_p6_functional_gate_r3.txt",
    "audit/test_logs/phase9_research_showcase_r3.txt",
    "audit/test_logs/phase11_final_full_suite_r3.txt",
    "audit/test_logs/phase11_final_doctor_r3.json",
    "audit/test_logs/master_spec_cli_tests_r3.txt",
    "audit/test_logs/master_spec_full_tests_r3.txt",
    "audit/test_logs/master_spec_release_full_tests_r3.txt",
    "audit/WORD_RENDER_QA_NOTES_R3.md",
    "audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md",
    "papers/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md",
    "papers/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md",
    "papers/P6_INITIAL_STATE_ROBUSTNESS_AND_DECODER_QUALITY_STATUS_V2_RECOVERY_R3_Q1.md",
    "papers/paper_4/APPENDIX.md",
    "papers/paper_5/APPENDIX.md",
    "papers/paper_6/APPENDIX.md",
    "results/real/v2-recovery-r1/nemar-nm000338-openbmi-p4-external-loso-recovery-r1/subject_level_results.csv",
    "results/real/v2-recovery-r1-independent-rerun/nemar-nm000338-openbmi-p4-external-loso-recovery-r1/subject_level_results.csv",
    "results/real/v2-recovery-r2/nemar-nm000311-jeong-p5-external-loso-24subject-r2/subject_level_results.csv",
    "results/real/v2-recovery-r2-independent-rerun/nemar-nm000311-jeong-p5-external-loso-24subject-r2/subject_level_results.csv",
    "results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2/run_records.json",
    "results/real/v2-recovery-r2-independent-rerun/p6_real_replay_initial_state_repeats_r2/run_records.json",
    "patches/myosim_v1_1_initial_state_recovery_r2.patch",
]
OPTIONAL = [
    "deliverables/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.docx",
    "deliverables/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.docx",
    "deliverables/P6_INITIAL_STATE_ROBUSTNESS_AND_DECODER_QUALITY_STATUS_V2_RECOVERY_R3_Q1.docx",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def row(rel: str) -> str:
    path = ROOT / rel
    return f"| `{rel}` | `{sha256(path)}` | {path.stat().st_size} |"


def main() -> None:
    missing = [rel for rel in REQUIRED if not (ROOT / rel).is_file()]
    if missing:
        raise SystemExit("Missing required artefacts: " + ", ".join(missing))
    rows = [row(rel) for rel in REQUIRED]
    optional_rows = [row(rel) for rel in OPTIONAL if (ROOT / rel).is_file()]
    text = [
        "# Verified Artifact Manifest",
        "## V2 Recovery R3 All-Specification Interim Current State",
        "",
        "This manifest lists selected governing, evidence, audit, manuscript, and result artefacts included in the current release. SHA-256 values are calculated from the exact repository bytes at manifest-generation time. It is a release-integrity record, not a new scientific result.",
        "",
        "| Artefact | SHA-256 | Bytes |",
        "|---|---|---:|",
        *rows,
    ]
    if optional_rows:
        text += ["", "## Word Deliverables", "", "| Artefact | SHA-256 | Bytes |", "|---|---|---:|", *optional_rows]
    text += [
        "",
        "## Interpretation",
        "",
        "The manifest confirms retained identities for P4/P5 primary and rerun outputs and P6 primary/rerun aggregate records. It does not change their interpretation. The R3 hard-stop remains binding: P6 does not contain an authenticated three-condition decoder-quality experiment.",
        "",
        "## References",
        "",
        "[1]: audit/V2_R3_INTEGRATION_VALIDATION.md \"R3 Integration Validation\"",
        "[2]: audit/ALL_SPECS_RED_TEAM_AUDIT_RECOVERY_R3.md \"All-Specification Red-Team Audit\"",
        "[3]: audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md \"P6 R3 Replay Identity Hard Stop\"",
        "",
        "The manifest and its interpretation are governed by the release validation and evidence-boundary records.[1] [2] [3]",
        "",
    ]
    OUTPUT.write_text("\n".join(text), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
