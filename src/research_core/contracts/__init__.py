"""Stable versioned interchange contracts for the research integration layer."""

from .base import ContractRecord, ContractValidationError, canonical_json, sha256_json
from .models import (
    ArtifactRecord,
    ArtifactRole,
    ControlCommandRecord,
    EvidenceClass,
    ExperimentRecord,
    IntentRecord,
    RepresentationRecord,
    RunStatus,
    SignalProvenanceRecord,
    SignalRecord,
    ensure_real_benchmark_records,
)
from .versioning import CONTRACT_SCHEMA_V1, SchemaVersion

__all__ = [
    "ArtifactRecord",
    "ArtifactRole",
    "CONTRACT_SCHEMA_V1",
    "ContractRecord",
    "ContractValidationError",
    "ControlCommandRecord",
    "EvidenceClass",
    "ExperimentRecord",
    "IntentRecord",
    "RepresentationRecord",
    "RunStatus",
    "SchemaVersion",
    "SignalProvenanceRecord",
    "SignalRecord",
    "canonical_json",
    "ensure_real_benchmark_records",
    "sha256_json",
]
