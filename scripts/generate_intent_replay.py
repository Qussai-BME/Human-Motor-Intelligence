#!/usr/bin/env python3
"""Generate a deterministic, explicitly synthetic MyoSim-compatible replay bundle.

This script is an integration smoke/demonstration path. It does not load EMG,
train a decoder, or produce a scientific benchmark. Every emitted event is
marked synthetic and is traceable through the MyoControl prediction adapter and
the explicit MyoSim label map.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from research_core.adapters import intent_from_myocontrol_prediction, intent_to_myosim_payload
from research_core.contracts import EvidenceClass
from research_core.contracts.base import canonical_json, sha256_json


LABEL_MAP = {"rest": "REST", "precision_pinch": "PINCH"}


def deterministic_prediction_stream() -> tuple[tuple[float, str, float], ...]:
    """Return a fixed synthetic intent sequence solely for repeatable plumbing tests."""
    stream: list[tuple[float, str, float]] = [(0.0, "rest", 0.99)]
    # Preserve the documented V1 pick-and-place event cadence while exercising
    # this repository's own upstream prediction-to-intent-to-label-map path.
    stream.extend((round(0.10 + index * 0.1, 2), "precision_pinch", 0.95) for index in range(30))
    stream.extend(((3.10, "rest", 0.99), (3.22, "rest", 0.99)))
    return tuple(stream)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a synthetic adapter-derived MyoSim replay CSV.")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/integrated_demo"))
    args = parser.parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    replay_path = output_dir / "adapter_generated_intent_replay.csv"
    intents = []
    payloads = []
    provenance = {
        "origin": EvidenceClass.SYNTHETIC.value,
        "fallback_reason": "deterministic integration demonstration fixture; not a real decoder output",
        "details": {"benchmark_eligible": False, "fixture": "integrated-demo-v1"},
    }
    for index, (timestamp, label, confidence) in enumerate(deterministic_prediction_stream()):
        prediction = {
            "predicted_class": label,
            "confidence": confidence,
            "probabilities": {label: confidence, "rest": 1.0 - confidence} if label != "rest" else {"rest": 1.0},
        }
        intent = intent_from_myocontrol_prediction(
            prediction,
            intent_id=f"synthetic-intent-{index:03d}",
            timestamp_utc=f"2026-08-22T12:00:{index:02d}+00:00",
            stream_time_seconds=timestamp,
            source_model_id="myocontrol-classical-decoder",
            model_version="synthetic-integration-fixture-v1",
            subject_id="synthetic-subject",
            session_id="synthetic-session",
            window_id=f"synthetic-window-{index:03d}",
            external_provenance=provenance,
            metadata={"integration_demo": True, "not_scientific_evidence": True},
        )
        payload = intent_to_myosim_payload(intent, label_map=LABEL_MAP)
        intents.append(intent.to_dict())
        payloads.append(payload)
    with replay_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["timestamp_s", "label", "confidence", "source_subject", "modality", "model_version", "window_id"],
        )
        writer.writeheader()
        for payload in payloads:
            writer.writerow(
                {
                    "timestamp_s": f"{payload.timestamp_s:.2f}",
                    "label": payload.label,
                    "confidence": f"{payload.confidence:.6g}",
                    "source_subject": payload.source_subject or "",
                    "modality": payload.modality,
                    "model_version": payload.model_version,
                    "window_id": payload.window_id or "",
                }
            )
    metadata_path = output_dir / "replay_bundle.json"
    metadata = {
        "bundle_kind": "synthetic-integrated-demo-replay",
        "evidence_class": "synthetic",
        "benchmark_eligible": False,
        "purpose": "deterministic contract and simulator integration demonstration only",
        "label_map": LABEL_MAP,
        "replay_csv": str(replay_path),
        "replay_csv_sha256": __import__("hashlib").sha256(replay_path.read_bytes()).hexdigest(),
        "intent_count": len(intents),
        "intent_records": intents,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"replay_csv": str(replay_path), "bundle": str(metadata_path), "intent_count": len(intents)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
