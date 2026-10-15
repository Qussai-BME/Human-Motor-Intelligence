#!/usr/bin/env python3
"""Prepare NinaPro feature caches one official subject archive at a time.

The script intentionally keeps only one downloaded/extracted subject in the
staging area. A source archive is deleted only after its 618-D per-subject
feature cache and metadata have been atomically written and validated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from litedan_p3.config import cache_input_hash, config_hash, load_config  # noqa: E402
from litedan_p3.data.ninapro import find_subject_files, subject_windows  # noqa: E402
from litedan_p3.features.hybrid import SCHEMA_VERSION, extract_feature_matrix  # noqa: E402
from litedan_p3.utils.repro import save_json  # noqa: E402


SUBJECT_FILE_RE = re.compile(r"S0*(?P<subject>\d+)_E(?P<exercise>\d+)_A\d+\.mat$", re.IGNORECASE)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_save_npz(path: Path, **arrays: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".npz", delete=False) as handle:
        temporary = Path(handle.name)
    try:
        np.savez_compressed(temporary, **arrays)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_save_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".json", delete=False, mode="w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temporary = Path(handle.name)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def load_inventory(path: Path, db: str) -> dict[int, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    database = data.get("databases", {}).get(db)
    if not isinstance(database, dict):
        raise ValueError(f"Inventory has no {db} entry: {path}")
    output: dict[int, dict[str, Any]] = {}
    for item in database.get("subjects", []):
        text = str(item.get("text", ""))
        match = re.fullmatch(r"s(\d+)\.zip", text, flags=re.IGNORECASE)
        if match is None:
            continue
        output[int(match.group(1))] = dict(item)
    return output


def download_archive(url: str, path: Path, expected_size: int | None, max_attempts: int = 6) -> dict[str, Any]:
    """Download an official archive with bounded automatic resume and retry.

    A partial file is retained across network interruptions. The next request uses
    HTTP Range when the source supports it; the official NinaPro host advertises
    byte-range support. A full-sized archive is accepted only when it is a valid
    ZIP container, so a failed transfer can never be mistaken for a cache input.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and expected_size is not None and path.stat().st_size == expected_size and zipfile.is_zipfile(path):
        return {"status": "reused", "bytes": path.stat().st_size, "sha256": sha256_file(path)}
    partial = path.with_suffix(path.suffix + ".part")
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        offset = partial.stat().st_size if partial.exists() else 0
        if expected_size is not None and offset > expected_size:
            partial.unlink(missing_ok=True)
            offset = 0
        headers = {"User-Agent": "LiteDAN-Paper3-staged-preparation/1.1"}
        if offset:
            headers["Range"] = f"bytes={offset}-"
        try:
            with requests.get(url, stream=True, timeout=(30, 180), headers=headers) as response:
                if offset and response.status_code == 200:
                    # The server ignored the range request; restart safely rather
                    # than appending duplicate bytes to a partial archive.
                    partial.unlink(missing_ok=True)
                    continue
                response.raise_for_status()
                mode = "ab" if offset else "wb"
                with partial.open(mode) as handle:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            handle.write(chunk)
            received = partial.stat().st_size
            if expected_size is not None and received != expected_size:
                raise RuntimeError(f"Incomplete transfer after attempt {attempt}: got {received}, expected {expected_size}")
            if not zipfile.is_zipfile(partial):
                partial.unlink(missing_ok=True)
                raise RuntimeError(f"Downloaded archive is not a valid ZIP container: {url}")
            os.replace(partial, path)
            return {
                "status": "resumed" if offset else "downloaded",
                "bytes": received,
                "sha256": sha256_file(path),
                "attempts": attempt,
            }
        except (requests.RequestException, OSError, RuntimeError) as exc:
            last_error = exc
            if attempt == max_attempts:
                break
            time.sleep(min(60, 5 * attempt))
    raise RuntimeError(f"Unable to download {url} after {max_attempts} attempts; partial bytes preserved at {partial}: {last_error}")


def extract_required_mat_files(archive: Path, destination: Path, subject: int, exercises: list[int]) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    matched: list[tuple[str, int]] = []
    with zipfile.ZipFile(archive) as source:
        for name in source.namelist():
            filename = Path(name).name
            match = SUBJECT_FILE_RE.fullmatch(filename)
            if match is None:
                continue
            if int(match.group("subject")) != subject:
                continue
            exercise = int(match.group("exercise"))
            if exercise in exercises:
                matched.append((name, exercise))
        available = {exercise for _, exercise in matched}
        missing = sorted(set(exercises) - available)
        if missing:
            raise RuntimeError(
                f"Subject S{subject:02d} archive lacks required exercise files {missing}; found exercises {sorted(available)}"
            )
        for name, _ in matched:
            filename = Path(name).name
            target = destination / filename
            with source.open(name) as reader, target.open("wb") as writer:
                shutil.copyfileobj(reader, writer, length=1024 * 1024)
    return sorted(Path(name).name for name, _ in matched)


