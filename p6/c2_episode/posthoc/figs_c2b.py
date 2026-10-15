import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _C2=_HERE.parent; _REPO=_C2.parents[1]; _OUT=_HERE/'outputs'
sys.path.insert(0,str(_REPO/'p6'/'c1_audit'/'scripts'))
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
RAW=_P(os.environ.get('C2_RAW',str(_C2)))
os.chdir(_OUT)
import sys, json, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from scipy import stats
from figstyle import *
A=json.load(open(_C2/'results'/'ANALYSIS.json')); N=json.load(open('final_numbers.json')); X=pd.read_csv('excess_over_chance_floor.csv')
Q=A['R1']['quality']; S=pd.read_csv(_C2/'results'/'sensitivity_episodes.csv')
DC={'D1':'#1B7F8C','D2':'#D98324','D3':'#7A4FA3','D4':'#8C6D1F','D5':'#2E8B57'}
DL={'D1':'D1 band power','D2':'D2 band-pair','D3':'D3 CSP+LDA','D4':'D4 Riemannian','D5':'D5 within-subject (reference)'}
keys=['D1','D2','D3','D4','D1_plt','D2_plt','D3_plt','D4_plt','D5_raw','D5_plt']
def dec(k): return k.split('_')[0]
# ---------- N4 real decoder quality and calibration
fig=plt.figure(figsize=(7.3,2.9)); gs=fig.add_gridspec(1,3,width_ratios=[1.2,1.0,1.15],wspace=0.5)
ax=fig.add_subplot(gs[0]); panel(ax,'A')
for i,k in enumerate(['D1','D2','D3','D4','D5_raw']):
    v=Q[k]; lo,hi=v['balanced_accuracy_exact95']; ax.errorbar(i,v['balanced_accuracy'],yerr=[[v['balanced_accuracy']-lo],[hi-v['balanced_accuracy']]],fmt='o',color=DC[dec(k)],ms=5,capsize=3,lw=1.4)
    ax.text(i,hi+0.004,f"{v['balanced_accuracy']:.3f}",ha='center',fontsize=6.3)
ax.axhline(0.5,color=C['thr'],ls='--',lw=1); ax.axhline(0.58,color=C['grey'],ls=':',lw=1); ax.text(4.4,0.5815,'V1 criterion 0.58',fontsize=5.8,color=C['grey'],ha='right',va='bottom')
ax.set_xticks(range(5)); ax.set_xticklabels(['D1','D2','D3','D4','D5*'],fontsize=7); ax.set_ylim(0.49,0.67); ax.set_ylabel('Balanced accuracy (exact 95% CI)'); ax.set_title('Held-out quality',fontsize=7.6)
ax.text(0.02,0.02,f"* within-subject, n = {Q['D5_raw']['n']:,} epochs (run R12)\n  others: n = {Q['D1']['n']:,}, subject-grouped CV",transform=ax.transAxes,fontsize=5.4)
ax=fig.add_subplot(gs[1]); panel(ax,'B')
for i,k in enumerate(['D1','D2','D3','D4','D5']):
    r=Q[k if k!='D5' else 'D5_raw']['share_conf_ge_0.75']; p=Q[(k+'_plt')]['share_conf_ge_0.75']
    ax.bar(i-0.19,r*100,width=0.36,color=DC[k]); ax.bar(i+0.19,p*100,width=0.36,color=DC[k],alpha=0.4)
    ax.text(i-0.19,r*100+2,f'{r*100:.0f}' if r>0.05 else f'{r*100:.1f}',ha='center',fontsize=5.8)
ax.set_xticks(range(5)); ax.set_xticklabels(['D1','D2','D3','D4','D5*'],fontsize=7); ax.set_ylabel('Events with confidence ≥ 0.75 (%)'); ax.set_title('Gate-pass share',fontsize=7.6); ax.set_ylim(0,112)
ax.legend(handles=[Rectangle((0,0),1,1,color=C['grey']),Rectangle((0,0),1,1,color=C['grey'],alpha=0.4)],labels=['raw','Platt'],frameon=False,fontsize=6.2,loc='upper left')
ax=fig.add_subplot(gs[2]); panel(ax,'C'); ax.plot([0.5,1],[0.5,1],color=C['grey'],ls=':',lw=1)
for k,ls in [('D3','-'),('D4','-'),('D5_raw','-'),('D3_plt','--')]:
    b=[x for x in Q[k]['reliability_bins'] if x['n']>=15]; ax.plot([x['mean_confidence'] for x in b],[x['accuracy'] for x in b],ls,marker='o',ms=3,color=DC[dec(k)],lw=1.2,label=k.replace('_',' '))
