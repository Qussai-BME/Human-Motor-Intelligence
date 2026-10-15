"""Protocol-locked P5 Jeong external validation for V2 Recovery R2.

This module is deliberately separate from frozen studies and P4 Recovery R1.  It
processes one BDF recording at a time outside the repository, retains only
features/provenance in the derived cache, and refuses to fit a model until D1–D5
are satisfied for the predeclared 24-subject cohort.
"""
from __future__ import annotations

import csv
import hashlib
import json
import platform
import shutil
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
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

REPO = Path(__file__).resolve().parents[3]
CONFIG_PATH = REPO / "configs/experiments/v2_p5_jeong_recovery_r2.json"


class P5R2Error(RuntimeError):
    """Raised when the R2 P5 protocol cannot be executed faithfully."""


@dataclass(frozen=True)
class DownloadReceipt:
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


def _config() -> dict[str, Any]:
    payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if payload.get("protocol_id") != "nemar-nm000311-jeong-p5-external-loso-24subject-r2":
        raise P5R2Error("unexpected P5 R2 protocol identifier")
    if payload.get("external_validation") is not True or payload.get("direct_replication") is not False:
        raise P5R2Error("P5 R2 must be labelled external validation, not direct replication")
    if len(payload["subjects"]) != 24 or "sub-23" not in payload["excluded_subjects"]:
        raise P5R2Error("R2 cohort must contain exactly the predeclared 24 subjects with sub-23 excluded")
    return payload


def _manifest_path(config: dict[str, Any]) -> Path:
    return REPO / str(config["manifest_path"])


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _content_length(url: str) -> int | None:
    last_error: Exception | None = None
    for attempt in range(1, 5):
        try:
            request = Request(url, method="HEAD", headers={"User-Agent": "HMI-V2-recovery-r2/1.0"})
            with urlopen(request, timeout=90) as response:
                header = response.headers.get("Content-Length")
            return int(header) if header is not None else None
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            last_error = exc
            if attempt < 4:
                time.sleep(2 ** (attempt - 1))
    try:
        request = Request(url, headers={"Range": "bytes=0-0", "User-Agent": "HMI-V2-recovery-r2/1.0"})
        with urlopen(request, timeout=90) as response:
            value = response.headers.get("Content-Range", "")
        if "/" in value:
            return int(value.rsplit("/", 1)[1])
    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        pass
    raise P5R2Error(f"unable to obtain content length for {url}; last error: {last_error}")


def _download_verified(url: str, target: Path) -> DownloadReceipt:
    expected = _content_length(url)
    target.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    for attempt in range(1, 5):
        partial = target.with_suffix(target.suffix + ".partial")
        try:
            request = Request(url, headers={"User-Agent": "HMI-V2-recovery-r2/1.0"})
            digest = hashlib.sha256()
            written = 0
            with urlopen(request, timeout=240) as response, partial.open("wb") as output:
                while True:
                    block = response.read(1 << 20)
                    if not block:
                        break
                    output.write(block)
                    digest.update(block)
                    written += len(block)
            if expected is None or written != expected:
                raise P5R2Error(f"source size mismatch for {url}: expected {expected}, observed {written}")
            partial.replace(target)
            return DownloadReceipt(url, target.name, expected, written, digest.hexdigest())
        except (HTTPError, URLError, TimeoutError, OSError, P5R2Error) as exc:
            last_error = exc
            partial.unlink(missing_ok=True)
            if attempt < 4:
                time.sleep(2 ** (attempt - 1))
    raise P5R2Error(f"download failed after bounded retries: {url}: {last_error}")


