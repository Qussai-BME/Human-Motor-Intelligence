#!/usr/bin/env python3
"""Create immutable checkpoint bundles for validated protocol-v1.1 artifacts.

A checkpoint includes the completed payload, mandatory sidecar provenance, active
configuration, official archive inventory, and an internal SHA-256 manifest. The
script refuses incomplete cache/experiment artifacts. It creates a local bundle that
is then uploaded by the calling workflow; the returned remote URL is registered in
an append-only checkpoint ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def add_file(source: Path, destination: Path, staged: list[Path]) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Required checkpoint input is absent: {source}")
    target = destination / source.name
    shutil.copy2(source, target)
    staged.append(target)


def checkpoint_feature_cache(args: argparse.Namespace) -> tuple[str, Path, dict[str, Any]]:
    db = args.db
    subject = int(args.subject)
    subject_id = f"S{subject:02d}"
    feature_dir = args.project_root / "artifacts_v1_1" / "features" / db
    cache = feature_dir / f"{subject_id}.npz"
    metadata = feature_dir / f"{subject_id}.json"
    if not cache.exists() or not metadata.exists():
        raise FileNotFoundError(f"Validated feature cache sidecar pair is incomplete for {db}/{subject_id}")
    meta = json.loads(metadata.read_text(encoding="utf-8"))
    required = ("db", "subject", "official_archive_url", "official_archive_bytes", "official_archive_sha256", "cache_input_hash", "feature_schema")
    missing = [field for field in required if field not in meta]
    if missing or meta.get("db") != db or int(meta.get("subject", -1)) != subject:
        raise ValueError(f"Invalid feature-cache provenance for {db}/{subject_id}; missing/mismatched {missing}")
    checkpoint_id = f"feature-{db}-{subject_id}"
    with tempfile.TemporaryDirectory(prefix=f"{checkpoint_id}-") as temp:
        stage = Path(temp) / checkpoint_id
        stage.mkdir()
        staged: list[Path] = []
        add_file(cache, stage, staged)
        add_file(metadata, stage, staged)
        add_file(args.project_root / "configs" / "protocol_v1_1.yaml", stage, staged)
        add_file(args.project_root / "audit_outputs" / "official_ninapro_download_inventory.json", stage, staged)
        manifest = {
            "checkpoint_id": checkpoint_id,
            "created_at_utc": utc_now(),
            "artifact_type": "validated_feature_cache",
            "dataset": db,
            "subject": subject,
            "source_metadata": meta,
            "files": [{"name": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path)} for path in staged],
        }
        manifest_path = stage / "CHECKPOINT_MANIFEST.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        bundle = args.checkpoint_root / "bundles" / f"{checkpoint_id}.tar.gz"
        bundle.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(bundle, "w:gz") as archive:
            archive.add(stage, arcname=checkpoint_id)
    record = {
        "checkpoint_id": checkpoint_id,
        "created_at_utc": utc_now(),
        "artifact_type": "validated_feature_cache",
        "dataset": db,
        "subject": subject,
        "bundle": str(bundle),
        "bundle_bytes": bundle.stat().st_size,
        "bundle_sha256": sha256_file(bundle),
        "remote_url": None,
        "source_metadata": meta,
    }
    return checkpoint_id, bundle, record


def cmd_create(args: argparse.Namespace) -> int:
    checkpoint_id, bundle, record = checkpoint_feature_cache(args)
    record_path = args.checkpoint_root / "records" / f"{checkpoint_id}.json"
    atomic_json(record_path, record)
    print(json.dumps({"checkpoint_id": checkpoint_id, "bundle": str(bundle), "record": str(record_path), "bundle_sha256": record["bundle_sha256"]}, indent=2))
    return 0


def cmd_register(args: argparse.Namespace) -> int:
    record_path = args.checkpoint_root / "records" / f"{args.checkpoint_id}.json"
    if not record_path.exists():
        raise FileNotFoundError(f"Checkpoint record not found: {record_path}")
    record = json.loads(record_path.read_text(encoding="utf-8"))
    bundle = Path(record["bundle"])
    if not bundle.exists() or sha256_file(bundle) != record["bundle_sha256"]:
        raise ValueError("Local checkpoint bundle is absent or no longer matches its recorded SHA-256")
    record["remote_url"] = args.remote_url
    record["registered_at_utc"] = utc_now()
    atomic_json(record_path, record)
    ledger = args.checkpoint_root / "CHECKPOINT_LEDGER.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps({"checkpoint_id": args.checkpoint_id, "remote_url": args.remote_url, "ledger": str(ledger)}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--checkpoint-root", type=Path, default=ROOT / "checkpoint_outputs")
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create-feature-cache")
    create.add_argument("--db", choices=("DB2", "DB3", "DB7"), required=True)
    create.add_argument("--subject", type=int, required=True)
    create.set_defaults(func=cmd_create)
    register = sub.add_parser("register-remote")
    register.add_argument("--checkpoint-id", required=True)
    register.add_argument("--remote-url", required=True)
    register.set_defaults(func=cmd_register)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"CHECKPOINT ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
