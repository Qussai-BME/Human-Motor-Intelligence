"""Schema-version primitives for the umbrella interchange contracts.

The contract package deliberately uses an explicit semantic version instead of
implicitly coupling its serialized records to the installed package version.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

_VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


@dataclass(frozen=True, order=True, slots=True)
class SchemaVersion:
    """An immutable semantic schema version with strict ``major.minor.patch`` form."""

    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> "SchemaVersion":
        """Parse a strict semantic schema version."""
        match = _VERSION_RE.fullmatch(value)
        if match is None:
            raise ValueError(
                "schema_version must use strict semantic version form 'major.minor.patch'"
            )
        return cls(*(int(group) for group in match.groups()))

    def __post_init__(self) -> None:
        if min(self.major, self.minor, self.patch) < 0:
            raise ValueError("schema version components must be non-negative")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def is_backward_compatible_with(self, earlier: "SchemaVersion") -> bool:
        """Return whether this version may read an older record without a major break."""
        return self.major == earlier.major and self >= earlier


CONTRACT_SCHEMA_V1 = SchemaVersion(1, 0, 0)
