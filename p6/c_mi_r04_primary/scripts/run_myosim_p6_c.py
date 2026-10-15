#!/usr/bin/env python3
"""Replay P6-C traces or ground-truth fixture streams through an external MyoSim checkout."""
from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path


def make_replay(src: Path, dst: Path, label_column: str = "prediction", confidence_column: str = "confidence") -> None:
    with src.open(newline="", encoding="utf-8") as handle, dst.open("w", newline="", encoding="utf-8") as output:
        reader = csv.DictReader(handle)
        fields = ["timestamp_s", "label", "confidence", "source_subject", "modality", "model_version", "window_id"]
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in reader:
            writer.writerow({
                "timestamp_s": row["timestamp_s"] if "timestamp_s" in row else row["replay_time_s"],
                # The packaged MyoSim fixture already uses the canonical
                # ``label`` column; decoder traces use ``prediction``.
                "label": row.get(label_column) or row.get("label"),
                "confidence": row[confidence_column] if confidence_column in row else "1.0",
                "source_subject": row.get("source_subject") or row.get("subject_id") or "unknown",
                "modality": row.get("modality") or "EEG",
                "model_version": row.get("model_version") or "P6-C1",
                "window_id": row.get("window_id") or row.get("source_event_id") or "unknown",
            })


def run_dir_for(root: Path, mode: str) -> Path:
    return root / "results" / "myosim" / mode


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--myosim-root", type=Path, required=True)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "configs/p6_mi_r04_mysim.yaml")
    ap.add_argument("--mode", choices=["fixture", "ground_truth", "decoder"], required=True)
    ap.add_argument("--trace-dir", type=Path, default=None)
    args = ap.parse_args()

    myosim_root = args.myosim_root.resolve()
    root = args.root.resolve()
    sys.path.insert(0, str(myosim_root / "src"))
    from myosim.core.config import load_config
    from myosim.experiments.task_runner import PickPlaceExperimentRunner
    from myosim.signals.replay import CsvIntentReplay

    cfg = load_config(args.config.resolve())
    if args.mode == "fixture":
        source_dir = myosim_root / "examples" / "intents"
        sources = [source_dir / "pick_place_replay.csv"]
        if not sources[0].exists():
            raise FileNotFoundError("MyoSim fixture pick_place_replay.csv not found")
    elif args.mode == "ground_truth":
        source_dir = root / "replay_csv" / "ground_truth"
        if not source_dir.exists():
            raise FileNotFoundError("Run make_ground_truth_replays.py first")
        sources = sorted(source_dir.glob("*.csv"))
    else:
        source_dir = args.trace_dir.resolve() if args.trace_dir else root / "traces"
        sources = sorted(source_dir.glob("M*/*.csv"))

    replay_dir = root / "replay_csv" / args.mode
    run_root = run_dir_for(root, args.mode)
    replay_dir.mkdir(parents=True, exist_ok=True)
    run_root.mkdir(parents=True, exist_ok=True)
    records = []
    if args.mode == "decoder" and len(sources) != 60:
        raise RuntimeError(f"Expected 60 decoder traces, found {len(sources)}")
    if args.mode == "ground_truth" and len(sources) != 20:
        raise RuntimeError(f"Expected 20 ground-truth fixture streams, found {len(sources)}")

    for src in sources:
        replay = replay_dir / src.name
        make_replay(src, replay)
        result = PickPlaceExperimentRunner(cfg, myosim_root).run(CsvIntentReplay(replay))
        output = result.to_dict()
        target = run_root / f"{src.stem}.json"
        target.write_text(json.dumps(output, indent=2, default=str) + "\n", encoding="utf-8")
        tm = output["task_metrics"]
        records.append({
            "source": str(src),
            "run_artifact": str(target.relative_to(root)),
            "task_success": bool(tm["success"]),
            "completion_time_s": tm["completion_time_s"],
            "final_error_m": tm["final_error_m"],
            "path_length_m": tm["path_length_m"],
            "command_corrections": tm["command_corrections"],
            "grasp_stability_steps": tm["grasp_stability_steps"],
            "final_state": tm["final_state"],
            "invalid_state_detected": bool(output["invalid_state_detected"]),
        })
    (root / "results/myosim" / f"{args.mode.upper()}_RESULTS.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    successes=sum(r["task_success"] for r in records)
    if args.mode == "fixture" and successes != len(records):
        raise SystemExit("P6-C1 control fixture failed: task is not validated for decoder comparison.")
    print(json.dumps({"mode": args.mode, "runs": len(records), "successes": successes}, indent=2))


if __name__ == "__main__":
    main()
