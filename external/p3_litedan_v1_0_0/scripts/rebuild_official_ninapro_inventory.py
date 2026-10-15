#!/usr/bin/env python3
"""Rebuild a validated official NinaPro archive inventory from the source pages.

The official DB2, DB3, and DB7 subject-list pages expose different, verified
archive URL conventions. This tool records those public URLs and requires a
successful official-host HEAD response with a positive Content-Length for every
configured subject before atomically writing the inventory consumed by staged
preparation.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "LiteDAN-Paper3-official-inventory-recovery/1.1"
SOURCE_PAGES = {
    "DB2": "https://ninapro.hevs.ch/instructions/DB2.html",
    "DB3": "https://ninapro.hevs.ch/instructions/DB3.html",
    "DB7": "https://ninapro.hevs.ch/instructions/DB7.html",
}


def archive_url(db: str, subject: int) -> str:
    if db == "DB2":
        return f"https://ninapro.hevs.ch/files/DB2_Preproc/DB2_s{subject}.zip"
    if db == "DB3":
        return f"https://ninapro.hevs.ch/files/db3_Preproc/s{subject}_0.zip"
    if db == "DB7":
        return f"https://ninapro.hevs.ch/files/DB7_Preproc/Subject_{subject}.zip"
    raise ValueError(f"Unsupported dataset: {db}")


def official_size(url: str, attempts: int = 3) -> int:
    error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.head(
                url,
                allow_redirects=True,
                timeout=(30, 120),
                headers={"User-Agent": USER_AGENT},
            )
            response.raise_for_status()
            final_host = requests.utils.urlparse(response.url).hostname
            if final_host != "ninapro.hevs.ch":
                raise RuntimeError(f"unexpected final host {final_host!r}")
            value = response.headers.get("Content-Length")
            if value is None or int(value) <= 0:
                raise RuntimeError(f"invalid Content-Length {value!r}")
            return int(value)
        except (requests.RequestException, RuntimeError, ValueError) as exc:
            error = exc
            if attempt < attempts:
                time.sleep(5 * attempt)
    raise RuntimeError(f"Unable to validate official archive endpoint {url}: {error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "protocol_v1_1.yaml")
    parser.add_argument("--output", type=Path, default=ROOT / "audit_outputs" / "official_ninapro_download_inventory.json")
    parser.add_argument("--db", choices=("DB2", "DB3", "DB7"), action="append", help="Restrict to named database; defaults to all three")
    args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    selected = args.db or ["DB2", "DB3", "DB7"]
    databases: dict[str, Any] = {}
    for db in selected:
        count = int(config["datasets"][db]["expected_subjects"])
        subjects = []
        for subject in range(1, count + 1):
            url = archive_url(db, subject)
            size = official_size(url)
            print(f"validated {db} S{subject:02d}: {size} bytes", flush=True)
            subjects.append({
                "text": f"s{subject}.zip",
                "url": url,
                "content_length": size,
                "source_page": SOURCE_PAGES[db],
            })
        databases[db] = {
            "source_page": SOURCE_PAGES[db],
            "subjects": subjects,
        }
    payload = {
        "inventory_name": "official_ninapro_subject_archives",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "user_agent": USER_AGENT,
        "databases": databases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(args.output)
    print(json.dumps({"output": str(args.output), "databases": {name: len(data["subjects"]) for name, data in databases.items()}}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"INVENTORY ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
