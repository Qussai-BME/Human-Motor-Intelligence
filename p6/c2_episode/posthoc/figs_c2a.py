import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _C2=_HERE.parent; _REPO=_C2.parents[1]; _OUT=_HERE/'outputs'
sys.path.insert(0,str(_REPO/'p6'/'c1_audit'/'scripts'))
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
RAW=_P(os.environ.get('C2_RAW',str(_C2)))
os.chdir(_OUT)
import sys, json, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from scipy import stats
from figstyle import *
N=json.load(open('final_numbers.json')); cells=pd.DataFrame(N['cells']); E=pd.read_csv(_C2/'results'/'emulator_episodes.csv')
CAL=C['blue']; FLAT=C['bad']
def cell(reg,rho,col,q): return cells[(cells.regime==reg)&(cells.rho==rho)].sort_values('q')
# ---------- N1: interface timeline (oracle, false-grasp example, X0 contrast)
from probe import run, episode
import probe
def ep(decoy,cd,grasp,cg):
    ev=[];t=0.0
    for _ in range(20): ev.append((t,'REST',0.99)); t+=0.1
    for _ in range(10): ev.append((t,decoy,cd)); t+=0.1
    for _ in range(10): ev.append((t,'REST',0.99)); t+=0.1
    for _ in range(10): ev.append((t,grasp,cg)); t+=0.1
    for _ in range(20): ev.append((t,'REST',0.99)); t+=0.1
    return ev
def timeline(ax_stream,ax_ctrl,ax_task,ev,title):
    r,log=run(ev); ts=[x[0] for x in log]; lab=[x[1] for x in log]; cmap={'REST':0,'OPEN':1,'CLOSE':2}
    ax_stream.step(ts,[cmap[l] for l in lab],where='post',color=C['ink'],lw=1.4)
    for (a,b,c_) in [(2.0,3.0,'#E8EEF5'),(4.0,5.0,'#FBE9E7')]: 
        for ax in (ax_stream,ax_ctrl,ax_task): ax.axvspan(a,b,color=c_,lw=0,zorder=0)
    ax_stream.set_yticks([0,1,2]); ax_stream.set_yticklabels(['REST','OPEN','CLOSE'],fontsize=6.4); ax_stream.set_title(title,fontsize=7.4)
    sm={'REST':0,'CANDIDATE':1,'CONFIRMED':2,'EXECUTING':3,'HOLD':4,'RELEASE':5}; st=[sm.get(x[2].upper(),0) for x in log]
    ax_ctrl.step(ts,st,where='post',color=C['M3'],lw=1.4); ax_ctrl.set_yticks([0,1,2,3,4,5]); ax_ctrl.set_yticklabels(['REST','CAND','CONF','EXEC','HOLD','REL'],fontsize=5.8)
    tsd={'APPROACH':0,'WAIT_FOR_GRASP':1,'TRANSPORT':2,'WAIT_FOR_RELEASE':3,'COMPLETE':4,'FAILED':5}; tk=[tsd.get(x[4].upper(),0) for x in log]
    ax_task.step(ts,tk,where='post',color=C['good'],lw=1.4); ax_task.set_yticks([0,1,2,3,4]); ax_task.set_yticklabels(['APPR','W-GRASP','TRANSP','W-REL','DONE'],fontsize=5.8)
    for tr in r['task_transitions']:
        ax_task.axvline(tr['timestamp_s'],color=C['grey'],lw=0.6,ls=':'); 
    return r
