import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _REPO=_HERE.parents[2]; _OUT=_HERE.parent/'outputs'
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
os.chdir(_OUT)
import json, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
from scipy import stats
from figstyle import *
O=json.load(open('numbers.json')); dd=pd.read_pickle('dd.pkl'); R=pd.DataFrame(json.load(open('diag_runs.json'))); S1=pd.DataFrame(json.load(open('diag_runs_notimeout.json')))
ROOT=str(_REPO/'p6'/'c_mi_r04_primary')
MS=['M1','M2','M3']; rng=np.random.default_rng(11)
# ===== Fig 7
fig,axs=plt.subplots(2,2,figsize=(7.3,5.0)); plt.subplots_adjust(wspace=0.38,hspace=0.52)
ax=axs[0,0]; panel(ax,'A')
rows=[('M1',O['registered_replay']['M1']),('M2',O['registered_replay']['M2']),('M3',O['registered_replay']['M3']),('ORACLE',O['registered_replay']['ORACLE'])]
for i,(m,d) in enumerate(rows):
    ax.errorbar(0,i,xerr=[[0],[d['cp_hi']*100]],fmt='o',color=C[m],ms=5.5,capsize=3,lw=1.5)
    ax.text(d['cp_hi']*100+0.8,i,f"0/20  (upper 95% bound {d['cp_hi']*100:.1f}%)",va='center',fontsize=6.3)
i=4; ax.errorbar(0,i+0.4,xerr=[[0],[O['pooled_decoder_0_of_60']['cp'][1]*100]],fmt='s',color=C['ink'],ms=5,capsize=3,lw=1.5)
ax.text(O['pooled_decoder_0_of_60']['cp'][1]*100+0.8,i+0.4,f"0/60  (upper bound {O['pooled_decoder_0_of_60']['cp'][1]*100:.1f}%)",va='center',fontsize=6.3)
ax.set_yticks([0,1,2,3,4.4]); ax.set_yticklabels(['M1','M2','M3','Oracle','Decoders\npooled']); ax.invert_yaxis(); ax.set_xlim(-1,42); ax.set_xlabel('Task-success rate (%)'); ax.set_title('Registered primary endpoint')
ax=axs[0,1]; panel(ax,'B')
dd['t_first']=dd.apply(lambda r: pd.read_csv(f'{ROOT}/traces/{r.model}/{r.model}_{r.subject}.csv').replay_time_s.iloc[0],axis=1)
for j,(tf,mk) in enumerate([(4.1,'o'),(4.2,'D')]):
    for i,m in enumerate(MS):
        d=dd[(dd.model==m)&(np.isclose(dd.t_first,tf))]; ax.scatter(i+rng.uniform(-0.22,0.22,len(d)),d.final_error*1000,s=16,marker=mk,color=C[m],alpha=0.8,lw=0)
ax.set_xticks(range(3)); ax.set_xticklabels(MS); ax.set_ylabel('Final error (mm)'); ax.set_title('Final error is set by stream onset')
ax.text(0.30,0.60,'● first event at 4.1 s (n = 51)\n◆ first event at 4.2 s (n = 9)',transform=ax.transAxes,fontsize=6.2,va='top')
ax.text(0.30,0.80,f"η² (onset) = {O['eta2_final_error']['first_event']:.2f}\nη² (model) < 10⁻¹⁶",transform=ax.transAxes,fontsize=6.6,va='top',color=C['thr'])
ax=axs[1,0]; panel(ax,'C')
for j,(tf,mk) in enumerate([(4.1,'o'),(4.2,'D')]):
    for i,m in enumerate(MS):
        d=dd[(dd.model==m)&(np.isclose(dd.t_first,tf))]; ax.scatter(i+rng.uniform(-0.22,0.22,len(d)),d['path']*1000,s=16,marker=mk,color=C[m],alpha=0.8,lw=0)
ax.set_xticks(range(3)); ax.set_xticklabels(MS); ax.set_ylabel('Path length (mm)'); ax.set_title('Path length: same structure')
ax.text(0.02,0.97,f"η² onset = {O['eta2_path']['first_event']:.2f}\nη² model = {O['eta2_path']['model']:.3f}",transform=ax.transAxes,fontsize=6.4,va='top',color=C['thr'])
ax=axs[1,1]; panel(ax,'D')
tot=[O['registered_replay'][m]['corr_total'] for m in MS]; pre=[O['registered_replay'][m]['corr_pre'] for m in MS]
for i,m in enumerate(MS):
    ax.bar(i,pre[i],color=C['blue'],width=0.6); ax.bar(i,tot[i]-pre[i],bottom=pre[i],color=C['bad'],width=0.6,alpha=0.9)
    ax.text(i,tot[i]+1,f"{tot[i]}",ha='center',fontsize=7,fontweight='bold')