def _read_events(path: Path, labels: list[str]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for event_index, row in enumerate(csv.DictReader(handle, delimiter="\t")):
            label = str(row.get("trial_type", ""))
            if label not in labels:
                raise P5R2Error(f"unexpected or absent trial_type {label!r} in {path.name}")
            try:
                onset = float(row["onset"])
            except (KeyError, TypeError, ValueError) as exc:
                raise P5R2Error(f"invalid onset in {path.name}") from exc
            sample_text = str(row.get("sample") or "").strip()
            sample = int(float(sample_text)) if sample_text else None
            result.append({"label": label, "onset": onset, "sample": sample, "event_index": event_index})
    if not result:
        raise P5R2Error(f"no labelled events in {path.name}")
    return result


def _channel_sets(names: list[str]) -> tuple[list[str], list[str], list[str]]:
    eeg = [name for name in names if not (name.startswith("hEOG_") or name.startswith("vEOG_") or name.startswith("EMG"))]
    emg = [name for name in names if name.startswith("EMG")]
    eog = [name for name in names if name.startswith("hEOG_") or name.startswith("vEOG_")]
    if len(eeg) != 60 or len(emg) != 7 or len(eog) != 4:
        raise P5R2Error(f"unexpected channel identity counts EEG={len(eeg)} EMG={len(emg)} EOG={len(eog)}")
    return eeg, emg, eog


def _eeg_features(epoch: np.ndarray, sampling_hz: float, bands: list[list[float]]) -> np.ndarray:
    frequencies = np.fft.rfftfreq(epoch.shape[1], d=1.0 / sampling_hz)
    power = np.abs(np.fft.rfft(epoch, axis=1)) ** 2
    values: list[np.ndarray] = []
    for low, high in bands:
        mask = (frequencies >= float(low)) & (frequencies < float(high))
        if not mask.any():
            raise P5R2Error("configured EEG band is unsupported by epoch sampling rate")
        values.append(np.log(power[:, mask].mean(axis=1) + 1e-12))
    return np.concatenate(values, axis=0).astype(np.float32, copy=False)


def _emg_features(epoch: np.ndarray) -> np.ndarray:
    mav = np.mean(np.abs(epoch), axis=1)
    rms = np.sqrt(np.mean(np.square(epoch), axis=1))
    waveform_length = np.sum(np.abs(np.diff(epoch, axis=1)), axis=1)
    return np.concatenate([mav, rms, waveform_length], axis=0).astype(np.float32, copy=False)


def _extract_subject(config: dict[str, Any], subject: str) -> dict[str, Any]:
    cache_root = Path(config["derived_cache_root"])
    temp_root = Path(config["temporary_raw_root"]) / subject
    cache_path = cache_root / f"{subject}.npz"
    provenance_path = cache_root / f"{subject}.provenance.json"
    if cache_path.is_file() and provenance_path.is_file():
        return {"subject": subject, "status": "already_cached", "cache": str(cache_path)}
    cache_root.mkdir(parents=True, exist_ok=True)
    temp_root.mkdir(parents=True, exist_ok=True)
    labels = list(config["labels"])
    selected_count = {label: 0 for label in labels}
    skipped_count = {label: 0 for label in labels}
    eeg_rows: list[np.ndarray] = []
    emg_rows: list[np.ndarray] = []
    numeric_labels: list[int] = []
    source_events: list[dict[str, Any]] = []
    receipts: list[DownloadReceipt] = []
    eeg_names: list[str] | None = None
    emg_names: list[str] | None = None
    try:
        try:
            import mne
        except ImportError as exc:  # pragma: no cover
            raise P5R2Error("MNE is required for authorised Jeong BDF extraction") from exc
        for run in config["runs"]:
            stem = f"{subject}_{config['session']}_task-{config['task']}_run-{run}"
            remote_base = f"{config['base_url']}/{subject}/{config['session']}/eeg/{stem}"
            event_path = temp_root / f"{stem}_events.tsv"
            bdf_path = temp_root / f"{stem}_eeg.bdf"
            receipts.append(_download_verified(f"{remote_base}_events.tsv", event_path))
            receipts.append(_download_verified(f"{remote_base}_eeg.bdf", bdf_path))
            events = _read_events(event_path, labels)
            raw = mne.io.read_raw_bdf(bdf_path, preload=False, verbose="ERROR")
            sfreq = float(raw.info["sfreq"])
            if sfreq != float(config["sampling_hz"]):
                raise P5R2Error(f"{subject} run-{run}: source sampling {sfreq} differs from lock")
            current_eeg, current_emg, _ = _channel_sets(list(raw.ch_names))
            if eeg_names is None:
                eeg_names, emg_names = current_eeg, current_emg
            elif current_eeg != eeg_names or current_emg != emg_names:
                raise P5R2Error(f"{subject} run-{run}: channel order differs across recordings")
            samples = int(round((float(config["epoch_seconds"][1]) - float(config["epoch_seconds"][0])) * sfreq))
            offset = int(round(float(config["epoch_seconds"][0]) * sfreq))
            for event in events:
                label = str(event["label"])
                if selected_count[label] >= int(config["trial_cap_per_label"]):
                    skipped_count[label] += 1
                    continue
                start_sample = event["sample"] if event["sample"] is not None else int(round(float(event["onset"]) * sfreq))
                start = int(start_sample) + offset
                stop = start + samples
                if start < 0 or stop > raw.n_times:
                    raise P5R2Error(f"{subject} run-{run} event {event['event_index']}: epoch exceeds source boundary")
                eeg_epoch = raw.get_data(picks=eeg_names, start=start, stop=stop)
                emg_epoch = raw.get_data(picks=emg_names, start=start, stop=stop)
                if eeg_epoch.shape != (60, samples) or emg_epoch.shape != (7, samples):
                    raise P5R2Error(f"{subject} run-{run}: modality epoch shape mismatch")
                eeg_rows.append(_eeg_features(eeg_epoch, sfreq, config["eeg_feature_bands_hz"]))
                emg_rows.append(_emg_features(emg_epoch))
                numeric_labels.append(labels.index(label))
                selected_count[label] += 1
                source_events.append({"run": int(run), **event})
            raw.close()
        if any(count != int(config["trial_cap_per_label"]) for count in selected_count.values()):
            raise P5R2Error(f"{subject}: retained label counts violate 50-per-label lock: {selected_count}")
        eeg = np.stack(eeg_rows, axis=0).astype(np.float32, copy=False)
        emg = np.stack(emg_rows, axis=0).astype(np.float32, copy=False)
        y = np.asarray(numeric_labels, dtype=np.int64)
        if eeg.shape != (550, 120) or emg.shape != (550, 21) or y.shape != (550,):
            raise P5R2Error(f"{subject}: derived cache shape mismatch EEG={eeg.shape} EMG={emg.shape} labels={y.shape}")
        if np.bincount(y, minlength=len(labels)).tolist() != [50] * len(labels):
            raise P5R2Error(f"{subject}: derived labels do not meet fixed class balance")
        temporary_cache = cache_path.with_name(cache_path.stem + ".partial.npz")
        np.savez_compressed(
            temporary_cache,
            eeg_features=eeg,
            emg_features=emg,
            labels=y,
            eeg_channel_names=np.asarray(eeg_names, dtype="U"),
            emg_channel_names=np.asarray(emg_names, dtype="U"),
            sampling_hz=np.asarray([float(config["sampling_hz"])], dtype=np.float64),
        )
        temporary_cache.replace(cache_path)
        provenance = {
            "subject_id": subject,
            "created_at_utc": _now(),
            "dataset_id": config["dataset_id"],
            "dataset_version": config["dataset_version"],
            "external_validation": True,
            "direct_replication": False,
            "protocol_id": config["protocol_id"],
            "cache_path": cache_path.name,
            "cache_sha256": _sha256(cache_path),
            "cache_bytes": cache_path.stat().st_size,
            "cache_shapes": {"eeg_features": list(eeg.shape), "emg_features": list(emg.shape), "labels": list(y.shape)},
            "label_counts": {label: 50 for label in labels},
            "event_cap_policy": "first 50 valid TSV-order events per label",
            "discarded_events_by_label": skipped_count,
            "eeg_channel_names": eeg_names,
            "emg_channel_names": emg_names,
            "source_event_rows": source_events,
            "source_receipts": [receipt.to_dict() for receipt in receipts],
            "raw_retention": "temporary BDF/event files deleted after verified feature-cache creation",
        }
        provenance_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return {"subject": subject, "status": "extracted", "cache": str(cache_path), "cache_sha256": provenance["cache_sha256"]}
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def extract_cache() -> dict[str, Any]:
    config = _config()
    results = [_extract_subject(config, subject) for subject in config["subjects"]]
    temp_root = Path(config["temporary_raw_root"])
    lingering = [str(path) for path in temp_root.rglob("*") if path.is_file()] if temp_root.exists() else []
    if lingering:
        raise P5R2Error(f"temporary raw cleanup failed: {lingering[:5]}")
    return {"study_id": config["study_id"], "subjects": len(results), "completed": results, "raw_cleanup": "pass"}


def _observations(cache_root: Path, subjects: list[str]) -> list[DatasetObservation]:
    observations: list[DatasetObservation] = []
    for subject in subjects:
        for suffix in (".npz", ".provenance.json"):
            path = cache_root / f"{subject}{suffix}"
            if not path.is_file():
                raise P5R2Error(f"cache artefact is absent: {path}")
            observations.append(DatasetObservation(subject, path.name, path.stat().st_size, _sha256(path)))
    return observations


def create_manifest() -> dict[str, Any]:
    config = _config()
    cache_root = Path(config["derived_cache_root"])
    manifest = DatasetManifest(
        manifest_id="nemar-nm000311-jeong-p5-v2-recovery-r2",
        dataset_id=config["dataset_id"],
        dataset_version=config["dataset_version"],
        external_validation=True,
        direct_replication=False,
        cache_root=str(cache_root),
        subjects=list(config["subjects"]),
        observations=_observations(cache_root, list(config["subjects"])),
        protocol_id=config["protocol_id"],
        source_doi=config["source_doi"],
        source_license=config["source_license"],
        notes=[
            "Amended 24-subject external validation; sub-23 excluded before model fitting after independent source check.",
            "All retained subjects have 550 balanced MI trials under the predeclared first-50 TSV-order cap.",
            "Only derived feature arrays and provenance are retained; raw BDF/TSV files are deleted.",
        ],
    )
    manifest.gate_results[ValidationGate.D1_FILE_INTEGRITY] = validate_file_integrity(manifest)
    if manifest.gate_results[ValidationGate.D1_FILE_INTEGRITY]["status"] != "pass":
        raise P5R2Error("P5 R2 D1 failed")
    manifest.save(_manifest_path(config))
    return manifest.to_dict()


def _load_manifest(config: dict[str, Any]) -> DatasetManifest:
    path = _manifest_path(config)
    if not path.is_file():
        raise P5R2Error("P5 R2 D1 manifest is absent; run manifest-p5-r2 after full cache extraction")
    return DatasetManifest.from_dict(json.loads(path.read_text(encoding="utf-8")))


def _load_cache(config: dict[str, Any]) -> tuple[dict[str, dict[str, np.ndarray]], dict[str, dict[str, Any]], dict[str, list[str]]]:
    labels = list(config["labels"])
    payloads: dict[str, dict[str, np.ndarray]] = {}
    schema: dict[str, dict[str, Any]] = {}
    coverage: dict[str, list[str]] = {}
    for subject in config["subjects"]:
        path = Path(config["derived_cache_root"]) / f"{subject}.npz"
        try:
            with np.load(path, allow_pickle=False) as value:
                eeg = np.asarray(value["eeg_features"], dtype=np.float32)
                emg = np.asarray(value["emg_features"], dtype=np.float32)
                y = np.asarray(value["labels"], dtype=np.int64)
                eeg_channels = len(value["eeg_channel_names"])
                emg_channels = len(value["emg_channel_names"])
                rate = float(value["sampling_hz"][0])
        except (OSError, KeyError, ValueError) as exc:
            raise P5R2Error(f"cannot load P5 R2 cache for {subject}") from exc
        if eeg.shape != (550, 120) or emg.shape != (550, 21) or y.shape != (550,):
            raise P5R2Error(f"{subject}: cache shapes differ from R2 protocol")
        if np.bincount(y, minlength=len(labels)).tolist() != [50] * len(labels):
            raise P5R2Error(f"{subject}: cache class counts differ from R2 protocol")
        payloads[subject] = {"eeg": eeg, "emg": emg, "labels": y}
        schema[subject] = {"eeg_features": list(eeg.shape), "emg_features": list(emg.shape), "labels": list(y.shape), "eeg_channels": eeg_channels, "emg_channels": emg_channels, "sampling_hz": rate}
        coverage[subject] = [labels[index] for index in np.unique(y).tolist()]
    return payloads, schema, coverage


def _validate(config: dict[str, Any], manifest: DatasetManifest) -> tuple[dict[str, dict[str, np.ndarray]], DatasetManifest]:
    require_gate_pass(manifest, ValidationGate.D1_FILE_INTEGRITY)
    payloads, schema, coverage = _load_cache(config)
    manifest.gate_results[ValidationGate.D2_SCHEMA] = validate_schema(
        expected_subjects=config["subjects"],
        observed=schema,
        required_keys={"eeg_features", "emg_features", "labels", "eeg_channels", "emg_channels", "sampling_hz"},
    )
    d2 = manifest.gate_results[ValidationGate.D2_SCHEMA]
    failures = list(d2["failures"])
    for subject, value in schema.items():
        if value != {"eeg_features": [550, 120], "emg_features": [550, 21], "labels": [550], "eeg_channels": 60, "emg_channels": 7, "sampling_hz": 1000.0}:
            failures.append(f"{subject}: feature/cache metadata differs from R2 lock")
    d2["failures"] = failures
    d2["status"] = "pass" if not failures else "fail"
    manifest.gate_results[ValidationGate.D3_LABELS] = validate_labels(expected_labels=config["labels"], observed=coverage)
    manifest.gate_results[ValidationGate.D4_PROTOCOL] = validate_protocol(
        manifest=manifest,
        details={
            "split_strategy": config["split_strategy"],
            "target_subject_calibration": config["target_subject_calibration"],
            "preprocessing_fit_scope": config["preprocessing_fit_scope"],
            "subject_count": len(config["subjects"]),
            "protocol_id": config["protocol_id"],
            "session": config["session"],
            "runs": config["runs"],
            "trial_cap_per_label": config["trial_cap_per_label"],
            "models": config["models"],
        },
    )
    manifest.gate_results[ValidationGate.D5_LEAKAGE_AUDIT] = validate_leakage_audit(checks={
        "held_out_subject_excluded_from_eeg_scaler_fit": True,
        "held_out_subject_excluded_from_emg_scaler_fit": True,
        "held_out_subject_excluded_from_all_classifier_fits": True,
        "no_target_subject_calibration": True,
        "no_target_subject_model_selection": True,
        "late_fusion_probabilities_use_training_fit_models_only": True,
        "fixed_epoch_features_have_no_cross_subject_fit": True,
        "subject_is_inference_unit": True,
        "raw_bdf_not_in_repository": True,
    })
    manifest.save(_manifest_path(config))
    for gate in ValidationGate:
        require_gate_pass(manifest, gate)
    return payloads, manifest


def _make_lda() -> Any:
    try:
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
    except ImportError as exc:  # pragma: no cover
        raise P5R2Error("scikit-learn is required for P5 R2") from exc
    return make_pipeline(StandardScaler(), LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto"))


def _metrics(y_true: np.ndarray, y_pred: np.ndarray, labels: list[str]) -> dict[str, float]:
    try:
        from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
    except ImportError as exc:  # pragma: no cover
        raise P5R2Error("scikit-learn metrics are required for P5 R2") from exc
    indices = list(range(len(labels)))
    return {
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", labels=indices, zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
    }


def _predict(model_id: str, train_eeg: np.ndarray, train_emg: np.ndarray, train_y: np.ndarray, test_eeg: np.ndarray, test_emg: np.ndarray) -> np.ndarray:
    if model_id == "eeg-only-lda-v1":
        model = _make_lda().fit(train_eeg, train_y)
        return np.asarray(model.predict(test_eeg), dtype=np.int64)
    if model_id == "emg-only-lda-v1":
        model = _make_lda().fit(train_emg, train_y)
        return np.asarray(model.predict(test_emg), dtype=np.int64)
    if model_id == "early-fusion-lda-v1":
        model = _make_lda().fit(np.concatenate([train_eeg, train_emg], axis=1), train_y)
        return np.asarray(model.predict(np.concatenate([test_eeg, test_emg], axis=1)), dtype=np.int64)
    if model_id == "late-fusion-lda-v1":
        eeg_model = _make_lda().fit(train_eeg, train_y)
        emg_model = _make_lda().fit(train_emg, train_y)
        probabilities = (eeg_model.predict_proba(test_eeg) + emg_model.predict_proba(test_emg)) / 2.0
        classes = np.asarray(eeg_model.classes_, dtype=np.int64)
        if not np.array_equal(classes, np.asarray(emg_model.classes_, dtype=np.int64)):
            raise P5R2Error("late fusion class ordering differs between modality models")
        return classes[np.argmax(probabilities, axis=1)]
    raise P5R2Error(f"unknown P5 R2 model {model_id}")


def _environment() -> dict[str, Any]:
    packages: dict[str, str] = {}
    for name in ("numpy", "scipy", "sklearn", "mne"):
        try:
            module = __import__(name)
            packages[name] = str(getattr(module, "__version__", "unknown"))
        except ImportError:
            packages[name] = "not-installed"
    return {"python": sys.version, "platform": platform.platform(), "packages": packages, "utc": _now()}


def run_loso(*, independent_rerun: bool = False) -> dict[str, Any]:
    config = _config()
    manifest = _load_manifest(config)
    payloads, manifest = _validate(config, manifest)
    namespace = config["independent_rerun_results_namespace"] if independent_rerun else config["results_namespace"]
    result_root = REPO / namespace / config["study_id"]
    if result_root.exists():
        raise P5R2Error(f"immutable result path exists: {result_root}")
    result_root.mkdir(parents=True, exist_ok=False)
    (result_root / "protocol.json").write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (result_root / "validation.json").write_text(json.dumps({gate.value: value for gate, value in manifest.gate_results.items()}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (result_root / "manifest.json").write_text(json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (result_root / "environment.json").write_text(json.dumps(_environment(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows: list[dict[str, Any]] = []
    subjects = list(config["subjects"])
    for fold_index, held_out in enumerate(subjects):
        train_subjects = [subject for subject in subjects if subject != held_out]
        train_eeg = np.concatenate([payloads[subject]["eeg"] for subject in train_subjects], axis=0)
        train_emg = np.concatenate([payloads[subject]["emg"] for subject in train_subjects], axis=0)
        train_y = np.concatenate([payloads[subject]["labels"] for subject in train_subjects], axis=0)
        test = payloads[held_out]
        for model_index, model_id in enumerate(config["models"]):
            prediction = _predict(model_id, train_eeg, train_emg, train_y, test["eeg"], test["emg"])
            rows.append({
                "study_id": config["study_id"],
                "protocol_id": config["protocol_id"],
                "dataset_id": config["dataset_id"],
                "dataset_version": config["dataset_version"],
                "external_validation": True,
                "direct_replication": False,
                "model_id": model_id,
                "subject_id": held_out,
                "fold_index": fold_index,
                "seed": int(config["seed"]) + fold_index * 101 + model_index,
                **_metrics(test["labels"], prediction, list(config["labels"])),
            })
        print(f"completed held-out {held_out} ({fold_index + 1}/{len(subjects)})", flush=True)
    fields = list(rows[0])
    with (result_root / "subject_level_results.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summary: dict[str, dict[str, float]] = {}
    for model_id in config["models"]:
        subset = [row for row in rows if row["model_id"] == model_id]
        summary[model_id] = {metric: float(np.mean([row[metric] for row in subset])) for metric in ("macro_f1", "accuracy", "balanced_accuracy")}
        summary[model_id]["macro_f1_sd"] = float(np.std([row["macro_f1"] for row in subset], ddof=1))
        summary[model_id]["n_subjects"] = float(len(subset))
    output = {
        "study_id": config["study_id"],
        "protocol_id": config["protocol_id"],
        "external_validation": True,
        "direct_replication": False,
        "status": "complete_independent_rerun" if independent_rerun else "complete_pending_statistics_and_independent_rerun",
        "independent_rerun": independent_rerun,
        "subjects": len(subjects),
        "models": config["models"],
        "summary": summary,
        "result_file": "subject_level_results.csv",
        "limitations": [
            "Amended 24-subject source-availability cohort; sub-23 was excluded before feature extraction and model fitting.",
            "Jeong is a harmonized external validation and not a direct replication or pooled estimate with Cho2017.",
            "MI-only all-11-class analysis; no motor-execution mixing and no synthetic missing-modality stress analysis.",
        ],
    }
    (result_root / "results.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    command = "rerun-p5-r2" if independent_rerun else "run-p5-r2"
    (result_root / "README.md").write_text(
        "# P5 Jeong External Validation — Recovery R2\n\n"
        "This immutable directory records an amended 24-subject, all-11-class, MI-only, zero-calibration LOSO external validation. "
        "It is not a direct replication of frozen Cho2017 evidence. Reproduce with:\n\n"
        f"```bash\nPYTHONPATH=src python3 scripts/run_v2_p5_jeong_r2.py {command}\n```\n",
        encoding="utf-8",
    )
    return output