fig=plt.figure(figsize=(7.3,4.7)); gs=fig.add_gridspec(3,3,width_ratios=[1,1,0.62],hspace=0.35,wspace=0.42)
axs={}
for j,(dec,cd,gr,cg,t) in enumerate([('OPEN',0.9,'CLOSE',0.9,'Correct trial pair'),('CLOSE',0.9,'CLOSE',0.9,'False confident CLOSE in decoy trial')]):
    a=[fig.add_subplot(gs[i,j]) for i in range(3)]
    for x in a[:2]: x.tick_params(axis='x',length=0); x.set_xticklabels([]); x.spines['bottom'].set_visible(False)
    r=timeline(a[0],a[1],a[2],ep(dec,cd,gr,cg),t); a[2].set_xlabel('Time (s)')
    for x in a: x.set_xlim(0,7)
    if j==0: a[0].set_ylabel('Stream'); a[1].set_ylabel('Controller'); a[2].set_ylabel('Task')
    a[0].text(2.5,2.45,'decoy',ha='center',fontsize=6,color=C['blue']); a[0].text(4.5,2.45,'grasp',ha='center',fontsize=6,color=C['bad']); a[0].set_ylim(-0.3,2.9)
    sc=('cue-correct' if (r['task_metrics']['success'] and j==0) else 'cue-incorrect (false grasp)')
    a[2].text(6.9,0.2,sc,ha='right',fontsize=6.0,color=C['good'] if j==0 else C['bad'],fontweight='bold')
    axs[j]=a
ax=fig.add_subplot(gs[:,2]); panel(ax,'C')
ax.bar([0,1],[0,100],color=[C['grey'],C['good']],width=0.6); ax.text(0,2,'0 / 100',ha='center',fontsize=7,fontweight='bold'); ax.text(1,102,'100 / 100',ha='center',fontsize=7,fontweight='bold')
ax.set_xticks([0,1]); ax.set_xticklabels(['C1 sparse\nformat (X0)','C2 episode\nformat'],fontsize=6.6); ax.set_ylim(0,118); ax.set_ylabel('Oracle cue-correct successes (of 100)'); ax.set_title('Ceiling control',fontsize=7.6)
panel(axs[0][0],'A'); panel(axs[1][0],'B')
fig.savefig('figs/N1_interface.png'); plt.close(fig)

# ---------- N2: emulator dose-response
an=json.load(open('c2_analytic_hold.json')); an=pd.DataFrame(an)
fig,axs_=plt.subplots(1,3,figsize=(7.3,2.8),sharey=True); plt.subplots_adjust(wspace=0.06)
for ax,rho in zip(axs_,(1.0,0.8,0.5)):
    for reg,col,lab in [('cal',CAL,'calibrated confidence'),('flat',FLAT,'uninformative, over-confident')]:
        d=cells[(cells.regime==reg)&(cells.rho==rho)].sort_values('q'); y=d.cue_correct_success.values; ci=np.array(list(d.cue_correct_success_ci.values))
        ax.fill_between(d.q,ci[:,0],ci[:,1],color=col,alpha=0.18,lw=0); ax.plot(d.q,y,'-o',color=col,ms=3.2,lw=1.4,label=lab)
        ax.plot(d.q,d.task_completion.values,':',color=col,lw=1.0,alpha=0.8)
        if rho==1.0: a_=an[an.cal==reg].sort_values('q'); ax.plot(a_.q,a_.cue_correct,'x',color='k',ms=3.5,alpha=0.7)
    ax.set_xlabel('Emulated decoder accuracy q'); ax.set_title(f'ρ = {rho}  ({"pure hold" if rho==1.0 else "re-draw "+str(round(1-rho,1))})',fontsize=7.6); ax.set_ylim(-0.02,1.03); ax.set_xlim(0.48,1.02)
panel(axs_[0],'A'); panel(axs_[1],'B'); panel(axs_[2],'C')
axs_[0].set_ylabel('Success rate (n = 500 per point)')
h=[Line2D([],[],color=CAL,marker='o',ms=3,label='calibrated: cue-correct'),Line2D([],[],color=FLAT,marker='o',ms=3,label='over-confident: cue-correct'),Line2D([],[],color=C['grey'],ls=':',label='task completion (dotted)'),Line2D([],[],color='k',marker='x',ls='',ms=4,label='closed-form expectation')]
axs_[0].legend(handles=h,frameon=False,fontsize=6.2,loc='upper left')
fig.savefig('figs/N2_dose_response.png'); plt.close(fig)

