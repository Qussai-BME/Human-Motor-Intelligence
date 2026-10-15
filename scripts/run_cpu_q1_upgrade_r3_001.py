from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def invsqrt(a: np.ndarray, floor: float = 1e-6) -> np.ndarray:
    vals, vecs = eigh((a + a.T) / 2.0)
    vals = np.maximum(vals, floor)
    return (vecs * (1.0 / np.sqrt(vals))) @ vecs.T


def logm_spd(a: np.ndarray, floor: float = 1e-6) -> np.ndarray:
    vals, vecs = eigh((a + a.T) / 2.0)
    vals = np.maximum(vals, floor)
    return (vecs * np.log(vals)) @ vecs.T


def cov_epoch(epoch: np.ndarray, reg: float = 1e-4) -> np.ndarray:
    x = epoch - epoch.mean(axis=1, keepdims=True)
    c = (x @ x.T) / max(1, x.shape[1] - 1)
    scale = float(np.trace(c) / max(1, c.shape[0]))
    return (c + c.T) / 2.0 + reg * max(scale, 1e-8) * np.eye(c.shape[0])


def upper_features(matrix: np.ndarray) -> np.ndarray:
    idx = np.triu_indices(matrix.shape[0])
    values = matrix[idx].copy()
    off = idx[0] != idx[1]
    values[off] *= np.sqrt(2.0)
    return values


def p4_covariances(epochs: np.ndarray) -> np.ndarray:
    x = epochs.astype(np.float64, copy=False)
    x = x - x.mean(axis=2, keepdims=True)
    covariances = np.einsum("nct,ndt->ncd", x, x, optimize=True) / max(1, x.shape[2] - 1)
    scales = np.trace(covariances, axis1=1, axis2=2) / max(1, covariances.shape[1])
    eye = np.eye(covariances.shape[1], dtype=np.float64)
    covariances = (covariances + np.swapaxes(covariances, 1, 2)) / 2.0
    covariances += (1e-4 * np.maximum(scales, 1e-8))[:, None, None] * eye[None, :, :]
    return covariances


def p4_features_from_covariances(covariances: np.ndarray, reference: np.ndarray | None) -> np.ndarray:
    matrices = covariances
    if reference is not None:
        transform = invsqrt(reference)
        matrices = np.einsum("ab,nbc,dc->nad", transform, matrices, transform, optimize=True)
        matrices = (matrices + np.swapaxes(matrices, 1, 2)) / 2.0
    values, vectors = np.linalg.eigh(matrices)
    values = np.maximum(values, 1e-6)
    logs = np.einsum("nki,nk,nkj->nij", vectors, np.log(values), vectors, optimize=True)
    idx = np.triu_indices(logs.shape[1])
    features = logs[:, idx[0], idx[1]].copy()
    off = idx[0] != idx[1]
    features[:, off] *= np.sqrt(2.0)
    return features


