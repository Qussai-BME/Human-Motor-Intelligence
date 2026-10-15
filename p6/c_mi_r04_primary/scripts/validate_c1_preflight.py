#!/usr/bin/env python3
"""Static preflight for P6-C before scientific execution."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]); args=ap.parse_args(); root=args.root.resolve()
    checks={}
    protocol=(root/"PROTOCOL_C1.md").read_text(encoding="utf-8")
    checks["protocol_declares_R04"]=bool(re.search(r"Primary run: \*\*R04\*\*",protocol))
    checks["protocol_declares_motor_imagery"]="motor imagery" in protocol.lower()
    cfg=(root/"configs/p6_mi_r04.yaml").read_text(encoding="utf-8")
    checks["config_declares_LOSO"]="subjects:" in cfg and "random_seed: 1701" in cfg
    checks["config_declares_abstract_mapping"]="abstract_control_labels_only" in cfg
    checks["scripts_present"]=all((root/"scripts"/name).exists() for name in ["run_p6_mi_r04.py","run_myosim_p6_c.py","make_ground_truth_replays.py","analyze_p6_mi_r04.py"])
    checks["no_raw_edf_in_release"] = not any(root.rglob("*.edf"))
    checks["no_current_r03_as_primary"] = not (root/"PRIMARY_R03").exists()
    status="PASS" if all(checks.values()) else "FAIL"
    out={"status":status,"checks":checks,"scientific_results_available":(root/"results/FINAL_STATISTICS.json").exists()}
    (root/"audit/C1_PREFLIGHT.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    if status != "PASS": raise SystemExit(2)
if __name__=="__main__": main()
