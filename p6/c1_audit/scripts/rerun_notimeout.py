import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _REPO=_HERE.parents[2]; _OUT=_HERE.parent/'outputs'
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
import sys, json, csv, glob, os, time
from pathlib import Path
import numpy as np
MYO=MYOSIM_DIR; sys.path.insert(0,str(MYO/'src'))
from myosim.core.config import load_config
from myosim.experiments.task_runner import PickPlaceExperimentRunner
from myosim.signals.replay import CsvIntentReplay
P6=_REPO/'p6'/'c_mi_r04_primary'
import yaml
_c=yaml.safe_load((P6/'configs/p6_mi_r04_mysim.yaml').read_text()); _c['task']['timeout_s']=1000.0
(_OUT/'cfg_no_timeout.yaml').write_text(yaml.safe_dump(_c)); cfg=load_config(_OUT/'cfg_no_timeout.yaml')
def run(csvp):
    log=[]
    def on_step(backend, event, control, task_step):
        log.append(dict(t=event.timestamp_s, label=str(event.intent_id).upper(), conf=float(event.confidence),
                        cmd=str(control.state_output.request.command.value), ctrl_state=str(control.state_output.state.value),
                        task_state=str(task_step.state.value)))
    res=PickPlaceExperimentRunner(cfg,MYO).run(CsvIntentReplay(csvp), on_step=on_step).to_dict()
    return res, log
out=[]
t0=time.time()
jobs=[]
for m in ['M1','M2','M3']:
    for s in range(1,21): jobs.append(('decoder',m,f'S{s:03d}',P6/f'replay_csv/decoder/{m}_S{s:03d}.csv'))
for s in range(1,21): jobs.append(('oracle','ORACLE',f'S{s:03d}',P6/f'replay_csv/ground_truth/GROUND_TRUTH_S{s:03d}.csv'))
for kind,m,s,p in jobs:
    res,log=run(p)
    tm=res['task_metrics']; cm=res['control_metrics']
    t_end=res['task_transitions'][-1]['timestamp_s'] if res['task_transitions'] else None
    # corrections counted only on events up to task termination
    prev=None; corr_pre=0
    for e in log:
        if prev is not None and e['cmd']!=prev and (t_end is None or e['t']<=t_end): corr_pre+=1
        prev=e['cmd']
    n_in=sum(1 for e in log if t_end is None or e['t']<=t_end)
    out.append(dict(kind=kind,model=m,subject=s,success=tm['success'],final_state=tm['final_state'],path=tm['path_length_m'],
        final_error=tm['final_error_m'],corr=tm['command_corrections'],corr_pre_termination=corr_pre,n_events_in_task_window=n_in,
        n_events=len(log),t_end=t_end,released=cm['released_command_count'],ctrl_trans=cm['state_transition_count'],
        task_reasons=[t['reason'] for t in res['task_transitions']],
        task_state_trace=[e['task_state'] for e in log], cmd_trace=[e['cmd'] for e in log], ctrl_trace=[e['ctrl_state'] for e in log]))
json.dump(out,open(_OUT/'diag_runs_notimeout.json','w'))
print('done',len(out),'runs in',round(time.time()-t0,1),'s')
