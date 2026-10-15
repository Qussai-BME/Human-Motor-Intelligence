#!/usr/bin/env python3
"""Validate the final DB2 recovery evidence prior to checkpointing and packaging."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FEATURE_ROOT = ROOT / "artifacts_v1_1" / "features" / "DB2"
LEDGER = ROOT / "checkpoint_outputs" / "CHECKPOINT_LEDGER.jsonl"
EXPECTED_SUBJECTS = list(range(1, 41))
EXPECTED_CACHE_HASH = "07240fdd6edb"
EXPECTED_CONFIG_HASH = "25442563a7c0"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    manifest_path = FEATURE_ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    assert manifest["db"] == "DB2"
    assert manifest["subjects"] == EXPECTED_SUBJECTS
    assert manifest["feature_schema"] == "current_618_v1"
    assert manifest["cache_input_hash"] == EXPECTED_CACHE_HASH
    assert manifest["config_hash"] == EXPECTED_CONFIG_HASH
    assert manifest["exercises"] == [1, 2]
    assert len(manifest["summary"]) == 40

    rows = []
    label_union: set[int] = set()
    feature_name_reference: list[str] | None = None
    for subject in EXPECTED_SUBJECTS:
        stem = f"S{subject:02d}"
        npz_path = FEATURE_ROOT / f"{stem}.npz"
        metadata_path = FEATURE_ROOT / f"{stem}.json"
        assert npz_path.is_file(), npz_path
        assert metadata_path.is_file(), metadata_path
        metadata = json.loads(metadata_path.read_text())
        assert metadata["db"] == "DB2"
        assert metadata["subject"] == subject
        assert metadata["cache_input_hash"] == EXPECTED_CACHE_HASH
        assert metadata["raw_features"] == 618
        assert metadata["feature_schema"] == "current_618_v1"
        assert metadata["exercises"] == [1, 2]
        assert metadata["official_archive_url"].endswith(f"DB2_s{subject}.zip")
        assert metadata["official_archive_bytes"] > 0
        assert len(metadata["official_archive_sha256"]) == 64

        with np.load(npz_path, allow_pickle=False) as cache:
            names = set(cache.files)
            assert {"features", "labels", "feature_names", "purity"}.issubset(names), (stem, names)
            X = cache["features"]
            y = cache["labels"]
            feature_names = [str(x) for x in cache["feature_names"].tolist()]
        assert X.ndim == 2 and X.shape[1] == 618, (stem, X.shape)
        assert y.ndim == 1 and y.shape[0] == X.shape[0], (stem, X.shape, y.shape)
        assert X.shape[0] == metadata["n_windows"], (stem, X.shape[0], metadata["n_windows"])
        assert np.isfinite(X).all(), stem
        assert len(feature_names) == 618 and len(set(feature_names)) == 618, stem
        if feature_name_reference is None:
            feature_name_reference = feature_names
        else:
            assert feature_names == feature_name_reference, stem
        label_union.update(int(v) for v in np.unique(y))
        rows.append(
            {
                "subject": subject,
                "n_windows": int(X.shape[0]),
                "n_labels": int(np.unique(y).size),
                "labels": [int(v) for v in np.unique(y).tolist()],
                "npz_sha256": sha256(npz_path),
                "metadata_sha256": sha256(metadata_path),
            }
        )

    ledger_records = {}
    for line in LEDGER.read_text().splitlines():
        record = json.loads(line)
        checkpoint_id = record.get("checkpoint_id", "")
        if checkpoint_id.startswith("feature-DB2-S"):
            ledger_records[checkpoint_id] = record
    for subject in EXPECTED_SUBJECTS:
        checkpoint_id = f"feature-DB2-S{subject:02d}"
        assert checkpoint_id in ledger_records, checkpoint_id
        assert ledger_records[checkpoint_id].get("remote_url"), checkpoint_id

    result = {
        "status": "passed",
        "dataset": "DB2",
        "subject_count": 40,
        "feature_schema": "current_618_v1",
        "features_per_window": 618,
        "cache_input_hash": EXPECTED_CACHE_HASH,
        "config_hash": EXPECTED_CONFIG_HASH,
        "exercises": [1, 2],
        "label_union": sorted(label_union),
        "label_union_count": len(label_union),
        "feature_order_sha256": hashlib.sha256(
            "\n".join(feature_name_reference or []).encode("utf-8")
        ).hexdigest(),
        "manifest_sha256": sha256(manifest_path),
        "remote_checkpoint_count": 40,
        "subjects": rows,
    }
    output = FEATURE_ROOT / "finalization_validation_v1_1.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in result if k != "subjects"}, indent=2))


if __name__ == "__main__":
    main()