ax.set_xlim(0.5,1.0); ax.set_ylim(0.3,1.02); ax.set_xlabel('Mean confidence (bin, n ≥ 15)'); ax.set_ylabel('Observed accuracy'); ax.set_title('Reliability',fontsize=7.6); ax.legend(frameon=False,fontsize=6.0,loc='lower right')
ax.text(0.505,0.325,f"ECE  D3 {Q['D3']['ece']:.2f} · D4 {Q['D4']['ece']:.2f} · D5 {Q['D5_raw']['ece']:.2f}",fontsize=5.8)
fig.savefig('figs/N4_real_decoder_quality.png'); plt.close(fig)

# ---------- N5 mechanism
M=pd.DataFrame(N['mechanism_table']); 
fig,axs=plt.subplots(1,3,figsize=(7.3,2.85)); plt.subplots_adjust(wspace=0.42)
ax=axs[0]; panel(ax,'A')
for _,r in M.iterrows():
    d=r.key.split('_')[0]; ax.scatter(r.share*100,r.succ*100,s=26,color=DC[d],marker='o' if not r.key.endswith('plt') else 's',zorder=3)
    
    if r.succ>0.05: ax.annotate(r.key.replace('_',' '),(r.share*100,r.succ*100),xytext=(3,3),textcoords='offset points',fontsize=5.6)
ax.set_xlabel('Events passing gate (%)'); ax.set_ylabel('Cue-correct success (%)'); ax.set_title('Gate-pass share',fontsize=7.6)
ax.text(0.04,0.93,f"Spearman ρ = {N['spearman_share_succ'][0]:.2f}\np = {N['spearman_share_succ'][1]:.0e}  (10 variants)",transform=ax.transAxes,fontsize=6.3,va='top')
ax=axs[1]; panel(ax,'B')
for _,r in M.iterrows():
    d=r.key.split('_')[0]; ax.scatter(r.ba,r.succ*100,s=26,color=DC[d],marker='o' if not r.key.endswith('plt') else 's',zorder=3)
ax.axvline(0.5,color=C['thr'],ls='--',lw=0.9); ax.set_xlabel('Balanced accuracy'); ax.set_ylabel('Cue-correct success (%)'); ax.set_title('Accuracy',fontsize=7.6)
ax.text(0.04,0.93,f"Spearman ρ = {N['spearman_ba_succ'][0]:.2f}\np = {N['spearman_ba_succ'][1]:.2f}  (10 variants)",transform=ax.transAxes,fontsize=6.3,va='top')
ax.legend(handles=[Line2D([],[],marker='o',ls='',color=C['ink'],ms=4,label='raw'),Line2D([],[],marker='s',ls='',color=C['ink'],ms=4,label='Platt')],frameon=False,fontsize=6,loc='center left',bbox_to_anchor=(0.0,0.62))
ax=axs[2]; panel(ax,'C'); x=X[(X.arm=='R1')&(X.thr==0.75)]; order=['D1','D2','D3','D4','D5']; w=0.36
for i,d in enumerate(order):
    for j,(v,al) in enumerate([('raw',1.0),('plt',0.4)]):
        r=x[(x.decoder==d)&(x.variant==v)].iloc[0]; xx=i+(j-0.5)*w; ax.bar(xx,r.excess*100,width=w*0.9,color=DC[d],alpha=al); ax.vlines(xx,r.excess_ci[0]*100 if isinstance(r.excess_ci,list) else json.loads(r.excess_ci)[0]*100,(r.excess_ci[1] if isinstance(r.excess_ci,list) else json.loads(r.excess_ci)[1])*100,color=C['ink'],lw=0.9)
ax.axhline(0,color='k',lw=0.7); ax.set_xticks(range(5)); ax.set_xticklabels(['D1','D2','D3','D4','D5*'],fontsize=7); ax.set_ylabel('Success above chance-matched floor (pp)'); ax.set_title('Accuracy-attributable utility',fontsize=7.6)
fig.savefig('figs/N5_mechanism.png'); plt.close(fig)

