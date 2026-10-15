#!/usr/bin/env python3
"""Finalize a synthetic replay-first MyoSim integration demonstration.

This script does not compute, alter, or reinterpret simulator metrics. It reads
MyoSim's public CLI output, preserves selected simulator-owned artifacts, marks
all evidence synthetic/non-benchmark, registers the execution locally, and
creates an umbrella reproducibility manifest.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
from typing import Any

from research_core.contracts import ArtifactRecord, ArtifactRole, EvidenceClass, ExperimentRecord, RunStatus, sha256_json
from research_core.provenance import ReproducibilityManifest, sha256_file
from research_core.registry import LocalResearchRegistry


COPY_NAMES = (
    "report.md",
    "summary.json",
    "provenance.json",
    "task_metrics.json",
    "control_metrics.json",
    "task_transitions.json",
    "control_transitions.json",
    "pick_place_clean.gif",
    "pick_place_debug.gif",
)


def _copy_existing(source_dir: Path, target_dir: Path) -> list[Path]:
    copied: list[Path] = []
    for name in COPY_NAMES:
        source = source_dir / name
        if source.is_file():
            target = target_dir / name
            shutil.copy2(source, target)
            copied.append(target)
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize a synthetic MyoSim integrated demo bundle.")
    parser.add_argument("--myosim-output", type=Path, required=True)
    parser.add_argument("--replay-bundle", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/integrated_demo"))
    parser.add_argument("--registry-dir", type=Path, default=Path("registry/local"))
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()

    output = json.loads(args.myosim_output.read_text(encoding="utf-8"))
    replay = json.loads(args.replay_bundle.read_text(encoding="utf-8"))
    run_id = str(output["run_id"])
    source_run_dir = Path(output["run_dir"])
    destination = args.output_dir / "myosim" / run_id
    destination.mkdir(parents=True, exist_ok=True)
    copied = _copy_existing(source_run_dir, destination)
    task_metrics = output["task_metrics"]
    control_metrics = output["control_metrics"]

    artifact_records: list[ArtifactRecord] = []
    for path in copied:
        suffix = path.suffix.lower()
        role = ArtifactRole.VIDEO if suffix == ".gif" else ArtifactRole.REPORT if path.name == "report.md" else ArtifactRole.OTHER
        artifact_records.append(
            ArtifactRecord(
                artifact_id=f"{run_id}-{path.stem}",
                role=role,
                uri=str(path),
                producing_run_id=run_id,
                evidence_class=EvidenceClass.SYNTHETIC,
                sha256=sha256_file(path),
                media_type="image/gif" if suffix == ".gif" else "application/json" if suffix == ".json" else "text/markdown",
                metadata={"source_project": "myosim", "integration_demo": True, "benchmark_eligible": False},
            )
        )
    configuration = {
        "replay_bundle_sha256": sha256_file(args.replay_bundle),
        "replay_csv_sha256": replay["replay_csv_sha256"],
        "myosim_run_id": run_id,
        "myosim_task": task_metrics["task_name"],
        "evidence_class": "synthetic",
        "benchmark_eligible": False,
    }
    manifest = ReproducibilityManifest.create(
        name="integrated-synthetic-replay-demo",
        project_id="human-motor-intelligence",
        protocol_id="intent-to-control-v1",
        dataset_id="synthetic-integration-fixture",
        configuration=configuration,
        seed=20260822,
        repo_root=args.repo_root,
        packages=("myosim",),
    )
    for path in copied:
        manifest = manifest.with_artifact(path, "myosim-output")
    manifest_path = manifest.write(destination / "umbrella_reproducibility_manifest.json")
    artifact_records.append(
        ArtifactRecord(
            artifact_id=f"{run_id}-umbrella-manifest",
            role=ArtifactRole.MANIFEST,
            uri=str(manifest_path),
            producing_run_id=run_id,
            evidence_class=EvidenceClass.SYNTHETIC,
            sha256=sha256_file(manifest_path),
            media_type="application/json",
            metadata={"source_project": "human-motor-intelligence", "benchmark_eligible": False},
        )
    )
    experiment = ExperimentRecord(
        experiment_id=f"integrated-demo-{run_id}",
        run_id=run_id,
        project_id="human-motor-intelligence",
        protocol_id="intent-to-control-v1",
        dataset_id="synthetic-integration-fixture",
        dataset_version="v1",
        modality="emg",
        subject_split="deterministic-replay",
        model_id="myocontrol-to-myosim-adapter-fixture",
        model_version="v1",
        seed=20260822,
        configuration_hash=sha256_json(configuration),
        status=RunStatus.SUCCEEDED,
        completed_at_utc="2026-08-22T00:00:00+00:00",
        environment=manifest.environment,
        metrics={
            "task_success": 1.0 if task_metrics.get("success") else 0.0,
            "completion_time_s": task_metrics.get("completion_time_s") or 0.0,
            "false_activation_rate": control_metrics.get("false_activation_rate", 0.0),
            "mean_confirmation_latency_s": control_metrics.get("mean_confirmation_latency_s", 0.0),
            "command_corrections": float(task_metrics.get("command_corrections", 0.0)),
        },
        artifact_ids=tuple(record.artifact_id for record in artifact_records),
        metadata={
            "synthetic": True,
            "benchmark_eligible": False,
            "purpose": "deterministic adapter/simulator integration demonstration only",
            "myosim_source_run_dir": str(source_run_dir),
        },
    )
    registry = LocalResearchRegistry(args.registry_dir)
    registry.register_experiment_run(experiment, event_context={"source": "integrated_synthetic_demo"})
    for record in artifact_records:
        registry.register(record, event_context={"source": "integrated_synthetic_demo"})
    registration_path = destination / "umbrella_contract_records.json"
    registration_path.write_text(
        json.dumps(
            {
                "experiment": experiment.to_dict(),
                "artifacts": [record.to_dict() for record in artifact_records],
                "note": "All records are synthetic/non-benchmark integration evidence.",
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    report_path = destination / "INTEGRATED_DEMO_REPORT.md"
    report_path.write_text(
        "# Integrated Replay Demonstration\n\n"
        "> **Evidence status:** synthetic deterministic integration fixture. This is not a biosignal benchmark, decoder validation, clinical result, or hardware demonstration.\n\n"
        "## Flow\n\n"
        "Serialized synthetic MyoControl-shaped prediction → `IntentRecord` → explicit MyoSim label map → MyoSim CSV replay → MyoSim control/safety/task pipeline → simulator-owned metrics and recordings.\n\n"
        "## MyoSim-Reported Outcomes\n\n"
        f"| Metric | Value |\n|---|---:|\n| Task | {task_metrics['task_name']} |\n| Success | {task_metrics['success']} |\n| Completion time (s) | {task_metrics['completion_time_s']} |\n| Final state | {task_metrics['final_state']} |\n| False activation rate | {control_metrics['false_activation_rate']} |\n| Mean confirmation latency (s) | {control_metrics['mean_confirmation_latency_s']} |\n\n"
        "## Reproducibility\n\n"
        f"The replay bundle and copied MyoSim artifacts are hashed in `{manifest_path.name}`. The registered run ID is `{run_id}`.\n",
        encoding="utf-8",
    )
    print(json.dumps({"demo_dir": str(destination), "run_id": run_id, "report": str(report_path), "manifest": str(manifest_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