# ---------- N3: calibration crossover, persistence, false grasp
def newcombe(k1,n1,k2,n2):
    def wil(k,n,z=1.959964):
        p=k/n; d=1+z*z/n; c=p+z*z/(2*n); w=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n)); return (c-w)/d,(c+w)/d
    l1,u1=wil(k1,n1); l2,u2=wil(k2,n2); p1,p2=k1/n1,k2/n2; D=p1-p2
    return D-np.sqrt((p1-l1)**2+(u2-p2)**2), D+np.sqrt((u1-p1)**2+(p2-l2)**2)
fig,axs_=plt.subplots(1,3,figsize=(7.3,2.7)); plt.subplots_adjust(wspace=0.42)
ax=axs_[0]; panel(ax,'A'); qs=sorted(E.q.unique()); rd=[];lo=[];hi=[]
for q in qs:
    a=E[(E.q==q)&(E.regime=='flat')&(E.rho==1.0)].cue_correct_success.sum(); b=E[(E.q==q)&(E.regime=='cal')&(E.rho==1.0)].cue_correct_success.sum(); l,h_=newcombe(a,500,b,500); rd.append((a-b)/500); lo.append(l); hi.append(h_)
ax.fill_between(qs,lo,hi,color=C['grey'],alpha=0.25,lw=0); ax.plot(qs,rd,'-o',color=C['ink'],ms=3.2,lw=1.3); ax.axhline(0,color='k',lw=0.7)
ax.set_ylim(-0.21,0.42); ax.text(0.50,0.41,'over-confident better',fontsize=6.3,color=FLAT,va='top'); ax.text(0.995,-0.17,'calibrated better',fontsize=6.3,color=CAL,ha='right',va='bottom')
ax.set_xlabel('Decoder accuracy q'); ax.set_ylabel('Risk difference (over-confident − calibrated)'); ax.set_title('Calibration crossover',fontsize=7.6)
ax=axs_[1]; panel(ax,'B')
for q,col in [(0.7,'#9BB7D4'),(0.8,'#5B8DB8'),(0.9,CAL)]:
    d=cells[(cells.regime=='cal')&(cells.q==q)].sort_values('rho'); ci=np.array(list(d.cue_correct_success_ci.values))
    ax.errorbar(d.rho,d.cue_correct_success,yerr=[d.cue_correct_success-ci[:,0],ci[:,1]-d.cue_correct_success],fmt='-o',color=col,ms=3.5,lw=1.3,capsize=2,label=f'q = {q}')
ax.set_xlabel('Persistence ρ'); ax.set_ylabel('Cue-correct success'); ax.set_xlim(0.45,1.05); ax.set_title('Persistence (calibrated)',fontsize=7.6); ax.legend(frameon=False,fontsize=6.3,loc='lower left')
ax=axs_[2]; panel(ax,'C')
for q,col in [(0.7,'#9BB7D4'),(0.8,'#5B8DB8'),(0.9,CAL)]:
    d=cells[(cells.regime=='cal')&(cells.q==q)].sort_values('rho'); ax.plot(d.rho,d.false_grasp,'-o',color=col,ms=3.5,lw=1.3)
for q,col in [(0.5,'#E6A39B'),(0.7,FLAT)]:
    d=cells[(cells.regime=='flat')&(cells.q==q)].sort_values('rho'); ax.plot(d.rho,d.false_grasp,'--s',color=col,ms=3.3,lw=1.1)
ax.set_xlabel('Persistence ρ'); ax.set_ylabel('False-grasp rate'); ax.set_xlim(0.45,1.05); ax.set_title('False grasps',fontsize=7.6)
ax.legend(handles=[Line2D([],[],color=CAL,marker='o',ms=3,label='calibrated, q = 0.7–0.9'),Line2D([],[],color=FLAT,marker='s',ls='--',ms=3,label='over-confident, q = 0.5, 0.7')],frameon=False,fontsize=6.0,loc='upper left')
fig.savefig('figs/N3_calibration_persistence.png'); plt.close(fig)
print('ok')
