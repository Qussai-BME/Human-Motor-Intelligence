import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _REPO=_HERE.parents[2]; _OUT=_HERE.parent/'outputs'
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
os.chdir(_OUT)
import json, glob, os, itertools
import numpy as np, pandas as pd
from scipy import stats
ROOT=str(_REPO/'p6'/'c_mi_r04_primary')
OUT={}
# ---------- decoder level
L=pd.DataFrame(json.load(open(f'{ROOT}/results/LOSO_RESULTS.json')))
tr=[]
for m in ['M1','M2','M3']:
    for s in range(1,21):
        t=pd.read_csv(f'{ROOT}/traces/{m}/{m}_S{s:03d}.csv'); tr.append(t)
T=pd.concat(tr,ignore_index=True)
T['correct']=T['correct'].astype(bool)
def cp(k,n,a=0.05):
    lo=0.0 if k==0 else stats.beta.ppf(a/2,k,n-k+1)
    hi=1.0 if k==n else stats.beta.ppf(1-a/2,k+1,n-k)
    return lo,hi
dec={}
for m in ['M1','M2','M3']:
    d=L[L.model_id==m]; t=T[T.model_id==m]
    k=int(t.correct.sum()); n=len(t); lo,hi=cp(k,n)
    bp=stats.binomtest(k,n,0.5,alternative='two-sided').pvalue
    ba=d.heldout_balanced_accuracy.values
    rng=np.random.default_rng(1701); bs=[ba[rng.integers(0,20,20)].mean() for _ in range(10000)]
    w=stats.wilcoxon(ba-0.5) if np.any(ba!=0.5) else None
    dec[m]=dict(pooled_acc=k/n,k=k,n=n,cp_lo=lo,cp_hi=hi,binom_p=bp,mean_ba=float(ba.mean()),median_ba=float(np.median(ba)),
        ba_ci=[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))],wilcoxon_vs_chance_p=float(w.pvalue),
        src_cv_mean=float(d.source_cv_balanced_accuracy.mean()),src_cv_sd=float(d.source_cv_balanced_accuracy.std()),
        logloss_mean=float(d.heldout_log_loss.mean()),acc_mean_subject=float(d.heldout_accuracy.mean()),
        n_subj_above_chance_thr=int((d.heldout_accuracy>=11/15).sum()),n_subj_below_half=int((d.heldout_accuracy<0.5).sum()),n_ge12=int((d.heldout_accuracy*15>=11.999).sum()),min_acc=float(d.heldout_accuracy.min()),max_acc=float(d.heldout_accuracy.max()))
OUT['decoder']=dec
piv=L.pivot(index='test_subject',columns='model_id',values='heldout_balanced_accuracy')
fr=stats.friedmanchisquare(piv.M1,piv.M2,piv.M3); n=20;k=3
OUT['friedman_heldout_ba']=dict(chi2=float(fr.statistic),p=float(fr.pvalue),kendall_W=float(fr.statistic/(n*(k-1))))
pw={}
ps=[]
for a,b in [('M1','M2'),('M1','M3'),('M2','M3')]:
    w=stats.wilcoxon(piv[a]-piv[b]); dz=(piv[a]-piv[b]).mean()/(piv[a]-piv[b]).std(ddof=1)
    pw[f'{a}-{b}']=dict(mean_diff=float((piv[a]-piv[b]).mean()),p=float(w.pvalue),dz=float(dz)); ps.append(w.pvalue)
# Holm
order=np.argsort(ps); holm=[None]*3; prev=0
for r,i in enumerate(order):
    adj=min(1,(3-r)*ps[i]); adj=max(adj,prev); prev=adj; holm[i]=adj
for (key,v),h in zip(pw.items(),holm): v['p_holm']=float(h)
OUT['pairwise_heldout_ba']=pw
# manipulation check: frozen ordering vs held-out ordering
OUT['frozen_order']={'M1':0.5051787825,'M2':0.4652740839,'M3':0.4656065307,'gap_M3_minus_M2':0.4656065307-0.4652740839}
# binomial thresholds
OUT['chance_thresholds']=dict(n15_alpha05_k=int(min(k for k in range(16) if 1-stats.binom.cdf(k-1,15,0.5)<=0.05)),
    n300_thr=float(stats.binom.ppf(0.95,300,0.5)/300))
