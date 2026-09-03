"""Shared mapping and provenance helpers for thin external-boundary adapters."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from research_core.contracts import ContractValidationError, EvidenceClass, SignalProvenanceRecord
from research_core.contracts.base import validate_identifier, validate_non_empty


class AdapterError(ValueError):
    """Raised when an external artifact is incomplete or cannot safely map to a contract."""


def required(mapping: Mapping[str, Any], key: str) -> Any:
    """Return a required external field with a clear adapter-level error."""
    if key not in mapping or mapping[key] is None:
        raise AdapterError(f"external export is missing required field '{key}'")
    return mapping[key]


def optional_identifier(value: Any, field_name: str) -> str | None:
    """Normalize an optional identifier supplied by an external export."""
    if value is None:
        return None
    try:
        return validate_identifier(str(value), field_name)
    except ContractValidationError as exc:
        raise AdapterError(str(exc)) from exc


def provenance_from_export(
    export: Mapping[str, Any] | None,
    *,
    adapter_id: str,
    adapter_version: str,
    default_origin: EvidenceClass = EvidenceClass.UNKNOWN,
) -> SignalProvenanceRecord:
    """Build explicit umbrella provenance from a public export mapping.

    The caller always declares adapter identity. Missing source evidence remains
    `unknown`; this deliberately prevents an imported file from becoming a
    benchmark-eligible real-data record by implication.
    """
    source = dict(export or {})
    try:
        origin = EvidenceClass(source.get("origin", default_origin))
    except ValueError as exc:
        raise AdapterError("provenance origin must be real, synthetic, or unknown") from exc
    source_dataset_id = source.get("source_dataset_id") or source.get("source_dataset")
    details = dict(source.get("details") or {})
    if "benchmark_eligible" not in details:
        details["benchmark_eligible"] = False
    fallback_reason = source.get("fallback_reason")
    if origin is EvidenceClass.SYNTHETIC and not fallback_reason:
        fallback_reason = "external adapter declared synthetic source"
    try:
        return SignalProvenanceRecord(
            origin=origin,
            source_dataset_id=str(source_dataset_id) if source_dataset_id is not None else None,
            dataset_version=source.get("dataset_version"),
            source_uri=source.get("source_uri"),
            license_id=source.get("license_id"),
            adapter_id=adapter_id,
            adapter_version=adapter_version,
            fallback_reason=fallback_reason,
            details=details,
        )
    except ContractValidationError as exc:
        raise AdapterError(str(exc)) from exc


def safe_metadata(mapping: Mapping[str, Any] | None) -> dict[str, Any]:
    """Return shallow metadata without treating arbitrary values as executable configuration."""
    if mapping is None:
        return {}
    if not isinstance(mapping, Mapping):
        raise AdapterError("metadata must be a mapping")
    return {str(key): value for key, value in mapping.items()}
