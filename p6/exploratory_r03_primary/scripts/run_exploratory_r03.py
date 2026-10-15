#!/usr/bin/env python3
"""Generate the released P6 exploratory R03 EEG traces.

This script intentionally implements the exact retained R03 experiment class:
PhysioNet EEGMMIDB R03 motor execution, not motor imagery. It never silently
switches to another run. Data and output locations are supplied explicitly so
no workstation-specific paths leak into the public release.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import trapezoid
from scipy.signal import welch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import pyedflib

FS = 160.0
DEFAULT_SUBJECTS = [f"S{i:03d}" for i in range(1, 21)]
MODELS = ["M1", "M2", "M3"]
RUN_ID = "R03"
MODEL_SPEC = {
    "M1": {"family": "broad_band", "bands": [(8, 30)], "C": 0.1},
    "M2": {"family": "band_pair", "bands": [(8, 12), (13, 30)], "C": 1.0},
    "M3": {"family": "band_pair_asymmetry", "bands": [(8, 12), (13, 30)], "C": 2.0},
}
CONTROL_MAPPING_ID = "R03_T1_to_OPEN_T2_to_CLOSE_abstract_v1"


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require_r03_path(path: Path) -> None:
    if not path.name.endswith("R03.edf"):
        raise ValueError(f"Expected R03 EDF for this released exploratory protocol, got: {path.name}")


def load_subject(data_root: Path, sid: str):
    path = data_root / f"{sid}R03.edf"
    require_r03_path(path)
    if not path.exists():
        raise FileNotFoundError(f"Missing required EDF: {path}")
    reader = pyedflib.EdfReader(str(path))
    try:
        n = reader.signals_in_file
        X = np.asarray([reader.readSignal(i) for i in range(min(64, n))], dtype=np.float32)
        onset, _duration, descriptions = reader.readAnnotations()
    finally:
        reader.close()
    events = []
    for o, code in zip(onset, descriptions):
        code = code.decode() if isinstance(code, bytes) else str(code)
        if code in ("T1", "T2"):
            events.append((float(o), 1 if code == "T1" else 2, code))
    epochs, labels, ids, onsets, source_labels = [], [], [], [], []
    for k, (o, y, code) in enumerate(events):
        a = int(round((o + 1.0) * FS))
        b = int(round((o + 3.5) * FS))
        if b <= X.shape[1]:
            epochs.append(X[:, a:b])
            labels.append(y)
            ids.append(f"{sid}-R03-{k:03d}")
            onsets.append(o)
            source_labels.append(code)
    return np.asarray(epochs), np.asarray(labels), ids, onsets, source_labels


def features(epochs: np.ndarray, model_id: str) -> np.ndarray:
    spec = MODEL_SPEC[model_id]
    channels = [c for c in range(7, 64) if c < epochs.shape[1]]
    output = []
    for trial in epochs:
        row = []
        for channel in channels:
            freqs, power = welch(trial[channel], fs=FS, nperseg=min(256, trial.shape[-1]))
            mask = (freqs >= 4) & (freqs <= 40)
            total = trapezoid(power[mask], freqs[mask]) + 1e-12
            for lo, hi in spec["bands"]:
                band = (freqs >= lo) & (freqs <= hi)
                row.append(np.log((trapezoid(power[band], freqs[band]) + 1e-12) / total))
        output.append(row)
    z = np.asarray(output, dtype=np.float32)
    if model_id == "M3":
        half = z.shape[1] // 2
        z = np.c_[z, z[:, :half] - z[:, half:2 * half]]
    return z


def fit(train_x: np.ndarray, train_y: np.ndarray, model_id: str):
    X = features(train_x, model_id)
    model = Pipeline([
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, C=MODEL_SPEC[model_id]["C"], random_state=1701)),
    ])
    cv = StratifiedKFold(3, shuffle=True, random_state=1701)
    score = float(np.mean(cross_val_score(model, X, train_y, cv=cv, scoring="balanced_accuracy")))
    model.fit(X, train_y)
    return model, score


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, type=Path, help="Directory containing S001R03.edf ... S020R03.edf")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1], help="P6 primary output directory")
    parser.add_argument("--subjects", nargs="+", default=DEFAULT_SUBJECTS, help="Held-out subjects (default: S001..S020)")
    args = parser.parse_args()
    data_root = args.data_root.resolve()
    out = args.output_dir.resolve()
    out.joinpath("results").mkdir(parents=True, exist_ok=True)
    out.joinpath("traces").mkdir(parents=True, exist_ok=True)
    out.joinpath("audit").mkdir(parents=True, exist_ok=True)

    subjects = list(args.subjects)
    data, dataset_manifest = {}, []
    for sid in subjects:
        path = data_root / f"{sid}R03.edf"
        require_r03_path(path)
        data[sid] = load_subject(data_root, sid)
        dataset_manifest.append({"source_file": path.name, "sha256": file_sha(path), "bytes": path.stat().st_size})

    (out / "audit/DATASET_MANIFEST.json").write_text(json.dumps({
        "dataset": "PhysioNet EEG Motor Movement/Imagery Dataset",
        "version": "1.0.0",
        "run": RUN_ID,
        "task_type": "motor_execution",
        "subjects": subjects,
        "sampling_rate_hz": FS,
        "source_url": "https://physionet.org/content/eegmmidb/1.0.0/",
        "doi": "10.13026/C28G6P",
        "raw_files_are_not_redistributed": True,
        "files": dataset_manifest,
    }, indent=2) + "\n")

    rows, traces = [], []
    for test_sid in subjects:
        train = [data[s] for s in subjects if s != test_sid]
        train_x = np.concatenate([x[0] for x in train])
        train_y = np.concatenate([x[1] for x in train])
        test_x, test_y, test_ids, onsets, source_labels = data[test_sid]
        for model_id in MODELS:
            model, cv_score = fit(train_x, train_y, model_id)
            probabilities = model.predict_proba(features(test_x, model_id))
            predictions = model.classes_[np.argmax(probabilities, axis=1)]
            model_dir = out / "traces" / model_id
            model_dir.mkdir(parents=True, exist_ok=True)
            trace = model_dir / f"{model_id}_{test_sid}.csv"
            source_hash = file_sha(data_root / f"{test_sid}R03.edf")
            fields = [
                "trace_id", "subject_id", "dataset", "dataset_version", "source_recording", "run_id",
                "source_event_id", "source_event_label", "source_onset_s", "replay_time_s", "ground_truth",
                "prediction", "confidence", "correct", "modality", "preprocessing_version", "model_family",
                "model_id", "model_version", "source_file_sha256", "control_mapping_id",
            ]
            with trace.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                for i, (event_id, pred, gt, proba, onset, source_label) in enumerate(
                    zip(test_ids, predictions, test_y, probabilities, onsets, source_labels)
                ):
                    writer.writerow({
                        "trace_id": f"{model_id}_{test_sid}_{i:03d}",
                        "subject_id": test_sid,
                        "dataset": "PhysioNet EEGMMIDB",
                        "dataset_version": "1.0.0",
                        "source_recording": f"{test_sid}R03.edf",
                        "run_id": RUN_ID,
                        "source_event_id": event_id,
                        "source_event_label": source_label,
                        "source_onset_s": f"{onset:.6f}",
                        "replay_time_s": f"{onset:.6f}",
                        "ground_truth": "OPEN" if int(gt) == 1 else "CLOSE",
                        "prediction": "OPEN" if int(pred) == 1 else "CLOSE",
                        "confidence": f"{float(np.max(proba)):.8f}",
                        "correct": int(pred) == int(gt),
                        "modality": "EEG",
                        "preprocessing_version": "window_1.0_3.5s_welch_v2",
                        "model_family": MODEL_SPEC[model_id]["family"],
                        "model_id": model_id,
                        "model_version": "p6-exploratory-r03-v1.0",
                        "source_file_sha256": source_hash,
                        "control_mapping_id": CONTROL_MAPPING_ID,
                    })
            trace_hash = file_sha(trace)
            rows.append({
                "model_id": model_id,
                "test_subject": test_sid,
                "n_trials": len(test_y),
                "source_cv_balanced_accuracy": cv_score,
                "heldout_accuracy": float(accuracy_score(test_y, predictions)),
                "heldout_balanced_accuracy": float(balanced_accuracy_score(test_y, predictions)),
                "heldout_log_loss": float(log_loss(test_y, probabilities, labels=model.classes_)),
                "trace": str(trace.relative_to(out)),
                "trace_sha256": trace_hash,
            })
            traces.append({
                "model_id": model_id,
                "subject_id": test_sid,
                "trace": str(trace.relative_to(out)),
                "trace_sha256": trace_hash,
                "source_file": f"{test_sid}R03.edf",
                "source_file_sha256": source_hash,
                "timing_semantics": "replay_time_s equals source_onset_s; no time transformation",
            })

    means = {m: float(np.mean([r["source_cv_balanced_accuracy"] for r in rows if r["model_id"] == m])) for m in MODELS}
    order = sorted(MODELS, key=lambda m: means[m])
    mapping = {"quality_low": order[0], "quality_mid": order[1], "quality_high": order[2]}
    (out / "results/LOSO_RESULTS.json").write_text(json.dumps(rows, indent=2) + "\n")
    (out / "results/QUALITY_MAPPING.json").write_text(json.dumps({
        "neutral_model_ids": MODELS,
        "source_cv_mean_balanced_accuracy": means,
        "ranking_metric": "mean 3-fold balanced accuracy on source training data only",
        "quality_mapping": mapping,
        "frozen_before_task_analysis": True,
        "study_status": "exploratory",
    }, indent=2) + "\n")
    (out / "results/TRACE_MANIFEST.json").write_text(json.dumps({
        "schema": "hmi.p6.trace-manifest.v3",
        "status": "EXPLORATORY_TRACE_GENERATION",
        "trace_count": len(traces),
        "study_status": "exploratory",
        "source_run": RUN_ID,
        "source_task_type": "motor_execution",
        "trace_self_hash_not_embedded": True,
        "hash_rule": "SHA-256 is recorded externally in this manifest; trace CSVs do not contain a self-referential hash column.",
        "authenticity_rule": "direct held-out inference from real EDF; source and trace checksums recorded",
        "control_mapping_id": CONTROL_MAPPING_ID,
        "traces": traces,
    }, indent=2) + "\n")
    (out / "audit/ENVIRONMENT.json").write_text(json.dumps({
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "protocol_run": RUN_ID,
    }, indent=2) + "\n")
    print(json.dumps({"source_cv": means, "quality_mapping": mapping, "traces": len(traces)}, indent=2))


if __name__ == "__main__":
    main()