# ---------- confidence / calibration
cal={}
for m in ['M1','M2','M3']:
    t=T[T.model_id==m]; c=t.confidence.values; y=t.correct.values.astype(float)
    bins=np.linspace(0.5,1.0,6); idx=np.digitize(c,bins)-1; ece=0; rel=[]
    for b in range(5):
        mk=idx==b
        if mk.sum()>0:
            ece+=mk.mean()*abs(y[mk].mean()-c[mk].mean()); rel.append((float(c[mk].mean()),float(y[mk].mean()),int(mk.sum())))
    hi=c>=0.75
    cal[m]=dict(frac_ge_075=float(hi.mean()),n_ge_075=int(hi.sum()),acc_hi=float(y[hi].mean()) if hi.sum() else None,acc_lo=float(y[~hi].mean()),
        mean_conf=float(c.mean()),acc=float(y.mean()),ece=float(ece),rel=rel,
        frac_pred_close=float((t.prediction=='CLOSE').mean()),frac_true_close=float((t.ground_truth=='CLOSE').mean()))
OUT['calibration']=cal
# ---------- timing & reachability
gaps=[];maxrun={}
def maxrun_of(labels,conf,thr=0.75):
    best=cur=0;prev=None
    for l,c in zip(labels,conf):
        if c>=thr:
            cur = cur+1 if l==prev else 1; prev=l
        else: cur=0; prev=None
        best=max(best,cur)
    return best
for m in ['M1','M2','M3']:
    mr=[]
    for s in range(1,21):
        t=pd.read_csv(f'{ROOT}/traces/{m}/{m}_S{s:03d}.csv'); mr.append(maxrun_of(t.prediction,t.confidence)); gaps+=list(np.diff(t.replay_time_s))
    maxrun[m]=mr
mr=[]
for s in range(1,21):
    g=pd.read_csv(f'{ROOT}/replay_csv/ground_truth/GROUND_TRUTH_S{s:03d}.csv'); mr.append(maxrun_of(g.label,g.confidence))
maxrun['ORACLE']=mr
OUT['max_consecutive_confident_same_label']={k:dict(values=v,mean=float(np.mean(v)),n_ge4=int(sum(x>=4 for x in v))) for k,v in maxrun.items()}
gaps=np.array(gaps)
OUT['inter_event_gap_s']=dict(mean=float(gaps.mean()),sd=float(gaps.std()),min=float(gaps.min()),max=float(gaps.max()),frac_gt_8=float((gaps>8.0).mean()))
# ---------- downstream: registered replay + diagnostics
D=pd.DataFrame(json.load(open(_OUT/'diag_runs.json')))
S1=pd.DataFrame(json.load(open(_OUT/'diag_runs_notimeout.json')))
arch=pd.DataFrame(json.load(open(f'{ROOT}/results/myosim/DECODER_RESULTS.json'))); arch['key']=arch.source.str.extract(r'(M\d_S\d+)')
dd=D[D.kind=='decoder'].copy(); dd['key']=dd.model+'_'+dd.subject
mm=dd.merge(arch,on='key')
OUT['reexecution']=dict(n=len(mm),success_equal=bool((mm.success==mm.task_success).all()),
    path_max_abs_diff=float(np.abs(mm['path']-mm.path_length_m).max()),final_err_max_abs_diff=float(np.abs(mm.final_error-mm.final_error_m).max()),
    corr_equal=bool((mm['corr'].values==mm.command_corrections.values).all()),final_state_equal=bool((mm.final_state_x==mm.final_state_y).all()) if 'final_state_x' in mm else None)
# rerun archive compare
rer=json.load(open(_REPO/'p6'/'c_mi_r04_rerun'/'results'/'myosim'/'DECODER_RESULTS.json'))
rer=pd.DataFrame(rer); rer['key']=rer.source.str.extract(r'(M\d_S\d+)'); m2=arch.merge(rer,on='key',suffixes=('_p','_r'))
OUT['primary_vs_rerun_archive']=dict(n=len(m2),final_err_equal=bool(np.allclose(m2.final_error_m_p,m2.final_error_m_r,atol=0,rtol=0)),
    corr_equal=bool((m2.command_corrections_p==m2.command_corrections_r).all()),success_equal=bool((m2.task_success_p==m2.task_success_r).all()))
