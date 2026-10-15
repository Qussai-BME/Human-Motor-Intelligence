#!/usr/bin/env python3
"""Analyze the declared P6 R2 initial-state repeat cohort; no decoder-quality inference."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import norm


def wilson_interval(successes: int, total: int, alpha: float = 0.05) -> list[float]:
    if total < 1:
        raise ValueError("total must be positive")
    z = float(norm.ppf(1.0 - alpha / 2.0))
    p = successes / total
    denominator = 1.0 + z * z / total
    centre = (p + z * z / (2.0 * total)) / denominator
    half = z * np.sqrt((p * (1.0 - p) / total) + (z * z / (4.0 * total * total))) / denominator
    return [float(max(0.0, centre - half)), float(min(1.0, centre + half))]


def bootstrap_mean(values: np.ndarray, seed: int = 20260824, resamples: int = 10_000) -> list[float]:
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(values), size=(resamples, len(values)))
    means = values[indices].mean(axis=1)
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def describe(values: list[float], *, seed: int) -> dict[str, Any]:
    array = np.asarray(values, dtype=float)
    return {
        "n": int(len(array)),
        "mean": float(array.mean()),
        "standard_deviation": float(array.std(ddof=1)) if len(array) > 1 else None,
        "median": float(np.median(array)),
        "minimum": float(array.min()),
        "maximum": float(array.max()),
        "bootstrap_95_percent_ci_mean": bootstrap_mean(array, seed=seed),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cohort_dir", type=Path)
    args = parser.parse_args()
    root = args.cohort_dir.resolve()
    protocol = json.loads((root / "protocol.json").read_text(encoding="utf-8"))
    records = json.loads((root / "run_records.json").read_text(encoding="utf-8"))
    expected = list(range(20260901, 20260921))
    observed = [int(item["seed"]) for item in records]
    if protocol["protocol_id"] != "p6-real-replay-initial-state-repeats-recovery-r2" or protocol["mode"] != "primary":
        raise SystemExit("wrong P6 R2 primary cohort identity")
    if observed != expected or protocol["seeds"] != expected or len(records) != 20:
        raise SystemExit("P6 R2 seed cohort is incomplete or reordered")
    states = [tuple(item["initial_qpos"]) for item in records]
    if len(set(states)) != 20:
        raise SystemExit("declared seed cohort did not produce 20 distinct initial qpos vectors")
    if any(item["invalid_state_detected"] for item in records):
        raise SystemExit("invalid simulator state observed; analysis must stop")
    successes = sum(bool(item["success"]) for item in records)
    failures = len(records) - successes
    successful_times = [float(item["completion_time_s"]) for item in records if item["completion_time_s"] is not None]
    output: dict[str, Any] = {
        "analysis_id": "p6-initial-state-repeat-statistics-recovery-r2",
        "protocol_id": protocol["protocol_id"],
        "origin": "real_replay_initial_state_variation",
        "benchmark_eligible": False,
        "cohort_dir": str(root),
        "run_count": len(records),
        "seeds": observed,
        "variation_factor": {
            "distribution_id": "uniform_forearm_xy_v1",
            "forearm_x_offset_m": describe([float(item["forearm_x_offset_m"]) for item in records], seed=20260825),
            "forearm_y_offset_m": describe([float(item["forearm_y_offset_m"]) for item in records], seed=20260826),
            "distinct_initial_qpos_count": len(set(states)),
        },
        "primary_endpoints": {
            "task_success": {"count": successes, "proportion": successes / len(records), "wilson_95_percent_ci": wilson_interval(successes, len(records))},
            "completion_time_successful_runs_s": describe(successful_times, seed=20260827) if successful_times else {"n": 0, "status": "undefined_no_successful_runs"},
            "final_error_m": describe([float(item["final_error_m"]) for item in records], seed=20260828),
        },
        "secondary_endpoints": {
            "task_failure": {"count": failures, "proportion": failures / len(records), "wilson_95_percent_ci": wilson_interval(failures, len(records))},
            "final_state_counts": dict(sorted(Counter(str(item["final_state"]) for item in records).items())),
            "path_length_m": describe([float(item["path_length_m"]) for item in records], seed=20260829),
            "grasp_stability_steps": describe([float(item["grasp_stability_steps"]) for item in records], seed=20260830),
            "command_corrections": describe([float(item["command_corrections"]) for item in records], seed=20260831),
            "invalid_state_count": sum(bool(item["invalid_state_detected"]) for item in records),
        },
        "interpretation_boundary": [
            "The decoder replay stream is fixed across all runs; these data do not estimate a decoder-quality dose response.",
            "The cohort varies only declared initial forearm position and is a simulation systems result, not biomedical validation.",
            "The single unperturbed baseline is a compatibility control, not a comparator cohort for inferential testing.",
        ],
    }
    target = root / "statistics_initial_state_repeats.json"
    target.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"statistics_path": str(target), "success_count": successes, "failure_count": failures, "distinct_initial_qpos_count": len(set(states))}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
