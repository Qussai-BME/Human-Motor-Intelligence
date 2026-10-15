#!/usr/bin/env python3
"""Generate Q1 appendices from existing P4/P5/P6 artefacts without recomputation."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path("<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1")
P4 = ROOT / "results/real/v2-recovery-r1/nemar-nm000338-openbmi-p4-external-loso-recovery-r1"
P4_RERUN = ROOT / "results/real/v2-recovery-r1-independent-rerun/nemar-nm000338-openbmi-p4-external-loso-recovery-r1"
P5 = ROOT / "results/real/v2-recovery-r2/nemar-nm000311-jeong-p5-external-loso-24subject-r2"
P5_RERUN = ROOT / "results/real/v2-recovery-r2-independent-rerun/nemar-nm000311-jeong-p5-external-loso-24subject-r2"
P6 = ROOT / "results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2"
P6_RERUN = ROOT / "results/real/v2-recovery-r2-independent-rerun/p6_real_replay_initial_state_repeats_r2"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    line = "| " + " | ".join(headers) + " |\n"
    line += "|" + "|".join("---" for _ in headers) + "|\n"
    for row in rows:
        line += "| " + " | ".join(str(x).replace("|", "\\|") for x in row) + " |\n"
    return line


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def compact_model(value: str) -> str:
    return {
        "eeg-linear-v1": "Linear",
        "eeg-lda-v1": "LDA",
        "eeg-linear-svm-v1": "Linear SVM",
        "eeg-spectral-v1": "Spectral",
        "eeg-lightweight-cnn-tcn-v1": "Compact CNN",
        "eeg-only-lda-v1": "EEG-only LDA",
        "emg-only-lda-v1": "EMG-only LDA",
        "early-fusion-lda-v1": "Early-fusion LDA",
        "late-fusion-lda-v1": "Late-fusion LDA",
    }.get(value, value)


def model_appendix(paper: str, result: Path, rerun: Path, title: str, primary_boundary: str, output: Path) -> None:
    records = load_csv(result / "subject_level_results.csv")
    stats = json.loads((result / "statistics_macro_f1.json").read_text(encoding="utf-8"))
    validation = json.loads((result / "validation.json").read_text(encoding="utf-8"))
    protocol = json.loads((result / "protocol.json").read_text(encoding="utf-8"))
    manifest = json.loads((result / "manifest.json").read_text(encoding="utf-8"))
    text = f"# {paper} Appendix — V2 Recovery R3 Q1 Standard\n\n"
    text += f"## A. Scope and Evidence Boundary\n\n{primary_boundary}\n\n"
    text += "This appendix is rendered from the locked primary artefacts. It does not rerun a model, modify a cohort, or calculate a new result. The primary and independent rerun are separate reproducibility executions, not pooled evidence.\n\n"
    text += "## B. Protocol, Validation, and Reproducibility Record\n\n"
    validation_rows = []
    for gate, payload in validation.items():
        status = payload.get("status", "pass" if isinstance(payload, dict) and not payload.get("failures") else "unknown")
        failures = payload.get("failures", []) if isinstance(payload, dict) else []
        validation_rows.append([gate, str(status), str(len(failures)), "; ".join(str(x) for x in failures) or "—"])
    text += markdown_table(["Gate", "Status", "Failure count", "Failure detail"], validation_rows) + "\n"
    text += markdown_table(
        ["Artefact", "Primary location", "Rerun / check"],
        [
            ["Protocol", "`protocol.json`", f"Protocol ID: `{protocol.get('protocol_id', 'see file')}`"],
            ["Manifest", "`manifest.json`", f"Manifest ID: `{manifest.get('manifest_id', manifest.get('study_id', 'see file'))}`"],
            ["Environment", "`environment.json`", "Captured with primary execution"],
            ["Results", "`subject_level_results.csv`", f"{len(records)} observations; rerun at `{rerun.relative_to(ROOT)}`"],
            ["Statistics", "`statistics_macro_f1.json`", f"{stats.get('inference_unit', 'subject')} is the inference unit"],
        ],
    ) + "\n"
    text += "## C. Full Subject-Level Result Table\n\n"
    rows = []
    for row in records:
        rows.append([
            row["subject_id"],
            compact_model(row["model_id"]),
            row["fold_index"],
            row["seed"],
            f"{float(row['macro_f1']):.6f}",
            f"{float(row['accuracy']):.6f}",
            f"{float(row['balanced_accuracy']):.6f}",
        ])
    text += markdown_table(["Subject", "Condition", "Fold", "Seed", "Macro-F1", "Accuracy", "Balanced accuracy"], rows) + "\n"
    text += "## D. Descriptive and Pairwise Statistical Tables\n\n"
    descriptions = []
    for item in stats.get("descriptive", []):
        descriptions.append([
            compact_model(item.get("model_id", "")),
            f"{item.get('mean', float('nan')):.6f}",
            f"{item.get('std', float('nan')):.6f}",
            f"{item.get('median', float('nan')):.6f}",
            f"{item.get('bootstrap_95_percent_ci_mean', [float('nan'), float('nan')])[0]:.6f}–{item.get('bootstrap_95_percent_ci_mean', [float('nan'), float('nan')])[1]:.6f}",
            str(item.get("n", "")),
        ])
    if descriptions:
        text += markdown_table(["Condition", "Mean", "SD", "Median", "Bootstrap 95% CI", "n"], descriptions) + "\n"
    pairwise_rows = []
    for item in stats.get("pairwise", []):
        pairwise_rows.append([
            compact_model(item.get("model_a", "")),
            compact_model(item.get("model_b", "")),
            str(item.get("wilcoxon_statistic", "")),
            f"{item.get('p_value_raw', item.get('p_value', float('nan'))):.8f}",
            f"{item.get('p_value_holm', float('nan')):.8f}",
            str(item.get("holm_rank", "")),
            f"{item.get('paired_sign_effect', float('nan')):.6f}",
        ])
    text += markdown_table(["Condition A", "Condition B", "Wilcoxon W", "Raw p", "Holm p", "Holm rank", "Paired-sign effect"], pairwise_rows) + "\n"
    omnibus = stats.get("friedman", {})
    text += f"Friedman omnibus: χ²={omnibus.get('statistic', 'see artefact')}, df={omnibus.get('df', 'see artefact')}, p={omnibus.get('p_value', 'see artefact')}.\n\n"
    text += "## E. Figures and Confusion-Matrix Availability\n\n"
    figure_name = "p4_openbmi_subject_level_macro_f1.png" if paper == "P4" else "p5_jeong_subject_level_macro_f1.png"
    text += f"![Subject-level macro-F1 figure](../../results/{result.relative_to(ROOT / 'results')}/{figure_name})\n\n"
    text += "Prediction-level true/predicted label arrays were not retained in the locked public result artefacts. Consequently, no post hoc confusion matrix is generated in this appendix. Recomputing predictions after lock would be a new computation and is not authorized for this integration step. The subject-level outcomes, validation, and statistics above are the complete retained primary evidence.\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")


def p6_appendix(output: Path) -> None:
    records = json.loads((P6 / "run_records.json").read_text(encoding="utf-8"))
    stats = json.loads((P6 / "statistics_initial_state_repeats.json").read_text(encoding="utf-8"))
    protocol = json.loads((P6 / "protocol.json").read_text(encoding="utf-8"))
    text = "# P6 Appendix — V2 Recovery R3 Q1 Standard\n\n"
    text += "## A. Scope and R3 Status\n\n"
    text += "R2 is a 20-state MyoSim integration-fixture stress test. R3 decoder-quality comparison is **not executed** because the retained replay is `synthetic-demo` / `example-decoder-v1` and no immutable mid-tier/best trace with authoritative provenance is available. See `audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md`.\n\n"
    text += "## B. Protocol and Reproducibility Record\n\n"
    text += markdown_table(
        ["Artefact", "Primary record", "Rerun/interpretation"],
        [
            ["Protocol", "`protocol.json`", f"Protocol ID: `{protocol.get('protocol_id', 'see file')}`"],
            ["Replay", "`pick_place_replay.csv`", "R3 audit reclassifies identity as synthetic integration fixture; not decoder-quality condition"],
            ["State factor", "`uniform_forearm_xy_v1`", "20 prespecified seeds; 20 distinct qpos states"],
            ["Primary records", "20 run JSON artefacts plus `run_records.json`", f"Exact rerun at `{P6_RERUN.relative_to(ROOT)}`"],
            ["Statistics", "`statistics_initial_state_repeats.json`", "Wilson proportions and bootstrap continuous summaries"],
        ],
    ) + "\n"
    text += "## C. Full Per-Record Table\n\n"
    rows = []
    for record in records:
        rows.append([
            str(record["seed"]),
            f"{float(record['forearm_x_offset_m']):.6f}",
            f"{float(record['forearm_y_offset_m']):.6f}",
            str(record["success"]),
            str(record["final_state"]),
            "—" if record.get("completion_time_s") is None else f"{float(record['completion_time_s']):.6f}",
            f"{float(record['final_error_m']):.6f}",
            f"{float(record['path_length_m']):.6f}",
            str(record["grasp_stability_steps"]),
            str(record["command_corrections"]),
        ])
    text += markdown_table(["Seed", "x offset (m)", "y offset (m)", "Success", "Final state", "Completion time (s)", "Final error (m)", "Path length (m)", "Stability steps", "Corrections"], rows) + "\n"
    text += "## D. Endpoint Table\n\n"
    primary = stats["primary_endpoints"]
    secondary = stats["secondary_endpoints"]
    text += markdown_table(
        ["Endpoint", "Result"],
        [
            ["Task success", f"{primary['task_success']['count']}/{stats['run_count']}; Wilson 95% CI {primary['task_success']['wilson_95_percent_ci'][0]:.6f}–{primary['task_success']['wilson_95_percent_ci'][1]:.6f}"],
            ["Task failure", f"{secondary['task_failure']['count']}/{stats['run_count']}; Wilson 95% CI {secondary['task_failure']['wilson_95_percent_ci'][0]:.6f}–{secondary['task_failure']['wilson_95_percent_ci'][1]:.6f}"],
            ["Final error mean", f"{primary['final_error_m']['mean']:.6f} m; bootstrap 95% CI {primary['final_error_m']['bootstrap_95_percent_ci_mean'][0]:.6f}–{primary['final_error_m']['bootstrap_95_percent_ci_mean'][1]:.6f}"],
            ["Path length mean", f"{secondary['path_length_m']['mean']:.6f} m; bootstrap 95% CI {secondary['path_length_m']['bootstrap_95_percent_ci_mean'][0]:.6f}–{secondary['path_length_m']['bootstrap_95_percent_ci_mean'][1]:.6f}"],
            ["Final states", ", ".join(f"{k}: {v}" for k, v in secondary['final_state_counts'].items())],
            ["Invalid states", str(secondary['invalid_state_count'])],
        ],
    ) + "\n"
    text += "## E. Figure, Validation, and Confusion-Matrix Availability\n\n"
    text += "![Declared state offsets and descriptive final error](../../results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2/p6_initial_state_offsets_final_error.png)\n\n"
    text += "The baseline compatibility check, post-patch inert-default check, bounded-state preflight, 20-run completeness record, and exact independent rerun are documented in the linked R2 audits. A class confusion matrix is not a meaningful retained endpoint for this simulator task: the locked P6 records task transitions/outcomes rather than a multi-class classifier prediction table. R3 decoder-condition tables do not exist because no valid R3 condition traces were supplied.\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")


def main() -> None:
    model_appendix(
        "P4",
        P4,
        P4_RERUN,
        "P4: Strict zero-calibration OpenBMI external validation",
        "P4 is a 54-subject external binary-MI validation. It is not a direct numerical replication of BCI IV-2a and its pairwise testing is within OpenBMI only.",
        ROOT / "papers/paper_4/APPENDIX.md",
    )
    model_appendix(
        "P5",
        P5,
        P5_RERUN,
        "P5: Amended Jeong2020 all-11-class external fusion validation",
        "P5 is a 24-subject amended external MI-only validation. It is not a direct replication of frozen Cho2017 and no score may be pooled across sources.",
        ROOT / "papers/paper_5/APPENDIX.md",
    )
    p6_appendix(ROOT / "papers/paper_6/APPENDIX.md")
    print(json.dumps({"p4": "papers/paper_4/APPENDIX.md", "p5": "papers/paper_5/APPENDIX.md", "p6": "papers/paper_6/APPENDIX.md"}, indent=2))


if __name__ == "__main__":
    main()
