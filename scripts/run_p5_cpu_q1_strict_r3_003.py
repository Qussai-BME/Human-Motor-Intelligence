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


def conf(prob: np.ndarray) -> np.ndarray:
    ent = -(np.clip(prob, 1e-12, 1) * np.log(np.clip(prob, 1e-12, 1))).sum(axis=1)
    return 1.0 - ent / np.log(max(2, prob.shape[1]))


def m(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    return {"macro_f1": float(f1_score(y, p, average="macro")), "accuracy": float(accuracy_score(y, p)), "balanced_accuracy": float(balanced_accuracy_score(y, p))}


def indices(n: int, pct: int) -> np.ndarray:
    k = int(round(n * pct / 100.0))
    return np.unique(np.round(np.linspace(0, n - 1, k)).astype(int)) if k else np.asarray([], dtype=int)


def drop(x: np.ndarray, n_channels: int, width: int, pct: int) -> np.ndarray:
    y = x.copy()
    for c in indices(n_channels, pct):
        y[:, c * width:(c + 1) * width] = 0.0
    return y


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=20261003)
    args = ap.parse_args()
    subjects = sorted(args.cache_root.glob("sub-*.npz"), key=lambda p: int(p.stem.split("-")[1]))
    data = {p.stem: np.load(p, allow_pickle=False) for p in subjects}
    test_variants = [("clean", 0), ("eeg_dropout", 10), ("eeg_dropout", 20), ("emg_dropout", 10), ("emg_dropout", 20), ("missing_emg", 0), ("missing_eeg", 0)]
    records, trials = [], []
    for held in subjects:
        train = [p for p in subjects if p != held]
        ytr = np.concatenate([data[p.stem]["labels"] for p in train])
        eegtr = np.concatenate([data[p.stem]["eeg_features"] for p in train])
        emgtr = np.concatenate([data[p.stem]["emg_features"] for p in train])
        eeg_model = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(eegtr, ytr)
        emg_model = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(emgtr, ytr)
        d = data[held.stem]
        y = d["labels"]
        for variant, pct in test_variants:
            eeg = d["eeg_features"].astype(np.float64)
            emg = d["emg_features"].astype(np.float64)
            if variant == "eeg_dropout":
                eeg = drop(eeg, 60, 2, pct)
            elif variant == "emg_dropout":
                emg = drop(emg, 7, 3, pct)
            eeg_available = variant != "missing_eeg"
            emg_available = variant != "missing_emg"
            ep = eeg_model.predict_proba(eeg) if eeg_available else None
            mp = emg_model.predict_proba(emg) if emg_available else None
            classes = eeg_model.classes_
            ec = conf(ep) if ep is not None else None
            mc = conf(mp) if mp is not None else None
            if ep is None:
                available = mp
                selected = np.full(len(y), "emg", dtype=object)
            elif mp is None:
                available = ep
                selected = np.full(len(y), "eeg", dtype=object)
            else:
                available = (ep + mp) / 2.0
                selected = np.where(ec >= mc, "eeg", "emg")
            if ep is None or mp is None:
                weighted = available
                selective = available
            else:
                w = ec / np.maximum(ec + mc, 1e-12)
                weighted = w[:, None] * ep + (1.0 - w[:, None]) * mp
                selective = np.where((ec >= mc)[:, None], ep, mp)
            preds = {
                "eeg_only": classes[np.argmax(ep, axis=1)] if ep is not None else classes[np.argmax(mp, axis=1)],
                "emg_only": classes[np.argmax(mp, axis=1)] if mp is not None else classes[np.argmax(ep, axis=1)],
                "static_mean_fusion": classes[np.argmax(available, axis=1)],
                "confidence_weighted_fusion": classes[np.argmax(weighted, axis=1)],
                "confidence_selective_fusion": classes[np.argmax(selective, axis=1)],
            }
            for name, pred in preds.items():
                records.append({"subject": held.stem, "variant": variant, "level_percent": int(pct), "condition": name, "selected_eeg_fraction": float(np.mean(selected == "eeg")), **m(y, pred)})
            for i, label in enumerate(y.tolist()):
                row = {"subject": held.stem, "variant": variant, "level_percent": int(pct), "trial": i, "label": int(label), "selected_modality": str(selected[i])}
                if ep is not None:
                    row["eeg_confidence"] = float(ec[i])
                if mp is not None:
                    row["emg_confidence"] = float(mc[i])
                row.update({f"{name}_prediction": int(pred[i]) for name, pred in preds.items()})
                trials.append(row)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "subject_level_results.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    (args.output / "trial_predictions.json").write_text(json.dumps(trials, indent=2), encoding="utf-8")
    (args.output / "protocol.json").write_text(json.dumps({"task": "P5 strict CPU Q1 selective fusion clean-train corrupted-test and missing-modality fallback", "subjects": len(subjects), "test_variants": test_variants, "classifier": "LDA lsqr shrinkage=auto", "loso": True, "training_is_clean_for_all_test_variants": True, "confidence_selective_rule": "select modality with higher entropy-derived confidence; ties EEG", "seed": args.seed}, indent=2), encoding="utf-8")
    (args.output / "environment.json").write_text(json.dumps({"python": sys.version, "platform": platform.platform(), "numpy": np.__version__, "timestamp_utc": datetime.now(timezone.utc).isoformat()}, indent=2), encoding="utf-8")
    (args.output / "manifest.json").write_text(json.dumps({"cache_root": str(args.cache_root), "cache_files": {p.name: sha256(p) for p in subjects}, "raw_recordings": "external and not included", "status": "new extension; frozen P5 R2 untouched"}, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
