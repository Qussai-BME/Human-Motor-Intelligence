import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _C2=_HERE.parent; _REPO=_C2.parents[1]; _OUT=_HERE/'outputs'
sys.path.insert(0,str(_REPO/'p6'/'c1_audit'/'scripts'))
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
RAW=_P(os.environ.get('C2_RAW',str(_C2)))
os.chdir(_OUT)
import pandas as pd, numpy as np, json
R=str(_C2)+'/'
Rr=pd.read_csv(R+'results/real_episodes.csv'); Rr['dc']=Rr.decoy_confidence.round(3); Rr['gc']=Rr.grasp_confidence.round(3)
rng=np.random.default_rng(20261008); rows=[]
for (arm,dec,var),d in Rr.groupby(['arm','decoder','variant']):
    subs=d.subject.values if arm!='R0' else d.subject.values; us=np.unique(subs); idx={s:np.where(subs==s)[0] for s in us}
    for thr in (0.55,0.60,0.65,0.70,0.75,0.85):
        Gc=((d.grasp_label=='CLOSE')&(d.gc>=thr-1e-12)).values; Fc=((d.decoy_label=='CLOSE')&(d.dc>=thr-1e-12)).values
        obs=Gc&~Fc
        # pooled outputs of both trial slots
        a_pool=np.r_[((d.decoy_label=='CLOSE')&(d.dc>=thr-1e-12)).values,Gc].mean(); null=a_pool*(1-a_pool)
        # selective accuracy: P(correct | pass) pooled
        passd=np.r_[(d.dc>=thr-1e-12).values,(d.gc>=thr-1e-12).values]; corr=np.r_[(d.decoy_label=='OPEN').values,(d.grasp_label=='CLOSE').values]
        sel=corr[passd].mean() if passd.sum()>0 else np.nan
        bs=[]
        for _ in range(1000):
            ch=rng.choice(us,len(us)); ii=np.concatenate([idx[s] for s in ch])
            gc=Gc[ii];fc=Fc[ii]; ap=np.r_[fc,gc].mean(); bs.append((gc&~fc).mean()-ap*(1-ap))
        rows.append(dict(arm=arm,decoder=dec,variant=var,thr=thr,observed=float(obs.mean()),chance_matched_floor=float(null),excess=float(obs.mean()-null),excess_ci=[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))],selective_accuracy=float(sel),pass_share=float(passd.mean()),n_pass=int(passd.sum())))
df=pd.DataFrame(rows); df.to_csv('excess_over_chance_floor.csv',index=False)
pd.set_option('display.width',200)
print(df[(df.arm=='R1')&(df.thr.isin([0.55,0.75]))][['decoder','variant','thr','observed','chance_matched_floor','excess','excess_ci','selective_accuracy','pass_share']].round(3).to_string(index=False))
print(df[df.arm=='R0'][df.thr==0.75][['decoder','observed','chance_matched_floor','excess','excess_ci','pass_share']].round(3).to_string(index=False))
