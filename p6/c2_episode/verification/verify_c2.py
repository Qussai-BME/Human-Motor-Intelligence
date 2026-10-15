import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _C2=_HERE.parent; _REPO=_C2.parents[1]; _OUT=_HERE/'outputs'
sys.path.insert(0,str(_REPO/'p6'/'c1_audit'/'scripts'))
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
RAW=_P(os.environ.get('C2_RAW',str(_C2)))
import sys, random, pandas as pd, numpy as np, csv
from pathlib import Path
from probe import *
R=_C2; RR=RAW
def run_csv(path,cfg=BASE):
    log=[]
    def on_step(b,e,c,ts): log.append((round(e.timestamp_s,3),str(e.intent_id).upper(),str(c.state_output.state.value),str(c.state_output.request.command.value),str(ts.state.value)))
    r=PickPlaceExperimentRunner(cfg,MYO).run(CsvIntentReplay(path),on_step=on_step).to_dict()
    tm=r['task_metrics']; trans=[(x['timestamp_s'],x['reason']) for x in r['task_transitions']]
    onset=[t for t,rs in trans if rs=='decoded_grasp_command']; onset=onset[0] if onset else None
    fa=any((2.0<=t<4.0) and st=='EXECUTING' and cmd=='CLOSE' for t,l,st,cmd,ts in log)
    comp=tm['final_state']=='COMPLETE'; ok=onset is not None and 4.0<=onset<=5.5
    return dict(task_completion=comp,false_grasp=fa,cue=bool(comp and ok and not fa),onset=onset)
if __name__=='__main__':
    random.seed(7)
    E=pd.read_csv(R/'results/emulator_episodes.csv').set_index('episode_id'); Rl=pd.read_csv(R/'results/real_episodes.csv').set_index('episode_id')
    samp=[('E',i) for i in random.sample(list(E.index),150)]+[('R',i) for i in random.sample([i for i in Rl.index if i.startswith('R1')],120)]+[('R',i) for i in random.sample([i for i in Rl.index if i.startswith('R0')],30)]
    bad=0; n=0
    for kind,i in samp:
        df=E if kind=='E' else Rl; row=df.loc[i]
        arm='E' if kind=='E' else ('R0' if i.startswith('R0') else 'R1')
        p=RR/'replay_csv'/arm/f'{i}.csv'
        out=run_csv(p); n+=1
        exp=dict(task_completion=bool(row.task_completion),false_grasp=bool(row.false_grasp),cue=bool(row.cue_correct_success))
        got=dict(task_completion=out['task_completion'],false_grasp=out['false_grasp'],cue=out['cue'])
        if exp!=got: bad+=1; print('MISMATCH',i,exp,got)
    print('re-run',n,'episodes; mismatches',bad)
