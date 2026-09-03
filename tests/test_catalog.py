from __future__ import annotations

from research_core.registry import LocalResearchRegistry
from research_core.registry.catalog import catalog_entries, seed_registry


def test_seed_catalog_registers_required_research_entities_without_paper3(tmp_path) -> None:
    registry = LocalResearchRegistry(tmp_path / "registry")
    stored = seed_registry(registry)

    assert len(stored) == len(catalog_entries())
    assert {entry.entity_id for entry in registry.list("dataset")} >= {
        "ninapro-db2",
        "ninapro-db3",
        "ninapro-db7",
        "bci-competition-iv-2a",
        "way-eeg-gal",
        "mit-bih-arrhythmia-v1",
    }
    assert {entry.entity_id for entry in registry.list("protocol")} == {
        "emg-loso-v1",
        "eeg-loso-v1",
        "eeg-mi-v1",
        "emg-eeg-fusion-v1",
        "intent-to-control-v1",
    }
    assert "paper-3" not in {entry.entity_id for entry in registry.list("protocol")}
    assert registry.get("benchmark", "emg-loso-db7").document["protocol_id"] == "emg-loso-v1"


def test_seed_catalog_is_idempotent_for_same_registry(tmp_path) -> None:
    registry = LocalResearchRegistry(tmp_path / "registry")
    first = seed_registry(registry)
    second = seed_registry(registry)

    assert [entry.content_hash for entry in first] == [entry.content_hash for entry in second]
