#!/usr/bin/env python3
"""Subject-level P5 Recovery R2 statistics for an immutable Jeong result directory."""
from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import friedmanchisquare, wilcoxon


def bootstrap_mean_ci(values: np.ndarray, *, seed: int, resamples: int = 10_000) -> list[float]:
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(values), size=(resamples, len(values)))
    means = values[indices].mean(axis=1)
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def holm_adjust(records: list[dict[str, Any]]) -> None:
    ordered = sorted(enumerate(records), key=lambda item: float(item[1]["p_value_raw"]))
    running = 0.0
    family = len(records)
    for rank, (index, record) in enumerate(ordered):
        adjusted = min(1.0, (family - rank) * float(record["p_value_raw"]))
        running = max(running, adjusted)
        records[index]["holm_rank"] = rank + 1
        records[index]["p_value_holm"] = running


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result_dir", type=Path)
    parser.add_argument("--metric", default="macro_f1")
    parser.add_argument("--seed", type=int, default=20260824)
    args = parser.parse_args()
    root = args.result_dir.resolve()
    source = root / "subject_level_results.csv"
    if not source.is_file():
        raise SystemExit(f"subject-level result file not found: {source}")
    with source.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("no subject-level result rows")
    required = {"model_id", "subject_id", args.metric, "external_validation", "direct_replication", "protocol_id", "dataset_id"}
    missing = required - set(rows[0])
    if missing:
        raise SystemExit(f"required columns missing: {sorted(missing)}")
    if any(row["external_validation"].lower() != "true" or row["direct_replication"].lower() != "false" for row in rows):
        raise SystemExit("result identity is not external_validation=true/direct_replication=false")
    protocol_ids = {row["protocol_id"] for row in rows}
    datasets = {row["dataset_id"] for row in rows}
    if protocol_ids != {"nemar-nm000311-jeong-p5-external-loso-24subject-r2"} or datasets != {"nemar-nm000311-jeong2020"}:
        raise SystemExit("result directory does not match the locked P5 R2 identity")
    models = sorted({row["model_id"] for row in rows})
    subjects = sorted({row["subject_id"] for row in rows})
    values: dict[str, dict[str, float]] = {model: {} for model in models}
    for row in rows:
        model, subject = row["model_id"], row["subject_id"]
        if subject in values[model]:
            raise SystemExit(f"duplicate observation: {model}/{subject}")
        values[model][subject] = float(row[args.metric])
    if any(set(values[model]) != set(subjects) for model in models):
        raise SystemExit("model subject sets differ; paired inference is invalid")
    arrays = {model: np.asarray([values[model][subject] for subject in subjects], dtype=float) for model in models}
    summaries: dict[str, dict[str, Any]] = {}
    for index, model in enumerate(models):
        item = arrays[model]
        summaries[model] = {
            "n_subjects": len(item),
            "mean": float(item.mean()),
            "standard_deviation": float(item.std(ddof=1)),
            "median": float(np.median(item)),
            "minimum": float(item.min()),
            "maximum": float(item.max()),
            "bootstrap_95_percent_ci_mean": bootstrap_mean_ci(item, seed=args.seed + index),
        }
    statistic, omnibus_p = friedmanchisquare(*(arrays[model] for model in models))
    pairwise: list[dict[str, Any]] = []
    for first, second in itertools.combinations(models, 2):
        diff = arrays[first] - arrays[second]
        nonzero = diff[diff != 0]
        if len(nonzero) == 0:
            test_statistic, p_value = 0.0, 1.0
        else:
            test = wilcoxon(arrays[first], arrays[second], alternative="two-sided", zero_method="wilcox", method="auto")
            test_statistic, p_value = float(test.statistic), float(test.pvalue)
        paired_sd = float(diff.std(ddof=1))
        pairwise.append({
            "model_a": first,
            "model_b": second,
            "metric": args.metric,
            "n_subjects": len(subjects),
            "mean_paired_difference_a_minus_b": float(diff.mean()),
            "median_paired_difference_a_minus_b": float(np.median(diff)),
            "standardized_mean_difference_paired": float(diff.mean() / paired_sd) if paired_sd > 0 else None,
            "paired_sign_effect": float((np.sum(nonzero > 0) - np.sum(nonzero < 0)) / len(nonzero)) if len(nonzero) else 0.0,
            "wilcoxon_statistic": test_statistic,
            "p_value_raw": p_value,
        })
    holm_adjust(pairwise)
    payload = {
        "analysis_id": "p5-jeong-subject-level-statistics-recovery-r2",
        "result_directory": str(root),
        "metric": args.metric,
        "inference_unit": "subject",
        "external_validation": True,
        "direct_replication": False,
        "protocol_id": next(iter(protocol_ids)),
        "dataset_id": next(iter(datasets)),
        "bootstrap": {"resamples": 10_000, "percentile_interval": 0.95, "seed": args.seed},
        "subject_count": len(subjects),
        "models": models,
        "subjects": subjects,
        "summaries": summaries,
        "omnibus": {
            "test": "Friedman chi-square",
            "statistic": float(statistic),
            "p_value": float(omnibus_p),
            "conditions": len(models),
            "subjects": len(subjects),
            "interpretation": "Within-Jeong paired model-comparison result only; it does not rank or pool metrics against frozen Cho2017 evidence.",
        },
        "pairwise": pairwise,
        "multiplicity": {"method": "Holm", "family": "all six predeclared P5 R2 model-pair comparisons", "comparison_count": len(pairwise)},
        "limitations": [
            "Bootstrap intervals summarize the retained 24-subject cohort and are not population guarantees.",
            "This is an amended source-availability cohort, not a direct replication of frozen Cho2017.",
            "Independent deterministic rerun is required before final manuscript integration.",
        ],
    }
    target = root / f"statistics_{args.metric}.json"
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"statistics_path": str(target), "subject_count": len(subjects), "models": models, "friedman_p_value": float(omnibus_p)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