def validate_cache(path: Path, expected_subject: int, expected_hash: str) -> bool:
    metadata_path = path.with_suffix(".json")
    if not path.exists() or not metadata_path.exists():
        return False
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        with np.load(path, allow_pickle=False) as payload:
            features = payload["features"]
            labels = payload["labels"]
            purity = payload["purity"]
            names = payload["feature_names"]
        return bool(
            metadata.get("subject") == expected_subject
            and metadata.get("feature_schema") == SCHEMA_VERSION
            and metadata.get("cache_input_hash") == expected_hash
            and features.ndim == 2
            and features.shape[1] == 618
            and labels.ndim == 1
            and purity.ndim == 1
            and names.ndim == 1
            and len(names) == 618
            and len(features) == len(labels) == len(purity)
            and np.isfinite(features).all()
            and np.isfinite(purity).all()
            and len(set(names.tolist())) == 618
        )
    except (OSError, KeyError, ValueError, TypeError, json.JSONDecodeError):
        return False


def process_subject(args: argparse.Namespace, cfg, entry, subject: int, inventory_item: dict[str, Any], cache_hash: str) -> dict[str, Any]:
    exercises = [int(x) for x in entry.exercise or []]
    output = cfg.artifact_root / "features" / args.db
    cache_path = output / f"S{subject:02d}.npz"
    meta_path = output / f"S{subject:02d}.json"
    if validate_cache(cache_path, subject, cache_hash):
        return {"subject": subject, "status": "reused_valid_cache", "cache": str(cache_path)}

    args.stage_root.mkdir(parents=True, exist_ok=True)
    required_free = int(args.min_free_gib * 1024**3)
    free = shutil.disk_usage(args.stage_root).free
    if free < required_free:
        raise RuntimeError(
            f"Insufficient free space before S{subject:02d}: {free / 1024**3:.2f} GiB available, "
            f"minimum configured is {args.min_free_gib:.2f} GiB"
        )

    subject_stage = args.stage_root / args.db / f"S{subject:02d}"
    archive = subject_stage / f"{args.db}_S{subject:02d}.zip"
    raw_root = subject_stage / "raw"
    subject_stage.mkdir(parents=True, exist_ok=True)
    started = utc_now()
    try:
        download_info = download_archive(
            str(inventory_item["url"]),
            archive,
            int(inventory_item["content_length"]) if inventory_item.get("content_length") else None,
        )
        extracted_files = extract_required_mat_files(archive, raw_root, subject, exercises)
        discovered = {exercise: [path.name for path in find_subject_files(raw_root, exercise, subject)] for exercise in exercises}
        if any(not files for files in discovered.values()):
            raise RuntimeError(f"Required files not discoverable after extraction: {discovered}")

        payload = subject_windows(raw_root, subject, exercises, cfg.protocol)
        features, names = extract_feature_matrix(
            payload["windows"],
            fs=cfg.protocol.fs,
            n_jobs=args.feature_workers,
        )
        if features.ndim != 2 or features.shape[1] != 618:
            raise RuntimeError(f"S{subject:02d}: expected [n, 618] features; got {features.shape}")
        if len(features) != len(payload["labels"]) or len(features) != len(payload["purity"]):
            raise RuntimeError(f"S{subject:02d}: feature/label/purity row count mismatch")
        if not np.isfinite(features).all():
            raise RuntimeError(f"S{subject:02d}: non-finite extracted features")
        if len(names) != 618 or len(set(names)) != 618:
            raise RuntimeError(f"S{subject:02d}: invalid feature-name schema")

        atomic_save_npz(
            cache_path,
            features=np.asarray(features, dtype=np.float32),
            labels=np.asarray(payload["labels"], dtype=np.int32),
            purity=np.asarray(payload["purity"], dtype=np.float32),
            feature_names=np.asarray(names, dtype=str),
        )
        metadata = {
            "db": args.db,
            "subject": subject,
            "exercises": exercises,
            "n_windows": int(len(payload["labels"])),
            "raw_features": int(features.shape[1]),
            "feature_schema": SCHEMA_VERSION,
            "cache_input_hash": cache_hash,
            "source_files": sorted(set(payload["source_files"])),
            "official_archive_url": inventory_item["url"],
            "official_archive_bytes": download_info["bytes"],
            "official_archive_sha256": download_info["sha256"],
            "download_status": download_info["status"],
            "extracted_files": extracted_files,
            "started_at_utc": started,
            "completed_at_utc": utc_now(),
        }
        atomic_save_json(metadata, meta_path)
        if not validate_cache(cache_path, subject, cache_hash):
            raise RuntimeError(f"S{subject:02d}: written cache failed validation")
        return {"subject": subject, "status": "prepared", "cache": str(cache_path), "metadata": metadata}
    finally:
        if not args.keep_raw_stage and validate_cache(cache_path, subject, cache_hash):
            shutil.rmtree(subject_stage, ignore_errors=True)


