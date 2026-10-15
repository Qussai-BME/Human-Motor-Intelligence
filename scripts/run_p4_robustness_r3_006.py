from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def features(x: np.ndarray) -> np.ndarray:
    x = x.astype(np.float64, copy=False)
    z = x - x.mean(axis=2, keepdims=True)
    return np.concatenate([z.std(axis=2), np.mean(np.abs(z), axis=2), np.diff(z, axis=2).std(axis=2)], axis=1)


def drop_channels(x: np.ndarray, pct: int) -> np.ndarray:
    y = x.copy(); k = int(round(x.shape[1] * pct / 100.0))
    if not k: return y
    for c in np.unique(np.round(np.linspace(0, x.shape[1]-1, k)).astype(int)): y[:, c, :] = 0.0
    return y


def perturb(x: np.ndarray, kind: str, pct: int, scale: float, seed: int) -> np.ndarray:
    if kind == "clean": return x.copy()
    if kind == "feature_group_dropout": return drop_channels(x, pct)
    if kind == "additive_noise":
        rng = np.random.default_rng(seed); return x + rng.normal(0.0, scale * pct / 100.0, size=x.shape)
    if kind == "temporal_jitter":
        shift = int(round(x.shape[2] * pct / 100.0)); return np.roll(x, shift, axis=2)
    raise ValueError(kind)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cache-root", type=Path, required=True); ap.add_argument("--output", type=Path, required=True); ap.add_argument("--seed", type=int, default=20261006); a = ap.parse_args()
    files = sorted(a.cache_root.glob("sub-*.npz"), key=lambda p: int(p.stem.split("-")[1])); data = {p.stem: np.load(p, allow_pickle=False) for p in files}; rows=[]; trials=[]
    variants = [("clean",0),("feature_group_dropout",10),("feature_group_dropout",20),("additive_noise",10),("additive_noise",20),("temporal_jitter",10),("temporal_jitter",20)]
    for held in files:
        train = [p for p in files if p != held]; ytr=np.concatenate([data[p.stem]["labels"] for p in train]); tr_epochs=np.concatenate([data[p.stem]["epochs"] for p in train]); tr_feat=features(tr_epochs); model=LinearDiscriminantAnalysis(solver="lsqr",shrinkage="auto").fit(tr_feat,ytr); test=data[held.stem]; scale=float(np.std(tr_epochs));
        for kind,pct in variants:
            ep=perturb(test["epochs"],kind,pct,scale,a.seed+int(held.stem.split("-")[1])); pred=model.predict(features(ep)); y=test["labels"]; met={"subject":held.stem,"variant":kind,"level_percent":pct,"representation":"temporal","train_is_clean":True,"classifier":"LDA lsqr shrinkage=auto","macro_f1":float(f1_score(y,pred,average="macro")),"accuracy":float(accuracy_score(y,pred)),"balanced_accuracy":float(balanced_accuracy_score(y,pred))}; rows.append(met); trials.extend({"subject":held.stem,"variant":kind,"level_percent":pct,"trial":i,"label":int(yy),"prediction":int(pp)} for i,(yy,pp) in enumerate(zip(y.tolist(),pred.tolist())))
    a.output.mkdir(parents=True,exist_ok=True); (a.output/"subject_level_results.json").write_text(json.dumps(rows,indent=2)); (a.output/"trial_predictions.json").write_text(json.dumps(trials,indent=2)); (a.output/"protocol.json").write_text(json.dumps({"task":"P4 clean-train corrupted-test robustness extension","subjects":len(files),"representation":"temporal features; strongest lightweight representation from Exp2","variants":variants,"feature_group_definition":"channel group zeroing","noise_definition":"Gaussian test-only noise scaled by clean-training epoch SD","jitter_definition":"deterministic circular temporal shift","training_is_clean_for_all_variants":True,"loso":True,"seed":a.seed},indent=2)); (a.output/"environment.json").write_text(json.dumps({"python":sys.version,"platform":platform.platform(),"numpy":np.__version__,"timestamp_utc":__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()},indent=2)); (a.output/"manifest.json").write_text(json.dumps({"cache_root":str(a.cache_root),"cache_files":{p.name:sha256(p) for p in files},"raw_recordings":"external and not included","status":"new extension; frozen P4 outputs untouched"},indent=2))

if __name__ == "__main__": main()
