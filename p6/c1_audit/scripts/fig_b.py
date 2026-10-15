import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _REPO=_HERE.parents[2]; _OUT=_HERE.parent/'outputs'
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
os.chdir(_OUT)
import json, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from scipy import stats
from figstyle import *
O=json.load(open('numbers.json')); T=pd.read_pickle('T.pkl'); L=pd.read_pickle('L.pkl'); dd=pd.read_pickle('dd.pkl')
R=json.load(open('diag_runs.json')); R=pd.DataFrame(R)
ROOT=str(_REPO/'p6'/'c_mi_r04_primary')
def cp(k,n,a=0.05):
    lo=0.0 if k==0 else stats.beta.ppf(a/2,k,n-k+1); hi=1.0 if k==n else stats.beta.ppf(1-a/2,k+1,n-k); return lo,hi
MS=['M1','M2','M3']

# ===== Fig 4 confidence & calibration
fig=plt.figure(figsize=(7.3,2.75)); gs=fig.add_gridspec(1,3,width_ratios=[1.25,1,1.05],wspace=0.42)
ax=fig.add_subplot(gs[0]); panel(ax,'A')
bins=np.linspace(0.5,1.0,26)
for m in MS:
    c=T[T.model_id==m].confidence.values; h,_=np.histogram(c,bins=bins,density=False)
    ax.step(bins[:-1],h/len(c)*100,where='post',color=C[m],lw=1.5,label=m)
ax.axvline(0.75,color=C['thr'],ls='--',lw=1); ax.text(0.742,17.4,'controller\nthreshold 0.75',fontsize=6.2,color=C['thr'],va='top',ha='right')
ax.set_xlabel('Decoder confidence'); ax.set_ylabel('Share of events per bin (%)'); ax.set_title('Confidence distributions'); 
ax.set_xlim(0.5,1.0)
for i,m in enumerate(MS):
    ax.text(0.995,14.6-1.5*i,f"{m}: {O['calibration'][m]['frac_ge_075']*100:.0f}% of events ≥ 0.75",color=C[m],fontsize=6.3,va='top',ha='right',fontweight='bold')
ax=fig.add_subplot(gs[1]); panel(ax,'B')
ax.plot([0.5,1],[0.5,1],color=C['grey'],ls=':',lw=1)
for m in MS:
    rel=np.array(O['calibration'][m]['rel']); ax.plot(rel[:,0],rel[:,1],color=C[m],lw=1.2,alpha=0.8); ax.scatter(rel[:,0],rel[:,1],s=rel[:,2]*0.8+8,color=C[m],alpha=0.85,lw=0)
ax.set_xlim(0.5,1.0); ax.set_ylim(0.2,1.02); ax.set_xlabel('Mean confidence (bin)'); ax.set_ylabel('Observed accuracy'); ax.set_title('Reliability')
for i,m in enumerate(MS): ax.text(0.505,0.27-0.0*i+ -0.0,'',fontsize=6)
ax.text(0.52,0.30,'ECE  M1 0.08 · M2 0.24 · M3 0.27',fontsize=6.3,color=C['ink'])
ax=fig.add_subplot(gs[2]); panel(ax,'C')
w=0.36
for i,m in enumerate(MS):
    d=O['calibration'][m]; n=300; nh=d['n_ge_075']; nl=n-nh; kh=round(d['acc_hi']*nh) if nh else 0; kl=round(d['acc_lo']*nl)
    for j,(k,nn,lab) in enumerate([(kl,nl,'<0.75'),(kh,nh,'≥0.75')]):
        a=k/nn; lo,hi=cp(k,nn); x=i+(j-0.5)*w
        ax.bar(x,a,width=w*0.92,color=C[m],alpha=0.45 if j==0 else 1.0)
        ax.vlines(x,lo,hi,color=C['ink'],lw=0.9); ax.text(x,0.02,f'n={nn}',ha='center',fontsize=5.6,color='white' if True else C['ink'],rotation=90,va='bottom')
