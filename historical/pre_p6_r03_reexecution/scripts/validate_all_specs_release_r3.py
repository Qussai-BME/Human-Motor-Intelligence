#!/usr/bin/env python3
"""Validate the all-specification R3 interim release without recomputing scientific results."""
from __future__ import annotations

import hashlib
import re
import zipfile
from pathlib import Path

ROOT = Path("<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1")
OUT = ROOT / "audit/ALL_SPECS_RELEASE_VALIDATION_R3.md"
P4 = ROOT / "results/real/v2-recovery-r1/nemar-nm000338-openbmi-p4-external-loso-recovery-r1"
P4R = ROOT / "results/real/v2-recovery-r1-independent-rerun/nemar-nm000338-openbmi-p4-external-loso-recovery-r1"
P5 = ROOT / "results/real/v2-recovery-r2/nemar-nm000311-jeong-p5-external-loso-24subject-r2"
P5R = ROOT / "results/real/v2-recovery-r2-independent-rerun/nemar-nm000311-jeong-p5-external-loso-24subject-r2"
P6 = ROOT / "results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2"
P6R = ROOT / "results/real/v2-recovery-r2-independent-rerun/p6_real_replay_initial_state_repeats_r2"

REQUIRED = [
    "README.md",
    "historical/README_V1_1_BASELINE_PRESERVED.md",
    "PUBLIC_REVIEW_DISCLOSURE_R3.md",
    "PUBLICATION_CHECKLIST_R3.md",
    "LICENSE",
    "NOTICE.md",
    "CITATION.cff",
    "specifications/README.md",
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
    "REPRODUCIBILITY.md",
    "ROADMAP.md",
    "COMMERCIALIZATION_NOTES.md",
    "RELEASE_CHANGELOG.md",
    "RELEASE_NOTES_MASTER_END_TO_END_R3.md",
    "FINAL_PROGRAM_RELEASE_NOTES_R3_ALL_SPECS_INTERIM.md",
    "IMPLEMENTATION_STATUS_RECOVERY_R3.md",
    "VERIFIED_ARTIFACT_MANIFEST.md",
    "audit/SPECIFICATION_COMPLETION_MATRIX_ALL_SPECS_R3.md",
    "audit/ALL_SPECS_RED_TEAM_AUDIT_RECOVERY_R3.md",
    "audit/WORD_RENDER_QA_NOTES_R3.md",
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
    "deliverables/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.docx",
    "deliverables/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.docx",
    "deliverables/P6_INITIAL_STATE_ROBUSTNESS_AND_DECODER_QUALITY_STATUS_V2_RECOVERY_R3_Q1.docx",
]

