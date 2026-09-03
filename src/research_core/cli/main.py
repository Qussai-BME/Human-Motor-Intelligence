"""Local, dependency-free Research-OS command-line interface.

The CLI intentionally exposes stable registry navigation, integrity, provenance,
and diagnostic operations. It does not offer generic model execution, automatic
reproduction, cloud upload, or decoder-control commands unless the governing
protocol and evidence boundary support them.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from research_core.adapters import import_myoadapt_manifest
from research_core.contracts import EvidenceClass
from research_core.provenance import ReproducibilityManifest
from research_core.registry import LocalResearchRegistry
from research_core.registry.catalog import seed_registry

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENTITY_COMMANDS = ("dataset", "protocol", "experiment", "benchmark", "artifact", "report")


def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))


def _registry_summary(registry: LocalResearchRegistry) -> dict[str, Any]:
    document = json.loads(registry.path.read_text(encoding="utf-8"))
    return {
        "registry": str(registry.path),
        "schema_version": document["schema_version"],
        "entity_counts": {entity_type: len(entries) for entity_type, entries in sorted(document["entities"].items())},
    }


def _check_integrity(registry: LocalResearchRegistry) -> dict[str, Any]:
    document = json.loads(registry.path.read_text(encoding="utf-8"))
    checked = 0
    failures: list[str] = []
    for entity_type, entries in document["entities"].items():
        for entity_id in entries:
            try:
                registry.get(entity_type, entity_id)
                checked += 1
            except Exception as exc:  # Preserve all encountered integrity failures in one actionable report.
                failures.append(f"{entity_type}:{entity_id}: {exc}")
    return {"registry": str(registry.path), "checked": checked, "verified": not failures, "failures": failures}


def _doctor(registry: LocalResearchRegistry) -> dict[str, Any]:
    """Provide a non-invasive public/researcher preflight report.

    The doctor command checks only local structure and registry integrity. It
    deliberately reports P3/P6 as evidence gates rather than attempting to
    fetch data, import external dependencies, or create new results.
    """
    required_documents = (
        "README.md",
        "PUBLIC_REVIEW_DISCLOSURE_R3.md",
        "REPRODUCIBILITY.md",
        "SCIENTIFIC_LIMITATIONS.md",
        "audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md",
        "papers/RESEARCH_GATE_PREPARATION_RECOVERY_R3.md",
    )
    present_documents = {relative: (PROJECT_ROOT / relative).is_file() for relative in required_documents}
    raw_suffixes = {".bdf", ".edf", ".gdf", ".set", ".fif", ".npz"}
    raw_or_cache = [
        path.relative_to(PROJECT_ROOT).as_posix()
        for path in PROJECT_ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and path.suffix.lower() in raw_suffixes
    ]
    return {
        "project_root": str(PROJECT_ROOT),
        "registry_integrity": _check_integrity(registry),
        "public_review_documents": present_documents,
        "data_governance": {
            "raw_or_derived_cache_paths_detected": raw_or_cache,
            "status": "pass" if not raw_or_cache else "attention_required",
        },
        "evidence_gates": {
            "p3": "pending_original_author_package",
            "p6_r3": "blocked_pending_authentic_trace_provenance",
            "p6_r2_scope": "simulator_integration_fixture_systems_evidence_only",
        },
        "command_boundary": (
            "This CLI supports local metadata, integrity, and provenance workflows. "
            "Generic experiment execution/reproduction, cloud operations, and decoder control are intentionally unavailable."
        ),
    }


def _add_entity_command(commands: argparse._SubParsersAction[argparse.ArgumentParser], name: str) -> None:
    """Register a read-only typed registry navigation command."""
    command = commands.add_parser(name, help=f"List, show, or validate registered {name} metadata.")
    actions = command.add_subparsers(dest="entity_action", required=True)
    actions.add_parser("list", help=f"List registered {name} entries.")
    show = actions.add_parser("show", help=f"Show one validated {name} entry.")
    show.add_argument("entity_id")
    if name == "protocol":
        validate = actions.add_parser("validate", help="Validate one stored protocol definition and show governance fields.")
        validate.add_argument("entity_id")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hmi",
        description="Human Motor Intelligence Research-OS MVP (local-only, metadata-first).",
    )
    parser.add_argument("--registry-dir", type=Path, default=Path("registry/local"))
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("seed", help="Seed the deterministic baseline research catalog.")
    commands.add_parser("summary", help="Print entity counts and registry path.")
    commands.add_parser("integrity", help="Validate stored content hashes for all local registry entries.")
    commands.add_parser("doctor", help="Run local public-review, registry, and evidence-gate diagnostics without executing research.")

    for name in ENTITY_COMMANDS:
        _add_entity_command(commands, name)

    list_command = commands.add_parser("list", help="Legacy generic list command; prefer typed entity commands.")
    list_command.add_argument("entity_type")

    show_command = commands.add_parser("show", help="Legacy generic show command; prefer typed entity commands.")
    show_command.add_argument("entity_type")
    show_command.add_argument("entity_id")

    run_command = commands.add_parser("runs", help="Query registered runs by exact metadata filters.")
    run_command.add_argument("--protocol-id")
    run_command.add_argument("--dataset-id")
    run_command.add_argument("--model-id")
    run_command.add_argument("--status")

    verify = commands.add_parser("verify-manifest", help="Verify a reproducibility manifest and its artifact hashes.")
    verify.add_argument("manifest", type=Path)

    importer = commands.add_parser("import-myoadapt", help="Import an external MyoAdapt run manifest by reference.")
    importer.add_argument("manifest", type=Path)
    importer.add_argument("--experiment-id", required=True)
    importer.add_argument("--run-id", required=True)
    importer.add_argument("--protocol-id", required=True)
    importer.add_argument("--dataset-id", required=True)
    importer.add_argument("--dataset-version", required=True)
    importer.add_argument("--modality", default="emg")
    importer.add_argument("--subject-split", required=True)
    importer.add_argument("--model-id")
    importer.add_argument("--model-version", default="external-manifest")
    importer.add_argument("--evidence-class", choices=[item.value for item in EvidenceClass], default="unknown")
    importer.add_argument(
        "--benchmark-eligible",
        action="store_true",
        help="Only for a separately validated real-data/protocol-compatible import; false by default.",
    )
    return parser


def _handle_typed_entity_command(args: argparse.Namespace, registry: LocalResearchRegistry) -> int:
    """Execute a stable, read-only typed registry operation."""
    entity_type = args.command
    if args.entity_action == "list":
        _print([entry.to_dict() for entry in registry.list(entity_type)])
        return 0
    entry = registry.get(entity_type, args.entity_id)
    if args.entity_action == "show":
        _print(entry.to_dict())
        return 0
    if entity_type == "protocol" and args.entity_action == "validate":
        document = entry.document
        _print(
            {
                "validated": True,
                "protocol": entry.to_dict(),
                "governance": {
                    "status": document["status"],
                    "version": document["version"],
                    "statistical_unit": document["statistical_unit"],
                    "leakage_constraints": list(document["leakage_constraints"]),
                    "metrics": list(document["metrics"]),
                    "seeds": list(document["seeds"]),
                },
            }
        )
        return 0
    raise AssertionError(f"Unhandled typed entity action: {entity_type} {args.entity_action}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    registry = LocalResearchRegistry(args.registry_dir)
    if args.command == "seed":
        entries = seed_registry(registry)
        _print({"seeded": len(entries), **_registry_summary(registry)})
        return 0
    if args.command == "summary":
        _print(_registry_summary(registry))
        return 0
    if args.command == "integrity":
        report = _check_integrity(registry)
        _print(report)
        return 0 if report["verified"] else 1
    if args.command == "doctor":
        report = _doctor(registry)
        _print(report)
        return 0 if report["registry_integrity"]["verified"] and report["data_governance"]["status"] == "pass" else 1
    if args.command in ENTITY_COMMANDS:
        return _handle_typed_entity_command(args, registry)
    if args.command == "list":
        _print([entry.to_dict() for entry in registry.list(args.entity_type)])
        return 0
    if args.command == "show":
        _print(registry.get(args.entity_type, args.entity_id).to_dict())
        return 0
    if args.command == "runs":
        entries = registry.query_runs(
            protocol_id=args.protocol_id,
            dataset_id=args.dataset_id,
            model_id=args.model_id,
            status=args.status,
        )
        _print([entry.to_dict() for entry in entries])
        return 0
    if args.command == "verify-manifest":
        report = ReproducibilityManifest.verify(args.manifest)
        _print(report)
        return 0 if report["verified"] else 1
    if args.command == "import-myoadapt":
        source = args.manifest.resolve()
        manifest = json.loads(source.read_text(encoding="utf-8"))
        bundle = import_myoadapt_manifest(
            manifest,
            manifest_uri=str(source),
            experiment_id=args.experiment_id,
            run_id=args.run_id,
            protocol_id=args.protocol_id,
            dataset_id=args.dataset_id,
            dataset_version=args.dataset_version,
            modality=args.modality,
            subject_split=args.subject_split,
            model_id=args.model_id,
            model_version=args.model_version,
            evidence_class=EvidenceClass(args.evidence_class),
            benchmark_eligible=args.benchmark_eligible,
        )
        experiment_entry, run_entry = registry.register_experiment_run(
            bundle.experiment,
            event_context={"source": "hmi_cli_import_myoadapt"},
        )
        artifacts = [
            registry.register(artifact, event_context={"source": "hmi_cli_import_myoadapt"}).to_dict()
            for artifact in bundle.artifacts
        ]
        _print({"experiment": experiment_entry.to_dict(), "run": run_entry.to_dict(), "artifacts": artifacts})
        return 0
    raise AssertionError(f"Unhandled command {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