ax.axhline(0.5,color=C['thr'],ls='--',lw=1); ax.set_xticks(range(3)); ax.set_xticklabels(MS); ax.set_ylim(0,0.95); ax.set_ylabel('Accuracy')
ax.set_title('Accuracy by confidence gate'); ax.legend(handles=[Rectangle((0,0),1,1,color=C['grey'],alpha=0.45),Rectangle((0,0),1,1,color=C['grey'])],labels=['conf < 0.75','conf ≥ 0.75'],frameon=False,loc='upper right',fontsize=6.2)
fig.savefig('figs/fig4_confidence_calibration.png'); plt.close(fig)

# ===== Fig 5 timeline anatomy (S015)
sub='S015'
trM3=pd.read_csv(f'{ROOT}/traces/M3/M3_{sub}.csv'); gt=pd.read_csv(f'{ROOT}/replay_csv/ground_truth/GROUND_TRUTH_{sub}.csv')
run=R[(R.kind=='decoder')&(R.model=='M3')&(R.subject==sub)].iloc[0]
fig,axs=plt.subplots(4,1,figsize=(7.3,4.9),sharex=True,gridspec_kw=dict(height_ratios=[1.35,1.0,1.15,0.55],hspace=0.28))
t0=trM3.replay_time_s.iloc[0]; tend=float(run.t_end)
def shade(ax):
    ax.axvspan(t0,tend,color='#DCEBF7',alpha=0.9,lw=0); 
def raster(ax,t,lab,conf,title,col):
    shade(ax)
    for ti,l,c in zip(t,lab,conf):
        mk='^' if l=='OPEN' else 'v'; hi=c>=0.75
        ax.vlines(ti,0.5,c,color=col,lw=0.9,alpha=0.6)
        ax.scatter(ti,c,marker=mk,s=34,facecolor=col if hi else 'white',edgecolor=col,lw=1.1,zorder=4)
    ax.axhline(0.75,color=C['thr'],ls='--',lw=0.9); ax.set_ylim(0.5,1.06); ax.set_ylabel('Confidence'); ax.set_title(title,fontsize=7.6)
raster(axs[0],trM3.replay_time_s,trM3.prediction,trM3.confidence,'M3 decoder output, subject S015 (one prediction per trial)',C['M3'])
axs[0].text(tend+1.0,0.96,'task already FAILED →  later events cannot affect the endpoint',fontsize=6.3,color=C['bad'],va='center')
axs[0].legend(handles=[Line2D([],[],marker='^',ls='',color=C['ink'],mfc=C['ink'],ms=5,label='OPEN'),Line2D([],[],marker='v',ls='',color=C['ink'],mfc=C['ink'],ms=5,label='CLOSE'),
   Line2D([],[],marker='o',ls='',color=C['ink'],mfc='white',ms=5,label='hollow = conf < 0.75 (rejected)')],ncol=3,frameon=False,loc='lower center',fontsize=6.2,bbox_to_anchor=(0.5,1.22))
raster(axs[1],gt.timestamp_s,gt.label,gt.confidence,'Oracle stream (true labels, confidence = 1.0)',C['ORACLE'])
# controller state
states=['REST','CANDIDATE','CONFIRMED','EXECUTING','HOLD']; ymap={s:i for i,s in enumerate(states)}
ct=[s.upper() for s in run.ctrl_trace]; yy=[ymap.get(s,0) for s in ct]; ts=trM3.replay_time_s.values
shade(axs[2]); axs[2].step(ts,yy,where='post',color=C['M3'],lw=1.6); axs[2].scatter(ts,yy,color=C['M3'],s=14,zorder=4)
axs[2].set_yticks(range(len(states))); axs[2].set_yticklabels(states,fontsize=6.4); axs[2].set_ylabel('Controller'); axs[2].set_title('Decision-engine state after each event (M3, S015)',fontsize=7.6)
# task band
shade(axs[3]); axs[3].barh(0,tend-t0,left=t0,height=0.6,color=C['blue'],alpha=0.85); axs[3].barh(0,125-tend,left=tend,height=0.6,color=C['bad'],alpha=0.85)
axs[3].text(t0-0.8,0,'APPROACH',color=C['blue'],ha='right',va='center',fontsize=6.0,fontweight='bold'); axs[3].text((tend+125)/2,0,'FAILED (task_timeout at %.1f s) — controller keeps processing'%tend,color='white',ha='center',va='center',fontsize=6.3,fontweight='bold')
axs[3].set_yticks([]); axs[3].set_ylim(-0.5,0.5); axs[3].set_xlabel('Replay time (s)'); axs[3].set_xlim(0,125); axs[3].set_ylabel('Task',rotation=0,labelpad=14)
for a in axs[:3]: a.spines['bottom'].set_visible(False); a.tick_params(axis='x',length=0)
axs[0].text(t0+0.4,1.04,'task window (8.0 s)',fontsize=6.4,color=C['blue'],va='top')
fig.savefig('figs/fig5_timeline.png'); plt.close(fig)

