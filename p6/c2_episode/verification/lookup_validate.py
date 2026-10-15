import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _C2=_HERE.parent; _REPO=_C2.parents[1]; _OUT=_HERE/'outputs'
sys.path.insert(0,str(_REPO/'p6'/'c1_audit'/'scripts'))
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
RAW=_P(os.environ.get('C2_RAW',str(_C2)))
import sys, yaml, random, pandas as pd, numpy as np, json
from verify_c2 import run_csv, BASE, MYO
from myosim.core.config import load_config
from pathlib import Path
R=_C2; RR=RAW
E=pd.read_csv(R/'results/emulator_episodes.csv'); Rr=pd.read_csv(R/'results/real_episodes.csv')
def lk(dl,dp,gl,gp): return (gl=='CLOSE' and gp) and not (dl=='CLOSE' and dp)
# (1) hold lookup vs recorded, thr 0.75
Eh=E[E.rho==1.0]; pred=[lk(r.decoy_label,r.decoy_pass,r.grasp_label,r.grasp_pass) for r in Eh.itertuples()]
print('E rho=1 lookup agreement',np.mean(np.array(pred)==Eh.cue_correct_success.values),len(Eh))
for arm in ('R0','R1'):
    d=Rr[Rr.arm==arm]; p=[lk(r.decoy_label,r.decoy_confidence>=0.75,r.grasp_label,r.grasp_confidence>=0.75) for r in d.itertuples()]
    print(arm,'lookup agreement',np.mean(np.array(p)==d.cue_correct_success.values),len(d))
# (2) threshold validation: run MyoSim at other thresholds on real R1 episodes
random.seed(11); d=Rr[(Rr.arm=='R1')&(Rr.decoder.isin(['D3','D4','D5']))]
res={}
for thr in (0.55,0.60,0.70):
    c=yaml.safe_load(open(R/'config'/'p6_c2_mysim.yaml')); c['control']['confidence_threshold']=thr; tmp=f'/tmp/thr_{thr}.yaml'; yaml.safe_dump(c,open(tmp,'w')); cfg=load_config(tmp)
    ids=random.sample(list(d.episode_id),100); bad=0
    for i in ids:
        row=d[d.episode_id==i].iloc[0]; out=run_csv(RR/'replay_csv'/'R1'/f'{i}.csv',cfg)
        exp=lk(row.decoy_label,row.decoy_confidence>=thr,row.grasp_label,row.grasp_confidence>=thr)
        if bool(out['cue'])!=bool(exp): bad+=1
    res[thr]=bad; print('threshold',thr,'MyoSim vs lookup mismatches',bad,'/100',flush=True)
json.dump(res,open('lookup_threshold_validation.json','w'))