def metrics(y: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    return {
        "macro_f1": float(f1_score(y, pred, average="macro")),
        "accuracy": float(accuracy_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
    }


def environment() -> dict[str, object]:
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "protocol_runner": "run_cpu_q1_upgrade_r3_001.py",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def run_p4(cache_root: Path, out: Path, seed: int, conditions: tuple[str, ...] = ("log_euclidean", "aligned_log_euclidean")) -> None:
    subjects = sorted(cache_root.glob("sub-*.npz"), key=lambda p: int(p.stem.split("-")[1]))
    data = {p.stem: np.load(p, allow_pickle=False) for p in subjects}
    covariance_cache = {p.stem: p4_covariances(data[p.stem]["epochs"]) for p in subjects}
    log_feature_cache = ({p.stem: p4_features_from_covariances(covariance_cache[p.stem], None) for p in subjects}
                         if "log_euclidean" in conditions else {})
    records = []
    trial_rows = []
    for held in subjects:
        train_subjects = [p for p in subjects if p != held]
        train_labels = np.concatenate([data[p.stem]["labels"] for p in train_subjects], axis=0)
        held_labels = data[held.stem]["labels"]
        train_covs = np.concatenate([covariance_cache[p.stem] for p in train_subjects], axis=0)
        reference = np.mean(train_covs, axis=0)
        for condition in conditions:
            if condition == "log_euclidean":
                x_train = np.concatenate([log_feature_cache[p.stem] for p in train_subjects], axis=0)
                x_test = log_feature_cache[held.stem]
            else:
                x_train = p4_features_from_covariances(train_covs, reference)
                x_test = p4_features_from_covariances(covariance_cache[held.stem], reference)
            model = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto")
            model.fit(x_train, train_labels)
            pred = model.predict(x_test)
            row = {"subject": held.stem, "condition": condition, **metrics(held_labels, pred)}
            records.append(row)
            for i, (y, p) in enumerate(zip(held_labels.tolist(), pred.tolist())):
                trial_rows.append({"subject": held.stem, "condition": condition, "trial": i, "label": int(y), "prediction": int(p)})
    out.mkdir(parents=True, exist_ok=True)
    (out / "subject_level_results.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    (out / "trial_predictions.json").write_text(json.dumps(trial_rows, indent=2), encoding="utf-8")
    (out / "protocol.json").write_text(json.dumps({"task": "P4 CPU Q1 upgrade", "subjects": len(subjects), "conditions": ["log_euclidean", "aligned_log_euclidean"], "seed": seed, "loso": True, "covariance_regularization": "1e-4 * mean diagonal", "classifier": "LDA lsqr shrinkage=auto"}, indent=2), encoding="utf-8")
    (out / "environment.json").write_text(json.dumps(environment(), indent=2), encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps({"cache_root": str(cache_root), "cache_files": {p.name: sha256(p) for p in subjects}, "source": "derived cache; raw recordings external", "status": "new extension; frozen baselines untouched"}, indent=2), encoding="utf-8")


def entropy_confidence(prob: np.ndarray) -> np.ndarray:
    k = prob.shape[1]
    ent = -(np.clip(prob, 1e-12, 1.0) * np.log(np.clip(prob, 1e-12, 1.0))).sum(axis=1)
    return 1.0 - ent / np.log(max(2, k))


def run_p5(cache_root: Path, out: Path, seed: int) -> None:
    subjects = sorted(cache_root.glob("sub-*.npz"), key=lambda p: int(p.stem.split("-")[1]))
    data = {p.stem: np.load(p, allow_pickle=False) for p in subjects}
    records, trial_rows = [], []
    for held in subjects:
        train_subjects = [p for p in subjects if p != held]
        eeg_x = np.concatenate([data[p.stem]["eeg_features"] for p in train_subjects], axis=0)
        emg_x = np.concatenate([data[p.stem]["emg_features"] for p in train_subjects], axis=0)
        y_train = np.concatenate([data[p.stem]["labels"] for p in train_subjects], axis=0)
        test = data[held.stem]
        y_test = test["labels"]
        models = {}
        for name, x in (("eeg", eeg_x), ("emg", emg_x)):
            model = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto")
            model.fit(x, y_train)
            models[name] = model
        probs = {name: models[name].predict_proba(test[f"{name}_features"]) for name in ("eeg", "emg")}
        classes = models["eeg"].classes_
        eeg_conf = entropy_confidence(probs["eeg"])
        emg_conf = entropy_confidence(probs["emg"])
        weights = eeg_conf / np.maximum(eeg_conf + emg_conf, 1e-12)
        fused = weights[:, None] * probs["eeg"] + (1.0 - weights[:, None]) * probs["emg"]
        predictions = {
            "eeg_only": models["eeg"].predict(test["eeg_features"]),
            "emg_only": models["emg"].predict(test["emg_features"]),
            "static_mean_fusion": classes[np.argmax((probs["eeg"] + probs["emg"]) / 2.0, axis=1)],
            "confidence_weighted_fusion": classes[np.argmax(fused, axis=1)],
        }
        for condition, pred in predictions.items():
            records.append({"subject": held.stem, "condition": condition, **metrics(y_test, pred)})
        for i, y in enumerate(y_test.tolist()):
            row = {"subject": held.stem, "trial": i, "label": int(y), "eeg_confidence": float(eeg_conf[i]), "emg_confidence": float(emg_conf[i]), "eeg_weight": float(weights[i])}
            row.update({f"{name}_prediction": int(pred[i]) for name, pred in predictions.items()})
            trial_rows.append(row)
    out.mkdir(parents=True, exist_ok=True)
    (out / "subject_level_results.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    (out / "trial_predictions.json").write_text(json.dumps(trial_rows, indent=2), encoding="utf-8")
    (out / "protocol.json").write_text(json.dumps({"task": "P5 CPU Q1 upgrade", "subjects": len(subjects), "conditions": list({r["condition"] for r in records}), "fusion": "entropy confidence weighted posterior", "seed": seed, "loso": True, "classifier": "LDA lsqr shrinkage=auto"}, indent=2), encoding="utf-8")
    (out / "environment.json").write_text(json.dumps(environment(), indent=2), encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps({"cache_root": str(cache_root), "cache_files": {p.name: sha256(p) for p in subjects}, "source": "derived cache; raw recordings external", "status": "new extension; frozen baselines untouched"}, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p4-cache", type=Path)
    parser.add_argument("--p5-cache", type=Path)
    parser.add_argument("--p4-out", type=Path)
    parser.add_argument("--p5-out", type=Path)
    parser.add_argument("--seed", type=int, default=20261001)
    parser.add_argument("--p4-conditions", nargs="+", choices=["log_euclidean", "aligned_log_euclidean"], default=["log_euclidean", "aligned_log_euclidean"])
    args = parser.parse_args()
    if args.p4_cache and args.p4_out:
        run_p4(args.p4_cache, args.p4_out, args.seed, tuple(args.p4_conditions))
    if args.p5_cache and args.p5_out:
        run_p5(args.p5_cache, args.p5_out, args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
