#!/usr/bin/env python3
"""Analyze P6-C1 outcomes without trial-level pseudoreplication."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import numpy as np
from scipy.stats import friedmanchisquare

MODELS = ("M1", "M2", "M3")
METRICS = ("final_error_m", "path_length_m", "command_corrections", "grasp_stability_steps")

def load_records(path: Path) -> list[dict]:
    rows = json.loads(path.read_text())
    if len(rows) != 60:
        raise RuntimeError(f"Expected 60 decoder outcomes, found {len(rows)}")
    out=[]
    for r in rows:
        m = re.search(r"/(M[123])_(S\d{3})\.csv$", r["source"])
        if not m:
            raise ValueError(f"Cannot recover model/subject from {r['source']}")
        out.append({**r, "model_id": m.group(1), "subject_id": m.group(2)})
    return out

def bootstrap_ci(values: np.ndarray, seed: int = 1701) -> list[float]:
    values=np.asarray(values,dtype=float)
    if len(values)==0: return [None, None]
    rng=np.random.default_rng(seed)
    means=np.mean(values[rng.integers(0,len(values),size=(10000,len(values)))],axis=1)
    return [float(np.quantile(means,0.025)), float(np.quantile(means,0.975))]

def paired_effect(a: np.ndarray,b: np.ndarray, seed: int) -> dict:
    d=np.asarray(a,dtype=float)-np.asarray(b,dtype=float)
    mean=float(np.mean(d)); sd=float(np.std(d,ddof=1)) if len(d)>1 else float("nan")
    return {"mean_difference_a_minus_b":mean,"cohens_dz":float(mean/sd) if sd>0 else None,"ci95_mean_difference":bootstrap_ci(d,seed)}

def summarize(root: Path, label: str) -> dict:
    rows=load_records(root/"results/myosim/DECODER_RESULTS.json")
    by={m:{} for m in MODELS}
    for r in rows: by[r["model_id"]][r["subject_id"]]=r
    subjects=sorted(set(by["M1"]) & set(by["M2"]) & set(by["M3"]))
    if len(subjects)!=20: raise RuntimeError(f"Expected 20 paired subjects, found {len(subjects)}")
    stats={}
    for metric in METRICS:
        vals={m:np.array([by[m][s][metric] for s in subjects],dtype=float) for m in MODELS}
        result={"summary":{}}
        for m,v in vals.items(): result["summary"][m]={"n_subjects":len(v),"mean":float(np.mean(v)),"median":float(np.median(v)),"ci95_mean":bootstrap_ci(v,1701+ord(m[-1]))}
        if any(np.ptp(v)>0 for v in vals.values()):
            f=friedmanchisquare(*(vals[m] for m in MODELS))
            result["friedman"]={"chi_square":float(f.statistic),"p_value":float(f.pvalue),"kendall_W":float(f.statistic/(len(subjects)*2))}
        else: result["friedman"]={"not_run":"all model values are constant"}
        result["paired_effects"]={}
        for i,a in enumerate(MODELS):
            for b in MODELS[i+1:]: result["paired_effects"][f"{a}_minus_{b}"]=paired_effect(vals[a],vals[b],1900+i)
        stats[metric]=result
    success={m:int(sum(bool(by[m][s]["task_success"]) for s in subjects)) for m in MODELS}
    return {"label":label,"n_subjects":20,"n_models":3,"subjects":subjects,"primary_endpoint":"task_success","success_counts":success,"success_inferential_test":"not_run_degenerate_zero_success","continuous_endpoints":stats,"run_level_artifacts":60}

def main()->None:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,required=True); args=ap.parse_args(); root=args.root.resolve()
    primary=summarize(root,"primary")
    rerun_root=root.parent/"c_mi_r04_rerun"
    rerun=summarize(rerun_root,"rerun") if (rerun_root/"results/myosim/DECODER_RESULTS.json").exists() else None
    payload={"protocol":"P6-C1-MI-R04-v1.0","quality_mapping":json.loads((root/"results/QUALITY_MAPPING.json").read_text())["quality_mapping"],"fixture_gate":json.loads((root/"results/myosim/FIXTURE_RESULTS.json").read_text()),"primary":primary,"rerun":rerun,"interpretation":"The fixture passed, but task success was zero for all decoder-conditioned runs; therefore decoder-quality-to-task-success inference is non-discriminative. Continuous endpoints are exploratory and inference is paired at subject level."}
    (root/"results/FINAL_STATISTICS.json").write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps(payload,indent=2))
if __name__=="__main__": main()
