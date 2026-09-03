"""Dataset-integrity contracts for auditable V2 external validation.

The module intentionally records validation evidence separately from model results.
It contains no dataset-specific score or conclusion and never reads raw recordings
from the repository.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable, Mapping
import json


class DatasetValidationError(RuntimeError):
    """Raised when a locked validation gate cannot be satisfied."""


class ValidationGate(str, Enum):
    """The ordered gates required before any scientific benchmark is eligible."""

    D1_FILE_INTEGRITY = "D1_file_integrity"
    D2_SCHEMA = "D2_schema"
    D3_LABELS = "D3_labels"
    D4_PROTOCOL = "D4_protocol"
    D5_LEAKAGE_AUDIT = "D5_leakage_audit"


@dataclass(frozen=True)
class DatasetObservation:
    """A cache artefact with source receipt and deterministic digest."""

    subject_id: str
    relative_path: str
    byte_count: int
    sha256: str
    source_url: str | None = None
    source_content_length: int | None = None

    def __post_init__(self) -> None:
        if not self.subject_id.startswith("sub-"):
            raise DatasetValidationError("subject_id must have `sub-` prefix")
        if self.byte_count < 1:
            raise DatasetValidationError("byte_count must be positive")
        if len(self.sha256) != 64 or any(ch not in "0123456789abcdef" for ch in self.sha256):
            raise DatasetValidationError("sha256 must be a lowercase SHA-256 hexadecimal digest")
        if self.source_content_length is not None and self.source_content_length < 1:
            raise DatasetValidationError("source_content_length must be positive when supplied")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DatasetManifest:
    """A dataset cache manifest and independently reviewable validation record."""

    manifest_id: str
    dataset_id: str
    dataset_version: str
    external_validation: bool
    direct_replication: bool
    cache_root: str
    subjects: list[str]
    observations: list[DatasetObservation]
    protocol_id: str
    source_doi: str
    source_license: str
    gate_results: dict[ValidationGate, dict[str, Any]] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.external_validation or self.direct_replication:
            raise DatasetValidationError(
                "V2 external manifests must explicitly state external_validation=true and direct_replication=false"
            )
        if not self.subjects or len(set(self.subjects)) != len(self.subjects):
            raise DatasetValidationError("manifest subject list must be nonempty and unique")
        if set(self.subjects) != {ob.subject_id for ob in self.observations}:
            raise DatasetValidationError("observations must cover exactly the locked manifest subject set")

    @property
    def benchmark_ready(self) -> bool:
        return all(self.gate_results.get(gate, {}).get("status") == "pass" for gate in ValidationGate)

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "dataset_id": self.dataset_id,
            "dataset_version": self.dataset_version,
            "external_validation": self.external_validation,
            "direct_replication": self.direct_replication,
            "cache_root": self.cache_root,
            "subjects": self.subjects,
            "observations": [ob.to_dict() for ob in self.observations],
            "protocol_id": self.protocol_id,
            "source_doi": self.source_doi,
            "source_license": self.source_license,
            "gate_results": {gate.value: value for gate, value in self.gate_results.items()},
            "benchmark_ready": self.benchmark_ready,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "DatasetManifest":
        raw_gates = payload.get("gate_results", {})
        return cls(
            manifest_id=str(payload["manifest_id"]),
            dataset_id=str(payload["dataset_id"]),
            dataset_version=str(payload["dataset_version"]),
            external_validation=bool(payload["external_validation"]),
            direct_replication=bool(payload["direct_replication"]),
            cache_root=str(payload["cache_root"]),
            subjects=[str(value) for value in payload["subjects"]],
            observations=[DatasetObservation(**value) for value in payload["observations"]],
            protocol_id=str(payload["protocol_id"]),
            source_doi=str(payload["source_doi"]),
            source_license=str(payload["source_license"]),
            gate_results={ValidationGate(key): dict(value) for key, value in raw_gates.items()},
            notes=[str(value) for value in payload.get("notes", [])],
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _digest(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_file_integrity(manifest: DatasetManifest) -> dict[str, Any]:
    """Recompute cache digests and verify the cache contains no raw BDF/EDF files."""
    root = Path(manifest.cache_root)
    failures: list[str] = []
    total_bytes = 0
    raw_extensions = {".bdf", ".edf", ".gdf", ".vhdr", ".eeg"}
    for candidate in root.rglob("*") if root.exists() else []:
        if candidate.is_file() and candidate.suffix.lower() in raw_extensions:
            failures.append(f"raw recording retained in cache: {candidate.relative_to(root)}")
    for observation in manifest.observations:
        path = root / observation.relative_path
        if not path.is_file():
            failures.append(f"missing cache file: {observation.relative_path}")
            continue
        size = path.stat().st_size
        total_bytes += size
        if size != observation.byte_count:
            failures.append(f"size mismatch: {observation.relative_path}")
        if _digest(path) != observation.sha256:
            failures.append(f"digest mismatch: {observation.relative_path}")
    return {
        "status": "pass" if not failures else "fail",
        "checked_observations": len(manifest.observations),
        "total_bytes": total_bytes,
        "failures": failures,
    }


def validate_schema(*, expected_subjects: Iterable[str], observed: Mapping[str, Mapping[str, Any]], required_keys: set[str]) -> dict[str, Any]:
    """Validate metadata schema without accepting model-derived evidence."""
    expected = set(expected_subjects)
    failures: list[str] = []
    if set(observed) != expected:
        failures.append("observed subject set differs from locked subject list")
    for subject in sorted(expected & set(observed)):
        missing = sorted(required_keys - set(observed[subject]))
        if missing:
            failures.append(f"{subject}: missing schema keys {missing}")
    return {"status": "pass" if not failures else "fail", "failures": failures, "required_keys": sorted(required_keys)}


def validate_labels(*, expected_labels: Iterable[str], observed: Mapping[str, Iterable[str]]) -> dict[str, Any]:
    """Require every held-out subject to contain exactly the predeclared label set."""
    required = set(expected_labels)
    failures: list[str] = []
    coverage: dict[str, list[str]] = {}
    for subject, values in sorted(observed.items()):
        present = set(values)
        coverage[subject] = sorted(present)
        if present != required:
            failures.append(f"{subject}: labels differ from locked set; missing={sorted(required - present)}, extra={sorted(present - required)}")
    return {"status": "pass" if not failures else "fail", "expected_labels": sorted(required), "coverage": coverage, "failures": failures}


def validate_protocol(*, manifest: DatasetManifest, details: Mapping[str, Any]) -> dict[str, Any]:
    """Record explicit evidence that the cache matches the locked protocol boundary."""
    required = {"split_strategy", "target_subject_calibration", "preprocessing_fit_scope", "subject_count", "protocol_id"}
    missing = sorted(required - set(details))
    failures = [f"protocol detail missing: {key}" for key in missing]
    if details.get("split_strategy") != "leave-one-subject-out":
        failures.append("split_strategy is not leave-one-subject-out")
    if details.get("target_subject_calibration") is not False:
        failures.append("target_subject_calibration must be false")
    if details.get("preprocessing_fit_scope") != "training-fold-only":
        failures.append("fitted preprocessing scope must be training-fold-only")
    if details.get("subject_count") != len(manifest.subjects):
        failures.append("protocol subject_count differs from manifest")
    if details.get("protocol_id") != manifest.protocol_id:
        failures.append("protocol_id differs from manifest")
    return {"status": "pass" if not failures else "fail", "details": dict(details), "failures": failures}


def validate_leakage_audit(*, checks: Mapping[str, bool]) -> dict[str, Any]:
    """Require affirmative implementation evidence for each leakage-control claim."""
    if not checks:
        raise DatasetValidationError("leakage audit requires explicit checks")
    failures = sorted(name for name, passed in checks.items() if passed is not True)
    return {"status": "pass" if not failures else "fail", "checks": dict(checks), "failures": failures}


def require_gate_pass(manifest: DatasetManifest, gate: ValidationGate) -> None:
    """Stop a benchmark when a gate has not passed using enum-safe access."""
    result = manifest.gate_results.get(gate)
    if result is None or result.get("status") != "pass":
        raise DatasetValidationError(f"{gate.value} has not passed")
