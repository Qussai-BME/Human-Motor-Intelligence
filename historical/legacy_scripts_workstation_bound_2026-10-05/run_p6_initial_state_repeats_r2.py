#!/usr/bin/env python3
"""Run declared P6 R2 initial-state repeat cohorts without changing replay/control/task."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import asdict, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path("<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1")
MYOSIM_ROOT = Path("<LOCAL_WORKSPACE>/dependencies/myosim_v1_1")
CONFIG_PATH = REPO / "configs/experiments/p6_initial_state_repeats_recovery_r2.yaml"
REPLAY_PATH = MYOSIM_ROOT / "examples/intents/pick_place_replay.csv"
PROTOCOL_ID = "p6-real-replay-initial-state-repeats-recovery-r2"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def code_fingerprint() -> dict[str, Any]:
    tracked = [
        MYOSIM_ROOT / "src/myosim/core/config.py",
        MYOSIM_ROOT / "src/myosim/simulation/mujoco_backend.py",
        MYOSIM_ROOT / "src/myosim/experiments/task_runner.py",
    ]
    payload = {str(path.relative_to(MYOSIM_ROOT)): sha256(path) for path in tracked}
    try:
        commit = subprocess.check_output(["git", "-C", str(MYOSIM_ROOT), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        commit = "unavailable"
    return {"source_root": str(MYOSIM_ROOT), "git_commit": commit, "tracked_source_sha256": payload}


def environment() -> dict[str, Any]:
    packages: dict[str, str] = {}
    for name in ("numpy", "mujoco", "yaml", "myosim"):
        try:
            module = __import__(name)
            packages[name] = str(getattr(module, "__version__", "unknown"))
        except ImportError:
            packages[name] = "not-installed"
    return {"python": sys.version, "platform": platform.platform(), "packages": packages, "utc": now()}


def run_one(seed: int) -> dict[str, Any]:
    from myosim.core.config import load_config
    from myosim.experiments.task_runner import PickPlaceExperimentRunner
    from myosim.signals.replay import CsvIntentReplay

    config = load_config(CONFIG_PATH)
    config = replace(config, run=replace(config.run, seed=seed))
    if not config.initial_state.enabled or config.initial_state.distribution_id != "uniform_forearm_xy_v1":
        raise RuntimeError("P6 R2 requires the declared uniform_forearm_xy_v1 initial-state configuration")
    result = PickPlaceExperimentRunner(config, MYOSIM_ROOT).run(CsvIntentReplay(REPLAY_PATH))
    payload = result.to_dict()
    initial = payload["initial_state"]
    offsets = initial["initial_joint_offsets"]
    if set(offsets) != {"forearm_x", "forearm_y"}:
        raise RuntimeError("declared initial-state offsets were not recorded exactly")
    if not 0.0 <= float(offsets["forearm_x"]) <= 0.020 or not -0.015 <= float(offsets["forearm_y"]) <= 0.015:
        raise RuntimeError("realized initial-state offset is outside the R2 declared range")
    if initial["initial_named_joint_positions"]["forearm_x"] != offsets["forearm_x"] or initial["initial_named_joint_positions"]["forearm_y"] != offsets["forearm_y"]:
        raise RuntimeError("observed initial state does not match declared offsets")
    return {
        "protocol_id": PROTOCOL_ID,
        "origin": "real_replay_initial_state_variation",
        "benchmark_eligible": False,
        "replay": {"path": str(REPLAY_PATH), "sha256": sha256(REPLAY_PATH)},
        "config": asdict(config),
        "result": payload,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seeds", required=True, nargs="+", type=int)
    parser.add_argument("--mode", required=True, choices=("probes", "primary", "independent-rerun"))
    args = parser.parse_args()
    seeds = list(args.seeds)
    if len(seeds) != len(set(seeds)) or any(seed < 0 for seed in seeds):
        raise SystemExit("seeds must be unique non-negative integers")
    if args.mode in {"primary", "independent-rerun"} and seeds != list(range(20260901, 20260921)):
        raise SystemExit("primary and independent-rerun modes require exactly seeds 20260901..20260920")
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"immutable output path already exists: {output}")
    output.mkdir(parents=True, exist_ok=False)
    (output / "protocol.json").write_text(json.dumps({
        "protocol_id": PROTOCOL_ID,
        "mode": args.mode,
        "seeds": seeds,
        "config_path": str(CONFIG_PATH),
        "replay_path": str(REPLAY_PATH),
        "origin": "real_replay_initial_state_variation",
        "benchmark_eligible": False,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output / "environment.json").write_text(json.dumps(environment(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output / "code_fingerprint.json").write_text(json.dumps(code_fingerprint(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    records: list[dict[str, Any]] = []
    for index, seed in enumerate(seeds, start=1):
        record = run_one(seed)
        (output / f"run-{seed}.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        metrics = record["result"]["task_metrics"]
        initial = record["result"]["initial_state"]
        records.append({
            "seed": seed,
            "success": bool(metrics["success"]),
            "completion_time_s": float(metrics["completion_time_s"]) if metrics["completion_time_s"] is not None else None,
            "final_error_m": float(metrics["final_error_m"]),
            "path_length_m": float(metrics["path_length_m"]),
            "grasp_stability_steps": int(metrics["grasp_stability_steps"]),
            "command_corrections": int(metrics["command_corrections"]),
            "final_state": str(metrics["final_state"]),
            "invalid_state_detected": bool(record["result"]["invalid_state_detected"]),
            "forearm_x_offset_m": float(initial["initial_joint_offsets"]["forearm_x"]),
            "forearm_y_offset_m": float(initial["initial_joint_offsets"]["forearm_y"]),
            "initial_qpos": initial["initial_qpos"],
            "initial_named_joint_positions": initial["initial_named_joint_positions"],
        })
        print(f"completed seed {seed} ({index}/{len(seeds)})", flush=True)
    (output / "run_records.json").write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "mode": args.mode, "run_count": len(records), "seeds": seeds}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
