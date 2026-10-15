from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.signal import welch
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def metrics(y, pred):
    return {"macro_f1": float(f1_score(y, pred, average="macro")), "accuracy": float(accuracy_score(y, pred)), "balanced_accuracy": float(balanced_accuracy_score(y, pred))}


def temporal_features(x: np.ndarray) -> np.ndarray:
    x = x.astype(np.float64, copy=False)
    centered = x - x.mean(axis=2, keepdims=True)
    std = centered.std(axis=2)
    mean_abs = np.mean(np.abs(centered), axis=2)
    diff = np.diff(centered, axis=2)
    diff_std = diff.std(axis=2)
    return np.concatenate([std, mean_abs, diff_std], axis=1)


def spectral_features(x: np.ndarray, fs: float) -> np.ndarray:
    x = x.astype(np.float64, copy=False)
    freqs, pxx = welch(x, fs=fs, nperseg=min(128, x.shape[2]), axis=2)
    bands = ((4.0, 8.0), (8.0, 13.0), (13.0, 30.0), (30.0, 45.0))
    out = []
    for lo, hi in bands:
        mask = (freqs >= lo) & (freqs < hi)
        out.append(np.log1p(np.trapz(pxx[:, :, mask], freqs[mask], axis=2)))
    return np.concatenate(out, axis=1)


def covariance_log_features(x: np.ndarray) -> np.ndarray:
    x = x.astype(np.float64, copy=False)
    x = x - x.mean(axis=2, keepdims=True)
    cov = np.einsum("nct,ndt->ncd", x, x, optimize=True) / max(1, x.shape[2] - 1)
    scale = np.trace(cov, axis1=1, axis2=2) / x.shape[1]
    cov = (cov + np.swapaxes(cov, 1, 2)) / 2.0
    cov += (1e-4 * np.maximum(scale, 1e-8))[:, None, None] * np.eye(x.shape[1])[None, :, :]
    vals, vecs = np.linalg.eigh(cov)
    vals = np.maximum(vals, 1e-6)
    logs = np.einsum("nki,nk,nkj->nij", vecs, np.log(vals), vecs, optimize=True)
    idx = np.triu_indices(x.shape[1])
    f = logs[:, idx[0], idx[1]].copy()
    f[:, idx[0] != idx[1]] *= np.sqrt(2.0)
    return f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=20261004)
    args = ap.parse_args()
    subjects = sorted(args.cache_root.glob("sub-*.npz"), key=lambda p: int(p.stem.split("-")[1]))
    data = {p.stem: np.load(p, allow_pickle=False) for p in subjects}
    feature_cache = {}
    for p in subjects:
        x = data[p.stem]["epochs"]
        fs = float(data[p.stem]["sampling_hz"][0])
        feature_cache[p.stem] = {"temporal": temporal_features(x), "spectral": spectral_features(x, fs), "covariance_log": covariance_log_features(x)}
    records, trials = [], []
    for held in subjects:
        train = [p for p in subjects if p != held]
        ytr = np.concatenate([data[p.stem]["labels"] for p in train])
        yte = data[held.stem]["labels"]
        for condition in ("temporal", "spectral", "covariance_log"):
            xtr = np.concatenate([feature_cache[p.stem][condition] for p in train])
            xte = feature_cache[held.stem][condition]
            model = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(xtr, ytr)
            pred = model.predict(xte)
            records.append({"subject": held.stem, "condition": condition, "classifier": "LDA lsqr shrinkage=auto", **metrics(yte, pred)})
            for i, (label, prediction) in enumerate(zip(yte.tolist(), pred.tolist())):
                trials.append({"subject": held.stem, "condition": condition, "trial": i, "label": int(label), "prediction": int(prediction)})
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "subject_level_results.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    (args.output / "trial_predictions.json").write_text(json.dumps(trials, indent=2), encoding="utf-8")
    (args.output / "protocol.json").write_text(json.dumps({"task": "P4 CPU Q1 representation family ablation", "subjects": len(subjects), "conditions": ["temporal", "spectral", "covariance_log"], "classifier": "LDA lsqr shrinkage=auto", "loso": True, "feature_definitions": {"temporal": "per-channel std, mean absolute deviation, first-difference SD", "spectral": "per-channel log bandpower 4-8/8-13/13-30/30-45 Hz Welch", "covariance_log": "regularized covariance log-Euclidean upper triangle with sqrt(2) off-diagonal scaling"}, "seed": args.seed}, indent=2), encoding="utf-8")
    (args.output / "environment.json").write_text(json.dumps({"python": sys.version, "platform": platform.platform(), "numpy": np.__version__, "timestamp_utc": datetime.now(timezone.utc).isoformat()}, indent=2), encoding="utf-8")
    (args.output / "manifest.json").write_text(json.dumps({"cache_root": str(args.cache_root), "cache_files": {p.name: sha256(p) for p in subjects}, "raw_recordings": "external and not included", "status": "new extension; frozen P4 outputs untouched"}, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
