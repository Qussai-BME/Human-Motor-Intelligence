#!/usr/bin/env python3
"""Replay released P6 exploratory R03 traces through an external MyoSim checkout."""
from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path


def make_replay(src: Path, dst: Path) -> None:
    with src.open(newline="", encoding="utf-8") as handle, dst.open("w", newline="", encoding="utf-8") as output:
        reader = csv.DictReader(handle)
        fields = ["timestamp_s", "label", "confidence", "source_subject", "modality", "model_version", "window_id"]
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in reader:
            writer.writerow({
                "timestamp_s": row["replay_time_s"],
                "label": row["prediction"],
                "confidence": row["confidence"],
                "source_subject": row["subject_id"],
                "modality": row["modality"],
                "model_version": row["model_id"],
                "window_id": row["source_event_id"],
            })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--myosim-root", required=True, type=Path, help="Path to the external MyoSim source checkout")
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parent / "myosim_exploratory_r03.yaml")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    myosim_root = args.myosim_root.resolve()
    root = args.root.resolve()
    if not (myosim_root / "src").exists():
        raise FileNotFoundError(f"Expected external MyoSim checkout with src/: {myosim_root}")
    sys.path.insert(0, str(myosim_root / "src"))
    try:
        from myosim.core.config import load_config
        from myosim.experiments.task_runner import PickPlaceExperimentRunner
        from myosim.signals.replay import CsvIntentReplay
    except ImportError as exc:
        raise SystemExit(
            "MyoSim runtime could not be imported. Supply --myosim-root pointing to a compatible public MyoSim checkout."
        ) from exc

    trace_root = root / "traces"
    results = root / "results"
    replay_dir = root / "replay_csv"
    run_dir = results / "myosim_runs"
    replay_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    cfg = load_config(args.config.resolve())
    records = []
    for model_dir in sorted(trace_root.iterdir()):
        if not model_dir.is_dir():
            continue
        for src in sorted(model_dir.glob("*.csv")):
            replay = replay_dir / src.name
            make_replay(src, replay)
            result = PickPlaceExperimentRunner(cfg, myosim_root).run(CsvIntentReplay(replay))
            output = result.to_dict()
            target = run_dir / f"{src.stem}.json"
            output.update({
                "trace_source": str(src.relative_to(root)),
                "replay_csv": str(replay.relative_to(root)),
                "model_id": model_dir.name,
            })
            target.write_text(json.dumps(output, indent=2, default=str) + "\n", encoding="utf-8")
            tm, cm = output["task_metrics"], output["control_metrics"]
            records.append({
                "trace": str(src.relative_to(root)),
                "model_id": model_dir.name,
                "subject_id": src.stem.split("_")[1],
                "task_success": tm["success"],
                "completion_time_s": tm["completion_time_s"],
                "final_error_m": tm["final_error_m"],
                "path_length_m": tm["path_length_m"],
                "command_corrections": tm["command_corrections"],
                "grasp_stability_steps": tm["grasp_stability_steps"],
                "final_state": tm["final_state"],
                "invalid_state_detected": output["invalid_state_detected"],
                "released_command_count_reconciled": sum(
                    1 for item in output["control_transitions"] if item.get("reason") == "single_authenticated_event_released"
                ),
                "run_artifact": str(target.relative_to(root)),
            })
    (results / "MYOSIM_RESULTS.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "runs": len(records),
        "successes": sum(r["task_success"] for r in records),
        "invalid_states": sum(r["invalid_state_detected"] for r in records),
    }, indent=2))


if __name__ == "__main__":
    main()
