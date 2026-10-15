from __future__ import annotations

import numpy as np
from scipy.stats import friedmanchisquare, t, wilcoxon


def mean_sd_ci(values: np.ndarray) -> dict[str, float]:
    x = np.asarray(values, dtype=float)
    n = len(x)
    mean = float(np.mean(x))
    sd = float(np.std(x, ddof=1)) if n > 1 else 0.0
    if n > 1:
        half = float(t.ppf(0.975, n - 1) * sd / np.sqrt(n))
        low, high = mean - half, mean + half
    else:
        low = high = mean
    return {"mean": mean, "sd": sd, "ci95_low": float(low), "ci95_high": float(high), "n": n}


def holm_adjust(p_values: list[float]) -> list[float]:
    if not p_values:
        return []
    p = np.asarray(p_values, dtype=float)
    order = np.argsort(p)
    adjusted = np.empty_like(p)
    running = 0.0
    m = len(p)
    for rank, idx in enumerate(order):
        value = min(1.0, (m - rank) * p[idx])
        running = max(running, value)
        adjusted[idx] = running
    return adjusted.tolist()


def paired_condition_stats(condition_values: dict[str, list[float]]) -> dict:
    names = list(condition_values)
    arrays = [np.asarray(condition_values[name], dtype=float) for name in names]
    if not arrays:
        return {"n": 0, "conditions": {}}
    n = len(arrays[0])
    if any(len(a) != n for a in arrays):
        raise ValueError("All conditions must contain the same number of paired subjects")
    result = {
        "n": n,
        "summary": {name: mean_sd_ci(condition_values[name]) for name in names},
        "friedman": None,
        "wilcoxon_vs_first": [],
    }
    if len(arrays) >= 3:
        stat, p = friedmanchisquare(*arrays)
        result["friedman"] = {"statistic": float(stat), "p_value": float(p)}
    if len(arrays) >= 2:
        raw = []
        ref = arrays[0]
        for name, arr in zip(names[1:], arrays[1:]):
            try:
                stat, p = wilcoxon(ref, arr, alternative="two-sided", zero_method="wilcox")
                raw.append((name, float(stat), float(p)))
            except ValueError:
                raw.append((name, float("nan"), float("nan")))
        finite = [x[2] for x in raw if np.isfinite(x[2])]
        adjusted = holm_adjust(finite)
        j = 0
        for name, stat, p in raw:
            p_adj = float(adjusted[j]) if np.isfinite(p) else float("nan")
            result["wilcoxon_vs_first"].append(
                {"condition": name, "statistic": stat, "p_raw": p, "p_holm": p_adj}
            )
            if np.isfinite(p):
                j += 1
    return result
