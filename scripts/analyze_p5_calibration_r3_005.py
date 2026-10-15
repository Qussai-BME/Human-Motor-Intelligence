from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> int:
    if len(sys.argv) != 2:
        return 2
    root = Path(sys.argv[1])
    rows = json.loads((root / "trial_probabilities.json").read_text())
    df = pd.DataFrame(rows)
    outputs = []
    for condition, g in df.groupby("condition", sort=True):
        probs = np.asarray(g["probabilities"].tolist(), dtype=float)
        labels = g["label"].to_numpy(dtype=int)
        classes = np.arange(probs.shape[1])
        pred = probs.argmax(axis=1)
        onehot = np.eye(probs.shape[1])[labels]
        brier = float(np.mean(np.sum((probs - onehot) ** 2, axis=1)))
        c = probs.max(axis=1)
        correct = (pred == labels).astype(float)
        bins = []
        ece = 0.0
        for lo, hi in zip(np.linspace(0, 1, 11)[:-1], np.linspace(0, 1, 11)[1:]):
            mask = (c >= lo) & ((c < hi) if hi < 1 else (c <= hi))
            if mask.any():
                acc = float(correct[mask].mean()); mean_c = float(c[mask].mean()); frac = float(mask.mean()); ece += frac * abs(acc - mean_c)
                bins.append({"lower": float(lo), "upper": float(hi), "n": int(mask.sum()), "mean_confidence": mean_c, "accuracy": acc})
        subject = []
        for sub, sg in g.groupby("subject", sort=True):
            p = np.asarray(sg["probabilities"].tolist(), dtype=float); y = sg["label"].to_numpy(dtype=int); pr = p.argmax(1); oh = np.eye(p.shape[1])[y]
            subject.append({"subject": sub, "brier": float(np.mean(np.sum((p-oh)**2, axis=1))), "ece": float(np.mean([abs(float((pr==y)[p.max(1)>=lo].mean()) - float(p.max(1)[p.max(1)>=lo].mean())) * float((p.max(1)>=lo).mean()) for lo in np.linspace(0, .9, 10) if (p.max(1)>=lo).any()]))})
        outputs.append({"condition": condition, "n_trials": int(len(g)), "n_subjects": int(g.subject.nunique()), "brier_score": brier, "ece_10_bin": float(ece), "mean_confidence": float(c.mean()), "accuracy": float(correct.mean()), "confidence_correct_point_biserial": float(np.corrcoef(c, correct)[0,1]) if c.std() and correct.std() else 0.0, "reliability_bins": bins, "subject_level_calibration": subject})
    result = {"conditions": outputs, "claim_boundary": "clean LOSO calibration extension; probabilities are uncalibrated model posteriors; no clinical reliability claim"}
    (root / "calibration_statistics.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