def summ(df):
    out={}
    for key,g in df.groupby('model'):
        k=int(g.success.sum()); n=len(g); lo,hi=cp(k,n)
        out[key]=dict(k=k,n=n,cp_lo=lo,cp_hi=hi,released=int(g.released.sum()),corr_total=int(g['corr'].sum()),corr_pre=int(g.corr_pre_termination.sum()),
                      events_in_window=float(g.n_events_in_task_window.mean()),states=g.final_state.value_counts().to_dict())
    return out
OUT['registered_replay']=summ(D)
OUT['S1_no_timeout']=summ(S1)
k=int(dd.success.sum()); OUT['pooled_decoder_0_of_60']=dict(k=k,n=60,cp=cp(k,60))
OUT['oracle_0_of_20']=dict(cp=cp(0,20))
# continuous endpoint structure
dd2=dd.copy(); dd2['t_first']=dd2.apply(lambda r: pd.read_csv(f'{ROOT}/traces/{r.model}/{r.model}_{r.subject}.csv').replay_time_s.iloc[0],axis=1)
grp=dd2.groupby('t_first').agg(n=('final_error','size'),fe_min=('final_error','min'),fe_max=('final_error','max'),pl_min=('path','min'),pl_max=('path','max'))
OUT['endpoint_by_first_event']=grp.reset_index().to_dict('records')
# variance decomposition: share of final_error variance explained by t_first vs model
import itertools
def eta2(df,col,fac):
    gm=df[col].mean(); ssb=sum(len(g)*(g[col].mean()-gm)**2 for _,g in df.groupby(fac)); sst=((df[col]-gm)**2).sum(); return float(ssb/sst) if sst>0 else None
OUT['eta2_final_error']=dict(first_event=eta2(dd2,'final_error','t_first'),model=eta2(dd2,'final_error','model'))
OUT['eta2_path']=dict(first_event=eta2(dd2,'path','t_first'),model=eta2(dd2,'path','model'))
# corrections vs n confident events
cc=[]
for _,r in dd.iterrows():
    t=pd.read_csv(f'{ROOT}/traces/{r.model}/{r.model}_{r.subject}.csv'); cc.append(int((t.confidence>=0.75).sum()))
dd['n_conf_hi']=cc
rho=stats.spearmanr(dd.n_conf_hi,dd['corr']); OUT['corr_vs_confident_events']=dict(rho=float(rho.statistic),p=float(rho.pvalue))
# accuracy-> corrections (subject-level heldout ba vs corrections)
dd=dd.merge(L[['model_id','test_subject','heldout_balanced_accuracy']].rename(columns={'model_id':'model','test_subject':'subject'}),on=['model','subject'])
rho2=stats.spearmanr(dd.heldout_balanced_accuracy,dd['corr']); OUT['corr_vs_heldout_ba']=dict(rho=float(rho2.statistic),p=float(rho2.pvalue))
# Friedman on corrections reproduced
pc=dd.pivot(index='subject',columns='model',values='corr'); f=stats.friedmanchisquare(pc.M1,pc.M2,pc.M3); OUT['friedman_corr_reproduced']=dict(chi2=float(f.statistic),p=float(f.pvalue))
json.dump(OUT,open(_OUT/'numbers.json','w'),indent=1,default=float)
dd.to_pickle(_OUT/'dd.pkl'); T.to_pickle(_OUT/'T.pkl'); L.to_pickle(_OUT/'L.pkl')
print(json.dumps({k:OUT[k] for k in ['decoder','friedman_heldout_ba','pairwise_heldout_ba','chance_thresholds','max_consecutive_confident_same_label','inter_event_gap_s','reexecution','primary_vs_rerun_archive','pooled_decoder_0_of_60','eta2_final_error','eta2_path','corr_vs_confident_events','corr_vs_heldout_ba','friedman_corr_reproduced']},indent=1,default=float)[:7000])
