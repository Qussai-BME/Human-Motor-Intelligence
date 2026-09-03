"""Local reproducibility manifests for umbrella orchestration and generated reports."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any

from research_core.contracts.base import canonical_json, json_safe, sha256_json, validate_sha256


MANIFEST_SCHEMA_VERSION = "1.0.0"


class ManifestError(RuntimeError):
    """Raised when a reproducibility manifest cannot be built or verified."""


def sha256_file(path: str | Path) -> str:
    """Return a streaming SHA-256 hash for an existing file."""
    target = Path(path)
    if not target.is_file():
        raise ManifestError(f"artifact file does not exist: {target}")
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def environment_fingerprint(packages: tuple[str, ...] = ()) -> dict[str, Any]:
    """Build a lightweight, deterministic environment description."""
    package_versions: dict[str, str] = {}
    for package in sorted(set(packages)):
        try:
            package_versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            package_versions[package] = "not-installed"
    return {
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "packages": package_versions,
    }


def git_evidence(repo_root: str | Path) -> dict[str, Any]:
    """Collect best-effort Git revision evidence without failing non-Git executions."""
    root = Path(repo_root).resolve()

    def run(*arguments: str) -> str:
        return subprocess.run(
            ["git", "-C", str(root), *arguments],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        ).stdout.strip()

    try:
        commit = run("rev-parse", "HEAD")
        if not commit:
            return {"available": False}
        return {
            "available": True,
            "commit": commit,
            "branch": run("rev-parse", "--abbrev-ref", "HEAD") or "detached",
            "dirty": bool(run("status", "--porcelain")),
            "describe": run("describe", "--always", "--tags") or commit[:12],
        }
    except (OSError, subprocess.TimeoutExpired):
        return {"available": False}


@dataclass(frozen=True, slots=True)
class ManifestArtifact:
    """Hash evidence for a single produced artifact."""

    path: str
    role: str
    sha256: str
    size_bytes: int

    def __post_init__(self) -> None:
        validate_sha256(self.sha256)
        if not self.path.strip() or not self.role.strip():
            raise ManifestError("manifest artifact path and role must be non-empty")
        if self.size_bytes < 0:
            raise ManifestError("manifest artifact size must be non-negative")


@dataclass(frozen=True, slots=True)
class ReproducibilityManifest:
    """Portable, immutable record of how an umbrella action produced its artifacts."""

    name: str
    project_id: str
    protocol_id: str
    dataset_id: str
    configuration: Mapping[str, Any]
    seed: int
    created_at_utc: str
    configuration_hash: str
    environment: Mapping[str, Any]
    environment_hash: str
    git: Mapping[str, Any]
    artifacts: tuple[ManifestArtifact, ...] = ()
    schema_version: str = MANIFEST_SCHEMA_VERSION

    @classmethod
    def create(
        cls,
        *,
        name: str,
        project_id: str,
        protocol_id: str,
        dataset_id: str,
        configuration: Mapping[str, Any],
        seed: int,
        repo_root: str | Path,
        packages: tuple[str, ...] = (),
    ) -> "ReproducibilityManifest":
        """Create a manifest before output artifacts have been registered."""
        if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
            raise ManifestError("seed must be a non-negative integer")
        if not all(value.strip() for value in (name, project_id, protocol_id, dataset_id)):
            raise ManifestError("name, project_id, protocol_id, and dataset_id must be non-empty")
        normalized_config = json_safe(configuration)
        environment = environment_fingerprint(packages)
        return cls(
            name=name,
            project_id=project_id,
            protocol_id=protocol_id,
            dataset_id=dataset_id,
            configuration=normalized_config,
            seed=seed,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            configuration_hash=sha256_json(normalized_config),
            environment=environment,
            environment_hash=sha256_json(environment),
            git=git_evidence(repo_root),
        )

    def with_artifact(self, path: str | Path, role: str) -> "ReproducibilityManifest":
        """Return a new manifest containing hash evidence for one generated artifact."""
        target = Path(path).resolve()
        artifact = ManifestArtifact(
            path=str(target),
            role=role,
            sha256=sha256_file(target),
            size_bytes=target.stat().st_size,
        )
        return ReproducibilityManifest(
            name=self.name,
            project_id=self.project_id,
            protocol_id=self.protocol_id,
            dataset_id=self.dataset_id,
            configuration=self.configuration,
            seed=self.seed,
            created_at_utc=self.created_at_utc,
            configuration_hash=self.configuration_hash,
            environment=self.environment,
            environment_hash=self.environment_hash,
            git=self.git,
            artifacts=(*self.artifacts, artifact),
            schema_version=self.schema_version,
        )

    def to_dict(self) -> dict[str, Any]:
        """Return canonical JSON-safe manifest content."""
        return json_safe(asdict(self))  # type: ignore[return-value]

    def write(self, path: str | Path) -> Path:
        """Write canonical JSON to an explicit local location."""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return target

    @staticmethod
    def verify(path: str | Path) -> dict[str, Any]:
        """Verify manifest configuration/environment hashes and all referenced artifact hashes."""
        source = Path(path)
        try:
            content = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ManifestError(f"cannot read manifest: {exc}") from exc
        if content.get("schema_version") != MANIFEST_SCHEMA_VERSION:
            raise ManifestError("unsupported manifest schema version")
        mismatches: list[str] = []
        if content.get("configuration_hash") != sha256_json(content.get("configuration", {})):
            mismatches.append("configuration_hash")
        if content.get("environment_hash") != sha256_json(content.get("environment", {})):
            mismatches.append("environment_hash")
        checked_artifacts = 0
        for artifact in content.get("artifacts", []):
            target = Path(artifact["path"])
            if not target.is_absolute():
                target = source.parent / target
            if not target.is_file():
                mismatches.append(f"missing:{target}")
                continue
            checked_artifacts += 1
            if sha256_file(target) != artifact.get("sha256"):
                mismatches.append(f"hash:{target}")
        return {
            "verified": not mismatches,
            "checked_artifacts": checked_artifacts,
            "mismatches": mismatches,
            "manifest": str(source),
        }
