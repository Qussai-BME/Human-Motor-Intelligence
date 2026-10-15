#!/usr/bin/env python3
"""Assemble the per-variant table used in the manuscript (paper_numbers.json) from verified outputs.
Run after final_numbers.py and excess.py. Inputs: results/ANALYSIS.json, results/real_episodes.csv,
outputs/final_numbers.json, outputs/verified_stats.json, outputs/excess_over_chance_floor.csv."""
import os, json
from pathlib import Path
import pandas as pd
from scipy import stats
_HERE=Path(__file__).resolve().parent; _C2=_HERE.parent; _OUT=_HERE/'outputs'
A=json.load(open(_C2/'results'/'ANALYSIS.json')); N=json.load(open(_OUT/'final_numbers.json')); V=json.load(open(_OUT/'verified_stats.json'))
X=pd.read_csv(_OUT/'excess_over_chance_floor.csv'); Rr=pd.read_csv(_C2/'results'/'real_episodes.csv'); env=json.load(open(_C2/'registry'/'ENVIRONMENT.json'))
def cp(k,n,a=0.05):
    lo=0.0 if k==0 else stats.beta.ppf(a/2,k,n-k+1); hi=1.0 if k==n else stats.beta.ppf(1-a/2,k+1,n-k); return float(lo),float(hi)
jl=lambda c: json.loads(c) if isinstance(c,str) else list(c)
Q=A['R1']['quality']; rows=[]; sw=pd.DataFrame(N['threshold_sweep'])
for (dec,var),d in Rr[Rr.arm=='R1'].groupby(['decoder','variant']):
    k=int(d.cue_correct_success.sum()); n=len(d); key=dec if (var=='raw' and dec in('D1','D2','D3','D4')) else f'{dec}_{var}'
    s75=sw[(sw.arm=='R1')&(sw.decoder==dec)&(sw.variant==var)&(sw.thr==0.75)].iloc[0]
    x75=X[(X.arm=='R1')&(X.decoder==dec)&(X.variant==var)&(X.thr==0.75)].iloc[0]; x55=X[(X.arm=='R1')&(X.decoder==dec)&(X.variant==var)&(X.thr==0.55)].iloc[0]
    q=Q[key]
    rows.append(dict(decoder=dec,variant=var,key=key,n=n,k=k,rate=k/n,ci=cp(k,n),ci_cluster=s75.ci_cluster,false_grasp=float(d.false_grasp.mean()),miss=float(d.miss.mean()),task_completion=float(d.task_completion.mean()),
        ba=q['balanced_accuracy'],ba_ci=q['balanced_accuracy_exact95'],ece=q['ece'],share=q['share_conf_ge_0.75'],floor75=float(x75.chance_matched_floor),excess75=float(x75.excess),excess75_ci=jl(x75.excess_ci),
        excess55=float(x55.excess),excess55_ci=jl(x55.excess_ci),succ55=float(sw[(sw.arm=='R1')&(sw.decoder==dec)&(sw.variant==var)&(sw.thr==0.55)].iloc[0].success)))
P={'r1':rows,'N':N,'V':V,'env':env}
P['r0x']=[dict(decoder=r.decoder,observed=r.observed,floor=r.chance_matched_floor,excess=r.excess,ci=jl(r.excess_ci),pass_share=r.pass_share) for _,r in X[(X.arm=='R0')&(X.thr==0.75)].iterrows()]
P['task_completion_flat']=None
json.dump(P,open(_OUT/'paper_numbers.json','w'),indent=1,default=float)
print('paper_numbers.json written')
