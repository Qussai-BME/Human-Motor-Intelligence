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
    for keys, group in frame.groupby(["variant", "level_percent", "condition"], sort=True):
        variant, level, condition = keys
        summaries.append({"variant": variant, "level_percent": int(level), "condition": condition, "n_subjects": int(group["subject"].nunique()), "macro_f1_mean": float(group["macro_f1"].mean()), "macro_f1_sd": float(group["macro_f1"].std(ddof=1)), "accuracy_mean": float(group["accuracy"].mean()), "balanced_accuracy_mean": float(group["balanced_accuracy"].mean()), "selected_eeg_fraction_mean": float(group["selected_eeg_fraction"].mean())})
    pairwise = []
    for (variant, level), group in frame.groupby(["variant", "level_percent"], sort=True):
        pivot = group.pivot(index="subject", columns="condition", values="macro_f1").dropna()
        for left, right in (("confidence_selective_fusion", "eeg_only"), ("confidence_selective_fusion", "static_mean_fusion"), ("confidence_selective_fusion", "confidence_weighted_fusion"), ("confidence_selective_fusion", "emg_only")):
            if left not in pivot or right not in pivot:
                continue
            d = pivot[left] - pivot[right]
            p = 1.0 if (d == 0).all() else float(wilcoxon(pivot[left], pivot[right], method="auto").pvalue)
            pairwise.append({"variant": variant, "level_percent": int(level), "left": left, "right": right, "n_pairs": int(len(pivot)), "p_raw": p, "median_difference": float(d.median()), "mean_difference": float(d.mean())})
    result = {"summary": summaries, "pairwise_macro_f1": pairwise, "claim_boundary": "clean-train corrupted-test feature-group proxy; no raw hardware or clinical claim"}
    (root / "statistics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
