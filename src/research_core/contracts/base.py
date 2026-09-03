"""Shared primitives for immutable, JSON-safe research contract records."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, fields, is_dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from math import isfinite
from types import MappingProxyType
from typing import Any
from urllib.parse import urlparse

from .versioning import CONTRACT_SCHEMA_V1, SchemaVersion

JsonPrimitive = str | int | float | bool | None
JsonValue = JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"]


class ContractValidationError(ValueError):
    """Raised when an interchange record violates a stable contract invariant."""


def utc_now_iso() -> str:
    """Return a timezone-aware ISO-8601 timestamp in UTC."""
    return datetime.now(timezone.utc).isoformat()


def validate_iso_timestamp(value: str, field_name: str) -> str:
    """Validate and canonicalize an ISO-8601 timestamp with timezone information."""
    if not isinstance(value, str) or not value.strip():
        raise ContractValidationError(f"{field_name} must be a non-empty ISO-8601 string")
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ContractValidationError(f"{field_name} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ContractValidationError(f"{field_name} must include an explicit timezone")
    return parsed.astimezone(timezone.utc).isoformat()


def validate_non_empty(value: str, field_name: str) -> str:
    """Validate a non-empty trimmed string."""
    if not isinstance(value, str) or not value.strip():
        raise ContractValidationError(f"{field_name} must be a non-empty string")
    return value.strip()


def validate_identifier(value: str, field_name: str) -> str:
    """Validate a stable identifier without prescribing a registry implementation."""
    normalized = validate_non_empty(value, field_name)
    if any(character.isspace() for character in normalized):
        raise ContractValidationError(f"{field_name} must not contain whitespace")
    return normalized


def validate_probability(value: float, field_name: str) -> float:
    """Validate a finite probability in the closed interval [0, 1]."""
    numeric = float(value)
    if not isfinite(numeric) or not 0.0 <= numeric <= 1.0:
        raise ContractValidationError(f"{field_name} must be a finite value in [0, 1]")
    return numeric


def validate_finite_non_negative(value: float, field_name: str) -> float:
    """Validate a finite non-negative numeric value."""
    numeric = float(value)
    if not isfinite(numeric) or numeric < 0:
        raise ContractValidationError(f"{field_name} must be finite and non-negative")
    return numeric


def validate_sha256(value: str | None, field_name: str = "sha256") -> str | None:
    """Validate a lowercase or uppercase 64-character SHA-256 digest when supplied."""
    if value is None:
        return None
    normalized = validate_non_empty(value, field_name).lower()
    if len(normalized) != 64 or any(character not in "0123456789abcdef" for character in normalized):
        raise ContractValidationError(f"{field_name} must be a 64-character hexadecimal SHA-256 digest")
    return normalized


def validate_uri_or_path(value: str, field_name: str) -> str:
    """Validate a local relative/absolute path or a non-credentialed URI reference."""
    normalized = validate_non_empty(value, field_name)
    parsed = urlparse(normalized)
    if parsed.scheme and parsed.scheme not in {"file", "https", "http", "s3"}:
        raise ContractValidationError(f"{field_name} uses unsupported URI scheme '{parsed.scheme}'")
    if parsed.username or parsed.password:
        raise ContractValidationError(f"{field_name} must not include credentials")
    return normalized


def frozen_mapping(value: Mapping[str, Any] | None, field_name: str) -> Mapping[str, Any]:
    """Validate mapping keys and expose an immutable shallow copy."""
    if value is None:
        return MappingProxyType({})
    if not isinstance(value, Mapping):
        raise ContractValidationError(f"{field_name} must be a mapping")
    normalized: dict[str, Any] = {}
    for key, item in value.items():
        normalized[validate_non_empty(str(key), f"{field_name} key")] = item
    return MappingProxyType(normalized)


def json_safe(value: Any) -> JsonValue:
    """Convert contract values into deterministic, JSON-safe primitives.

    This deliberately rejects arbitrary Python objects so records cannot silently
    embed native dataset arrays, model objects, secret-bearing configuration, or
    implementation-specific state.
    """
    if isinstance(value, Enum):
        return json_safe(value.value)
    if isinstance(value, datetime):
        return validate_iso_timestamp(value.isoformat(), "datetime")
    if isinstance(value, SchemaVersion):
        return str(value)
    if is_dataclass(value):
        return {item.name: json_safe(getattr(value, item.name)) for item in fields(value)}
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not isfinite(value):
            raise ContractValidationError("JSON contract values must be finite")
        return value
    if isinstance(value, Mapping):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [json_safe(item) for item in value]
    raise ContractValidationError(f"value of type {type(value).__name__} is not JSON-safe")


def canonical_json(value: Any) -> str:
    """Return a stable canonical JSON representation for hashing and persistence."""
    return json.dumps(json_safe(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    """Return a SHA-256 digest of canonical JSON."""
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True, kw_only=True)
class ContractRecord:
    """Base record carrying stable kind and schema-version metadata."""

    contract_kind: str = field(init=False, default="")
    schema_version: str = field(default_factory=lambda: str(CONTRACT_SCHEMA_V1))

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_kind", validate_identifier(self.contract_kind, "contract_kind"))
        try:
            version = SchemaVersion.parse(self.schema_version)
        except ValueError as exc:
            raise ContractValidationError(str(exc)) from exc
        if version.major != CONTRACT_SCHEMA_V1.major:
            raise ContractValidationError(
                f"unsupported {self.contract_kind} schema major version {version.major}; "
                f"supported major version is {CONTRACT_SCHEMA_V1.major}"
            )
        object.__setattr__(self, "schema_version", str(version))

    def to_dict(self) -> dict[str, JsonValue]:
        """Return a JSON-safe serializable representation of the record."""
        return json_safe({item.name: getattr(self, item.name) for item in fields(self)})  # type: ignore[return-value]

    def content_hash(self) -> str:
        """Return the deterministic content hash of this contract record."""
        return sha256_json(self.to_dict())