ax.set_xticks(range(3)); ax.set_xticklabels(MS); ax.set_ylabel('Corrections (sum, 20 runs)'); ax.set_ylim(0,52)
ax.legend(handles=[Rectangle((0,0),1,1,color=C['blue']),Rectangle((0,0),1,1,color=C['bad'],alpha=0.9)],labels=['before task end (0 in all runs)','after task already FAILED'],frameon=False,loc='upper left',fontsize=6.3)
ax.set_title('Corrections occur after task end')
fig.savefig('figs/fig7_registered_outcome.png'); plt.close(fig)

# ===== Fig 8 what exploratory metric tracks
fig,axs=plt.subplots(1,2,figsize=(7.3,2.8)); plt.subplots_adjust(wspace=0.32)
ax=axs[0]; panel(ax,'A')
for m in MS:
    d=dd[dd.model==m]; ax.scatter(d.n_conf_hi+rng.uniform(-0.18,0.18,len(d)),d['corr']+rng.uniform(-0.12,0.12,len(d)),s=20,color=C[m],alpha=0.8,lw=0,label=m)
ax.set_xlabel('Events with confidence ≥ 0.75 (per run, of 15)'); ax.set_ylabel('Command corrections'); ax.set_title('Tracks confident output')
ax.text(0.97,0.94,f"Spearman ρ = {O['corr_vs_confident_events']['rho']:.2f}\np = {O['corr_vs_confident_events']['p']:.1e} (n = 60)",transform=ax.transAxes,ha='right',va='top',fontsize=6.6)
ax.legend(frameon=False,loc='upper left',fontsize=6.4,bbox_to_anchor=(0.0,0.82))
ax=axs[1]; panel(ax,'B')
for m in MS:
    d=dd[dd.model==m]; ax.scatter(d.heldout_balanced_accuracy,d['corr']+rng.uniform(-0.12,0.12,len(d)),s=20,color=C[m],alpha=0.8,lw=0)
ax.axvline(0.5,color=C['thr'],ls='--',lw=1); ax.set_xlabel('Held-out balanced accuracy'); ax.set_ylabel('Command corrections'); ax.set_title('Does not track accuracy')
ax.text(0.97,0.94,f"Spearman ρ = {O['corr_vs_heldout_ba']['rho']:.2f}\np = {O['corr_vs_heldout_ba']['p']:.2f} (n = 60)",transform=ax.transAxes,ha='right',va='top',fontsize=6.6)
fig.savefig('figs/fig8_metric_tracking.png'); plt.close(fig)

# ===== Fig 9 sensitivity S1
fig,axs=plt.subplots(1,2,figsize=(7.3,2.7),gridspec_kw=dict(width_ratios=[1,1.35],wspace=0.35))
conds=['M1','M2','M3','ORACLE']; labs=['M1','M2','M3','Oracle']
ax=axs[0]; panel(ax,'A')
for i,m in enumerate(conds): ax.barh(i,20,color=C['bad'],alpha=0.85,height=0.62); ax.text(10,i,'FAILED by task timeout: 20 / 20',ha='center',va='center',color='white',fontsize=6.2,fontweight='bold')
ax.set_yticks(range(4)); ax.set_yticklabels(labs); ax.invert_yaxis(); ax.set_xlim(0,20); ax.set_xlabel('Runs (n = 20 per condition)'); ax.set_title('Registered timing (8.0-s task clock)')
ax=axs[1]; panel(ax,'B')
for i,m in enumerate(conds):
    st=O['S1_no_timeout'][m]['states']; a=st.get('WAIT_FOR_GRASP',0); b=st.get('WAIT_FOR_RELEASE',0); c=st.get('COMPLETE',0)
    ax.barh(i,a,color='#B8C1CC',height=0.62); ax.barh(i,b,left=a,color=C['blue'],height=0.62); ax.barh(i,c,left=a+b,color=C['good'],height=0.62)
    ax.text(a/2,i,f'{a}',ha='center',va='center',fontsize=6.4); 
    if b: ax.text(a+b/2,i,f'{b}',ha='center',va='center',fontsize=6.4,color='white',fontweight='bold')
ax.set_yticks(range(4)); ax.set_yticklabels(labs); ax.invert_yaxis(); ax.set_xlim(0,20); ax.set_xticks([0,5,10,15,20]); ax.set_xlabel('Runs (n = 20 per condition)'); ax.set_title('Timeout removed (post-hoc sensitivity S1)')
ax.legend(handles=[Rectangle((0,0),1,1,color='#B8C1CC'),Rectangle((0,0),1,1,color=C['blue']),Rectangle((0,0),1,1,color=C['good'])],labels=['WAIT_FOR_GRASP (no grasp executed)','WAIT_FOR_RELEASE (grasp + transport)','COMPLETE (0 in all)'],frameon=False,loc='upper center',bbox_to_anchor=(0.45,-0.28),ncol=1,fontsize=6.2)
fig.savefig('figs/fig9_sensitivity.png'); plt.close(fig)
print('ok')
