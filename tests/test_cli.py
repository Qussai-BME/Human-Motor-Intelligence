from __future__ import annotations

import json
from pathlib import Path

from research_core.cli.main import main
from research_core.provenance import ReproducibilityManifest


def _output(capsys) -> dict | list:
    return json.loads(capsys.readouterr().out)


def test_cli_seeds_summarizes_and_checks_integrity(tmp_path: Path, capsys) -> None:
    registry = tmp_path / "registry"
    assert main(["--registry-dir", str(registry), "seed"]) == 0
    seeded = _output(capsys)
    assert isinstance(seeded, dict)
    assert seeded["seeded"] == 22

    assert main(["--registry-dir", str(registry), "summary"]) == 0
    summary = _output(capsys)
    assert isinstance(summary, dict)
    assert summary["entity_counts"]["dataset"] == 6

    assert main(["--registry-dir", str(registry), "integrity"]) == 0
    integrity = _output(capsys)
    assert isinstance(integrity, dict)
    assert integrity["verified"] is True


def test_cli_typed_registry_navigation_and_doctor_are_read_only(tmp_path: Path, capsys) -> None:
    registry = tmp_path / "registry"
    assert main(["--registry-dir", str(registry), "seed"]) == 0
    _output(capsys)

    assert main(["--registry-dir", str(registry), "dataset", "list"]) == 0
    datasets = _output(capsys)
    assert isinstance(datasets, list)
    assert len(datasets) == 6
    dataset_id = datasets[0]["entity_id"]

    assert main(["--registry-dir", str(registry), "dataset", "show", dataset_id]) == 0
    dataset = _output(capsys)
    assert isinstance(dataset, dict)
    assert dataset["entity_type"] == "dataset"
    assert dataset["entity_id"] == dataset_id

    assert main(["--registry-dir", str(registry), "protocol", "list"]) == 0
    protocols = _output(capsys)
    assert isinstance(protocols, list)
    protocol_id = protocols[0]["entity_id"]

    assert main(["--registry-dir", str(registry), "protocol", "validate", protocol_id]) == 0
    protocol = _output(capsys)
    assert isinstance(protocol, dict)
    assert protocol["validated"] is True
    assert protocol["governance"]["statistical_unit"] == "subject"

    for entity in ("benchmark", "artifact", "report"):
        assert main(["--registry-dir", str(registry), entity, "list"]) == 0
        entries = _output(capsys)
        assert isinstance(entries, list)

    before = (registry / "registry.json").read_text(encoding="utf-8")
    assert main(["--registry-dir", str(registry), "doctor"]) == 0
    doctor = _output(capsys)
    assert isinstance(doctor, dict)
    assert doctor["registry_integrity"]["verified"] is True
    assert doctor["data_governance"]["status"] == "pass"
    assert doctor["evidence_gates"]["p3"] == "pending_original_author_package"
    assert doctor["evidence_gates"]["p6_r3"] == "blocked_pending_authentic_trace_provenance"
    assert (registry / "registry.json").read_text(encoding="utf-8") == before


def test_cli_verifies_manifest(tmp_path: Path, capsys) -> None:
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("content\n", encoding="utf-8")
    manifest = ReproducibilityManifest.create(
        name="cli-manifest",
        project_id="test-project",
        protocol_id="test-protocol-v1",
        dataset_id="test-dataset",
        configuration={"purpose": "test"},
        seed=1,
        repo_root=tmp_path,
    ).with_artifact(artifact, "test")
    path = manifest.write(tmp_path / "manifest.json")

    assert main(["verify-manifest", str(path)]) == 0
    result = _output(capsys)
    assert isinstance(result, dict)
    assert result["verified"] is True
