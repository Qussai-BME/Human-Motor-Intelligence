#!/usr/bin/env python3
"""Independent public-release gate (P6 C1, post-hoc audit and C2 readiness)."""
from __future__ import annotations

import csv
import hashlib
import json
import ast
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {"historical", ".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}
REQUIRED = [
    "README.md", "CITATION.cff", "LICENSE", "NOTICE.md", "DATA_AND_LICENSES.md",
    "SCIENTIFIC_LIMITATIONS.md", "P6_FINAL_STATUS.md", "p6/README.md",
    "p6/c_mi_r04_primary/PROTOCOL_C1.md", "p6/c_mi_r04_primary/README.md",
    "p6/c_mi_r04_primary/configs/p6_mi_r04.yaml",
    "p6/c_mi_r04_primary/scripts/run_p6_mi_r04.py",
    "p6/c_mi_r04_primary/scripts/run_myosim_p6_c.py",
    "papers/paper_6/P6_C1_MANUSCRIPT.md", "papers/paper_6/CLAIM_EVIDENCE_MATRIX.md",
    "papers/paper_6/RESULTS_SUMMARY.md", "papers/P6_SUPERSESSION_NOTICE.md",
    "p6/c1_audit/README.md", "p6/c1_audit/outputs/numbers.json", "p6/c1_audit/outputs/diag_runs.json",
    "p6/c2_episode/README.md", "p6/c2_episode/PROTOCOL_C2.md", "p6/c2_episode/results/ANALYSIS.json",
    "p6/c2_episode/results/emulator_episodes.csv", "p6/c2_episode/results/real_episodes.csv",
    "p6/c2_episode/registry/FREEZE_MANIFEST.json", "p6/c2_episode/raw_archives/SHA256SUMS.txt",
    "closure/11_P6_C2_CLOSURE_REPORT.md",
    "papers/paper_6/STATISTICAL_ANALYSIS_REPORT.md", "closure/P6_C1_EXECUTION_GATE.md",
    "release/RELEASE_MANIFEST.json", "release/RELEASE_READINESS.json",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def current_files():
    for p in ROOT.rglob("*"):
        if p.is_file() and not any(part in EXCLUDE for part in p.parts):
            yield p


def check_trace(path: Path) -> tuple[int, list[str]]:
    errors=[]
    with path.open(newline="", encoding="utf-8") as f:
        r=csv.DictReader(f); fields=set(r.fieldnames or [])
        required={"source_event_label","control_mapping_id","source_file_sha256","model_version","subject_id"}
        for miss in sorted(required-fields): errors.append(f"{path.relative_to(ROOT)} missing {miss}")
        if "trace_sha256" in fields: errors.append(f"{path.relative_to(ROOT)} embeds self-hash")
        rows=list(r)
    return len(rows),errors


def main() -> int:
    errors=[]; warnings=[]
    for rel in REQUIRED:
        if not (ROOT/rel).exists(): errors.append(f"MISSING_REQUIRED {rel}")
    # Parse current machine-readable files and compile all current Python.
    for p in current_files():
        try:
            if p.suffix.lower()==".json": json.loads(p.read_text(encoding="utf-8"))
            elif p.suffix.lower()==".toml": tomllib.loads(p.read_text(encoding="utf-8"))
            elif p.suffix.lower()==".py": ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
        except Exception as exc: errors.append(f"PARSE_ERROR {p.relative_to(ROOT)} {exc}")
    # Identity.
    pp=tomllib.loads((ROOT/"pyproject.toml").read_text(encoding="utf-8"))
    if pp["project"]["version"] != "1.2.0": errors.append("VERSION")
    if pp["project"]["authors"][0]["name"] != "Qussai Adlbi": errors.append("AUTHOR")
    cff=(ROOT/"CITATION.cff").read_text(encoding="utf-8")
    if 'version: "1.2.0"' not in cff: errors.append("CFF_VERSION")
    if 'given-names: "Qussai"' not in cff or 'family-names: "Adlbi"' not in cff: errors.append("CFF_AUTHOR")
    # Public tree hygiene.
    raw_ext={".edf",".bdf",".gdf",".set",".fif",".cnt",".eeg"}
    raw=[p for p in current_files() if p.suffix.lower() in raw_ext]
    if raw: errors.append("RAW_DATA " + ",".join(str(p.relative_to(ROOT)) for p in raw))
    for p in current_files():
        if p.is_symlink(): errors.append(f"SYMLINK {p.relative_to(ROOT)}")
        if p.suffix.lower() in {".md",".py",".json",".yaml",".yml",".toml",".txt"}:
            txt=p.read_text(encoding="utf-8",errors="ignore")
            blocked_tokens = ["/" + "home/ubuntu/", "REPLACE" + "-WITH-YOUR-REPOSITORY", "RECORDED" + "_AFTER_WRITE"]
            for token in blocked_tokens:
                if token in txt: errors.append(f"STALE_TOKEN {token} {p.relative_to(ROOT)}")
    # P6 R03 engineering baseline integrity.
    r03=ROOT/"p6/exploratory_r03_primary"; r03r=ROOT/"p6/exploratory_r03_rerun"
    p_traces=sorted(r03.glob("traces/M*/M*_S*.csv")); r_traces=sorted(r03r.glob("traces/M*/M*_S*.csv"))
    p_runs=sorted((r03/"results/myosim_runs").glob("M*_S*.json")); r_runs=sorted((r03r/"results/myosim_runs").glob("M*_S*.json"))
    if len(p_traces)!=60: errors.append(f"R03_PRIMARY_TRACES {len(p_traces)}")
    if len(r_traces)!=60: errors.append(f"R03_RERUN_TRACES {len(r_traces)}")
    if len(p_runs)!=60: errors.append(f"R03_PRIMARY_MYOSIM {len(p_runs)}")
    if len(r_runs)!=0: errors.append(f"R03_RERUN_MYOSIM_SHOULD_BE_ZERO {len(r_runs)}")
    for p in p_traces+r_traces:
        n,e=check_trace(p); errors.extend(e)
        if n!=15: errors.append(f"R03_TRACE_ROWS {p.relative_to(ROOT)} {n}")
    # C1 scientific execution and rerun integrity.
    c1_status=json.loads((ROOT/"p6/c_mi_r04_primary/results/STATUS.json").read_text())
    if c1_status.get("protocol") != "P6-C1-MI-R04-v1.0": errors.append("C1_STATUS_PROTOCOL")
    c1=ROOT/"p6/c_mi_r04_primary"; c1r=ROOT/"p6/c_mi_r04_rerun"
    c1_traces=sorted(c1.glob("traces/M*/M*_S*.csv")); c1_runs=sorted((c1/"results/myosim/decoder").glob("*.json"))
    c1r_traces=sorted(c1r.glob("traces/M*/M*_S*.csv")); c1r_runs=sorted((c1r/"results/myosim/decoder").glob("*.json"))
    if len(c1_traces)!=60: errors.append(f"C1_PRIMARY_TRACES {len(c1_traces)}")
    if len(c1_runs)!=60: errors.append(f"C1_PRIMARY_MYOSIM_RUNS {len(c1_runs)}")
    if len(c1r_traces)!=60: errors.append(f"C1_RERUN_TRACES {len(c1r_traces)}")
    if len(c1r_runs)!=60: errors.append(f"C1_RERUN_MYOSIM_RUNS {len(c1r_runs)}")
    if not (c1/"results/QUALITY_MAPPING.json").exists(): errors.append("C1_QUALITY_MAPPING_MISSING")
    if not (c1/"results/FINAL_STATISTICS.json").exists(): errors.append("C1_STATS_MISSING")
    if not (c1/"results/myosim/FIXTURE_RESULTS.json").exists(): errors.append("C1_FIXTURE_MISSING")
    rs=json.loads((c1r/"results/STATUS.json").read_text())
    if rs.get("scientific_status") != "SCIENTIFICALLY_COMPLETE": errors.append("C1_RERUN_STATUS")
    if rs.get("task_replay") != "complete": errors.append("C1_RERUN_TASK_REPLAY")
    # C2 episode-level study integrity.
    c2=ROOT/"p6/c2_episode"; c2_info={}
    try:
        freeze=json.loads((c2/"registry/FREEZE_MANIFEST.json").read_text())
        for rel,digest in freeze["files"].items():
            name=Path(rel).name; cand=c2/"registry/frozen"/(name+".frozen" if name.endswith(".py") else name)
            if not cand.exists() or sha256(cand)!=digest: errors.append(f"C2_FREEZE_HASH {name}")
        import pandas as pd
        e=pd.read_csv(c2/"results/emulator_episodes.csv"); rr=pd.read_csv(c2/"results/real_episodes.csv"); s=pd.read_csv(c2/"results/sensitivity_episodes.csv")
        cells=e.groupby(["regime","q","rho"]).size()
        if len(e)!=27000 or len(cells)!=54 or set(cells.unique())!={500}: errors.append("C2_EMULATOR_COUNTS")
        if int((rr.arm=="R0").sum())!=560 or int((rr.arm=="R1").sum())!=19750: errors.append("C2_REAL_COUNTS")
        if len(s)!=25600: errors.append("C2_SENSITIVITY_COUNTS")
        ana=json.loads((c2/"results/ANALYSIS.json").read_text())
        if ana.get("schema")!="P6-C2-ANALYSIS-v1": errors.append("C2_ANALYSIS_SCHEMA")
        for line in (c2/"raw_archives/SHA256SUMS.txt").read_text().splitlines():
            digest,name=line.split()
            if sha256(c2/"raw_archives"/name)!=digest: errors.append(f"C2_ARCHIVE_HASH {name}")
        c2_info={"emulator_episodes":len(e),"real_episodes":len(rr),"sensitivity_episodes":len(s),"freeze_files":len(freeze["files"])}
    except Exception as exc: errors.append(f"C2_CHECK {exc}")
    # Manifest integrity.
    mpath=ROOT/"release/RELEASE_MANIFEST.json"
    try:
        m=json.loads(mpath.read_text(encoding="utf-8")); entries=m["files"]
        paths=[x["path"] for x in entries]
        if paths != sorted(paths): errors.append("MANIFEST_ORDER")
        if len(paths)!=len(set(paths)): errors.append("MANIFEST_DUPLICATES")
        for e in entries:
            p=ROOT/e["path"]
            if not p.exists(): errors.append(f"MANIFEST_MISSING {e['path']}"); continue
            if p.stat().st_size!=e["bytes"] or sha256(p)!=e["sha256"]: errors.append(f"MANIFEST_HASH {e['path']}")
        if len(paths)!=m.get("file_count"): errors.append("MANIFEST_COUNT")
    except Exception as exc: errors.append(f"MANIFEST_PARSE {exc}")
    status="PASS" if not errors else "FAIL"
    out={"status":status,"r03_engineering_baseline":{"primary_traces":len(p_traces),"primary_myosim":len(p_runs),"rerun_traces":len(r_traces),"rerun_myosim":len(r_runs)},"c1":{"status":c1_status.get("scientific_status"),"primary_traces":len(c1_traces),"primary_myosim":len(c1_runs),"rerun_traces":len(c1r_traces),"rerun_myosim":len(c1r_runs)},"c2":c2_info,"errors":errors,"warnings":warnings}
    print(json.dumps(out,indent=2))
    return 0 if status=="PASS" else 2

if __name__=="__main__": raise SystemExit(main())