def finalize_manifest(cfg, entry, db: str, output: Path, cache_hash: str) -> dict[str, Any]:
    expected_subjects = list(range(1, int(entry.expected_subjects) + 1))
    summary = []
    reference_names: list[str] | None = None
    observed_labels: set[int] = set()
    for subject in expected_subjects:
        path = output / f"S{subject:02d}.npz"
        if not validate_cache(path, subject, cache_hash):
            raise RuntimeError(f"Cannot finalize: invalid/missing cache for S{subject:02d}")
        metadata = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
        with np.load(path, allow_pickle=False) as payload:
            names = payload["feature_names"].tolist()
            labels = payload["labels"]
        if reference_names is None:
            reference_names = names
        elif names != reference_names:
            raise RuntimeError(f"Feature ordering differs at S{subject:02d}")
        observed_labels.update(int(label) for label in np.unique(labels).tolist())
        summary.append(metadata)
    expected_labels = set(range(int(entry.expected_classes))) if entry.expected_classes else observed_labels
    if observed_labels != expected_labels:
        raise RuntimeError(
            f"Dataset-level label union mismatch: observed={sorted(observed_labels)}, expected={sorted(expected_labels)}"
        )
    manifest = {
        "db": db,
        "exercises": [int(x) for x in entry.exercise or []],
        "subjects": expected_subjects,
        "feature_schema": SCHEMA_VERSION,
        "config_hash": config_hash(cfg),
        "cache_input_hash": cache_hash,
        "created_at_utc": utc_now(),
        "preparation_mode": "official_subject_archives_staged_sequentially",
        "summary": summary,
    }
    atomic_save_json(manifest, output / "manifest.json")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, choices=("DB2", "DB3", "DB7"))
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "protocol_v1_1.yaml")
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "audit_outputs" / "official_ninapro_download_inventory.json",
    )
    parser.add_argument("--stage-root", type=Path, default=ROOT / "ninapro_staging")
    parser.add_argument("--subject", type=int, action="append", help="Process only this subject; can be repeated")
    parser.add_argument("--finalize-only", action="store_true", help="Validate all caches and write the dataset manifest")
    parser.add_argument("--feature-workers", type=int, default=3)
    parser.add_argument("--min-free-gib", type=float, default=8.0)
    parser.add_argument("--keep-raw-stage", action="store_true", help="Retain downloaded/extracted raw staging files after a valid cache write")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)
    if args.db not in cfg.datasets:
        raise SystemExit(f"Unknown database in configuration: {args.db}")
    entry = cfg.datasets[args.db]
    if not entry.exercise or not entry.expected_subjects or not entry.expected_classes:
        raise SystemExit(f"Incomplete dataset configuration for {args.db}")
    if args.feature_workers < 1:
        raise SystemExit("--feature-workers must be positive")
    inventory = load_inventory(args.inventory, args.db)
    expected_subjects = list(range(1, int(entry.expected_subjects) + 1))
    if sorted(inventory) != expected_subjects:
        raise SystemExit(f"Official inventory subject mismatch for {args.db}: {sorted(inventory)}")
    output = cfg.artifact_root / "features" / args.db
    output.mkdir(parents=True, exist_ok=True)
    cache_hash = cache_input_hash(cfg, entry)

    if args.finalize_only:
        manifest = finalize_manifest(cfg, entry, args.db, output, cache_hash)
        print(json.dumps({"status": "finalized", "manifest": manifest}, indent=2))
        return

    subjects = args.subject or expected_subjects
    if sorted(set(subjects)) != sorted(subjects):
        raise SystemExit("Subject IDs must be unique and sorted when supplied")
    invalid = sorted(set(subjects) - set(expected_subjects))
    if invalid:
        raise SystemExit(f"Invalid subjects for {args.db}: {invalid}")
    results = []
    for subject in subjects:
        began = time.perf_counter()
        record = process_subject(args, cfg, entry, subject, inventory[subject], cache_hash)
        record["elapsed_seconds"] = time.perf_counter() - began
        results.append(record)
        print(json.dumps(record, indent=2), flush=True)
    print(json.dumps({"db": args.db, "status": "subject_batch_complete", "results": results}, indent=2))


if __name__ == "__main__":
    main()
