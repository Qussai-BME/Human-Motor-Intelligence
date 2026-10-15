#!/usr/bin/env python3
"""Execute the registered P6-C motor-imagery LOSO decoder stage."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss

from p6_mi_core import (
    CONTROL_MAPPING_ID,
    DATASET,
    DATASET_VERSION,
    FS,
    MODEL_VERSION,
    MODELS,
    PREPROCESSING_VERSION,
    RUN_ID,
    control_label,
    environment_payload,
    fit_source_model,
    read_eegmmidb_r04,
    sha256_file,
    write_json,
)

DEFAULT_SUBJECTS = [f"S{i:03d}" for i in range(1, 21)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--subjects", nargs="+", default=DEFAULT_SUBJECTS)
    parser.add_argument("--seed", type=int, default=1701)
    args = parser.parse_args()

    root = args.output_dir.resolve()
    data_root = args.data_root.resolve()
    subjects = list(args.subjects)
    for sid in subjects:
        if sid not in DEFAULT_SUBJECTS:
            raise ValueError(f"Unsupported subject: {sid}")

    data: dict[str, tuple] = {}
    manifest: list[dict] = []
    for sid in subjects:
        path = data_root / sid / f"{sid}{RUN_ID}.edf"
        if not path.exists():
            # Also accept a flat directory because PhysioNet mirrors are commonly flattened.
            path = data_root / f"{sid}{RUN_ID}.edf"
        if not path.exists():
            raise FileNotFoundError(f"Missing required R04 EDF: {path}")
        data[sid] = read_eegmmidb_r04(path)
        epochs, labels, ids, onsets, source_labels = data[sid]
        classes, counts = np.unique(labels, return_counts=True)
        if set(classes.tolist()) != {1, 2}:
            raise ValueError(f"R04 subject {sid} does not contain both T1/T2 classes")
        if len(epochs) < 10:
            raise ValueError(f"Too few usable T1/T2 epochs for {sid}: {len(epochs)}")
        manifest.append(
            {
                "subject_id": sid,
                "source_file": path.name,
                "source_path_relative_to_data_root": str(path.relative_to(data_root)) if path.parent == data_root / sid else path.name,
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
                "run": RUN_ID,
                "task_type": "motor_imagery_unilateral_fist",
                "n_epochs": int(len(epochs)),
                "class_counts": {str(int(c)): int(n) for c, n in zip(classes, counts)},
                "first_t1_onset_s": next((float(o) for o, s in zip(onsets, source_labels) if s == "T1"), None),
                "first_t2_onset_s": next((float(o) for o, s in zip(onsets, source_labels) if s == "T2"), None),
            }
        )

    write_json(root / "audit/DATASET_MANIFEST.json", {
        "dataset": DATASET,
        "version": DATASET_VERSION,
        "doi": "10.13026/C28G6P",
        "source_url": "https://physionet.org/content/eegmmidb/1.0.0/",
        "run": RUN_ID,
        "task_type": "motor_imagery_unilateral_fist",
        "subjects": subjects,
        "sampling_rate_hz": FS,
        "epoch_window_s": [1.0, 3.5],
        "raw_files_are_not_redistributed": True,
        "files": manifest,
    })
    write_json(root / "audit/ENVIRONMENT.json", environment_payload())
    write_json(root / "results/STATUS.json", {
        "stage": "decoder_generation_complete",
        "task_replay": "pending",
        "scientific_status": "NOT_COMPLETE_UNTIL_CONTROL_FIXTURE_AND_MYOSIM_REPLAYS_PASS",
    })

    rows: list[dict] = []
    traces: list[dict] = []
    for held_out in subjects:
        train_epochs = np.concatenate([data[s][0] for s in subjects if s != held_out], axis=0)
        train_y = np.concatenate([data[s][1] for s in subjects if s != held_out], axis=0)
        test_epochs, test_y, test_ids, onsets, source_labels = data[held_out]
        for model_id in MODELS:
            model, source_cv = fit_source_model(train_epochs, train_y, model_id)
            probabilities = model.predict_proba(__import__("p6_mi_core").features(test_epochs, model_id))
            predictions = model.classes_[np.argmax(probabilities, axis=1)]
            trace_path = root / "traces" / model_id / f"{model_id}_{held_out}.csv"
            trace_path.parent.mkdir(parents=True, exist_ok=True)
            fields = [
                "trace_id", "subject_id", "dataset", "dataset_version", "source_recording", "run_id",
                "source_event_id", "source_event_label", "source_onset_s", "replay_time_s", "ground_truth",
                "prediction", "confidence", "correct", "modality", "preprocessing_version",
                "model_family", "model_id", "model_version", "source_file_sha256", "control_mapping_id",
            ]
            source_path = data_root / held_out / f"{held_out}{RUN_ID}.edf"
            if not source_path.exists():
                source_path = data_root / f"{held_out}{RUN_ID}.edf"
            source_hash = sha256_file(source_path)
            with trace_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                for i, (event_id, pred, gt, proba, onset, source_label) in enumerate(
                    zip(test_ids, predictions, test_y, probabilities, onsets, source_labels)
                ):
                    writer.writerow({
                        "trace_id": f"{model_id}_{held_out}_{i:03d}",
                        "subject_id": held_out,
                        "dataset": DATASET,
                        "dataset_version": DATASET_VERSION,
                        "source_recording": source_path.name,
                        "run_id": RUN_ID,
                        "source_event_id": event_id,
                        "source_event_label": source_label,
                        "source_onset_s": f"{onset:.6f}",
                        "replay_time_s": f"{onset:.6f}",
                        "ground_truth": control_label(source_label),
                        "prediction": control_label("T1" if int(pred) == 1 else "T2"),
                        "confidence": f"{float(np.max(proba)):.8f}",
                        "correct": bool(int(pred) == int(gt)),
                        "modality": "EEG",
                        "preprocessing_version": PREPROCESSING_VERSION,
                        "model_family": __import__("p6_mi_core").MODEL_SPEC[model_id]["family"],
                        "model_id": model_id,
                        "model_version": MODEL_VERSION,
                        "source_file_sha256": source_hash,
                        "control_mapping_id": CONTROL_MAPPING_ID,
                    })
            trace_sha = sha256_file(trace_path)
            rows.append({
                "model_id": model_id,
                "test_subject": held_out,
                "n_trials": int(len(test_y)),
                "source_cv_balanced_accuracy": float(source_cv),
                "heldout_accuracy": float(accuracy_score(test_y, predictions)),
                "heldout_balanced_accuracy": float(balanced_accuracy_score(test_y, predictions)),
                "heldout_log_loss": float(log_loss(test_y, probabilities, labels=model.classes_)),
                "trace": str(trace_path.relative_to(root)),
                "trace_sha256": trace_sha,
            })
            traces.append({
                "model_id": model_id,
                "subject_id": held_out,
                "trace": str(trace_path.relative_to(root)),
                "trace_sha256": trace_sha,
                "source_file": source_path.name,
                "source_file_sha256": source_hash,
                "timing_semantics": "replay_time_s equals source_onset_s; no time transformation",
            })

    means = {m: float(np.mean([r["source_cv_balanced_accuracy"] for r in rows if r["model_id"] == m])) for m in MODELS}
    ranking = sorted(MODELS, key=lambda m: means[m])
    write_json(root / "results/LOSO_RESULTS.json", rows)
    write_json(root / "results/QUALITY_MAPPING.json", {
        "neutral_model_ids": list(MODELS),
        "source_cv_mean_balanced_accuracy": means,
        "ranking_metric": "mean 3-fold balanced accuracy on source training data only",
        "quality_mapping": {"quality_low": ranking[0], "quality_mid": ranking[1], "quality_high": ranking[2]},
        "frozen_before_task_analysis": True,
        "study_status": "P6_C_primary_motor_imagery",
    })
    write_json(root / "results/TRACE_MANIFEST.json", {
        "schema": "hmi.p6.trace-manifest.v4",
        "status": "P6_C_MI_R04_TRACE_GENERATION",
        "trace_count": len(traces),
        "source_run": RUN_ID,
        "source_task_type": "motor_imagery",
        "control_mapping_id": CONTROL_MAPPING_ID,
        "trace_self_hash_not_embedded": True,
        "hash_rule": "SHA-256 is external to each trace CSV and recorded in this manifest.",
        "traces": traces,
    })
    print(json.dumps({"subjects": len(subjects), "traces": len(traces), "source_cv_means": means}, indent=2))


if __name__ == "__main__":
    main()
