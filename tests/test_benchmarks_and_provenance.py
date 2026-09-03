from __future__ import annotations

from pathlib import Path

import pytest

from research_core.benchmarks import BenchmarkEngine, BenchmarkError, SubjectMetricObservation
from research_core.contracts import ExperimentRecord, RunStatus
from research_core.provenance import ReproducibilityManifest
from research_core.reporting import write_benchmark_assets


def fixture_run(model_id: str, run_id: str) -> ExperimentRecord:
    """Create a test-only non-deliverable record to exercise aggregation invariants."""
    return ExperimentRecord(
        experiment_id=f"exp-{run_id}",
        run_id=run_id,
        project_id="test-project",
        protocol_id="test-protocol-v1",
        dataset_id="test-real-data-reference",
        dataset_version="test-version",
        modality="emg",
        subject_split="leave-one-subject-out",
        model_id=model_id,
        model_version="test-version",
        seed=42,
        configuration_hash="d" * 64,
        status=RunStatus.SUCCEEDED,
        completed_at_utc="2026-08-22T12:00:00+00:00",
        metadata={"benchmark_eligible": True, "test_fixture_only": True},
    )


def test_benchmark_requires_subject_level_protocol_consistent_observations(tmp_path: Path) -> None:
    run_a = fixture_run("model-a", "run-a")
    run_b = fixture_run("model-b", "run-b")
    observations = (
        SubjectMetricObservation("run-a", "test-protocol-v1", "test-real-data-reference", "model-a", "s1", "macro_f1", 0.4),
        SubjectMetricObservation("run-a", "test-protocol-v1", "test-real-data-reference", "model-a", "s2", "macro_f1", 0.6),
        SubjectMetricObservation("run-b", "test-protocol-v1", "test-real-data-reference", "model-b", "s1", "macro_f1", 0.5),
        SubjectMetricObservation("run-b", "test-protocol-v1", "test-real-data-reference", "model-b", "s2", "macro_f1", 0.7),
    )
    result = BenchmarkEngine.summarize(
        benchmark_id="test-benchmark",
        experiments=(run_a, run_b),
        observations=observations,
        metric_name="macro_f1",
    )

    assert result.summaries[0].subject_count == 2
    assert result.statistics["status"] == "not_run"
    paths = write_benchmark_assets(result, tmp_path / "assets")
    assert all(path.exists() for path in paths.values())
    assert "test-protocol-v1" in paths["markdown"].read_text(encoding="utf-8")
    assert "model-a" in paths["svg"].read_text(encoding="utf-8")


def test_benchmark_rejects_mixed_protocols_and_duplicate_subject_values() -> None:
    run = fixture_run("model-a", "run-a")
    duplicate = (
        SubjectMetricObservation("run-a", "test-protocol-v1", "test-real-data-reference", "model-a", "s1", "accuracy", 0.1),
        SubjectMetricObservation("run-a", "test-protocol-v1", "test-real-data-reference", "model-a", "s1", "accuracy", 0.2),
    )
    with pytest.raises(BenchmarkError, match="one subject-level value"):
        BenchmarkEngine.summarize(
            benchmark_id="test-benchmark",
            experiments=(run,),
            observations=duplicate,
            metric_name="accuracy",
        )


def test_manifest_stores_canonical_paths_for_relative_artifacts(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    output = Path("relative-output.txt")
    output.write_text("relative content\n", encoding="utf-8")
    manifest = ReproducibilityManifest.create(
        name="relative-path-test",
        project_id="test-project",
        protocol_id="test-protocol-v1",
        dataset_id="test-dataset",
        configuration={"mode": "relative-test"},
        seed=42,
        repo_root=tmp_path,
    ).with_artifact(output, "test-output")
    manifest_path = manifest.write(tmp_path / "manifest.json")
    assert Path(manifest.artifacts[0].path).is_absolute()
    assert ReproducibilityManifest.verify(manifest_path)["verified"] is True


def test_manifest_hashes_outputs_and_detects_tampering(tmp_path: Path) -> None:
    output = tmp_path / "output.txt"
    output.write_text("verified content\n", encoding="utf-8")
    manifest = ReproducibilityManifest.create(
        name="test-manifest",
        project_id="test-project",
        protocol_id="test-protocol-v1",
        dataset_id="test-dataset",
        configuration={"mode": "test"},
        seed=42,
        repo_root=tmp_path,
        packages=("pytest",),
    ).with_artifact(output, "test-output")
    manifest_path = manifest.write(tmp_path / "manifest.json")
    assert ReproducibilityManifest.verify(manifest_path)["verified"] is True

    output.write_text("modified content\n", encoding="utf-8")
    verification = ReproducibilityManifest.verify(manifest_path)
    assert verification["verified"] is False
    assert any(item.startswith("hash:") for item in verification["mismatches"])
