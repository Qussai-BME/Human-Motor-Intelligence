#!/usr/bin/env python3
"""Maintain the protocol-v1.1 strict-LOSO experiment registry.

The registry separates an immutable experiment plan from audited run snapshots.  Each
planned experiment has a deterministic identifier.  Synchronization reads existing
fold artifacts but never edits them; it validates strict-LOSO provenance, records the
per-fold metrics and runtime, and writes current JSON/CSV views plus an append-only
JSONL event log.  A run becomes COMPLETED only if every configured held-out subject
has one compatible completed fold and a matching complete summary.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_VERSION = "protocol-v1.1-experiment-registry.1"
CODE_VERSION = "protocol-v1.1.0"
PREPROCESSING_ORDER = "outer_LOSO>source_only_SelectKBest>source_only_StandardScaler>fit>held_out_prediction"
DEFAULT_DATASETS = ("DB2", "DB3", "DB7")
DEFAULT_CONDITIONS = (
    "lda",
    "random_forest",
    "xgb",
    "coral_xgb",
    "litedan",
    "litedan_fixed_0p1",
    "litedan_fixed_0p5",
    "litedan_fixed_1p0",
    "litedan_no_grl",
)
REQUIRED_METRICS = (
    "accuracy",
    "macro_f1",
    "macro_f1_fixed41",
    "kappa",
    "rest_recall",
    "active_only_accuracy",
    "active_only_macro_f1",
    "inflation_pp",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def experiment_id(db: str, condition: str) -> str:
    return f"P3V11-{db}-{condition.replace('_', '-').upper()}"


def architecture_version(condition: str) -> str | None:
    return "LDAN-v1.0" if condition.startswith("litedan") else None


def code_manifest() -> dict[str, Any]:
    critical = [
        ROOT / "src" / "litedan_p3" / "cli.py",
        ROOT / "src" / "litedan_p3" / "evaluation" / "pipeline.py",
        ROOT / "src" / "litedan_p3" / "models" / "litedan.py",
        ROOT / "src" / "litedan_p3" / "evaluation" / "stats.py",
    ]
    files = []
    for path in critical:
        if not path.exists():
            raise FileNotFoundError(f"Missing code file required for registry fingerprint: {path}")
        files.append({"path": str(path.relative_to(ROOT)), "sha256": sha256_file(path)})
    joint = "\n".join(f"{item['path']}:{item['sha256']}" for item in files)
    return {"code_version": CODE_VERSION, "code_fingerprint_sha256": sha256_text(joint), "files": files}


def config_fingerprint(config_path: Path) -> tuple[dict[str, Any], str]:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return config, sha256_file(config_path)


def cache_evidence(artifact_root: Path, db: str) -> dict[str, Any]:
    manifest_path = artifact_root / "features" / db / "manifest.json"
    evidence: dict[str, Any] = {
        "manifest_path": str(manifest_path),
        "manifest_exists": manifest_path.exists(),
        "manifest_sha256": sha256_file(manifest_path) if manifest_path.exists() else None,
        "cache_input_hash": None,
        "feature_schema": None,
    }
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        evidence["cache_input_hash"] = manifest.get("cache_input_hash")
        evidence["feature_schema"] = manifest.get("feature_schema")
        evidence["subjects"] = manifest.get("subjects")
    audit_path = artifact_root / "validation" / "cache_integrity_audit_v1_1.json"
    evidence["integrity_audit_path"] = str(audit_path)
    evidence["integrity_audit_sha256"] = sha256_file(audit_path) if audit_path.exists() else None
    if audit_path.exists():
        audit = load_json(audit_path)
        db_audit = audit.get("datasets", {}).get(db, {})
        evidence["integrity_audit_overall_valid"] = audit.get("overall_valid")
        evidence["integrity_audit_dataset_valid"] = db_audit.get("valid")
    else:
        evidence["integrity_audit_overall_valid"] = False
        evidence["integrity_audit_dataset_valid"] = False
    return evidence


def create_plan(config: dict[str, Any], config_path: Path, dataset_names: list[str], conditions: list[str]) -> dict[str, Any]:
    unknown_datasets = sorted(set(dataset_names) - set(config.get("datasets", {})))
    if unknown_datasets:
        raise ValueError(f"Unknown configured datasets: {unknown_datasets}")
    plan_time = utc_now()
    records = []
    for db in dataset_names:
        expected = int(config["datasets"][db]["expected_subjects"])
        for condition in conditions:
            records.append({
                "experiment_id": experiment_id(db, condition),
                "dataset": db,
                "condition": condition,
                "architecture_version": architecture_version(condition),
                "planned_at_utc": plan_time,
                "expected_subjects": list(range(1, expected + 1)),
                "strict_zero_calibration": True,
                "target_unlabelled_exposure": False,
                "preprocessing_order": PREPROCESSING_ORDER,
                "purpose": "required_definitive_protocol_v1_1_experiment",
            })
    return {
        "registry_version": REGISTRY_VERSION,
        "created_at_utc": plan_time,
        "config_path": str(config_path),
        "config_sha256": sha256_file(config_path),
        "records": records,
    }


def validate_fold(
    path: Path,
    expected: dict[str, Any],
    config_sha256: str,
    cache: dict[str, Any],
) -> dict[str, Any]:
    subject = int(expected["subject"])
    result: dict[str, Any] = {"test_subject": subject, "path": str(path), "exists": path.exists()}
    if not path.exists():
        result.update({"status": "MISSING", "valid": False, "errors": ["fold artifact is absent"]})
        return result
    try:
        payload = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        result.update({"status": "INVALID", "valid": False, "errors": [f"unreadable JSON: {exc}"]})
        return result

    errors: list[str] = []
    metrics = payload.get("metrics")
    expected_train = expected["expected_train_subjects"]
    protocol = payload.get("protocol", {})
    if payload.get("experiment_status") != "COMPLETED":
        errors.append("experiment_status is not COMPLETED")
    if payload.get("code_version") != CODE_VERSION:
        errors.append("code_version mismatch")
    if payload.get("config_hash") != expected["fold_config_hash"]:
        errors.append("fold config_hash differs from canonical application config hash")
    if payload.get("feature_schema") != cache.get("feature_schema"):
        errors.append("fold feature_schema differs from cache manifest")
    if payload.get("condition") != expected["condition"]:
        errors.append("condition mismatch")
    if payload.get("test_subject") != subject:
        errors.append("test_subject mismatch")
    if payload.get("train_subject_ids") != expected_train:
        errors.append("train_subject_ids mismatch")
    if protocol.get("strict_zero_calibration") is not True:
        errors.append("strict_zero_calibration is not true")
    if protocol.get("target_unlabelled_exposure") is not False:
        errors.append("target_unlabelled_exposure is not false")
    if protocol.get("preprocessing_order") != PREPROCESSING_ORDER:
        errors.append("preprocessing_order mismatch")
    if not isinstance(metrics, dict):
        errors.append("metrics are absent")
        metrics = {}
    else:
        absent = sorted(set(REQUIRED_METRICS) - set(metrics))
        if absent:
            errors.append(f"required metrics missing: {absent}")
    for field in ("n_train", "n_train_full", "n_test", "n_selected_features", "prep_seconds", "fit_seconds", "predict_seconds", "model_elapsed_seconds", "fold_elapsed_seconds"):
        if field not in payload:
            errors.append(f"provenance/runtime field missing: {field}")
    if payload.get("architecture_version") != expected["architecture_version"]:
        errors.append("architecture_version mismatch")

    result.update({
        "status": "COMPLETED" if not errors else "INVALID",
        "valid": not errors,
        "errors": errors,
        "fold_sha256": sha256_file(path),
        "metrics": metrics,
        "runtime_seconds": {
            name: payload.get(name)
            for name in ("prep_seconds", "fit_seconds", "predict_seconds", "model_elapsed_seconds", "fold_elapsed_seconds")
        },
        "provenance": {
            name: payload.get(name)
            for name in ("experiment_status", "architecture_version", "code_version", "config_hash", "feature_schema", "condition", "test_subject", "train_subject_ids", "seed", "n_train", "n_train_full", "n_test", "n_train_subjects", "n_selected_features", "selected_feature_indices")
        },
    })
    return result


def summary_validation(path: Path, record: dict[str, Any], cache: dict[str, Any], expected_subjects: list[int]) -> dict[str, Any]:
    evidence: dict[str, Any] = {"path": str(path), "exists": path.exists()}
    if not path.exists():
        evidence.update({"valid": False, "errors": ["summary is absent"]})
        return evidence
    try:
        summary = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        evidence.update({"valid": False, "errors": [f"unreadable summary: {exc}"]})
        return evidence
    errors = []
    if summary.get("db") != record["dataset"]:
        errors.append("summary dataset mismatch")
    if summary.get("condition") != record["condition"]:
        errors.append("summary condition mismatch")
    if summary.get("completed_subjects") != expected_subjects:
        errors.append("summary completed_subjects mismatch")
    if summary.get("requested_subjects") != expected_subjects:
        errors.append("summary requested_subjects mismatch")
    if summary.get("n_subjects") != len(expected_subjects):
        errors.append("summary n_subjects mismatch")
    if summary.get("feature_schema") != cache.get("feature_schema"):
        errors.append("summary feature_schema mismatch")
    evidence.update({"valid": not errors, "errors": errors, "sha256": sha256_file(path)})
    return evidence


def audit_record(
    plan_record: dict[str, Any],
    application_config_sha256: str,
    canonical_config_hash_value: str,
    cache: dict[str, Any],
    code: dict[str, Any],
    results_root: Path,
) -> dict[str, Any]:
    db = plan_record["dataset"]
    condition = plan_record["condition"]
    subjects = [int(subject) for subject in plan_record["expected_subjects"]]
    directory = results_root / db / condition
    fold_records = []
    for subject in subjects:
        fold_records.append(validate_fold(
            directory / f"fold_S{subject:02d}.json",
            {
                "subject": subject,
                "condition": condition,
                "architecture_version": plan_record["architecture_version"],
                "expected_train_subjects": [value for value in subjects if value != subject],
                "fold_config_hash": canonical_config_hash_value,
            },
            application_config_sha256,
            cache,
        ))
    counts = {
        "completed": sum(row["status"] == "COMPLETED" for row in fold_records),
        "missing": sum(row["status"] == "MISSING" for row in fold_records),
        "invalid": sum(row["status"] == "INVALID" for row in fold_records),
    }
    summary = summary_validation(directory / "summary.json", plan_record, cache, subjects)
    if not cache.get("manifest_exists") or not cache.get("integrity_audit_dataset_valid"):
        status = "BLOCKED_CACHE_INVALID"
    elif counts["invalid"]:
        status = "INVALID"
    elif counts["completed"] == len(subjects) and summary["valid"]:
        status = "COMPLETED"
    elif counts["completed"]:
        status = "IN_PROGRESS"
    else:
        status = "PLANNED"
    return {
        **plan_record,
        "status": status,
        "audited_at_utc": utc_now(),
        "results_directory": str(directory),
        "config": {"application_config_sha256": application_config_sha256, "fold_config_hash": canonical_config_hash_value},
        "code": code,
        "cache": cache,
        "fold_counts": counts,
        "folds": fold_records,
        "summary": summary,
    }


def canonical_config_hash(config_path: Path) -> str:
    """Obtain the exact config_hash implementation used by the experiment pipeline."""
    sys.path.insert(0, str(ROOT / "src"))
    from litedan_p3.config import config_hash, load_config  # pylint: disable=import-outside-toplevel
    return config_hash(load_config(config_path))


def write_csv_views(registry_root: Path, records: list[dict[str, Any]]) -> None:
    experiment_rows = []
    fold_rows = []
    for record in records:
        experiment_rows.append({
            "experiment_id": record["experiment_id"],
            "dataset": record["dataset"],
            "condition": record["condition"],
            "architecture_version": record["architecture_version"],
            "status": record["status"],
            "planned_at_utc": record["planned_at_utc"],
            "audited_at_utc": record["audited_at_utc"],
            "expected_folds": len(record["expected_subjects"]),
            "completed_folds": record["fold_counts"]["completed"],
            "missing_folds": record["fold_counts"]["missing"],
            "invalid_folds": record["fold_counts"]["invalid"],
            "application_config_sha256": record["config"]["application_config_sha256"],
            "fold_config_hash": record["config"]["fold_config_hash"],
            "code_fingerprint_sha256": record["code"]["code_fingerprint_sha256"],
            "cache_input_hash": record["cache"].get("cache_input_hash"),
            "cache_manifest_sha256": record["cache"].get("manifest_sha256"),
            "cache_integrity_audit_sha256": record["cache"].get("integrity_audit_sha256"),
            "summary_valid": record["summary"].get("valid"),
        })
        for fold in record["folds"]:
            provenance = fold.get("provenance", {})
            runtime = fold.get("runtime_seconds", {})
            metrics = fold.get("metrics", {})
            fold_rows.append({
                "experiment_id": record["experiment_id"],
                "dataset": record["dataset"],
                "condition": record["condition"],
                "test_subject": fold["test_subject"],
                "status": fold["status"],
                "valid": fold["valid"],
                "fold_sha256": fold.get("fold_sha256"),
                "accuracy": metrics.get("accuracy"),
                "macro_f1": metrics.get("macro_f1"),
                "active_only_macro_f1": metrics.get("active_only_macro_f1"),
                "fit_seconds": runtime.get("fit_seconds"),
                "fold_elapsed_seconds": runtime.get("fold_elapsed_seconds"),
                "seed": provenance.get("seed"),
                "train_subject_ids": json.dumps(provenance.get("train_subject_ids")),
                "selected_feature_count": provenance.get("n_selected_features"),
                "strict_zero_calibration": provenance.get("experiment_status") == "COMPLETED" and not fold.get("errors"),
                "errors": " | ".join(fold.get("errors", [])),
            })
    def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        keys = list(rows[0]) if rows else []
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)
    write_rows(registry_root / "experiment_registry.csv", experiment_rows)
    write_rows(registry_root / "fold_registry.csv", fold_rows)


def cmd_init(args: argparse.Namespace) -> int:
    config, _ = config_fingerprint(args.config)
    datasets = args.datasets or list(DEFAULT_DATASETS)
    conditions = args.conditions or list(DEFAULT_CONDITIONS)
    plan_path = args.registry_root / "experiment_plan.json"
    if plan_path.exists() and not args.force:
        raise FileExistsError(f"Plan already exists: {plan_path}. Use --force only to recreate before any experiment execution.")
    plan = create_plan(config, args.config, datasets, conditions)
    atomic_json(plan_path, plan)
    event_path = args.registry_root / "registry_events.jsonl"
    event_path.parent.mkdir(parents=True, exist_ok=True)
    with event_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"event": "PLAN_INITIALIZED", "at_utc": utc_now(), "plan_sha256": sha256_file(plan_path), "n_experiments": len(plan["records"])}, sort_keys=True) + "\n")
    print(json.dumps({"status": "PLAN_INITIALIZED", "plan": str(plan_path), "n_experiments": len(plan["records"])}, indent=2))
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    plan_path = args.registry_root / "experiment_plan.json"
    if not plan_path.exists():
        raise FileNotFoundError(f"No registry plan at {plan_path}; run init first.")
    plan = load_json(plan_path)
    _, application_config_sha256 = config_fingerprint(args.config)
    canonical_hash = canonical_config_hash(args.config)
    code = code_manifest()
    cache_by_db = {db: cache_evidence(args.artifact_root, db) for db in DEFAULT_DATASETS}
    records = []
    for plan_record in plan["records"]:
        audited = audit_record(
            plan_record,
            application_config_sha256,
            canonical_hash,
            cache_by_db[plan_record["dataset"]],
            code,
            args.results_root,
        )
        records.append(audited)
    snapshot = {
        "registry_version": REGISTRY_VERSION,
        "plan_path": str(plan_path),
        "plan_sha256": sha256_file(plan_path),
        "synced_at_utc": utc_now(),
        "records": records,
    }
    current_path = args.registry_root / "current_experiments.json"
    atomic_json(current_path, snapshot)
    write_csv_views(args.registry_root, records)
    status_counts: dict[str, int] = {}
    for record in records:
        status_counts[record["status"]] = status_counts.get(record["status"], 0) + 1
    event = {"event": "REGISTRY_SYNC", "at_utc": utc_now(), "snapshot_sha256": sha256_file(current_path), "status_counts": status_counts}
    with (args.registry_root / "registry_events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    print(json.dumps({"status": "SYNCED", "current": str(current_path), "status_counts": status_counts, "n_experiments": len(records)}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "protocol_v1_1.yaml")
    parser.add_argument("--artifact-root", type=Path, default=ROOT / "artifacts_v1_1")
    parser.add_argument("--results-root", type=Path, default=ROOT / "results_v1_1")
    parser.add_argument("--registry-root", type=Path, default=ROOT / "results_v1_1" / "registry")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--datasets", nargs="*", choices=DEFAULT_DATASETS)
    init.add_argument("--conditions", nargs="*", choices=DEFAULT_CONDITIONS)
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)
    sync = sub.add_parser("sync")
    sync.set_defaults(func=cmd_sync)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileNotFoundError, ValueError) as exc:
        print(f"REGISTRY ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
