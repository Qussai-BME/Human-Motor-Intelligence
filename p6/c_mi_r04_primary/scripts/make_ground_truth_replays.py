#!/usr/bin/env python3
"""Create model-independent ground-truth control replays from P6-C decoder traces."""
from __future__ import annotations
import argparse
import csv
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--traces", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for src in sorted(args.traces.glob("M1/*.csv")):
        sid = src.stem.split("_")[-1]
        out = args.output / f"GROUND_TRUTH_{sid}.csv"
        with src.open(newline="", encoding="utf-8") as h, out.open("w", newline="", encoding="utf-8") as o:
            r = csv.DictReader(h)
            w = csv.DictWriter(o, fieldnames=["timestamp_s", "label", "confidence", "source_subject", "modality", "model_version", "window_id"])
            w.writeheader()
            for row in r:
                w.writerow({
                    "timestamp_s": row["replay_time_s"],
                    "label": row["ground_truth"],
                    "confidence": "1.0",
                    "source_subject": sid,
                    "modality": "EEG-ground-truth-fixture",
                    "model_version": "P6-C1-ground-truth-fixture-v1",
                    "window_id": row["source_event_id"],
                })

if __name__ == "__main__":
    main()
