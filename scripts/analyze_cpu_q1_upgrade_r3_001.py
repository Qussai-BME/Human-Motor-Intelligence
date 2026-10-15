from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


def summarize(path: Path) -> dict[str, object]:
    rows = json.loads((path / "subject_level_results.json").read_text(encoding="utf-8"))
    frame = pd.DataFrame(rows)
    summary = []
    for condition, group in frame.groupby("condition", sort=True):
        summary.append({"condition": condition, "n_subjects": int(group["subject"].nunique()), **{f"{metric}_mean": float(group[metric].mean()) for metric in ["macro_f1", "accuracy", "balanced_accuracy"]}, **{f"{metric}_sd": float(group[metric].std(ddof=1)) for metric in ["macro_f1", "accuracy", "balanced_accuracy"]}})
    pairwise = []
    conditions = sorted(frame["condition"].unique())
    for i, left in enumerate(conditions):
        for right in conditions[i + 1:]:
            pivot = frame[frame["condition"].isin([left, right])].pivot(index="subject", columns="condition", values="macro_f1").dropna()
            if len(pivot) >= 2:
                stat = wilcoxon(pivot[left], pivot[right], zero_method="wilcox", alternative="two-sided", method="auto")
                pairwise.append({"left": left, "right": right, "n_pairs": int(len(pivot)), "wilcoxon_stat": float(stat.statistic), "p_raw": float(stat.pvalue), "median_difference_left_minus_right": float(np.median(pivot[left] - pivot[right]))})
    result = {"summary": summary, "pairwise_macro_f1": pairwise, "source": str(path), "claim_boundary": "new CPU extension namespace; not pooled with frozen P4/P5 results"}
    (path / "statistics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: analyze_cpu_q1_upgrade_r3_001.py OUTPUT_DIR...", file=sys.stderr)
        return 2
    for raw in sys.argv[1:]:
        result = summarize(Path(raw))
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
