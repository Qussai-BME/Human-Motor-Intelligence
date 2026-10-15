from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
from scipy.stats import wilcoxon


def main() -> int:
    if len(sys.argv) != 2:
        return 2
    root = Path(sys.argv[1])
    frame = pd.DataFrame(json.loads((root / "subject_level_results.json").read_text(encoding="utf-8")))
    summaries = []
    for keys, group in frame.groupby(["arm", "level_percent", "condition"], sort=True):
        arm, level, condition = keys
        summaries.append({"arm": arm, "level_percent": int(level), "condition": condition, "n_subjects": int(group["subject"].nunique()), "macro_f1_mean": float(group["macro_f1"].mean()), "macro_f1_sd": float(group["macro_f1"].std(ddof=1)), "accuracy_mean": float(group["accuracy"].mean()), "balanced_accuracy_mean": float(group["balanced_accuracy"].mean())})
    pairwise = []
    for (arm, level), group in frame.groupby(["arm", "level_percent"], sort=True):
        pivot = group.pivot(index="subject", columns="condition", values="macro_f1").dropna()
        for left, right in (("confidence_weighted_fusion", "eeg_only"), ("confidence_weighted_fusion", "static_mean_fusion"), ("confidence_weighted_fusion", "emg_only")):
            if left in pivot and right in pivot:
                difference = pivot[left] - pivot[right]
                if (difference == 0).all():
                    p_raw = 1.0
                else:
                    p_raw = float(wilcoxon(pivot[left], pivot[right], method="auto").pvalue)
                pairwise.append({"arm": arm, "level_percent": int(level), "left": left, "right": right, "n_pairs": int(len(pivot)), "p_raw": p_raw, "median_difference": float(difference.median())})
    result = {"summary": summaries, "pairwise_macro_f1": pairwise, "claim_boundary": "feature-group perturbation; not raw hardware robustness; new namespace only"}
    (root / "statistics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
