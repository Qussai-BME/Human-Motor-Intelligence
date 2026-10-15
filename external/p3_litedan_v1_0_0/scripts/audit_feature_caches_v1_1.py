#!/usr/bin/env python3
"""Audit protocol-v1.1 NinaPro feature caches without assuming identical labels per subject.

This auditor validates every cache independently, then confirms only the invariant that
belongs at dataset level: the union of observed labels must equal the configured class
universe.  It records subject-specific missing labels verbatim, which is necessary for
DB7 S21 where the official Exercise-2 recording lacks two functional movements.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def audit_subject(
    db: str,
    subject: int,
    feature_dir: Path,
    expected_cache_hash: str,
    reference_names: list[str] | None,
) -> tuple[dict[str, Any], list[str], list[str] | None]:
    errors: list[str] = []
    npz_path = feature_dir / f"S{subject:02d}.npz"
    json_path = feature_dir / f"S{subject:02d}.json"
    if not npz_path.exists():
        fail(errors, f"missing NPZ: {npz_path}")
    if not json_path.exists():
        fail(errors, f"missing metadata: {json_path}")
    if errors:
        return {"subject": subject, "valid": False, "errors": errors}, errors, reference_names

    try:
        metadata = load_json(json_path)
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"invalid metadata JSON: {exc}")
        return {"subject": subject, "valid": False, "errors": errors}, errors, reference_names

    try:
        with np.load(npz_path, allow_pickle=False) as data:
            keys = sorted(data.files)
            required = {"features", "labels", "purity", "feature_names"}
            if set(keys) != required:
                fail(errors, f"NPZ key mismatch: {keys}")
            features = data["features"]
            labels = data["labels"]
            purity = data["purity"]
            names = data["feature_names"]
    except (OSError, ValueError, KeyError) as exc:
        fail(errors, f"unreadable NPZ: {exc}")
        return {"subject": subject, "valid": False, "errors": errors}, errors, reference_names

    if metadata.get("db") != db:
        fail(errors, f"metadata db={metadata.get('db')!r}, expected {db!r}")
    if metadata.get("subject") != subject:
        fail(errors, f"metadata subject={metadata.get('subject')!r}, expected {subject}")
    if metadata.get("feature_schema") != "current_618_v1":
        fail(errors, f"feature_schema={metadata.get('feature_schema')!r}")
    if metadata.get("cache_input_hash") != expected_cache_hash:
        fail(errors, "metadata cache_input_hash differs from manifest")
    if metadata.get("raw_features") != 618:
        fail(errors, f"metadata raw_features={metadata.get('raw_features')!r}")
    if not metadata.get("official_archive_url", "").startswith("https://ninapro.hevs.ch/"):
        fail(errors, "official archive URL is absent or not on the NinaPro official host")
    if not isinstance(metadata.get("official_archive_bytes"), int) or metadata["official_archive_bytes"] <= 0:
        fail(errors, "official archive byte count is absent or invalid")
    archive_sha = metadata.get("official_archive_sha256", "")
    if not isinstance(archive_sha, str) or len(archive_sha) != 64:
        fail(errors, "official archive SHA-256 is absent or malformed")
    if sorted(metadata.get("extracted_files", [])) != sorted(metadata.get("source_files", [])):
        fail(errors, "source_files and extracted_files differ")

    if features.ndim != 2 or features.shape[1] != 618:
        fail(errors, f"features shape={tuple(features.shape)}, expected [n, 618]")
    if labels.ndim != 1 or purity.ndim != 1 or names.ndim != 1:
        fail(errors, "labels, purity, and feature_names must all be one-dimensional")
    if not (len(features) == len(labels) == len(purity)):
        fail(errors, "features/labels/purity length mismatch")
    if len(names) != 618 or len(set(names.tolist())) != 618:
        fail(errors, "feature_names are not 618 unique entries")
    if not np.isfinite(features).all():
        fail(errors, "features include non-finite values")
    if not np.isfinite(purity).all():
        fail(errors, "purity includes non-finite values")
    if metadata.get("n_windows") != int(len(labels)):
        fail(errors, "metadata n_windows does not match labels")

    names_list = names.tolist()
    if reference_names is None:
        reference_names = names_list
    elif names_list != reference_names:
        fail(errors, "feature-name ordering differs from reference subject")

    label_set = sorted(int(value) for value in np.unique(labels).tolist())
    record = {
        "subject": subject,
        "valid": not errors,
        "n_windows": int(len(labels)),
        "feature_shape": [int(value) for value in features.shape],
        "label_set": label_set,
        "label_count": len(label_set),
        "npz_bytes": npz_path.stat().st_size,
        "npz_sha256": sha256_file(npz_path),
        "metadata_sha256": sha256_file(json_path),
        "official_archive_url": metadata.get("official_archive_url"),
        "official_archive_bytes": metadata.get("official_archive_bytes"),
        "official_archive_sha256": metadata.get("official_archive_sha256"),
        "download_status": metadata.get("download_status"),
        "errors": errors,
    }
    return record, errors, reference_names


def audit_db(db: str, entry: dict[str, Any], artifact_root: Path) -> dict[str, Any]:
    feature_dir = artifact_root / "features" / db
    manifest_path = feature_dir / "manifest.json"
    expected_subjects = list(range(1, int(entry["expected_subjects"]) + 1))
    expected_labels = list(range(int(entry["expected_classes"])))
    errors: list[str] = []
    if not manifest_path.exists():
        return {"db": db, "valid": False, "errors": [f"missing manifest: {manifest_path}"]}

    try:
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        return {"db": db, "valid": False, "errors": [f"invalid manifest JSON: {exc}"]}

    if manifest.get("db") != db:
        fail(errors, f"manifest db={manifest.get('db')!r}, expected {db!r}")
    if manifest.get("subjects") != expected_subjects:
        fail(errors, f"manifest subject list differs from {expected_subjects}")
    if manifest.get("feature_schema") != "current_618_v1":
        fail(errors, f"manifest feature_schema={manifest.get('feature_schema')!r}")
    manifest_cache_hash = manifest.get("cache_input_hash")
    if not isinstance(manifest_cache_hash, str) or not manifest_cache_hash:
        fail(errors, "manifest cache_input_hash is absent")
    summary = manifest.get("summary")
    if not isinstance(summary, list) or len(summary) != len(expected_subjects):
        fail(errors, "manifest summary has incorrect length")

    reference_names: list[str] | None = None
    records: list[dict[str, Any]] = []
    all_labels: set[int] = set()
    for subject in expected_subjects:
        record, subject_errors, reference_names = audit_subject(
            db, subject, feature_dir, str(manifest_cache_hash), reference_names
        )
        records.append(record)
        errors.extend(f"S{subject:02d}: {message}" for message in subject_errors)
        all_labels.update(record.get("label_set", []))
        if isinstance(summary, list) and len(summary) == len(expected_subjects):
            on_manifest = summary[subject - 1]
            metadata_path = feature_dir / f"S{subject:02d}.json"
            if metadata_path.exists():
                try:
                    if on_manifest != load_json(metadata_path):
                        fail(errors, f"S{subject:02d}: manifest summary differs from metadata sidecar")
                except (OSError, json.JSONDecodeError) as exc:
                    fail(errors, f"S{subject:02d}: cannot compare manifest summary: {exc}")

    observed_labels = sorted(all_labels)
    if observed_labels != expected_labels:
        fail(errors, f"dataset label union={observed_labels}, expected={expected_labels}")
    missing_by_subject = {
        f"S{record['subject']:02d}": sorted(set(expected_labels) - set(record.get("label_set", [])))
        for record in records
    }

    return {
        "db": db,
        "valid": not errors,
        "expected_subjects": len(expected_subjects),
        "observed_subjects": len(records),
        "expected_label_union": expected_labels,
        "observed_label_union": observed_labels,
        "manifest_sha256": sha256_file(manifest_path),
        "manifest_cache_input_hash": manifest_cache_hash,
        "feature_order_sha256": hashlib.sha256(",".join(reference_names or []).encode("utf-8")).hexdigest(),
        "subjects": records,
        "missing_labels_by_subject": missing_by_subject,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "protocol_v1_1.yaml")
    parser.add_argument("--artifact-root", type=Path, default=ROOT / "artifacts_v1_1")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts_v1_1" / "validation" / "cache_integrity_audit_v1_1.json")
    args = parser.parse_args()

    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    datasets = config.get("datasets", {})
    reports = {db: audit_db(db, datasets[db], args.artifact_root) for db in ("DB2", "DB3", "DB7")}
    overall_valid = all(report.get("valid", False) for report in reports.values())
    payload = {
        "audit_name": "protocol_v1_1_feature_cache_integrity",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "config_path": str(args.config),
        "config_sha256": sha256_file(args.config),
        "artifact_root": str(args.artifact_root),
        "policy": {
            "per_subject_label_identity_required": False,
            "dataset_level_label_union_required": True,
            "reason": "Official recordings can have genuine subject-specific unavailable movements; such labels must be recorded, not fabricated.",
        },
        "overall_valid": overall_valid,
        "datasets": reports,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(args.output)
    print(json.dumps({
        "overall_valid": overall_valid,
        "output": str(args.output),
        "datasets": {db: {"valid": report.get("valid"), "subjects": report.get("observed_subjects")} for db, report in reports.items()},
    }, indent=2))
    return 0 if overall_valid else 2


if __name__ == "__main__":
    sys.exit(main())
