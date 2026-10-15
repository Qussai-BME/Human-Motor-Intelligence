#!/usr/bin/env python3
"""Create a deterministic subject-level macro-F1 figure for P5 Recovery R2."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1")
RESULT = ROOT / "results/real/v2-recovery-r2/nemar-nm000311-jeong-p5-external-loso-24subject-r2"
ORDER = ["eeg-only-lda-v1", "late-fusion-lda-v1", "early-fusion-lda-v1", "emg-only-lda-v1"]
LABELS = ["EEG-only\nLDA", "Late fusion\nLDA", "Early fusion\nLDA", "EMG-only\nLDA"]
COLORS = ["#3E6D9C", "#6B8E23", "#C17C37", "#9A4A4A"]


def main() -> None:
    with (RESULT / "subject_level_results.csv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    stats = json.loads((RESULT / "statistics_macro_f1.json").read_text(encoding="utf-8"))
    values = {model: np.asarray([float(row["macro_f1"]) for row in rows if row["model_id"] == model]) for model in ORDER}
    rng = np.random.default_rng(20260824)
    fig, axis = plt.subplots(figsize=(10.2, 6.3), dpi=220)
    axis.set_facecolor("#FBFCFD")
    for index, (model, label, color) in enumerate(zip(ORDER, LABELS, COLORS), start=1):
        sample = values[model]
        jitter = rng.uniform(-0.12, 0.12, size=len(sample))
        axis.scatter(np.full(len(sample), index) + jitter, sample, s=28, color=color, alpha=0.72, edgecolor="white", linewidth=0.45, zorder=3)
        summary = stats["summaries"][model]
        mean = float(summary["mean"])
        lo, hi = summary["bootstrap_95_percent_ci_mean"]
        axis.errorbar(index, mean, yerr=[[mean - lo], [hi - mean]], fmt="o", markersize=8.0, color="#151A20", capsize=6, capthick=1.5, linewidth=1.7, zorder=5)
        axis.text(index, hi + 0.008, f"{mean:.3f}", ha="center", va="bottom", fontsize=9, color="#151A20", fontweight="bold")
    axis.set_xticks(range(1, len(ORDER) + 1), LABELS, fontsize=10)
    axis.set_xlim(0.5, len(ORDER) + 0.5)
    axis.set_ylim(0.0, 0.20)
    axis.set_ylabel("Held-out subject macro-F1", fontsize=11)
    axis.set_title("P5 Jeong2020 external validation — MI-only all-11-class LOSO", loc="left", fontsize=13, fontweight="bold", pad=14)
    axis.text(0.0, 1.02, "24-subject amended source-availability cohort; points are subjects; black markers are mean ± bootstrap 95% CI", transform=axis.transAxes, fontsize=9.2, color="#4F5B66")
    axis.grid(axis="y", color="#D9E0E6", linewidth=0.8, alpha=0.9)
    axis.spines[["top", "right"]].set_visible(False)
    axis.spines[["left", "bottom"]].set_color("#6C7781")
    axis.tick_params(colors="#26313A")
    fig.text(0.01, 0.008, "External validation, not direct replication; macro-F1 is not equated mechanically with nominal 1/11 accuracy reference.", fontsize=8.3, color="#4F5B66")
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    output = RESULT / "p5_jeong_subject_level_macro_f1.png"
    fig.savefig(output, bbox_inches="tight")
    print(output)


if __name__ == "__main__":
    main()
