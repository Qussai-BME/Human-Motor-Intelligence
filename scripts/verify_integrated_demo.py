#!/usr/bin/env python3
"""Verify the committed end-to-end synthetic integration demonstration bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from research_core.provenance import ReproducibilityManifest
from research_core.registry import LocalResearchRegistry


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify synthetic end-to-end MyoSim integration evidence.")
    parser.add_argument("--root", type=Path, default=Path("artifacts/integrated_demo"))
    parser.add_argument("--registry-dir", type=Path, default=Path("registry/local"))
    args = parser.parse_args()
    root = args.root
    replay_bundle = json.loads((root / "replay_bundle.json").read_text(encoding="utf-8"))
    myosim_output = json.loads((root / "myosim_task_output.json").read_text(encoding="utf-8"))
    run_id = str(myosim_output["run_id"])
    demo_dir = root / "myosim" / run_id
    manifest_path = demo_dir / "umbrella_reproducibility_manifest.json"
    verification = ReproducibilityManifest.verify(manifest_path)
    registry = LocalResearchRegistry(args.registry_dir)
    experiment = registry.get("experiment", f"integrated-demo-{run_id}")
    checks = {
        "synthetic_bundle": replay_bundle.get("evidence_class") == "synthetic"
        and replay_bundle.get("benchmark_eligible") is False,
        "replay_event_count_matches_output": replay_bundle.get("intent_count") == myosim_output["control_metrics"]["event_count"],
        "task_success": myosim_output["task_metrics"].get("success") is True,
        "manifest_verified": verification["verified"],
        "experiment_is_nonbenchmark": experiment.document["metadata"].get("benchmark_eligible") is False
        and experiment.document["metadata"].get("synthetic") is True,
        "integrated_report_exists": (demo_dir / "INTEGRATED_DEMO_REPORT.md").is_file(),
    }
    report = {
        "run_id": run_id,
        "checks": checks,
        "all_passed": all(checks.values()),
        "manifest": verification,
        "evidence_boundary": "synthetic/non-benchmark integration evidence only",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
