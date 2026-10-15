from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def confidence(prob: np.ndarray) -> np.ndarray:
    k = prob.shape[1]
    ent = -(np.clip(prob, 1e-12, 1.0) * np.log(np.clip(prob, 1e-12, 1.0))).sum(axis=1)
    return 1.0 - ent / np.log(max(2, k))


def metrics(y: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    return {"macro_f1": float(f1_score(y, pred, average="macro")), "accuracy": float(accuracy_score(y, pred)), "balanced_accuracy": float(balanced_accuracy_score(y, pred))}


def dropout_indices(n_channels: int, level: int) -> np.ndarray:
    count = int(round(n_channels * level / 100.0))
    if count == 0:
        return np.asarray([], dtype=int)
    return np.unique(np.round(np.linspace(0, n_channels - 1, count)).astype(int))


def corrupt(x: np.ndarray, n_channels: int, n_features_per_channel: int, level: int) -> np.ndarray:
    out = x.copy()
    for channel in dropout_indices(n_channels, level):
        start = channel * n_features_per_channel
        out[:, start:start + n_features_per_channel] = 0.0
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20261002)
    args = parser.parse_args()
    subjects = sorted(args.cache_root.glob("sub-*.npz"), key=lambda p: int(p.stem.split("-")[1]))
    data = {p.stem: np.load(p, allow_pickle=False) for p in subjects}
    records, trial_rows = [], []
    levels = (0, 10, 20)
    arms = ("emg_corruption", "eeg_corruption", "missing_emg", "missing_eeg")
    for held in subjects:
        train_subjects = [p for p in subjects if p != held]
        y_train = np.concatenate([data[p.stem]["labels"] for p in train_subjects])
        y_test = data[held.stem]["labels"]
        for arm in arms:
            arm_levels = levels if "corruption" in arm else (0,)
            for level in arm_levels:
                def transform(d, modality):
                    eeg = d["eeg_features"].astype(np.float64)
                    emg = d["emg_features"].astype(np.float64)
                    if arm == "emg_corruption":
                        emg = corrupt(emg, 7, 3, level)
                    elif arm == "eeg_corruption":
                        eeg = corrupt(eeg, 60, 2, level)
                    elif arm == "missing_emg":
                        emg = np.zeros_like(emg)
                    elif arm == "missing_eeg":
                        eeg = np.zeros_like(eeg)
                    return eeg, emg
                train_eeg = np.concatenate([transform(data[p.stem], "eeg")[0] for p in train_subjects])
                train_emg = np.concatenate([transform(data[p.stem], "emg")[1] for p in train_subjects])
                test_eeg, test_emg = transform(data[held.stem], "test")
                eeg_model = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(train_eeg, y_train)
                emg_model = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(train_emg, y_train)
                eeg_prob = eeg_model.predict_proba(test_eeg)
                emg_prob = emg_model.predict_proba(test_emg)
                eeg_conf = confidence(eeg_prob)
                emg_conf = confidence(emg_prob)
                weight = eeg_conf / np.maximum(eeg_conf + emg_conf, 1e-12)
                classes = eeg_model.classes_
                preds = {
                    "eeg_only": classes[np.argmax(eeg_prob, axis=1)],
                    "emg_only": classes[np.argmax(emg_prob, axis=1)],
                    "static_mean_fusion": classes[np.argmax((eeg_prob + emg_prob) / 2.0, axis=1)],
                    "confidence_weighted_fusion": classes[np.argmax(weight[:, None] * eeg_prob + (1.0 - weight[:, None]) * emg_prob, axis=1)],
                }
                for condition, pred in preds.items():
                    records.append({"subject": held.stem, "arm": arm, "level_percent": level, "condition": condition, **metrics(y_test, pred)})
                for i, y in enumerate(y_test.tolist()):
                    row = {"subject": held.stem, "arm": arm, "level_percent": level, "trial": i, "label": int(y), "eeg_confidence": float(eeg_conf[i]), "emg_confidence": float(emg_conf[i]), "eeg_weight": float(weight[i])}
                    row.update({f"{name}_prediction": int(pred[i]) for name, pred in preds.items()})
                    trial_rows.append(row)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "subject_level_results.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    (args.output / "trial_predictions.json").write_text(json.dumps(trial_rows, indent=2), encoding="utf-8")
    (args.output / "protocol.json").write_text(json.dumps({"task": "P5 CPU Q1 corruption and missing-modality extension", "subjects": len(subjects), "arms": list(arms), "levels_percent": list(levels), "dropout": "deterministic evenly spaced feature groups", "classifier": "LDA lsqr shrinkage=auto", "loso": True, "seed": args.seed}, indent=2), encoding="utf-8")
    (args.output / "environment.json").write_text(json.dumps({"python": sys.version, "platform": platform.platform(), "numpy": np.__version__, "timestamp_utc": datetime.now(timezone.utc).isoformat()}, indent=2), encoding="utf-8")
    (args.output / "manifest.json").write_text(json.dumps({"cache_root": str(args.cache_root), "cache_files": {p.name: sha256(p) for p in subjects}, "raw_recordings": "external and not included", "status": "new extension; frozen P5 R2 untouched"}, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
