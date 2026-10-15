from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _setup(path: str | Path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def plot_subject_accuracy(frame: pd.DataFrame, output: str | Path) -> None:
    output = _setup(output)
    fig, ax = plt.subplots(figsize=(10, 6))
    for condition, group in frame.groupby("condition"):
        ordered = group.sort_values("test_subject")
        ax.plot(ordered["test_subject"], ordered["accuracy"], marker="o", linewidth=1.6, label=condition)
    ax.set_xlabel("Held-out subject")
    ax.set_ylabel("Accuracy")
    ax.set_title("Strict LOSO accuracy by held-out subject")
    ax.grid(alpha=0.18)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_metric_summary(frame: pd.DataFrame, metric: str, output: str | Path) -> None:
    output = _setup(output)
    summary = frame.groupby("condition")[metric].agg(["mean", "std"]).sort_values("mean")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.errorbar(summary.index, summary["mean"], yerr=summary["std"], fmt="o")
    ax.set_ylabel(metric)
    ax.set_xlabel("Condition")
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.18)
    fig.tight_layout()
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_lambda(history: pd.DataFrame, output: str | Path) -> None:
    output = _setup(output)
    fig, ax = plt.subplots(figsize=(8, 5))
    for condition, group in history.groupby("condition"):
        ordered = group.sort_values("epoch")
        ax.plot(ordered["epoch"], ordered["lambda_"], label=condition)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("λ")
    ax.set_title("Adversarial weighting schedules")
    ax.grid(alpha=0.18)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)
