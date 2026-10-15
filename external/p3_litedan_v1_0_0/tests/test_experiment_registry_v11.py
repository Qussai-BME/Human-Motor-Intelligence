from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "experiment_registry_v1_1.py"
CONFIG = ROOT / "configs" / "protocol_v1_1.yaml"
ARTIFACTS = ROOT / "artifacts_v1_1"


def test_registry_initializes_and_audits_without_fabricating_folds(tmp_path: Path) -> None:
    registry_root = tmp_path / "registry"
    results_root = tmp_path / "empty_results"
    common = [
        sys.executable,
        str(SCRIPT),
        "--config",
        str(CONFIG),
        "--artifact-root",
        str(ARTIFACTS),
        "--results-root",
        str(results_root),
        "--registry-root",
        str(registry_root),
    ]
    subprocess.run(
        common + ["init", "--datasets", "DB3", "--conditions", "lda"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        common + ["sync"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    plan = json.loads((registry_root / "experiment_plan.json").read_text(encoding="utf-8"))
    current = json.loads((registry_root / "current_experiments.json").read_text(encoding="utf-8"))
    assert len(plan["records"]) == 1
    assert plan["records"][0]["experiment_id"] == "P3V11-DB3-LDA"
    record = current["records"][0]
    assert record["status"] == "PLANNED"
    assert record["fold_counts"] == {"completed": 0, "missing": 11, "invalid": 0}
    assert len(record["folds"]) == 11
    assert all(fold["status"] == "MISSING" and not fold["valid"] for fold in record["folds"])
    assert record["cache"]["integrity_audit_dataset_valid"] is True
    assert len((registry_root / "registry_events.jsonl").read_text(encoding="utf-8").splitlines()) == 2
