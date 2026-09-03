#!/usr/bin/env python3
"""Run protocol-locked V2 external validation recovery stages.

P5 is intentionally not exposed because its selected source cohort failed the
availability gate. This script has no command that can override that hard stop.
"""
from __future__ import annotations

import argparse
import json

from research_core.experiments.v2_external import (
    create_openbmi_manifest,
    extract_openbmi_cache,
    run_openbmi_loso,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "stage",
        choices=("extract-p4", "manifest-p4", "run-p4", "rerun-p4"),
        help="The only permitted recovery stages. Run in order.",
    )
    args = parser.parse_args()
    if args.stage == "extract-p4":
        payload = extract_openbmi_cache()
    elif args.stage == "manifest-p4":
        payload = create_openbmi_manifest()
    elif args.stage == "run-p4":
        payload = run_openbmi_loso()
    else:
        payload = run_openbmi_loso(independent_rerun=True)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
