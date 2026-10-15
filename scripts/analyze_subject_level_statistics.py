#!/usr/bin/env python3
"""Subject-level statistics for immutable V2 external-validation result directories."""
from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import friedmanchisquare, wilcoxon


def percentile_bootstrap(values: np.ndarray, *, seed: int, resamples: int = 10_000) -> list[float]:
    rng = np.random.default_rng(seed)
    sample_indices = rng.integers(0, len(values), size=(resamples, len(values)))
    means = values[sample_indices].mean(axis=1)
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def holm_adjust(records: list[dict[str, Any]]) -> None:
    count = len(records)
    ordered = sorted(enumerate(records), key=lambda item: item[1]["p_value_raw"])
    running = 0.0
    for rank, (index, record) in enumerate(ordered):
        adjusted = min(1.0, (count - rank) * float(record["p_value_raw"]))
        running = max(running, adjusted)
        records[index]["p_value_holm"] = running
        records[index]["holm_rank"] = rank + 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result_dir", type=Path)
    parser.add_argument("--metric", default="macro_f1")
    parser.add_argument("--seed", type=int, default=20260823)
    args = parser.parse_args()
    result_dir = args.result_dir.resolve()
    result_path = result_dir / "subject_level_results.csv"
    if not result_path.is_file():
        raise SystemExit(f"subject-level result file not found: {result_path}")
    with result_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("no subject-level result rows")
    required = {"model_id", "subject_id", args.metric, "external_validation", "direct_replication"}
    missing = required - set(rows[0])
    if missing:
        raise SystemExit(f"required columns missing: {sorted(missing)}")
    if any(row["external_validation"].lower() != "true" or row["direct_replication"].lower() != "false" for row in rows):
        raise SystemExit("result file does not have required external-validation identity labels")
    models = sorted({row["model_id"] for row in rows})
    subjects = sorted({row["subject_id"] for row in rows})
    values: dict[str, dict[str, float]] = {model: {} for model in models}
    for row in rows:
        model = row["model_id"]
        subject = row["subject_id"]
        if subject in values[model]:
            raise SystemExit(f"duplicate subject/model observation: {subject}/{model}")
        values[model][subject] = float(row[args.metric])
    if any(set(values[model]) != set(subjects) for model in models):
        raise SystemExit("all models must cover the identical subject set for paired inference")
    summaries: dict[str, dict[str, Any]] = {}
    arrays: dict[str, np.ndarray] = {}
    for index, model in enumerate(models):
        array = np.asarray([values[model][subject] for subject in subjects], dtype=float)
        arrays[model] = array
        summaries[model] = {
            "n_subjects": len(array),
            "mean": float(array.mean()),
            "standard_deviation": float(array.std(ddof=1)),
            "median": float(np.median(array)),
            "minimum": float(array.min()),
            "maximum": float(array.max()),
            "bootstrap_95_percent_ci_mean": percentile_bootstrap(array, seed=args.seed + index),
        }
    friedman_statistic, friedman_p = friedmanchisquare(*(arrays[model] for model in models))
    comparisons: list[dict[str, Any]] = []
    for first, second in itertools.combinations(models, 2):
        difference = arrays[first] - arrays[second]
        nonzero = difference[difference != 0]
        if len(nonzero) == 0:
            statistic, p_value = 0.0, 1.0
        else:
            test = wilcoxon(arrays[first], arrays[second], alternative="two-sided", zero_method="wilcox", method="auto")
            statistic, p_value = float(test.statistic), float(test.pvalue)
        paired_sd = float(difference.std(ddof=1))
        comparisons.append({
            "model_a": first,
            "model_b": second,
            "metric": args.metric,
            "n_subjects": len(subjects),
            "mean_paired_difference_a_minus_b": float(difference.mean()),
            "median_paired_difference_a_minus_b": float(np.median(difference)),
            "standardized_mean_difference_paired": float(difference.mean() / paired_sd) if paired_sd > 0 else None,
            "paired_sign_effect": float((np.sum(nonzero > 0) - np.sum(nonzero < 0)) / len(nonzero)) if len(nonzero) else 0.0,
            "wilcoxon_statistic": statistic,
            "p_value_raw": p_value,
        })
    holm_adjust(comparisons)
    payload = {
        "analysis_id": "v2-subject-level-statistics-recovery-r1",
        "result_directory": str(result_dir),
        "metric": args.metric,
        "inference_unit": "subject",
        "external_validation": True,
        "direct_replication": False,
        "bootstrap": {"resamples": 10_000, "percentile_interval": 0.95, "seed": args.seed},
        "subject_count": len(subjects),
        "models": models,
        "subjects": subjects,
        "summaries": summaries,
        "omnibus": {
            "test": "Friedman chi-square",
            "statistic": float(friedman_statistic),
            "p_value": float(friedman_p),
            "conditions": len(models),
            "subjects": len(subjects),
            "interpretation": "Descriptive inferential output under the locked within-subject model comparison; it does not compare OpenBMI scores numerically to another dataset.",
        },
        "pairwise": comparisons,
        "multiplicity": {"method": "Holm", "family": "all predeclared model-pair comparisons", "comparison_count": len(comparisons)},
        "limitations": [
            "Confidence intervals are nonparametric bootstrap intervals across held-out subjects, not population guarantees.",
            "All pairwise tests are within OpenBMI only; they do not support numeric cross-dataset ranking.",
            "This output awaits an independent deterministic rerun before final manuscript integration.",
        ],
    }
    target = result_dir / f"statistics_{args.metric}.json"
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"statistics_path": str(target), "subject_count": len(subjects), "models": models, "friedman_p_value": float(friedman_p)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
