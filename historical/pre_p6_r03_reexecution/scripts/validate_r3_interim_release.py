#!/usr/bin/env python3
"""Validate R3 integration/release boundaries without recomputing scientific outcomes."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path("<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1")
OUT = ROOT / "audit/V2_R3_INTEGRATION_VALIDATION.md"
P4 = ROOT / "results/real/v2-recovery-r1/nemar-nm000338-openbmi-p4-external-loso-recovery-r1"
P4R = ROOT / "results/real/v2-recovery-r1-independent-rerun/nemar-nm000338-openbmi-p4-external-loso-recovery-r1"
P5 = ROOT / "results/real/v2-recovery-r2/nemar-nm000311-jeong-p5-external-loso-24subject-r2"
P5R = ROOT / "results/real/v2-recovery-r2-independent-rerun/nemar-nm000311-jeong-p5-external-loso-24subject-r2"
P6 = ROOT / "results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2"
P6R = ROOT / "results/real/v2-recovery-r2-independent-rerun/p6_real_replay_initial_state_repeats_r2"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def status(value: bool) -> str:
    return "PASS" if value else "FAIL"


def main() -> int:
    required = [
        ROOT / "papers/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md",
        ROOT / "papers/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md",
        ROOT / "papers/P6_INITIAL_STATE_ROBUSTNESS_AND_DECODER_QUALITY_STATUS_V2_RECOVERY_R3_Q1.md",
        ROOT / "papers/paper_4/APPENDIX.md",
        ROOT / "papers/paper_5/APPENDIX.md",
        ROOT / "papers/paper_6/APPENDIX.md",
        ROOT / "papers/paper_4/Q1_REVIEW.md",
        ROOT / "papers/paper_5/Q1_REVIEW.md",
        ROOT / "papers/paper_6/Q1_REVIEW.md",
        ROOT / "papers/paper_4/EVIDENCE_GAP_AUDIT.md",
        ROOT / "papers/paper_5/EVIDENCE_GAP_AUDIT.md",
        ROOT / "papers/paper_6/EVIDENCE_GAP_AUDIT.md",
        ROOT / "papers/Q1_EVIDENCE_EXPANSION_MASTER_AUDIT_RECOVERY_R3.md",
        ROOT / "papers/SIX_PAPER_RESEARCH_SYNTHESIS_RECOVERY_R3.md",
        ROOT / "papers/CROSS_REFERENCE_AUDIT_RECOVERY_R3.md",
        ROOT / "papers/CLAIM_EVIDENCE_MATRIX_V2_RECOVERY_R3.md",
        ROOT / "papers/REPRODUCIBILITY_MATRIX_V2_RECOVERY_R3.md",
        ROOT / "papers/RESEARCH_GATE_PREPARATION_RECOVERY_R3.md",
        ROOT / "audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md",
        ROOT / "papers/P6_DECODER_QUALITY_EXTENSION_STATUS_V2_RECOVERY_R3.md",
        ROOT / "FINAL_PROGRAM_RELEASE_NOTES.md",
        ROOT / "audit/V2_R3_TEST_EXECUTION_LOG.md",
        ROOT / "audit/V2_R3_PACKAGE_ASSEMBLY_AUDIT.md",
    ]
    required_check = all(path.exists() for path in required)
    p4_primary = digest(P4 / "subject_level_results.csv")
    p4_rerun = digest(P4R / "subject_level_results.csv")
    p5_primary = digest(P5 / "subject_level_results.csv")
    p5_rerun = digest(P5R / "subject_level_results.csv")
    p6_primary = digest(P6 / "run_records.json")
    p6_rerun = digest(P6R / "run_records.json")
    expected = {
        "P4 primary": "ffe44c5b1b989517f82ac30a9e83be3ee666e6689a846671ca9cfc14d5be17e8",
        "P5 primary": "a35b1cb5daa2cdae2078e7668eb1b028e4613c99e062df2b941183c7b971e36b",
    }
    p4_ok = p4_primary == p4_rerun == expected["P4 primary"]
    p5_ok = p5_primary == p5_rerun == expected["P5 primary"]
    p6_ok = p6_primary == p6_rerun

    raw_exts = {".bdf", ".edf", ".gdf", ".set", ".fif"}
    derived_exts = {".npz"}
    raw_files, derived_files = [], []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        suffix = path.suffix.lower()
        if suffix in raw_exts:
            raw_files.append(path.relative_to(ROOT).as_posix())
        if suffix in derived_exts:
            derived_files.append(path.relative_to(ROOT).as_posix())

    # Resolve image targets in the three appendices, allowing standard Markdown relative paths.
    image_issues = []
    for appendix in [ROOT / "papers/paper_4/APPENDIX.md", ROOT / "papers/paper_5/APPENDIX.md", ROOT / "papers/paper_6/APPENDIX.md"]:
        content = appendix.read_text(encoding="utf-8")
        for target in re.findall(r"!\[[^]]*\]\(([^)]+)\)", content):
            if not (appendix.parent / target).resolve().exists():
                image_issues.append(f"{appendix.relative_to(ROOT)} -> {target}")

    # Audit R3 documents only. Historical frozen documents are excluded by design.
    r3_docs = list((ROOT / "papers").glob("*R3*.md")) + [
        ROOT / "papers/paper_4/APPENDIX.md", ROOT / "papers/paper_5/APPENDIX.md", ROOT / "papers/paper_6/APPENDIX.md",
        ROOT / "papers/paper_4/Q1_REVIEW.md", ROOT / "papers/paper_5/Q1_REVIEW.md", ROOT / "papers/paper_6/Q1_REVIEW.md",
        ROOT / "papers/paper_4/EVIDENCE_GAP_AUDIT.md", ROOT / "papers/paper_5/EVIDENCE_GAP_AUDIT.md", ROOT / "papers/paper_6/EVIDENCE_GAP_AUDIT.md",
        ROOT / "FINAL_PROGRAM_RELEASE_NOTES.md",
    ]
    terms = ["real decoder", "tiny-cnn", "worst decoder", "decoder-quality result"]
    questionable = []
    qualifiers = ("not", "no ", "forbidden", "prohibited", "absent", "unmapped", "correction", "blocked", "not executed", "not provenanced", "invalidates", "unproven")
    for path in sorted(set(r3_docs)):
        if not path.exists():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            lowered = line.lower()
            for term in terms:
                if term in lowered and not any(q in lowered for q in qualifiers):
                    questionable.append(f"{path.relative_to(ROOT)}:{line_no}: {line.strip()}")

    report = [
        "# V2 Recovery R3 Interim Integration Validation",
        "",
        "This validation checks release integrity and evidence boundaries only. It does not rerun scientific models or derive new performance measures.",
        "",
        "## Artefact and Reproduction Checks",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
        f"| Required R3 integration documents ({len(required)}) | {status(required_check)} | All required manuscript, appendix, review, audit, and release-note files exist |",
        f"| P4 primary/rerun CSV | {status(p4_ok)} | `{p4_primary}` |",
        f"| P5 primary/rerun CSV | {status(p5_ok)} | `{p5_primary}` |",
        f"| P6 primary/rerun aggregate record | {status(p6_ok)} | primary/rerun SHA-256 `{p6_primary}` |",
        f"| Markdown appendix image targets | {status(not image_issues)} | {'No unresolved targets' if not image_issues else '; '.join(image_issues)} |",
        f"| Raw biosignal exclusion | {status(not raw_files)} | {'No .bdf/.edf/.gdf/.set/.fif in repository' if not raw_files else '; '.join(raw_files)} |",
        f"| Derived-cache exclusion | {status(not derived_files)} | {'No .npz cache in repository' if not derived_files else '; '.join(derived_files)} |",
        f"| R3 terminology audit | {status(not questionable)} | {'No unqualified prohibited P6 terms in current R3 surfaces' if not questionable else 'See findings below'} |",
        "",
        "## Terminology Findings",
        "",
    ]
    report += ([f"- {item}" for item in questionable] if questionable else ["No unqualified occurrence of `real decoder`, `tiny-CNN`, `worst decoder`, or `decoder-quality result` was found in non-historical R3 release surfaces."])
    report += [
        "",
        "## Mandatory Interpretation",
        "",
        "P6 R3 is blocked and unexecuted. The R2 input is an example/integration fixture identified in the R3 replay-identity hard-stop record; it may not be mapped to a decoder-quality condition. This interim release is therefore not the requested final authoritative all-complete R3 package.",
        "",
        "## References",
        "",
        "[1]: V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md \"R3 P6 Replay Identity Hard Stop\"",
        "[2]: ../papers/CROSS_REFERENCE_AUDIT_RECOVERY_R3.md \"R3 Cross-Reference Audit\"",
        "[3]: ../papers/REPRODUCIBILITY_MATRIX_V2_RECOVERY_R3.md \"R3 Reproducibility Matrix\"",
        "",
        "The terminology and release status are governed by the retained hard-stop and R3 programme records.[1] [2] [3]",
    ]
    OUT.write_text("\n".join(report) + "\n", encoding="utf-8")
    return 0 if all([required_check, p4_ok, p5_ok, p6_ok, not image_issues, not raw_files, not derived_files, not questionable]) else 2


if __name__ == "__main__":
    raise SystemExit(main())
