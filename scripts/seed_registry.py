#!/usr/bin/env python3
"""Initialize the repository's local registry from the curated seed catalog."""

from __future__ import annotations

import argparse
from pathlib import Path

from research_core.registry.catalog import seed_registry
from research_core.registry.store import LocalResearchRegistry


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed the local Human Motor Intelligence registry.")
    parser.add_argument(
        "--registry-dir",
        type=Path,
        default=Path("registry/local"),
        help="Local JSON registry directory (default: registry/local).",
    )
    args = parser.parse_args()
    registry = LocalResearchRegistry(args.registry_dir)
    entries = seed_registry(registry)
    print(f"Seeded {len(entries)} registry entries in {registry.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
