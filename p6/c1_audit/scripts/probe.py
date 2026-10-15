import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _REPO=_HERE.parents[2]; _OUT=_HERE.parent/'outputs'
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
import sys, csv, io, json, tempfile, os
from pathlib import Path
import numpy as np
MYO=MYOSIM_DIR; sys.path.insert(0,str(MYO/'src'))
from myosim.core.config import load_config
from myosim.experiments.task_runner import PickPlaceExperimentRunner
from myosim.signals.replay import CsvIntentReplay
P6=_REPO/'p6'/'c_mi_r04_primary'
BASE=load_config(P6/'configs/p6_mi_r04_mysim.yaml')
def write(events,path):
    with open(path,'w',newline='') as f:
        w=csv.writer(f); w.writerow(['timestamp_s','label','confidence','source_subject','modality','model_version','window_id'])
        for i,(t,l,c) in enumerate(events): w.writerow([f'{t:.3f}',l,f'{c:.3f}','probe','eeg-replay','probe',f'{i:04d}'])
def run(events,cfg=BASE):
    p=tempfile.mktemp(suffix='.csv'); write(events,p); log=[]
    def on_step(b,e,c,ts): log.append((round(e.timestamp_s,3),str(e.intent_id).upper(),str(c.state_output.state.value),str(c.state_output.request.command.value),str(ts.state.value)))
    r=PickPlaceExperimentRunner(cfg,MYO).run(CsvIntentReplay(p),on_step=on_step).to_dict(); os.remove(p)
    return r,log
def episode(dt=0.1,nw=5,nc=10,ng=10,nt=40,decoy='OPEN',grasp='CLOSE',cd=1.0,cg=1.0,t0=0.0):
    ev=[];t=t0
    def add(lab,n,c):
        nonlocal t
        for _ in range(n): ev.append((t,lab,c)); t+=dt
    add('REST',nw,0.99); add(decoy,nc,cd); add('REST',ng,0.99); add(grasp,nc,cg); add('REST',nt,0.99)
    return ev
if __name__=='__main__':
    for dt in (0.1,0.05,0.2):
        r,log=run(episode(dt=dt,nw=int(0.5/dt),nc=int(1.0/dt),ng=int(1.0/dt),nt=int(5.0/dt)))
        tm=r['task_metrics']; print('dt',dt,'success',tm['success'],'state',tm['final_state'],'t_complete',tm['completion_time_s'],'transitions',[(t['timestamp_s'],t['reason']) for t in r['task_transitions']],'err',round(tm['final_error_m'],4))