MARKDOWN_TO_CHECK = [
    ROOT / "README.md",
    ROOT / "PUBLIC_REVIEW_DISCLOSURE_R3.md",
    ROOT / "PUBLICATION_CHECKLIST_R3.md",
    ROOT / "NOTICE.md",
    ROOT / "audit/COMPREHENSIVE_PUBLIC_REVIEW_AUDIT_R3.md",
    ROOT / "audit/MASTER_END_TO_END_SPEC_COMPLIANCE_AUDIT_R3.md",
    ROOT / "audit/MASTER_END_TO_END_PACKAGE_ASSEMBLY_AUDIT_R3.md",
    ROOT / "audit/MASTER_SPEC_PHASE_GATE_LEDGER_R3.md",
    ROOT / "audit/MASTER_SPEC_PHASE4_P3_EVIDENCE_GATE_R3.md",
    ROOT / "audit/MASTER_SPEC_PHASE8_P6_FUNCTIONAL_GATE_R3.md",
    ROOT / "audit/MASTER_SPEC_PHASE10_PRODUCT_DISCOVERY_GATE_R3.md",
    ROOT / "audit/MASTER_SPEC_PHASE_COMPLETION_DOSSIER_R3.md",
    ROOT / "MASTER_END_TO_END_IMPLEMENTATION_STATUS_R3.md",
    ROOT / "docs/RESEARCH_SHOWCASE_QUICKSTART_R3.md",
    ROOT / "docs/MASTER_END_TO_END_ARCHITECTURE_R3.mmd",
    ROOT / "docs/figures/MASTER_END_TO_END_ARCHITECTURE_R3.png",
    ROOT / "FINAL_PROJECT_REPORT_RECOVERY_R3_ADDENDUM.md",
    ROOT / "REAL_DATA_VALIDATION_REPORT.md",
    ROOT / "BENCHMARK_REPORT.md",
    ROOT / "REPRODUCIBILITY_REPORT.md",
    ROOT / "CHILD_PROJECT_VALIDATION_MATRIX.md",
    ROOT / "SCIENTIFIC_LIMITATIONS.md",
    ROOT / "REPRODUCIBILITY.md",
    ROOT / "ROADMAP.md",
    ROOT / "COMMERCIALIZATION_NOTES.md",
    ROOT / "RELEASE_CHANGELOG.md",
    ROOT / "RELEASE_NOTES_MASTER_END_TO_END_R3.md",
    ROOT / "FINAL_PROGRAM_RELEASE_NOTES_R3_ALL_SPECS_INTERIM.md",
    ROOT / "IMPLEMENTATION_STATUS_RECOVERY_R3.md",
    ROOT / "audit/SPECIFICATION_COMPLETION_MATRIX_ALL_SPECS_R3.md",
    ROOT / "audit/ALL_SPECS_RED_TEAM_AUDIT_RECOVERY_R3.md",
]

EXPECTED_HASHES = {
    P4 / "subject_level_results.csv": "ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8",
    P5 / "subject_level_results.csv": "a35b1cb5daa2cdae2078e7668eb1b028e4613c99e062df2b941183c7b971e36b",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8", errors="replace")
    return " ".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml))


