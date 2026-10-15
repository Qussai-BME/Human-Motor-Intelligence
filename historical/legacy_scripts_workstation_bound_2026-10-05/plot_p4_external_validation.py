#!/usr/bin/env python3
"""Create a deterministic P4 OpenBMI subject-level macro-F1 figure."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


REPO = Path("<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1")
RESULT = REPO / "results/real/v2-recovery-r1/nemar-nm000338-openbmi-p4-external-loso-recovery-r1"


def main() -> None:
    with (RESULT / "subject_level_results.csv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    stats = json.loads((RESULT / "statistics_macro_f1.json").read_text(encoding="utf-8"))
    models = [
        "eeg-linear-v1",
        "eeg-lda-v1",
        "eeg-linear-svm-v1",
        "eeg-spectral-v1",
        "eeg-lightweight-cnn-tcn-v1",
    ]
    labels = ["Linear", "LDA", "Linear SVM", "Spectral", "Compact CNN"]
    values = {
        model: np.asarray([float(row["macro_f1"]) for row in rows if row["model_id"] == model], dtype=float)
        for model in models
    }
    if any(len(values[model]) != 54 for model in models):
        raise SystemExit("expected 54 subject-level observations per P4 condition")
    colors = ["#5679A6", "#799CBE", "#72A394", "#C9934B", "#A26B8D"]
    rng = np.random.default_rng(20260823)
    fig, ax = plt.subplots(figsize=(11.2, 6.5), layout="constrained")
    for index, (model, label, color) in enumerate(zip(models, labels, colors), start=1):
        array = values[model]
        jitter = rng.uniform(-0.10, 0.10, size=len(array))
        ax.scatter(np.full(len(array), index) + jitter, array, s=24, color=color, alpha=0.43, linewidths=0, zorder=2)
        mean = stats["summaries"][model]["mean"]
        lower, upper = stats["summaries"][model]["bootstrap_95_percent_ci_mean"]
        ax.errorbar(index, mean, yerr=[[mean - lower], [upper - mean]], fmt="D", color="#1F2933", markersize=6.5, capsize=5, linewidth=1.8, zorder=4)
    ax.axhline(0.5, color="#4C566A", linestyle="--", linewidth=1.2, zorder=1)
    ax.text(5.45, 0.507, "Nominal binary\naccuracy reference", ha="right", va="bottom", fontsize=9, color="#4C566A")
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.25, 1.0)
    ax.set_xticks(range(1, 6), labels)
    ax.set_ylabel("Held-out subject macro-F1")
    ax.set_title("OpenBMI external validation: zero-calibration subject-level LOSO")
    ax.text(
        0.01,
        -0.19,
        "Each point is one held-out subject (n=54 per condition). Diamonds show mean and 10,000-resample bootstrap 95% CI.\n"
        "OpenBMI is a harmonized external validation, not a direct replication of BCI Competition IV-2a.",
        transform=ax.transAxes,
        fontsize=9,
        va="top",
    )
    ax.spines[["top", "right"]].set_visible(False)
    output = RESULT / "p4_openbmi_subject_level_macro_f1.png"
    fig.savefig(output, dpi=220, bbox_inches="tight")
    print(output)


if __name__ == "__main__":
    main()
