#!/usr/bin/env python3
"""Create a deterministic initial-state/final-error figure for P6 Recovery R2."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1")
RESULT = ROOT / "results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2"


def main() -> None:
    records = json.loads((RESULT / "run_records.json").read_text(encoding="utf-8"))
    x = np.asarray([float(item["forearm_x_offset_m"]) * 1000.0 for item in records])
    y = np.asarray([float(item["forearm_y_offset_m"]) * 1000.0 for item in records])
    error = np.asarray([float(item["final_error_m"]) * 1000.0 for item in records])
    fig, axis = plt.subplots(figsize=(9.8, 6.4), dpi=220)
    axis.set_facecolor("#FBFCFD")
    scatter = axis.scatter(x, y, c=error, cmap="viridis", s=108, edgecolor="#1E2830", linewidth=0.55, zorder=3)
    for item, x_value, y_value in zip(records, x, y):
        axis.annotate(str(item["seed"])[-2:], (x_value, y_value), xytext=(4, 4), textcoords="offset points", fontsize=7.5, color="#1E2830")
    colorbar = fig.colorbar(scatter, ax=axis, pad=0.02)
    colorbar.set_label("Final planar error (mm)", fontsize=10)
    axis.set_xlim(-0.5, 20.5)
    axis.set_ylim(-16.0, 16.0)
    axis.axhline(0.0, color="#9BA7B0", linewidth=0.8, zorder=1)
    axis.axvline(0.0, color="#9BA7B0", linewidth=0.8, zorder=1)
    axis.set_xlabel("Declared forearm_x initial offset (mm)", fontsize=11)
    axis.set_ylabel("Declared forearm_y initial offset (mm)", fontsize=11)
    axis.set_title("P6 real-replay initial-state repeat cohort", loc="left", fontsize=13, fontweight="bold", pad=14)
    axis.text(0.0, 1.02, "20 distinct declared states; all runs ended in TRANSPORT; no invalid states; color is descriptive final error", transform=axis.transAxes, fontsize=9.3, color="#4F5B66")
    axis.grid(color="#D9E0E6", linewidth=0.8, alpha=0.9)
    axis.spines[["top", "right"]].set_visible(False)
    axis.spines[["left", "bottom"]].set_color("#6C7781")
    fig.text(0.01, 0.01, "Simulation systems result only. Fixed replay/controller; this figure does not estimate a decoder-quality effect or biomedical outcome.", fontsize=8.3, color="#4F5B66")
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    output = RESULT / "p6_initial_state_offsets_final_error.png"
    fig.savefig(output, bbox_inches="tight")
    print(output)


if __name__ == "__main__":
    main()
