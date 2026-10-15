from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def conf(p):
    e = -(np.clip(p, 1e-12, 1) * np.log(np.clip(p, 1e-12, 1))).sum(1)
    return 1 - e / np.log(max(2, p.shape[1]))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cache-root", type=Path, required=True); ap.add_argument("--output", type=Path, required=True); ap.add_argument("--seed", type=int, default=20261005); a = ap.parse_args()
    files = sorted(a.cache_root.glob("sub-*.npz"), key=lambda p: int(p.stem.split("-")[1])); d = {p.stem: np.load(p, allow_pickle=False) for p in files}; rows = []
    for held in files:
        tr = [p for p in files if p != held]; ytr = np.concatenate([d[p.stem]["labels"] for p in tr]);
        em = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(np.concatenate([d[p.stem]["eeg_features"] for p in tr]), ytr)
        mm = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(np.concatenate([d[p.stem]["emg_features"] for p in tr]), ytr)
        test = d[held.stem]; ep = em.predict_proba(test["eeg_features"]); mp = mm.predict_proba(test["emg_features"]); ec, mc = conf(ep), conf(mp); w = ec / np.maximum(ec + mc, 1e-12); classes = em.classes_
        probs = {"eeg_only": ep, "emg_only": mp, "static_mean_fusion": (ep + mp) / 2, "confidence_weighted_fusion": w[:, None] * ep + (1-w[:, None]) * mp, "confidence_selective_fusion": np.where((ec >= mc)[:, None], ep, mp)}
        for i, y in enumerate(test["labels"].tolist()):
            for name, p in probs.items():
                rows.append({"subject": held.stem, "trial": i, "label": int(y), "condition": name, "probabilities": [float(x) for x in p[i]], "confidence": float(conf(p[[i]])[0])})
    a.output.mkdir(parents=True, exist_ok=True); (a.output/"trial_probabilities.json").write_text(json.dumps(rows, indent=2)); (a.output/"protocol.json").write_text(json.dumps({"task":"P5 clean LOSO calibration extension","subjects":len(files),"conditions":["eeg_only","emg_only","static_mean_fusion","confidence_weighted_fusion","confidence_selective_fusion"],"calibration":"probabilities stored per trial; no post-hoc calibration","seed":a.seed}, indent=2)); (a.output/"environment.json").write_text(json.dumps({"python":sys.version,"platform":platform.platform(),"numpy":np.__version__}, indent=2)); (a.output/"manifest.json").write_text(json.dumps({"cache_root":str(a.cache_root),"cache_files":{p.name:sha256(p) for p in files},"raw_recordings":"external and not included","status":"new extension; frozen P5 R2 untouched"}, indent=2))

if __name__ == "__main__": main()
