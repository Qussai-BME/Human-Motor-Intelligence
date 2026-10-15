#!/usr/bin/env python3
"""Verify a local umbrella reproducibility manifest and return a non-zero code on mismatch."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from research_core.provenance import ReproducibilityManifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a Human Motor Intelligence reproducibility manifest.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    result = ReproducibilityManifest.verify(args.manifest)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
