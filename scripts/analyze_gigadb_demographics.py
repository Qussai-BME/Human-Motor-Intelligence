#!/usr/bin/env python3
"""Summarize official GigaDB demographic metadata for a predeclared cohort."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean, stdev


def parse_response(path: Path) -> list[dict]:
    outer = json.loads(path.read_text(encoding="utf-8"))
    payload = json.loads(outer) if isinstance(outer, str) else outer
    return payload["data"]["data"]


def summarize(rows: list[dict]) -> dict:
    ages = [int(row["sample_attributes"]["Age"]) for row in rows]
    sexes = [row["sample_attributes"]["sex"].lower() for row in rows]
    return {
        "n": len(rows),
        "age_mean": mean(ages),
        "age_sd": stdev(ages) if len(ages) > 1 else None,
        "age_min": min(ages),
        "age_max": max(ages),
        "sex_counts": {sex: sexes.count(sex) for sex in sorted(set(sexes))},
        "subjects": [row["sample_id"] for row in sorted(rows, key=lambda item: int(item["sample_id"].removeprefix("sub")))],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--excluded", default="sub23")
    args = parser.parse_args()
    rows = parse_response(args.input)
    excluded = [row for row in rows if row["sample_id"] == args.excluded]
    included = [row for row in rows if row["sample_id"] != args.excluded]
    if len(rows) != 25 or len(excluded) != 1 or len(included) != 24:
        raise SystemExit("Unexpected source cohort cardinality")
    result = {
        "source": str(args.input),
        "excluded_subject": args.excluded,
        "all_25": summarize(rows),
        "included_24": summarize(included),
        "excluded_1": summarize(excluded),
        "comparison_note": "Descriptive only; no inferential demographic test is meaningful for a single objectively excluded participant.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