def extract_local_targets(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    targets += re.findall(r"^\[[^\]]+\]:\s+([^\s]+)", text, flags=re.MULTILINE)
    return [target for target in targets if not target.startswith(("http://", "https://", "mailto:", "#"))]


def main() -> int:
    missing = [item for item in REQUIRED if not (ROOT / item).is_file()]
    p4_primary = sha256(P4 / "subject_level_results.csv")
    p4_rerun = sha256(P4R / "subject_level_results.csv")
    p5_primary = sha256(P5 / "subject_level_results.csv")
    p5_rerun = sha256(P5R / "subject_level_results.csv")
    p6_primary = sha256(P6 / "run_records.json")
    p6_rerun = sha256(P6R / "run_records.json")
    rerun_checks = [
        ("P4 primary/rerun exactness", p4_primary == p4_rerun == EXPECTED_HASHES[P4 / "subject_level_results.csv"], p4_primary),
        ("P5 primary/rerun exactness", p5_primary == p5_rerun == EXPECTED_HASHES[P5 / "subject_level_results.csv"], p5_primary),
        ("P6 primary/rerun exactness", p6_primary == p6_rerun, p6_primary),
    ]

    forbidden_exts = {".bdf", ".edf", ".gdf", ".set", ".fif", ".npz"}
    forbidden = []
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.suffix.lower() in forbidden_exts:
            forbidden.append(path.relative_to(ROOT).as_posix())

    unresolved_links = []
    for path in MARKDOWN_TO_CHECK:
        # Required assets can include binary files (for example, the rendered
        # architecture PNG). Only text documents are valid Markdown link sources.
        if path.suffix.lower() not in {".md", ".mmd"}:
            continue
        for target in extract_local_targets(path):
            clean_target = target.split("#", 1)[0]
            if not clean_target:
                continue
            if not (path.parent / clean_target).resolve().exists():
                unresolved_links.append(f"{path.relative_to(ROOT)} -> {target}")

    document_expectations = {
        "deliverables/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.docx": [
            "OpenBMI", "Abstract", "Supplementary Appendix", "external validation",
        ],
        "deliverables/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.docx": [
            "EEG", "EMG", "Abstract", "Supplementary Appendix", "amended",
        ],
        "deliverables/P6_INITIAL_STATE_ROBUSTNESS_AND_DECODER_QUALITY_STATUS_V2_RECOVERY_R3_Q1.docx": [
            "Simulator Initial-State", "Supplementary Appendix", "R3 decoder-quality", "Not executed",
        ],
    }
    docx_issues = []
    for rel, expected_terms in document_expectations.items():
        text = docx_text(ROOT / rel)
        absent = [term for term in expected_terms if term not in text]
        if absent:
            docx_issues.append(f"{rel}: missing {', '.join(absent)}")

    appendices = [ROOT / "papers/paper_4/APPENDIX.md", ROOT / "papers/paper_5/APPENDIX.md"]
    nan_occurrences = []
    for path in appendices:
        if re.search(r"\bnan\b", path.read_text(encoding="utf-8"), flags=re.IGNORECASE):
            nan_occurrences.append(path.relative_to(ROOT).as_posix())

    forbidden_paths = [
        ROOT / "audit/V2_PROTOCOL_AMENDMENT_RECOVERY_R2_004.md",
        ROOT / "results/real/v2-recovery-r3",
    ]
    invalid_p6_execution = [path.relative_to(ROOT).as_posix() for path in forbidden_paths if path.exists()]

    passed = not any([missing, forbidden, unresolved_links, docx_issues, nan_occurrences, invalid_p6_execution]) and all(ok for _, ok, _ in rerun_checks)
    rows = [
        ("Required all-specification documents and Word files", not missing, "All required files present" if not missing else "; ".join(missing)),
        ("P4/P5/P6 retained rerun checks", all(ok for _, ok, _ in rerun_checks), "; ".join(f"{name}: {digest}" for name, _, digest in rerun_checks)),
        ("Raw/derived/cache exclusion", not forbidden, "No forbidden extensions" if not forbidden else "; ".join(forbidden)),
        ("Current all-specification local Markdown links", not unresolved_links, "No unresolved local targets" if not unresolved_links else "; ".join(unresolved_links)),
        ("Word content integrity", not docx_issues, "Three DOCX files contain expected title/section/evidence terms" if not docx_issues else "; ".join(docx_issues)),
        ("Appendix raw-p table integrity", not nan_occurrences, "No `nan` values in P4/P5 appendices" if not nan_occurrences else "; ".join(nan_occurrences)),
        ("P6 hard-stop enforcement", not invalid_p6_execution, "No R2_004 or R3 P6 execution namespace present" if not invalid_p6_execution else "; ".join(invalid_p6_execution)),
    ]
    lines = [
        "# All-Specification Release Validation",
        "## V2 Recovery R3 Current-State",
        "",
        "This validation audits release completeness and integrity only. It does not rerun research models or create any new scientific performance outcome.",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]
    for label, ok, detail in rows:
        lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |")
    lines += [
        "",
        "## Mandatory Interpretation",
        "",
        "The expanded release is suitable as a professionally documented interim current-state package. It remains non-final-authoritative: P3 is pending and P6 R3 has not executed any decoder-quality comparison because authentic provenance-linked traces are absent.",
        "",
        "## References",
        "",
        "[1]: SPECIFICATION_COMPLETION_MATRIX_ALL_SPECS_R3.md \"All-Specification Completion Matrix\"",
        "[2]: ALL_SPECS_RED_TEAM_AUDIT_RECOVERY_R3.md \"All-Specification Red-Team Audit\"",
        "[3]: V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md \"P6 R3 Replay Identity Hard Stop\"",
        "",
        "The validation result follows the all-specification matrix, red-team audit, and P6 hard-stop record.[1] [2] [3]",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