# ---------- N6 gate sweep for real decoders
SW=pd.DataFrame(N['threshold_sweep']); SW=SW[SW.arm=='R1']; thr=sorted(SW.thr.unique())
fig,axs=plt.subplots(1,2,figsize=(7.3,2.9)); plt.subplots_adjust(wspace=0.32)
ax=axs[0]; panel(ax,'A')
for d in ['D1','D2','D3','D4','D5']:
    s=SW[(SW.decoder==d)&(SW.variant=='raw')].sort_values('thr'); ax.plot(s.thr,s.success*100,'-o',ms=3,color=DC[d],lw=1.3,label=d)
    if d!='D5':
        s=SW[(SW.decoder==d)&(SW.variant=='plt')].sort_values('thr'); ax.plot(s.thr,s.success*100,'--',color=DC[d],lw=1.0,alpha=0.8)
ax.axvline(0.75,color=C['thr'],ls=':',lw=1); ax.text(0.757,33,'registered gate',fontsize=5.8,color=C['thr'],rotation=90,va='top')
ax.set_xlabel('Confidence threshold of the decision engine'); ax.set_ylabel('Cue-correct success (%)'); ax.set_title('Observed success (solid raw, dashed Platt)',fontsize=7.4); ax.legend(frameon=False,fontsize=6,ncol=2,loc='upper center',bbox_to_anchor=(0.45,0.80))
ax=axs[1]; panel(ax,'B')
for d in ['D1','D3','D4','D5']:
    for v,ls in [('raw','-'),('plt','--')]:
        s=X[(X.arm=='R1')&(X.decoder==d)&(X.variant==v)].sort_values('thr')
        if len(s)==0: continue
        ci=np.array([json.loads(c) if isinstance(c,str) else c for c in s.excess_ci]); ax.plot(s.thr,s.excess*100,ls,marker='o',ms=2.8,color=DC[d],lw=1.2,label=f'{d} {v}')
        if v=='raw': ax.fill_between(s.thr,ci[:,0]*100,ci[:,1]*100,color=DC[d],alpha=0.12,lw=0)
ax.axhline(0,color='k',lw=0.7); ax.set_xlabel('Confidence threshold'); ax.set_ylabel('Success above chance-matched floor (pp)'); ax.set_title('Accuracy-attributable utility',fontsize=7.4); ax.legend(frameon=False,fontsize=5.6,ncol=2,loc='upper right')
fig.savefig('figs/N6_gate_sweep.png'); plt.close(fig)

# ---------- N7 controller-parameter sensitivity (emulator)
Ssum=S.groupby(['q','regime','threshold','confirmation_windows']).cue_correct_success.mean().reset_index()
fig,axs=plt.subplots(2,4,figsize=(7.3,3.7)); plt.subplots_adjust(wspace=0.14,hspace=0.55)
thrs=[0.6,0.7,0.75,0.85]; cws=[1,2,3,5]; im=None
for r,reg in enumerate(['cal','flat']):
    for c_,q in enumerate([0.6,0.7,0.8,0.9]):
        ax=axs[r,c_]; Z=np.array([[Ssum[(Ssum.q==q)&(Ssum.regime==reg)&(Ssum.threshold==t)&(Ssum.confirmation_windows==w)].cue_correct_success.iloc[0] for w in cws] for t in thrs])
        im=ax.imshow(Z,origin='lower',vmin=0,vmax=1,cmap='viridis',aspect='auto')
        for i in range(4):
            for j in range(4): ax.text(j,i,f'{Z[i,j]:.2f}',ha='center',va='center',fontsize=5.2,color='white' if Z[i,j]<0.55 else 'black')
        ax.set_xticks(range(4)); ax.set_xticklabels(cws,fontsize=6); ax.set_yticks(range(4)); ax.set_yticklabels(thrs if c_==0 else [],fontsize=6)
        ax.set_title(f"{'calibrated' if reg=='cal' else 'over-confident'}, q = {q}",fontsize=6.4)
        if r==1: ax.set_xlabel('Confirmation windows',fontsize=6.4)
        if c_==0: ax.set_ylabel('Threshold',fontsize=6.4)
cb=fig.colorbar(im,ax=axs,fraction=0.025,pad=0.02); cb.set_label('Cue-correct success',fontsize=6.4); cb.ax.tick_params(labelsize=6)
fig.savefig('figs/N7_sensitivity.png'); plt.close(fig)
print('ok')
