#!/usr/bin/env python3
"""Acquire only the 20 official PhysioNet EEGMMIDB R04 EDF inputs required by P6-C1."""
from __future__ import annotations
import argparse, hashlib, re
from pathlib import Path
from urllib.request import urlopen, Request

BASE="https://physionet.org/files/eegmmidb/1.0.0"
SUBJECTS=[f"S{i:03d}" for i in range(1,21)]

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def fetch(url:str,dst:Path)->None:
    req=Request(url,headers={'User-Agent':'Human-Motor-Intelligence-P6-C1/0.1'})
    with urlopen(req,timeout=60) as r, dst.open('wb') as f:
        while True:
            b=r.read(1024*1024)
            if not b: break
            f.write(b)

def main()->None:
    ap=argparse.ArgumentParser(); ap.add_argument('--output-root',type=Path,required=True); ap.add_argument('--subjects',nargs='+',default=SUBJECTS); args=ap.parse_args()
    out=args.output_root.resolve(); out.mkdir(parents=True,exist_ok=True)
    for sid in args.subjects:
        if sid not in SUBJECTS: raise ValueError(sid)
        d=out/sid; d.mkdir(parents=True,exist_ok=True); target=d/f'{sid}R04.edf'
        if not target.exists(): fetch(f'{BASE}/{sid}/{target.name}',target)
        print(sid,target.stat().st_size,sha256(target))

if __name__=='__main__': main()
