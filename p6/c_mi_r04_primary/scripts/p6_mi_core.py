#!/usr/bin/env python3
"""Self-contained P6-C EEG/EDF parsing and decoder utilities.

The implementation avoids workstation-bound paths and optional binary EDF readers.
It parses the EDF+ layout used by PhysioNet EEGMMIDB directly and keeps the scientific
protocol identical to the retained R03 feature/model definitions except for the source run.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import trapezoid
from scipy.signal import welch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FS = 160.0
MODELS = ("M1", "M2", "M3")
MODEL_SPEC: dict[str, dict[str, Any]] = {
    "M1": {"family": "broad_band", "bands": [(8, 30)], "C": 0.1},
    "M2": {"family": "band_pair", "bands": [(8, 12), (13, 30)], "C": 1.0},
    "M3": {"family": "band_pair_asymmetry", "bands": [(8, 12), (13, 30)], "C": 2.0},
}
RUN_ID = "R04"
DATASET = "PhysioNet EEG Motor Movement/Imagery Dataset"
DATASET_VERSION = "1.0.0"
CONTROL_MAPPING_ID = "P6_C1_R04_T1_TO_OPEN_T2_TO_CLOSE_ABSTRACT_v1"
PREPROCESSING_VERSION = "window_1.0_3.5s_welch_v2"
MODEL_VERSION = "p6-c1-mi-r04-v1.0"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _ascii(raw: bytes) -> str:
    return raw.decode("ascii", errors="ignore").rstrip(" \x00")


def _ints(header: bytes) -> tuple[int, int, float, int]:
    header_bytes = int(_ascii(header[184:192]))
    n_records = int(_ascii(header[236:244]))
    duration = float(_ascii(header[244:252]))
    n_signals = int(_ascii(header[252:256]))
    if header_bytes < 256 or n_records <= 0 or n_signals <= 0 or duration <= 0:
        raise ValueError("Invalid EDF header fields")
    return header_bytes, n_records, duration, n_signals


def _parse_signal_headers(header: bytes, n_signals: int) -> list[dict[str, Any]]:
    start = 256
    labels = [header[start + i * 16 : start + (i + 1) * 16] for i in range(n_signals)]
    base = start + 16 * n_signals

    def field(width: int, offset: int, i: int) -> str:
        a = base + offset * n_signals + i * width
        return _ascii(header[a : a + width])

    out: list[dict[str, Any]] = []
    for i in range(n_signals):
        # Relative to the block after labels: transducer (80), physical
        # dimension (8), physical min/max (8 each), digital min/max (8 each),
        # prefilter (80), then samples/record (8).
        phys_min = float(field(8, 88, i))
        phys_max = float(field(8, 96, i))
        dig_min = int(field(8, 104, i))
        dig_max = int(field(8, 112, i))
        samples = int(field(8, 200, i))
        if dig_max == dig_min or samples <= 0:
            raise ValueError(f"Invalid EDF signal header at index {i}")
        out.append(
            {
                "label": _ascii(labels[i]),
                "physical_min": phys_min,
                "physical_max": phys_max,
                "digital_min": dig_min,
                "digital_max": dig_max,
                "samples_per_record": samples,
            }
        )
    return out


def _parse_annotations(raw: bytes) -> list[tuple[float, str]]:
    text = raw.decode("latin-1", errors="ignore")
    found: list[tuple[float, str]] = []
    for segment in text.split("\x00"):
        if not segment or "\x14" not in segment:
            continue
        fields = segment.split("\x14")
        onset_duration = fields[0]
        if "\x15" in onset_duration:
            onset_text = onset_duration.split("\x15", 1)[0]
        else:
            onset_text = onset_duration
        onset_match = re.search(r"[+-]?\d+(?:\.\d+)?", onset_text)
        if not onset_match:
            continue
        onset = float(onset_match.group(0))
        for annotation in fields[1:]:
            annotation = annotation.strip(" \x00")
            if annotation in {"T0", "T1", "T2"}:
                found.append((onset, annotation))
    return found


def read_eegmmidb_r04(path: Path) -> tuple[np.ndarray, np.ndarray, list[str], list[float], list[str]]:
    """Read the 64 EEG channels and T1/T2 event annotations from one EDF+ file."""
    if path.name.upper()[-7:] != "R04.EDF":
        raise ValueError(f"P6-C requires an R04 EDF file, got {path.name}")
    raw = path.read_bytes()
    if len(raw) < 256:
        raise ValueError(f"EDF file is too small: {path}")
    header_bytes, n_records, _record_duration, n_signals = _ints(raw[:256])
    header_len = 256 + n_signals * 256
    if header_bytes != header_len:
        raise ValueError(f"Unexpected EDF header length: {header_bytes} != {header_len}")
    signal_headers = _parse_signal_headers(raw[:header_bytes], n_signals)
    eeg_indices = [i for i, h in enumerate(signal_headers) if "annotation" not in h["label"].lower()][:64]
    if len(eeg_indices) < 64:
        raise ValueError(f"Expected at least 64 EEG channels, found {len(eeg_indices)}")
    annotation_indices = [i for i, h in enumerate(signal_headers) if "annotation" in h["label"].lower()]
    if not annotation_indices:
        raise ValueError("EDF+ annotation channel not found")
    annotation_index = annotation_indices[0]

    samples_total = sum(signal_headers[i]["samples_per_record"] for i in eeg_indices)
    # Store each EEG signal as float32; one R04 recording is small enough for this representation.
    arrays = [np.empty(signal_headers[i]["samples_per_record"] * n_records, dtype=np.float32) for i in eeg_indices]
    annotations_raw = bytearray()
    offset = header_bytes
    for record in range(n_records):
        for i in range(n_signals):
            n = signal_headers[i]["samples_per_record"]
            byte_count = n * 2
            chunk = raw[offset : offset + byte_count]
            if len(chunk) != byte_count:
                raise ValueError("Truncated EDF data record")
            if i == annotation_index:
                annotations_raw.extend(chunk)
            elif i in eeg_indices:
                idx = eeg_indices.index(i)
                digital = np.frombuffer(chunk, dtype="<i2").astype(np.float32)
                h = signal_headers[i]
                scale = (h["physical_max"] - h["physical_min"]) / (h["digital_max"] - h["digital_min"])
                arrays[idx][record * n : (record + 1) * n] = (
                    (digital - h["digital_min"]) * scale + h["physical_min"]
                )
            offset += byte_count

    lengths = {len(x) for x in arrays}
    if len(lengths) != 1:
        raise ValueError("EEG channels have inconsistent total lengths")
    X = np.vstack(arrays)
    events = _parse_annotations(bytes(annotations_raw))
    selected = [(onset, label) for onset, label in events if label in {"T1", "T2"}]
    epochs: list[np.ndarray] = []
    labels: list[int] = []
    ids: list[str] = []
    onsets: list[float] = []
    source_labels: list[str] = []
    for k, (onset, source_label) in enumerate(selected):
        a = int(round((onset + 1.0) * FS))
        b = int(round((onset + 3.5) * FS))
        if a < 0 or b > X.shape[1] or b <= a:
            continue
        epochs.append(X[:, a:b])
        labels.append(1 if source_label == "T1" else 2)
        ids.append(f"{path.stem}-event-{k:03d}")
        onsets.append(onset)
        source_labels.append(source_label)
    if len(epochs) == 0:
        raise ValueError(f"No usable T1/T2 R04 epochs found in {path.name}")
    return np.asarray(epochs), np.asarray(labels), ids, onsets, source_labels


def features(epochs: np.ndarray, model_id: str) -> np.ndarray:
    spec = MODEL_SPEC[model_id]
    if epochs.ndim != 3 or epochs.shape[1] < 64:
        raise ValueError("Expected epochs shaped (n_trials, >=64 channels, n_samples)")
    channels = list(range(7, 64))
    output: list[list[float]] = []
    for trial in epochs:
        row: list[float] = []
        for channel in channels:
            freqs, power = welch(trial[channel], fs=FS, nperseg=min(256, trial.shape[-1]))
            mask = (freqs >= 4) & (freqs <= 40)
            total = trapezoid(power[mask], freqs[mask]) + 1e-12
            for lo, hi in spec["bands"]:
                band = (freqs >= lo) & (freqs <= hi)
                row.append(math.log((trapezoid(power[band], freqs[band]) + 1e-12) / total))
        output.append(row)
    z = np.asarray(output, dtype=np.float32)
    if model_id == "M3":
        half = z.shape[1] // 2
        z = np.c_[z, z[:, :half] - z[:, half : 2 * half]]
    return z


def fit_source_model(train_epochs: np.ndarray, train_y: np.ndarray, model_id: str):
    X = features(train_epochs, model_id)
    model = Pipeline(
        [
            ("scale", StandardScaler()),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000, C=MODEL_SPEC[model_id]["C"], random_state=1701
                ),
            ),
        ]
    )
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=1701)
    score = float(np.mean(cross_val_score(model, X, train_y, cv=cv, scoring="balanced_accuracy")))
    model.fit(X, train_y)
    return model, score


def control_label(source_label: str) -> str:
    if source_label == "T1":
        return "OPEN"
    if source_label == "T2":
        return "CLOSE"
    raise ValueError(f"Unsupported R04 source label: {source_label}")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, Any]:
    try:
        import scipy
        import sklearn
    except Exception:
        scipy = sklearn = None
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": getattr(scipy, "__version__", None),
        "scikit_learn": getattr(sklearn, "__version__", None),
        "protocol_run": RUN_ID,
    }
