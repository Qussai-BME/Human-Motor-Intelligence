import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _REPO=_HERE.parents[2]; _OUT=_HERE.parent/'outputs'
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
os.chdir(_OUT)
import json, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from scipy import stats
from figstyle import *
O=json.load(open('numbers.json')); L=pd.read_pickle('L.pkl'); T=pd.read_pickle('T.pkl')

# ---------------- Fig 3: decoder performance vs chance
fig=plt.figure(figsize=(7.3,2.9)); gs=fig.add_gridspec(1,3,width_ratios=[1.55,1.0,1.05],wspace=0.42)
ax=fig.add_subplot(gs[0]); panel(ax,'A')
piv=L.pivot(index='test_subject',columns='model_id',values='heldout_balanced_accuracy')
rng=np.random.default_rng(3)
for i,m in enumerate(['M1','M2','M3']):
    v=piv[m].values; x=i+rng.uniform(-0.17,0.17,len(v))
    ax.scatter(x,v,s=13,color=C[m],alpha=0.75,lw=0,zorder=3)
    ax.hlines(v.mean(),i-0.3,i+0.3,color=C[m],lw=2.2,zorder=4)
    bp=stats.bootstrap((v,),np.mean,confidence_level=0.95,random_state=1,n_resamples=5000).confidence_interval
    ax.vlines(i,bp.low,bp.high,color=C['ink'],lw=1.2,zorder=5)
ax.axhspan(0.5-0.2,0.5+0.2,color='#E3E7ED',alpha=0.0)
ax.axhline(0.5,color=C['thr'],ls='--',lw=1); ax.text(-0.46,0.512,'chance',color=C['thr'],fontsize=6.8,ha='left',va='bottom')
ax.set_xticks([0,1,2]); ax.set_xticklabels(['M1','M2','M3']); ax.set_ylim(0.15,0.95); ax.set_ylabel('Held-out balanced accuracy (n = 15 / subject)')
ax.set_title('Per-subject LOSO performance')
ax.text(0.02,0.04,'Friedman χ²(2)=0.88, p=0.65, W=0.02',transform=ax.transAxes,fontsize=6.6,color=C['ink'])
ax=fig.add_subplot(gs[1]); panel(ax,'B')
for i,m in enumerate(['M1','M2','M3']):
    d=O['decoder'][m]; ax.errorbar(i,d['pooled_acc'],yerr=[[d['pooled_acc']-d['cp_lo']],[d['cp_hi']-d['pooled_acc']]],fmt='o',color=C[m],ms=5.5,capsize=3,lw=1.4)
    ax.text(i+0.12,d['pooled_acc'],f"{d['pooled_acc']:.3f}",ha='left',va='center',fontsize=6.6,color=C['ink'])
ax.axhline(0.5,color=C['thr'],ls='--',lw=1); ax.axhline(O['chance_thresholds']['n300_thr'],color=C['grey'],ls=':',lw=1)
ax.text(-0.46,0.5495,'p < .05 threshold',fontsize=6,color=C['grey'],ha='left',va='bottom')
ax.set_xticks([0,1,2]); ax.set_xticklabels(['M1','M2','M3']); ax.set_xlim(-0.5,2.85); ax.set_ylim(0.40,0.62); ax.set_ylabel('Pooled accuracy (n = 300)')
ax.set_title('Pooled, exact 95% CI')
ax=fig.add_subplot(gs[2]); panel(ax,'C')
src=[O['decoder'][m]['src_cv_mean'] for m in ['M1','M2','M3']]
for i,m in enumerate(['M1','M2','M3']):
    s=L[L.model_id==m].source_cv_balanced_accuracy.values
    ax.bar(i,src[i],color=C[m],width=0.78,alpha=0.9); ax.errorbar(i,src[i],yerr=1.96*s.std()/np.sqrt(20),color=C['ink'],capsize=3,lw=1)
    ax.text(i,0.4235,f'{src[i]:.3f}',ha='center',va='bottom',fontsize=6.2,color='white',fontweight='bold')
ax.axhline(0.5,color=C['thr'],ls='--',lw=1)
ax.set_ylim(0.42,0.54); ax.set_xticks([0,1,2]); ax.set_xticklabels(['M1','M2','M3']); ax.set_ylabel('Source-CV balanced accuracy (frozen)')
ax.set_title('Basis of the quality freeze')
ax.plot([1,1,2,2],[0.478,0.481,0.481,0.478],color=C['ink'],lw=0.9); ax.text(1.5,0.4825,'M3 − M2 = 0.0003',ha='center',va='bottom',fontsize=6.3)
fig.savefig('figs/fig3_decoder_vs_chance.png'); plt.close(fig)
print('ok')
