import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _C2=_HERE.parent; _REPO=_C2.parents[1]; _OUT=_HERE/'outputs'
sys.path.insert(0,str(_REPO/'p6'/'c1_audit'/'scripts'))
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
RAW=_P(os.environ.get('C2_RAW',str(_C2)))
os.chdir(_OUT)
import pandas as pd, numpy as np, json, itertools
from scipy import stats
R=str(_C2)+'/'
E=pd.read_csv(R+'results/emulator_episodes.csv'); Rr=pd.read_csv(R+'results/real_episodes.csv'); S=pd.read_csv(R+'results/sensitivity_episodes.csv'); A=json.load(open(R+'results/ANALYSIS.json'))
def cp(k,n,a=0.05):
    lo=0.0 if k==0 else stats.beta.ppf(a/2,k,n-k+1); hi=1.0 if k==n else stats.beta.ppf(1-a/2,k+1,n-k); return float(lo),float(hi)
O={}
# ---- emulator cells
cells=[]
for (reg,q,rho),d in E.groupby(['regime','q','rho']):
    row=dict(regime=reg,q=q,rho=rho,n=len(d))
    for m in ['cue_correct_success','task_completion','false_grasp','miss']:
        k=int(d[m].sum()); row[m]=k/len(d); row[m+'_ci']=cp(k,len(d))
    cells.append(row)
O['cells']=cells
# analytic vs MC (rho=1)
an=json.load(open('c2_analytic_hold.json')); z=[]
for r in an:
    d=E[(E.regime==r['cal'])&(E.q==r['q'])&(E.rho==1.0)]; p=r['cue_correct']; n=len(d); se=np.sqrt(max(p*(1-p),1e-9)/n)
    z.append(dict(regime=r['cal'],q=r['q'],analytic=p,mc=float(d.cue_correct_success.mean()),z=float((d.cue_correct_success.mean()-p)/se) if 0<p<1 else 0.0))
O['analytic_check']=z; O['analytic_max_abs_z']=float(max(abs(x['z']) for x in z))
# ---- exact episode-level decomposition for real arms
Rr['dc']=Rr.decoy_confidence.round(3); Rr['gc']=Rr.grasp_confidence.round(3)
def decomp(d,thr):
    G=((d.grasp_label=='CLOSE')&(d.gc>=thr-1e-12)); F=((d.decoy_label=='CLOSE')&(d.dc>=thr-1e-12)); succ=G&~F
    return G,F,succ
sweep=[]; rng=np.random.default_rng(20261008)
for (arm,dec,var),d in Rr.groupby(['arm','decoder','variant']):
    subs=d.subject.values; us=np.unique(subs); idx={s:np.where(subs==s)[0] for s in us}
    for thr in (0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85):
        G,F,S_=decomp(d,thr); k=int(S_.sum())
        bs=[]
        for _ in range(1000):
            ch=rng.choice(us,len(us)); ii=np.concatenate([idx[s] for s in ch]); bs.append(S_.values[ii].mean())
        sweep.append(dict(arm=arm,decoder=dec,variant=var,thr=thr,n=len(d),success=k/len(d),ci_cluster=[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))],
                          p_grasp=float(G.mean()),p_false=float(F.mean()),both=float((G&F).mean()),miss=float(1-G.mean())))
O['threshold_sweep']=sweep
# registered threshold 0.75 consistency with recorded
chk=[]
for (arm,dec,var),d in Rr.groupby(['arm','decoder','variant']):
    G,F,S_=decomp(d,0.75); chk.append(dict(arm=arm,decoder=dec,variant=var,lookup=int(S_.sum()),recorded=int(d.cue_correct_success.sum()),n=len(d)))
O['lookup_vs_recorded']=chk
# ---- mechanism across real variants
q=A['R1']['quality']; rows=[]
for k,v in q.items():
    dec,var=(k.split('_')+['raw'])[:2] if '_' in k else (k,'raw')
    rows.append(dict(key=k,ba=v['balanced_accuracy'],ece=v['ece'],share=v['share_conf_ge_0.75']))
qd=pd.DataFrame(rows)
succ={}
for (arm,dec,var),d in Rr[Rr.arm=='R1'].groupby(['arm','decoder','variant']): succ[f'{dec}' if (var=='raw' and dec in('D1','D2','D3','D4')) else f'{dec}_{var}']=float(d.cue_correct_success.mean())
qd['succ']=qd.key.map(succ); qd=qd.dropna()
O['mechanism_table']=qd.to_dict('records')
O['spearman_ba_succ']=[float(x) for x in stats.spearmanr(qd.ba,qd.succ)]; O['spearman_share_succ']=[float(x) for x in stats.spearmanr(qd.share,qd.succ)]
raw=qd[qd.key.isin(['D1','D2','D3','D4','D5_raw'])]; O['spearman_raw_ba']=[float(x) for x in stats.spearmanr(raw.ba,raw.succ)]; O['spearman_raw_share']=[float(x) for x in stats.spearmanr(raw.share,raw.succ)]
# ---- R0
r0=[]
for dec,d in Rr[Rr.arm=='R0'].groupby('decoder'):
    G,F,S_=decomp(d,0.75); k=int(d.cue_correct_success.sum()); r0.append(dict(decoder=dec,n=len(d),k=k,rate=k/len(d),ci=cp(k,len(d)),p_grasp=float(G.mean()),p_false=float(F.mean()),pass_share=float(np.r_[d.dc.values,d.gc.values].__ge__(0.75).mean())))
O['R0']=r0
# ---- sensitivity summary
O['sens_cols']=S.columns.tolist()
json.dump(O,open('final_numbers.json','w'),indent=1,default=float)
sw=pd.DataFrame(sweep); sw=sw[sw.arm=='R1']
print(sw[(sw.thr.isin([0.55,0.6,0.65,0.7,0.75]))&(sw.variant.isin(['raw','plt']))].pivot_table(index=['decoder','variant'],columns='thr',values='success').round(3).to_string())
print('analytic max |z|',O['analytic_max_abs_z']); print(O['spearman_ba_succ'],O['spearman_share_succ'],O['spearman_raw_ba'],O['spearman_raw_share'])
print(O['R0']); print([ (c['decoder'],c['variant'],c['lookup'],c['recorded']) for c in chk if c['arm']=='R1'])
print(S.head(2).to_string())
