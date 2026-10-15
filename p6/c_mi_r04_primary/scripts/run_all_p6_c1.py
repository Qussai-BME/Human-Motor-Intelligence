#!/usr/bin/env python3
"""Orchestrate the complete P6-C1 execution in the required gate order."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

P=Path(__file__).resolve().parents[1]
S=P/'scripts'

def run(cmd:list[str])->None:
    print('>',' '.join(map(str,cmd)),flush=True)
    subprocess.run(cmd,check=True)

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--data-root',type=Path,required=True)
    ap.add_argument('--myosim-root',type=Path,required=True)
    args=ap.parse_args()
    run([sys.executable,str(S/'run_p6_mi_r04.py'),'--data-root',str(args.data_root),'--output-dir',str(P)])
    run([sys.executable,str(S/'make_ground_truth_replays.py'),'--traces',str(P/'traces'),'--output',str(P/'replay_csv/ground_truth')])
    # Fixture is deliberately separate from decoder-conditioned evidence.
    run([sys.executable,str(S/'run_myosim_p6_c.py'),'--myosim-root',str(args.myosim_root),'--root',str(P),'--mode','fixture'])
    run([sys.executable,str(S/'run_myosim_p6_c.py'),'--myosim-root',str(args.myosim_root),'--root',str(P),'--mode','decoder'])
    rerun=P.parent/'c_mi_r04_rerun'
    run([sys.executable,str(S/'run_p6_mi_r04.py'),'--data-root',str(args.data_root),'--output-dir',str(rerun)])
    run([sys.executable,str(S/'run_myosim_p6_c.py'),'--myosim-root',str(args.myosim_root),'--root',str(rerun),'--mode','decoder'])
    run([sys.executable,str(S/'analyze_p6_mi_r04.py'),'--root',str(P)])

if __name__=='__main__': main()
