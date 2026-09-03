#!/usr/bin/env python3
"""Stage runner for the predeclared V2 Recovery R2 P5 cohort."""
from __future__ import annotations

import argparse
import json

from research_core.experiments.v2_p5_jeong_r2 import create_manifest, extract_cache, run_loso


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run protocol-locked P5 Jeong external validation Recovery R2 stages."
    )
    parser.add_argument(
        "stage", choices=("extract-p5-r2", "manifest-p5-r2", "run-p5-r2", "rerun-p5-r2")
    )
    args = parser.parse_args()
    if args.stage == "extract-p5-r2":
        result = extract_cache()
    elif args.stage == "manifest-p5-r2":
        result = create_manifest()
    elif args.stage == "run-p5-r2":
        result = run_loso(independent_rerun=False)
    else:
        result = run_loso(independent_rerun=True)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
