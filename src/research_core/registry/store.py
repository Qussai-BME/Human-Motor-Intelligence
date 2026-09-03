"""Atomic local persistence for research metadata and contract records."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
from typing import Any

from research_core.contracts import ArtifactRecord, ContractRecord, ExperimentRecord, sha256_json
from research_core.contracts.base import ContractValidationError, json_safe, validate_identifier

from .models import RegistryDefinition


REGISTRY_SCHEMA_VERSION = "1.0.0"


class RegistryError(RuntimeError):
    """Raised for local registry persistence, lookup, or integrity failures."""


@dataclass(frozen=True, slots=True)
class StoredEntry:
    """An immutable stored entity envelope."""

    entity_type: str
    entity_id: str
    content_hash: str
    registered_at_utc: str
    document: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "content_hash": self.content_hash,
            "registered_at_utc": self.registered_at_utc,
            "document": json_safe(self.document),
        }


class LocalResearchRegistry:
    """JSON-backed, local-first registry for metadata and external artifact references.

    The storage design favors transparent review and version control over a
    database service. It supports stable entities and an append-only event log;
    concurrent writers are intentionally out of scope for the MVP.
    """

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).expanduser().resolve()
        self.path = self.root / "registry.json"
        self.events_path = self.root / "events.jsonl"
        self.root.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write_document(self._empty_document())

    @staticmethod
    def _empty_document() -> dict[str, Any]:
        return {
            "schema_version": REGISTRY_SCHEMA_VERSION,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "entities": {},
        }

    def _read_document(self) -> dict[str, Any]:
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                document = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            raise RegistryError(f"cannot read registry at {self.path}: {exc}") from exc
        if document.get("schema_version") != REGISTRY_SCHEMA_VERSION:
            raise RegistryError(
                f"unsupported registry schema version {document.get('schema_version')!r}; "
                f"expected {REGISTRY_SCHEMA_VERSION}"
            )
        if not isinstance(document.get("entities"), dict):
            raise RegistryError("registry entities must be an object")
        return document

    def _write_document(self, document: Mapping[str, Any]) -> None:
        serialized = json.dumps(json_safe(document), indent=2, sort_keys=True, ensure_ascii=False)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=self.root, prefix=".registry-", suffix=".tmp", delete=False
        ) as handle:
            handle.write(serialized)
            handle.write("\n")
            temporary_path = Path(handle.name)
        temporary_path.replace(self.path)

    def _append_event(self, event: Mapping[str, Any]) -> None:
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(json_safe(event), sort_keys=True, ensure_ascii=False))
            handle.write("\n")

    @staticmethod
    def _identity(entry: RegistryDefinition | ContractRecord) -> tuple[str, str]:
        if isinstance(entry, RegistryDefinition):
            return entry.entity_type, entry.entity_id
        if isinstance(entry, ExperimentRecord):
            return "experiment", entry.experiment_id
        if isinstance(entry, ArtifactRecord):
            return "artifact", entry.artifact_id
        document = entry.to_dict()
        identifier = document.get(f"{entry.contract_kind}_id")
        if not isinstance(identifier, str):
            identifier = entry.content_hash()
        return f"contract:{entry.contract_kind}", identifier

    @staticmethod
    def _entry_document(entry: RegistryDefinition | ContractRecord) -> dict[str, Any]:
        return entry.to_dict()

    def register(
        self,
        entry: RegistryDefinition | ContractRecord,
        *,
        replace: bool = False,
        event_context: Mapping[str, Any] | None = None,
    ) -> StoredEntry:
        """Validate and atomically register a metadata or contract record.

        Existing entities cannot be overwritten unless ``replace=True``. A
        replacement is visible in the JSONL event log and should be justified by
        the caller's event context.
        """
        entity_type, entity_id = self._identity(entry)
        entity_type = validate_identifier(entity_type, "entity_type")
        entity_id = validate_identifier(entity_id, "entity_id")
        record = self._entry_document(entry)
        content_hash = sha256_json(record)
        document = self._read_document()
        entities: dict[str, dict[str, Any]] = document["entities"]
        collection = entities.setdefault(entity_type, {})
        existing = collection.get(entity_id)
        if existing and not replace:
            if existing.get("content_hash") == content_hash:
                return StoredEntry(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    content_hash=content_hash,
                    registered_at_utc=existing["registered_at_utc"],
                    document=existing["document"],
                )
            raise RegistryError(
                f"{entity_type}:{entity_id} already exists with a different content hash; "
                "pass replace=True only with documented governance rationale"
            )
        registered_at = datetime.now(timezone.utc).isoformat()
        stored = StoredEntry(
            entity_type=entity_type,
            entity_id=entity_id,
            content_hash=content_hash,
            registered_at_utc=registered_at,
            document=record,
        )
        collection[entity_id] = stored.to_dict()
        self._write_document(document)
        self._append_event(
            {
                "event_type": "registry_entry_registered" if existing is None else "registry_entry_replaced",
                "timestamp_utc": registered_at,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "content_hash": content_hash,
                "context": dict(event_context or {}),
            }
        )
        return stored

    def register_experiment_run(
        self,
        experiment: ExperimentRecord,
        *,
        replace: bool = False,
        event_context: Mapping[str, Any] | None = None,
    ) -> tuple[StoredEntry, StoredEntry]:
        """Register an experiment definition and its concrete run atomically.

        Both records point to the exact same validated contract document but
        remain queryable using the separate entity types required by the master
        specification.
        """
        experiment_entry = self.register(experiment, replace=replace, event_context=event_context)
        run_document = experiment.to_dict()
        run_document["registry_view"] = "run"
        run_hash = sha256_json(run_document)
        document = self._read_document()
        collection = document["entities"].setdefault("run", {})
        existing = collection.get(experiment.run_id)
        if existing and not replace:
            if existing.get("content_hash") == run_hash:
                return experiment_entry, StoredEntry(
                    entity_type="run",
                    entity_id=experiment.run_id,
                    content_hash=run_hash,
                    registered_at_utc=existing["registered_at_utc"],
                    document=existing["document"],
                )
            raise RegistryError(
                f"run:{experiment.run_id} already exists with a different content hash; pass replace=True to revise"
            )
        registered_at = datetime.now(timezone.utc).isoformat()
        run_entry = StoredEntry(
            entity_type="run",
            entity_id=experiment.run_id,
            content_hash=run_hash,
            registered_at_utc=registered_at,
            document=run_document,
        )
        collection[experiment.run_id] = run_entry.to_dict()
        self._write_document(document)
        self._append_event(
            {
                "event_type": "run_registered" if existing is None else "run_replaced",
                "timestamp_utc": registered_at,
                "entity_type": "run",
                "entity_id": experiment.run_id,
                "content_hash": run_hash,
                "context": dict(event_context or {}),
            }
        )
        return experiment_entry, run_entry

    def get(self, entity_type: str, entity_id: str) -> StoredEntry:
        """Return one stored entity by type and identity."""
        entity_type = validate_identifier(entity_type, "entity_type")
        entity_id = validate_identifier(entity_id, "entity_id")
        document = self._read_document()
        try:
            stored = document["entities"][entity_type][entity_id]
        except KeyError as exc:
            raise RegistryError(f"unknown registry entry {entity_type}:{entity_id}") from exc
        expected_hash = sha256_json(stored["document"])
        if stored.get("content_hash") != expected_hash:
            raise RegistryError(f"registry integrity failure for {entity_type}:{entity_id}")
        return StoredEntry(
            entity_type=entity_type,
            entity_id=entity_id,
            content_hash=stored["content_hash"],
            registered_at_utc=stored["registered_at_utc"],
            document=stored["document"],
        )

    def list(self, entity_type: str) -> tuple[StoredEntry, ...]:
        """List validated entries of one entity type in deterministic identity order."""
        entity_type = validate_identifier(entity_type, "entity_type")
        document = self._read_document()
        records = document["entities"].get(entity_type, {})
        return tuple(self.get(entity_type, entry_id) for entry_id in sorted(records))

    def query_runs(
        self,
        *,
        protocol_id: str | None = None,
        dataset_id: str | None = None,
        model_id: str | None = None,
        status: str | None = None,
    ) -> tuple[StoredEntry, ...]:
        """Return runs matching exact metadata filters for reproducible comparison."""
        candidates = self.list("run")
        filters = {
            key: value
            for key, value in {
                "protocol_id": protocol_id,
                "dataset_id": dataset_id,
                "model_id": model_id,
                "status": status,
            }.items()
            if value is not None
        }
        return tuple(
            candidate
            for candidate in candidates
            if all(candidate.document.get(key) == value for key, value in filters.items())
        )

    def import_many(
        self,
        entries: Iterable[RegistryDefinition | ContractRecord],
        *,
        replace: bool = False,
        event_context: Mapping[str, Any] | None = None,
    ) -> tuple[StoredEntry, ...]:
        """Register a finite collection, stopping at the first invalid or conflicting entity."""
        stored: list[StoredEntry] = []
        for entry in entries:
            stored.append(self.register(entry, replace=replace, event_context=event_context))
        return tuple(stored)