# ===== Fig 6 reachability
fig=plt.figure(figsize=(7.3,2.7)); gs=fig.add_gridspec(1,3,width_ratios=[1,1,1.25],wspace=0.5)
ax=fig.add_subplot(gs[0]); panel(ax,'A')
gaps=[]
for m in MS:
    for s in range(1,21): gaps+=list(np.diff(pd.read_csv(f'{ROOT}/traces/{m}/{m}_S{s:03d}.csv').replay_time_s))
ax.hist(gaps,bins=np.arange(7.9,8.45,0.05),color=C['blue'],alpha=0.85,edgecolor='white',lw=0.4)
ax.axvline(8.0,color=C['thr'],ls='--',lw=1.1); ax.text(7.98,ax.get_ylim()[1]*0.95,'task timeout\n8.0 s',color=C['thr'],fontsize=6.3,ha='right',va='top')
ax.set_xlabel('Inter-event gap (s)'); ax.set_ylabel('Count (840 gaps)'); ax.set_title('Trial cadence vs task clock'); ax.set_xlim(7.7,8.45)
ax=fig.add_subplot(gs[1]); panel(ax,'B')
ax.bar([0],[2],color=C['blue'],width=0.6); ax.bar([1],[4],color=C['grey'],width=0.6)
ax.text(0,2.1,'2',ha='center',fontsize=8,fontweight='bold'); ax.text(1,4.1,'4',ha='center',fontsize=8,fontweight='bold')
ax.set_xticks([0,1]); ax.set_xticklabels(['delivered\nbefore task end\n(60 / 60 runs)','needed to\nrelease one\ncommand'],fontsize=6.4); ax.set_ylim(0,5.2); ax.set_ylabel('Events (windows)'); ax.set_title('Events vs requirement')
ax=fig.add_subplot(gs[2]); panel(ax,'C')
mr=O['max_consecutive_confident_same_label']; order=['M1','M2','M3','ORACLE']; rng=np.random.default_rng(4)
for i,m in enumerate(order):
    v=np.array(mr[m]['values']); ax.scatter(i+rng.uniform(-0.2,0.2,len(v)),v+rng.uniform(-0.12,0.12,len(v)),s=14,color=C[m],alpha=0.8,lw=0)
    ax.hlines(v.mean(),i-0.32,i+0.32,color=C[m],lw=2)
    ax.text(i,6.15,f"{mr[m]['n_ge4']}/20",ha='center',fontsize=6.6,color=C[m],fontweight='bold')
ax.axhline(3.5,color=C['thr'],ls='--',lw=1); ax.text(3.45,3.62,'release needs ≥ 4',fontsize=6.2,color=C['thr'],ha='right',va='bottom')
ax.set_xticks(range(4)); ax.set_xticklabels(['M1','M2','M3','Oracle']); ax.set_ylim(-0.4,6.7); ax.set_ylabel('Longest confident same-label run'); ax.set_title('Per-stream persistence')
fig.savefig('figs/fig6_reachability.png'); plt.close(fig)
print('ok')
