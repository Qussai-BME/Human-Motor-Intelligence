from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


def bootstrap_ci(values: np.ndarray, seed: int = 20261004, n: int = 20000) -> list[float]:
    rng = np.random.default_rng(seed)
    draws = rng.choice(values, size=(n, values.size), replace=True).mean(axis=1)
    return [float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))]


def sign_flip_p(values: np.ndarray, seed: int = 20261004, n: int = 20000) -> float:
    rng = np.random.default_rng(seed)
    observed = abs(float(values.mean()))
    signs = rng.choice(np.array([-1.0, 1.0]), size=(n, values.size))
    null = np.abs((signs * values[None, :]).mean(axis=1))
    return float((1.0 + np.sum(null >= observed)) / (n + 1.0))


def summarize(left: pd.Series, right: pd.Series, label: str) -> dict[str, object]:
    d = (left - right).to_numpy(dtype=float)
    if np.allclose(d, 0.0):
        wilcox_p = 1.0
    else:
        wilcox_p = float(wilcoxon(left, right, method="auto").pvalue)
    return {"comparison": label, "n_subjects": int(d.size), "mean_difference": float(d.mean()), "median_difference": float(np.median(d)), "sd_difference": float(d.std(ddof=1)), "bootstrap_95_ci_mean_difference": bootstrap_ci(d), "wilcoxon_p_raw": wilcox_p, "sign_flip_permutation_p": sign_flip_p(d), "paired_effect_size_mean_over_sd": float(d.mean() / d.std(ddof=1)) if d.std(ddof=1) else 0.0}


def main() -> int:
    if len(sys.argv) != 3:
        return 2
    ext_root = Path(sys.argv[1])
    frozen_csv = Path(sys.argv[2])
    ext = pd.DataFrame(json.loads((ext_root / "subject_level_results.json").read_text(encoding="utf-8")))
    baseline = pd.read_csv(frozen_csv)
    best = baseline[baseline["model_id"] == "eeg-lightweight-cnn-tcn-v1"][["subject_id", "macro_f1", "accuracy", "balanced_accuracy"]].rename(columns={"subject_id": "subject", "macro_f1": "best_baseline_macro_f1", "accuracy": "best_baseline_accuracy", "balanced_accuracy": "best_baseline_balanced_accuracy"})
    pivot = ext.pivot(index="subject", columns="condition", values="macro_f1").reset_index()
    merged = best.merge(pivot, on="subject", validate="one_to_one")
    comparisons = []
    for left, right, label in (("best_baseline_macro_f1", "covariance_log", "best_frozen_baseline_minus_covariance_log"), ("temporal", "covariance_log", "temporal_minus_covariance_log"), ("spectral", "covariance_log", "spectral_minus_covariance_log"), ("temporal", "spectral", "temporal_minus_spectral")):
        comparisons.append(summarize(merged[left], merged[right], label))
    summaries = []
    for condition in ("temporal", "spectral", "covariance_log"):
        col = merged[condition]
        summaries.append({"condition": condition, "n_subjects": int(col.size), "macro_f1_mean": float(col.mean()), "macro_f1_sd": float(col.std(ddof=1)), "macro_f1_min": float(col.min()), "macro_f1_max": float(col.max())})
    result = {"summary": summaries, "paired_comparisons": comparisons, "best_frozen_model": "eeg-lightweight-cnn-tcn-v1", "claim_boundary": "new representation extension; no pooling with frozen P4; covariance geometry alone is not a superiority claim"}
    (ext_root / "statistics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (ext_root / "paired_subject_table.csv").write_text(merged.to_csv(index=False), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
