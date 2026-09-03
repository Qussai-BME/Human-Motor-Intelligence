"""Thin importer for MyoAdapt's exported JSON run-manifest shape."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from research_core.contracts import (
    ArtifactRecord,
    ArtifactRole,
    EvidenceClass,
    ExperimentRecord,
    RunStatus,
    sha256_json,
)
from research_core.contracts.base import ContractValidationError

from .common import AdapterError, required, safe_metadata


ADAPTER_ID = "myoadapt-run-manifest"
ADAPTER_VERSION = "1.0.0"


@dataclass(frozen=True, slots=True)
class ImportedRunBundle:
    """An imported experiment contract and its source-manifest/output references."""

    experiment: ExperimentRecord
    artifacts: tuple[ArtifactRecord, ...]


def import_myoadapt_manifest(
    manifest: Mapping[str, Any],
    *,
    manifest_uri: str,
    experiment_id: str,
    run_id: str,
    protocol_id: str,
    dataset_id: str,
    dataset_version: str,
    modality: str,
    subject_split: str,
    model_id: str | None = None,
    model_version: str = "external-manifest",
    metrics: Mapping[str, float] | None = None,
    evidence_class: EvidenceClass = EvidenceClass.UNKNOWN,
    benchmark_eligible: bool = False,
) -> ImportedRunBundle:
    """Normalize a MyoAdapt `RunManifest` export by reference.

    The adapter accepts the public manifest dictionary and its external path. It
    neither imports MyoAdapt Python modules nor modifies the originating
    manifest. Because a manifest alone cannot prove dataset access/protocol
    compatibility, benchmark eligibility defaults to false and must be supplied
    only by a validated ingest workflow.
    """
    if not isinstance(manifest, Mapping):
        raise AdapterError("MyoAdapt manifest must be a mapping")
    config = manifest.get("config", {})
    if not isinstance(config, Mapping):
        raise AdapterError("MyoAdapt manifest config must be a mapping")
    resolved_model_id = model_id or str(required(manifest, "model"))
    resolved_metrics = dict(metrics or {})
    metadata = {
        "adapter_id": ADAPTER_ID,
        "adapter_version": ADAPTER_VERSION,
        "external_schema_version": manifest.get("schema_version", "unknown"),
        "external_run_name": manifest.get("run_name"),
        "external_environment_hash": manifest.get("environment_hash_sha256"),
        "external_git": manifest.get("git", {}),
        "benchmark_eligible": benchmark_eligible,
        "evidence_class": evidence_class.value,
        "source_manifest_uri": manifest_uri,
    }
    try:
        experiment = ExperimentRecord(
            experiment_id=experiment_id,
            run_id=run_id,
            project_id="myoadapt-v2",
            protocol_id=protocol_id,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            modality=modality,
            subject_split=subject_split,
            model_id=resolved_model_id,
            model_version=model_version,
            seed=int(required(manifest, "seed")),
            configuration_hash=sha256_json(config),
            status=RunStatus.IMPORTED,
            code_commit=(manifest.get("git") or {}).get("commit") if isinstance(manifest.get("git"), Mapping) else None,
            environment=safe_metadata(manifest.get("environment")),
            metrics=resolved_metrics,
            artifact_ids=(f"{run_id}-manifest",),
            started_at_utc=manifest.get("started_at_utc"),
            completed_at_utc=manifest.get("ended_at_utc"),
            metadata=metadata,
        )
        artifacts: list[ArtifactRecord] = [
            ArtifactRecord(
                artifact_id=f"{run_id}-manifest",
                role=ArtifactRole.MANIFEST,
                uri=manifest_uri,
                producing_run_id=run_id,
                evidence_class=evidence_class,
                sha256=None,
                media_type="application/json",
                metadata={"external_project": "myoadapt", "external_schema_version": manifest.get("schema_version")},
            )
        ]
        for index, output in enumerate(manifest.get("outputs", [])):
            if not isinstance(output, Mapping) or not output.get("path"):
                continue
            role_value = str(output.get("role") or "other")
            try:
                role = ArtifactRole(role_value)
            except ValueError:
                role = ArtifactRole.OTHER
            artifacts.append(
                ArtifactRecord(
                    artifact_id=f"{run_id}-output-{index}",
                    role=role,
                    uri=str(output["path"]),
                    producing_run_id=run_id,
                    evidence_class=evidence_class,
                    sha256=output.get("sha256"),
                    size_bytes=output.get("size_bytes"),
                    metadata={"external_project": "myoadapt", "external_role": role_value},
                )
            )
    except (ContractValidationError, TypeError, ValueError) as exc:
        raise AdapterError(f"invalid MyoAdapt manifest mapping: {exc}") from exc
    return ImportedRunBundle(experiment=experiment, artifacts=tuple(artifacts))
