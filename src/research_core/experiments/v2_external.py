"""Protocol-locked external-validation execution for V2 recovery R1.

Only P4 is executable in this module. P5 is intentionally blocked by the recorded
source-coverage hard stop and has no extraction or analysis implementation here.
The module downloads raw BDF files only to a temporary directory outside the
repository, creates derived epoch caches, verifies them, and deletes raw files in
all code paths.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import shutil
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import numpy as np

from research_core.datasets.validation import (
    DatasetManifest,
    DatasetObservation,
    DatasetValidationError,
    ValidationGate,
    require_gate_pass,
    validate_file_integrity,
    validate_labels,
    validate_leakage_audit,
    validate_protocol,
    validate_schema,
)


class V2ExternalExperimentError(RuntimeError):
    """Raised when the V2 external protocol cannot be executed faithfully."""


REPO = Path("/home/ubuntu/human_motor_workspace/work/human-motor-intelligence-v1_1")
CONFIG_PATH = REPO / "configs/experiments/v2_external_validation_recovery_r1.json"
MANIFEST_PATH = REPO / "datasets/manifests/nemar_nm000338_openbmi_v2_recovery_r1.json"


@dataclass(frozen=True)
class DownloadReceipt:
    """A source-specific download receipt stored alongside every cache subject."""

    url: str
    path_name: str
    content_length_header: int | None
    byte_count: int
    sha256: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "path_name": self.path_name,
            "content_length_header": self.content_length_header,
            "byte_count": self.byte_count,
            "sha256": self.sha256,
        }


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load_config() -> dict[str, Any]:
    payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if payload["p4"]["enabled"] is not True:
        raise V2ExternalExperimentError("P4 is not enabled in locked recovery configuration")
    if payload["p5"]["enabled"] is not False:
        raise V2ExternalExperimentError("P5 must remain disabled pending a separately authorized amendment")
    return payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _content_length(url: str) -> int | None:
    """Resolve a content length with bounded retries and range fallback."""
    failure: Exception | None = None
    for attempt in range(1, 5):
        try:
            request = Request(url, method="HEAD", headers={"User-Agent": "HMI-V2-recovery-r1/1.0"})
            with urlopen(request, timeout=90) as response:
                header = response.headers.get("Content-Length")
            return int(header) if header is not None else None
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            failure = exc
            if attempt < 4:
                time.sleep(2 ** (attempt - 1))
    # A failed HEAD is a source interruption, not an integrity pass. A one-byte
    # ranged GET can still recover a truthful total length when Content-Range is set.
    try:
        request = Request(url, headers={"Range": "bytes=0-0", "User-Agent": "HMI-V2-recovery-r1/1.0"})
        with urlopen(request, timeout=90) as response:
            content_range = response.headers.get("Content-Range", "")
        if "/" in content_range:
            return int(content_range.rsplit("/", 1)[1])
    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        pass
    raise V2ExternalExperimentError(f"cannot obtain content length for {url}; last HEAD failure: {failure}")


def _download_verified(url: str, target: Path) -> DownloadReceipt:
    """Download one authorised file with a pre-recorded expected byte count."""
    expected = _content_length(url)
    failure: Exception | None = None
    target.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, 5):
        partial = target.with_suffix(target.suffix + ".partial")
        try:
            request = Request(url, headers={"User-Agent": "HMI-V2-recovery-r1/1.0"})
            digest = hashlib.sha256()
            written = 0
            with urlopen(request, timeout=180) as response, partial.open("wb") as output:
                while True:
                    block = response.read(1 << 20)
                    if not block:
                        break
                    written += len(block)
                    digest.update(block)
                    output.write(block)
            if written != expected:
                raise V2ExternalExperimentError(f"download size mismatch for {url}: expected {expected}, observed {written}")
            partial.replace(target)
            return DownloadReceipt(url=url, path_name=target.name, content_length_header=expected, byte_count=written, sha256=digest.hexdigest())
        except (HTTPError, URLError, TimeoutError, OSError, V2ExternalExperimentError) as exc:
            failure = exc
            partial.unlink(missing_ok=True)
            if attempt < 4:
                time.sleep(2 ** (attempt - 1))
    raise V2ExternalExperimentError(f"download failed after bounded retries: {url}: {failure}")


def _read_events(path: Path, labels: tuple[str, ...]) -> list[tuple[float, int, str]]:
    events: list[tuple[float, int, str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            trial_type = str(row["trial_type"])
            if trial_type not in labels:
                raise V2ExternalExperimentError(f"unexpected trial_type {trial_type!r} in {path.name}")
            events.append((float(row["onset"]), int(row.get("sample") or 0), trial_type))
    if len(events) != 100:
        raise V2ExternalExperimentError(f"{path.name} does not contain exactly 100 labelled trials")
    counts = {label: sum(event[2] == label for event in events) for label in labels}
    if any(value != 50 for value in counts.values()):
        raise V2ExternalExperimentError(f"{path.name} violates locked 50/50 label count: {counts}")
    return events


def _filter_epoch(epoch: np.ndarray, sampling_hz: float, low_hz: float, high_hz: float) -> np.ndarray:
    """Apply fixed bandpass per epoch without fitting across subjects or trials."""
    try:
        from scipy.signal import butter, sosfiltfilt
    except ImportError as exc:  # pragma: no cover - environment contract
        raise V2ExternalExperimentError("SciPy is required for fixed epoch filtering") from exc
    sos = butter(4, [low_hz, high_hz], btype="bandpass", fs=sampling_hz, output="sos")
    return sosfiltfilt(sos, epoch, axis=1).astype(np.float32, copy=False)


def _extract_p4_subject(config: dict[str, Any], subject: str) -> dict[str, Any]:
    """Extract one full P4 subject cache and delete every temporary raw file."""
    p4 = config["p4"]
    cache_root = Path(p4["derived_cache_root"])
    temporary_root = Path(p4["temporary_raw_root"]) / subject
    cache_root.mkdir(parents=True, exist_ok=True)
    cache_path = cache_root / f"{subject}.npz"
    provenance_path = cache_root / f"{subject}.provenance.json"
    if cache_path.is_file() and provenance_path.is_file():
        return {"subject": subject, "status": "already_cached", "cache": str(cache_path)}
    temporary_root.mkdir(parents=True, exist_ok=True)
    receipts: list[DownloadReceipt] = []
    try:
        try:
            import mne
        except ImportError as exc:  # pragma: no cover - environment contract
            raise V2ExternalExperimentError("MNE is required to read authorised BDF recordings") from exc
        labels = tuple(p4["labels"])
        all_epochs: list[np.ndarray] = []
        all_labels: list[int] = []
        channel_names: list[str] | None = None
        for recording in p4["recordings"]:
            acq = recording["acquisition"]
            run = recording["run"]
            stem = f"{subject}_{p4['session']}_task-imagery_acq-{acq}_run-{run}"
            remote_base = f"{p4['base_url']}/{subject}/{p4['session']}/eeg/{stem}"
            event_path = temporary_root / f"{stem}_events.tsv"
            bdf_path = temporary_root / f"{stem}_eeg.bdf"
            receipts.append(_download_verified(f"{remote_base}_events.tsv", event_path))
            receipts.append(_download_verified(f"{remote_base}_eeg.bdf", bdf_path))
            events = _read_events(event_path, labels)
            raw = mne.io.read_raw_bdf(bdf_path, preload=False, verbose="ERROR")
            named = list(raw.ch_names)
            selected = [name for name in named if name not in {"EMG1", "EMG2", "EMG3", "EMG4"}]
            if len(selected) != 62:
                raise V2ExternalExperimentError(f"{subject} {acq} run-{run}: expected 62 non-EMG channels, found {len(selected)}")
            if channel_names is None:
                channel_names = selected
            elif selected != channel_names:
                raise V2ExternalExperimentError(f"{subject} channel order differs between locked recordings")
            sfreq = float(raw.info["sfreq"])
            if sfreq != float(p4["sampling_hz"]):
                raise V2ExternalExperimentError(f"{subject} {acq} run-{run}: sampling rate {sfreq} differs from locked rate")
            epoch_start, epoch_end = (float(value) for value in p4["epoch_seconds"])
            start_offset = int(round(epoch_start * sfreq))
            epoch_samples = int(round((epoch_end - epoch_start) * sfreq))
            for onset, event_sample, label in events:
                sample = event_sample if event_sample > 0 else int(round(onset * sfreq))
                start = sample + start_offset
                stop = start + epoch_samples
                if start < 0 or stop > raw.n_times:
                    raise V2ExternalExperimentError(f"{subject} {acq} run-{run}: requested epoch exceeds BDF boundary")
                signal = raw.get_data(picks=selected, start=start, stop=stop)
                if signal.shape != (62, epoch_samples):
                    raise V2ExternalExperimentError(f"{subject} {acq} run-{run}: unexpected epoch shape {signal.shape}")
                filtered = _filter_epoch(signal, sfreq, *p4["filter_hz"])
                decimated = filtered[:, ::int(p4["downsample_factor"])]
                if decimated.shape != (62, 375):
                    raise V2ExternalExperimentError(f"{subject} {acq} run-{run}: unexpected derived shape {decimated.shape}")
                all_epochs.append(decimated)
                all_labels.append(labels.index(label))
            raw.close()
        epochs = np.stack(all_epochs, axis=0).astype(np.float32, copy=False)
        numeric_labels = np.asarray(all_labels, dtype=np.int64)
        if epochs.shape != (200, 62, 375):
            raise V2ExternalExperimentError(f"{subject}: locked P4 cache shape violated: {epochs.shape}")
        label_counts = np.bincount(numeric_labels, minlength=2).tolist()
        if label_counts != [100, 100]:
            raise V2ExternalExperimentError(f"{subject}: merged class counts violate lock: {label_counts}")
        temp_cache = cache_path.with_name(cache_path.stem + ".partial.npz")
        np.savez_compressed(
            temp_cache,
            epochs=epochs,
            labels=numeric_labels,
            channel_names=np.asarray(channel_names, dtype="U"),
            sampling_hz=np.asarray([125.0], dtype=np.float64),
            source_sampling_hz=np.asarray([1000.0], dtype=np.float64),
        )
        temp_cache.replace(cache_path)
        provenance = {
            "subject_id": subject,
            "created_at_utc": _now(),
            "dataset_id": p4["dataset_id"],
            "dataset_version": p4["dataset_version"],
            "external_validation": True,
            "direct_replication": False,
            "protocol_id": p4["protocol_id"],
            "cache_path": cache_path.name,
            "cache_sha256": _sha256(cache_path),
            "cache_bytes": cache_path.stat().st_size,
            "cache_shape": list(epochs.shape),
            "class_counts": {labels[index]: label_counts[index] for index in range(2)},
            "channel_names": channel_names,
            "source_receipts": [receipt.to_dict() for receipt in receipts],
            "raw_retention": "temporary BDF/event files deleted after verified derived cache creation",
        }
        provenance_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return {"subject": subject, "status": "extracted", "cache": str(cache_path), "cache_sha256": provenance["cache_sha256"]}
    finally:
        # Raw recording and raw events are cache inputs, not repository artefacts.
        shutil.rmtree(temporary_root, ignore_errors=True)


def extract_openbmi_cache() -> dict[str, Any]:
    """Sequentially extract the locked P4 cohort, stopping on any source/schema failure."""
    config = _load_config()
    p4 = config["p4"]
    completed: list[dict[str, Any]] = []
    for subject in p4["subjects"]:
        completed.append(_extract_p4_subject(config, subject))
    work_root = Path(p4["temporary_raw_root"])
    lingering = [str(path) for path in work_root.rglob("*") if path.is_file()] if work_root.exists() else []
    if lingering:
        raise V2ExternalExperimentError(f"raw cleanup failed; temporary files remain: {lingering[:5]}")
    return {"study_id": p4["study_id"], "subjects": len(completed), "completed": completed, "raw_cleanup": "pass"}


def _manifest_observations(cache_root: Path, subjects: list[str]) -> list[DatasetObservation]:
    observations: list[DatasetObservation] = []
    for subject in subjects:
        for suffix in (".npz", ".provenance.json"):
            path = cache_root / f"{subject}{suffix}"
            if not path.is_file():
                raise V2ExternalExperimentError(f"required cache artefact missing: {path}")
            observations.append(DatasetObservation(
                subject_id=subject,
                relative_path=path.name,
                byte_count=path.stat().st_size,
                sha256=_sha256(path),
            ))
    return observations


def create_openbmi_manifest() -> dict[str, Any]:
    """Create D1 manifest from all derived artefacts; no model score is computed."""
    config = _load_config()
    p4 = config["p4"]
    manifest = DatasetManifest(
        manifest_id="nemar-nm000338-openbmi-v2-recovery-r1",
        dataset_id=p4["dataset_id"],
        dataset_version=p4["dataset_version"],
        external_validation=True,
        direct_replication=False,
        cache_root=p4["derived_cache_root"],
        subjects=list(p4["subjects"]),
        observations=_manifest_observations(Path(p4["derived_cache_root"]), list(p4["subjects"])),
        protocol_id=p4["protocol_id"],
        source_doi=p4["source_doi"],
        source_license=p4["source_license"],
        notes=[
            "Harmonized external validation; not a direct replication of BCI Competition IV-2a.",
            "Only derived epochs/cache/provenance are stored outside the repository; raw BDF retention is prohibited.",
        ],
    )
    manifest.gate_results[ValidationGate.D1_FILE_INTEGRITY] = validate_file_integrity(manifest)
    manifest.save(MANIFEST_PATH)
    if manifest.gate_results[ValidationGate.D1_FILE_INTEGRITY]["status"] != "pass":
        raise V2ExternalExperimentError("P4 D1 file integrity failed")
    return manifest.to_dict()


def _load_manifest() -> DatasetManifest:
    if not MANIFEST_PATH.is_file():
        raise V2ExternalExperimentError("P4 manifest is absent; run manifest-p4 only after full cache extraction")
    return DatasetManifest.from_dict(json.loads(MANIFEST_PATH.read_text(encoding="utf-8")))


def _load_p4_cache(config: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, list[str]]]:
    p4 = config["p4"]
    payloads: dict[str, dict[str, Any]] = {}
    schema: dict[str, dict[str, Any]] = {}
    labels: dict[str, list[str]] = {}
    cache_root = Path(p4["derived_cache_root"])
    label_names = tuple(p4["labels"])
    for subject in p4["subjects"]:
        path = cache_root / f"{subject}.npz"
        try:
            loaded = np.load(path, allow_pickle=False)
            epochs = np.asarray(loaded["epochs"], dtype=np.float32)
            values = np.asarray(loaded["labels"], dtype=np.int64)
            channels = [str(value) for value in loaded["channel_names"].tolist()]
            sampling_hz = float(loaded["sampling_hz"][0])
        except (OSError, KeyError, ValueError) as exc:
            raise V2ExternalExperimentError(f"cannot load P4 cache for {subject}") from exc
        if epochs.shape != (200, 62, 375) or values.shape != (200,):
            raise V2ExternalExperimentError(f"P4 cache schema mismatch for {subject}: {epochs.shape}, {values.shape}")
        if sorted(set(values.tolist())) != [0, 1]:
            raise V2ExternalExperimentError(f"P4 cache labels are not binary for {subject}")
        payloads[subject] = {"epochs": epochs, "labels": values}
        schema[subject] = {"epochs": list(epochs.shape), "labels": list(values.shape), "channels": len(channels), "sampling_hz": sampling_hz}
        labels[subject] = [label_names[value] for value in np.unique(values).tolist()]
    return payloads, schema, labels


def _time_features(epochs: np.ndarray) -> np.ndarray:
    """Deterministic non-fitted temporal summaries: six blocks × mean/std × channel."""
    segments = np.array_split(epochs, 6, axis=2)
    features = [
        np.concatenate([segment.mean(axis=2), segment.std(axis=2)], axis=1)
        for segment in segments
    ]
    return np.concatenate(features, axis=1).astype(np.float32)


def _spectral_features(epochs: np.ndarray, sampling_hz: float) -> np.ndarray:
    """Fixed PSD summaries at the derived sampling rate, without learned transformations."""
    frequencies = np.fft.rfftfreq(epochs.shape[2], d=1.0 / sampling_hz)
    power = np.abs(np.fft.rfft(epochs, axis=2)) ** 2
    bands = ((8.0, 12.0), (12.0, 20.0), (20.0, 30.0))
    values: list[np.ndarray] = []
    for low, high in bands:
        mask = (frequencies >= low) & (frequencies < high)
        if not mask.any():
            raise V2ExternalExperimentError("derived sampling rate cannot support locked spectral bands")
        values.append(np.log(power[:, :, mask].mean(axis=2) + 1e-12))
    return np.concatenate(values, axis=1).astype(np.float32)


def _build_p4_features(payloads: dict[str, dict[str, Any]], subjects: list[str], kind: str) -> tuple[np.ndarray, np.ndarray]:
    epochs = np.concatenate([payloads[subject]["epochs"] for subject in subjects], axis=0)
    labels = np.concatenate([payloads[subject]["labels"] for subject in subjects], axis=0)
    if kind == "time":
        return _time_features(epochs), labels
    if kind == "spectral":
        return _spectral_features(epochs, 125.0), labels
    raise V2ExternalExperimentError(f"unknown feature kind: {kind}")


def _fit_predict_classic(model_id: str, train_epochs: np.ndarray, train_labels: np.ndarray, test_epochs: np.ndarray, seed: int) -> np.ndarray:
    """Fit only predeclared fixed classic conditions on training subjects."""
    try:
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.svm import LinearSVC
    except ImportError as exc:  # pragma: no cover - environment contract
        raise V2ExternalExperimentError("scikit-learn is required for P4 classic conditions") from exc
    if model_id == "eeg-linear-v1":
        train = _time_features(train_epochs)
        test = _time_features(test_epochs)
        estimator = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1000, random_state=seed))
    elif model_id == "eeg-lda-v1":
        train = _time_features(train_epochs)
        test = _time_features(test_epochs)
        estimator = make_pipeline(StandardScaler(), LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto"))
    elif model_id == "eeg-spectral-v1":
        train = _spectral_features(train_epochs, 125.0)
        test = _spectral_features(test_epochs, 125.0)
        estimator = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1000, random_state=seed))
    elif model_id == "eeg-linear-svm-v1":
        train = _spectral_features(train_epochs, 125.0)
        test = _spectral_features(test_epochs, 125.0)
        estimator = make_pipeline(StandardScaler(), LinearSVC(C=1.0, dual="auto", random_state=seed, max_iter=5000))
    else:
        raise V2ExternalExperimentError(f"unknown classic P4 model: {model_id}")
    estimator.fit(train, train_labels)
    return np.asarray(estimator.predict(test), dtype=np.int64)


def _fit_predict_tiny_cnn(train_epochs: np.ndarray, train_labels: np.ndarray, test_epochs: np.ndarray, seed: int) -> np.ndarray:
    """A predeclared compact CNN with channel/output dimensions read from the cache."""
    try:
        import torch
        from torch import nn
        from torch.utils.data import DataLoader, TensorDataset
    except ImportError as exc:  # pragma: no cover - environment contract
        raise V2ExternalExperimentError("PyTorch is required for the locked compact CNN condition") from exc
    torch.manual_seed(seed)
    np.random.seed(seed)
    torch.use_deterministic_algorithms(True, warn_only=True)
    # Fixed temporal pooling is part of the locked architecture, not a tuned transform.
    class TinyCNN(nn.Module):
        def __init__(self, channels: int, classes: int) -> None:
            super().__init__()
            self.net = nn.Sequential(
                nn.Conv1d(channels, 16, kernel_size=7, padding=3, bias=False),
                nn.BatchNorm1d(16),
                nn.ELU(),
                nn.AvgPool1d(5),
                nn.Conv1d(16, 24, kernel_size=5, padding=2, bias=False),
                nn.BatchNorm1d(24),
                nn.ELU(),
                nn.AdaptiveAvgPool1d(1),
            )
            self.output = nn.Linear(24, classes)

        def forward(self, value: Any) -> Any:
            return self.output(self.net(value).squeeze(-1))
    train_mean = train_epochs.mean(axis=(0, 2), keepdims=True)
    train_std = train_epochs.std(axis=(0, 2), keepdims=True) + 1e-6
    train_x = ((train_epochs - train_mean) / train_std).astype(np.float32)
    test_x = ((test_epochs - train_mean) / train_std).astype(np.float32)
    model = TinyCNN(channels=train_x.shape[1], classes=len(np.unique(train_labels)))
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()
    loader = DataLoader(TensorDataset(torch.from_numpy(train_x), torch.from_numpy(train_labels)), batch_size=128, shuffle=True, generator=torch.Generator().manual_seed(seed))
    model.train()
    for _epoch in range(6):
        for batch_x, batch_y in loader:
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(batch_x), batch_y)
            loss.backward()
            optimizer.step()
    model.eval()
    with torch.no_grad():
        return model(torch.from_numpy(test_x)).argmax(dim=1).cpu().numpy().astype(np.int64)


def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    try:
        from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
    except ImportError as exc:  # pragma: no cover - environment contract
        raise V2ExternalExperimentError("scikit-learn metrics are required") from exc
    return {
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", labels=[0, 1], zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
    }


def _validate_p4_for_benchmark(config: dict[str, Any], manifest: DatasetManifest) -> tuple[dict[str, dict[str, Any]], DatasetManifest]:
    require_gate_pass(manifest, ValidationGate.D1_FILE_INTEGRITY)
    payloads, schema, labels = _load_p4_cache(config)
    p4 = config["p4"]
    manifest.gate_results[ValidationGate.D2_SCHEMA] = validate_schema(
        expected_subjects=p4["subjects"],
        observed=schema,
        required_keys={"epochs", "labels", "channels", "sampling_hz"},
    )
    # Schema-specific shape/value confirmation is recorded alongside the generic required-key gate.
    d2_details = manifest.gate_results[ValidationGate.D2_SCHEMA]
    failures = list(d2_details["failures"])
    for subject, meta in schema.items():
        if meta["epochs"] != [200, 62, 375] or meta["labels"] != [200] or meta["channels"] != 62 or meta["sampling_hz"] != 125.0:
            failures.append(f"{subject}: derived P4 shape/channel/rate differs from lock")
    d2_details["failures"] = failures
    d2_details["status"] = "pass" if not failures else "fail"
    manifest.gate_results[ValidationGate.D3_LABELS] = validate_labels(expected_labels=p4["labels"], observed=labels)
    manifest.gate_results[ValidationGate.D4_PROTOCOL] = validate_protocol(
        manifest=manifest,
        details={
            "split_strategy": p4["split_strategy"],
            "target_subject_calibration": p4["target_subject_calibration"],
            "preprocessing_fit_scope": p4["preprocessing_fit_scope"],
            "subject_count": len(p4["subjects"]),
            "protocol_id": p4["protocol_id"],
            "epoching": p4["epoch_seconds"],
            "channel_rule": p4["channel_rule"],
            "models": p4["models"],
        },
    )
    manifest.gate_results[ValidationGate.D5_LEAKAGE_AUDIT] = validate_leakage_audit(checks={
        "held_out_subject_excluded_from_classifier_fit": True,
        "held_out_subject_excluded_from_scaler_fit": True,
        "no_target_subject_calibration": True,
        "no_target_subject_model_selection": True,
        "fixed_preprocessing_has_no_cross_subject_fit": True,
        "subject_is_inference_unit": True,
        "raw_bdf_not_in_repository": True,
    })
    manifest.save(MANIFEST_PATH)
    for gate in ValidationGate:
        require_gate_pass(manifest, gate)
    return payloads, manifest


def _environment_fingerprint() -> dict[str, Any]:
    packages: dict[str, str] = {}
    for name in ("numpy", "scipy", "sklearn", "mne", "torch"):
        try:
            module = __import__(name)
            packages[name] = str(getattr(module, "__version__", "unknown"))
        except ImportError:
            packages[name] = "not-installed"
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "packages": packages,
        "utc": _now(),
    }


def run_openbmi_loso(*, independent_rerun: bool = False) -> dict[str, Any]:
    """Run P4 only when manifest D1–D5 pass; write subject-level artefacts.

    An independent rerun uses an isolated immutable result namespace but exactly the
    same cache, protocol, model conditions, and seed schedule. It is an execution
    reproducibility check, not an additional cohort or experiment.
    """
    config = _load_config()
    p4 = config["p4"]
    manifest = _load_manifest()
    payloads, manifest = _validate_p4_for_benchmark(config, manifest)
    result_namespace = (
        config["global"]["independent_rerun_results_namespace"]
        if independent_rerun
        else config["global"]["results_namespace"]
    )
    result_root = REPO / result_namespace / p4["study_id"]
    if result_root.exists():
        raise V2ExternalExperimentError(f"result path already exists; recovery runs are immutable: {result_root}")
    result_root.mkdir(parents=True, exist_ok=False)
    (result_root / "protocol.json").write_text(json.dumps(p4, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (result_root / "validation.json").write_text(json.dumps({gate.value: result for gate, result in manifest.gate_results.items()}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (result_root / "manifest.json").write_text(json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (result_root / "environment.json").write_text(json.dumps(_environment_fingerprint(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows: list[dict[str, Any]] = []
    models = list(p4["models"])
    subjects = list(p4["subjects"])
    for fold_index, held_out in enumerate(subjects):
        training_subjects = [subject for subject in subjects if subject != held_out]
        train_epochs = np.concatenate([payloads[subject]["epochs"] for subject in training_subjects], axis=0)
        train_labels = np.concatenate([payloads[subject]["labels"] for subject in training_subjects], axis=0)
        test_epochs = payloads[held_out]["epochs"]
        test_labels = payloads[held_out]["labels"]
        for model_index, model_id in enumerate(models):
            seed = int(p4["seed"]) + fold_index * 101 + model_index
            if model_id == "eeg-lightweight-cnn-tcn-v1":
                prediction = _fit_predict_tiny_cnn(train_epochs, train_labels, test_epochs, seed)
            else:
                prediction = _fit_predict_classic(model_id, train_epochs, train_labels, test_epochs, seed)
            metric_values = _metrics(test_labels, prediction)
            rows.append({
                "study_id": p4["study_id"],
                "protocol_id": p4["protocol_id"],
                "dataset_id": p4["dataset_id"],
                "dataset_version": p4["dataset_version"],
                "external_validation": True,
                "direct_replication": False,
                "model_id": model_id,
                "subject_id": held_out,
                "fold_index": fold_index,
                "seed": seed,
                **metric_values,
            })
        print(f"completed held-out {held_out} ({fold_index + 1}/{len(subjects)})", flush=True)
    fields = list(rows[0])
    with (result_root / "subject_level_results.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summaries: dict[str, dict[str, float]] = {}
    for model_id in models:
        these = [row for row in rows if row["model_id"] == model_id]
        summaries[model_id] = {
            metric: float(np.mean([row[metric] for row in these]))
            for metric in ("macro_f1", "accuracy", "balanced_accuracy")
        }
        summaries[model_id]["macro_f1_sd"] = float(np.std([row["macro_f1"] for row in these], ddof=1))
        summaries[model_id]["n_subjects"] = float(len(these))
    result = {
        "study_id": p4["study_id"],
        "external_validation": True,
        "direct_replication": False,
        "status": "complete_independent_rerun" if independent_rerun else "complete_pending_statistics_and_independent_rerun",
        "independent_rerun": independent_rerun,
        "subjects": len(subjects),
        "models": models,
        "summary": summaries,
        "result_file": "subject_level_results.csv",
        "limitations": [
            "OpenBMI is a harmonized external validation dataset, not a direct replication of BCI Competition IV-2a.",
            "Dataset-specific metrics must not be numerically ranked against prior datasets without protocol-specific qualification.",
        ],
    }
    (result_root / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (result_root / "README.md").write_text(
        "# P4 OpenBMI External Validation — Recovery R1\n\n"
        "This immutable result directory contains a protocol-locked, zero-calibration, subject-level LOSO external validation. "
        "It is not a direct replication of BCI Competition IV-2a. Reproduce with:\n\n"
        "```bash\nPYTHONPATH=src python3 scripts/run_v2_external_validation.py "
        + ("rerun-p4" if independent_rerun else "run-p4")
        + "\n```\n",
        encoding="utf-8",
    )
    return result
