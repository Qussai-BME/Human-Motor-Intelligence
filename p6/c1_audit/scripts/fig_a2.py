import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _REPO=_HERE.parents[2]; _OUT=_HERE.parent/'outputs'
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
os.chdir(_OUT)
import json, numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from figstyle import *

def mk(figsize,ylim):
    fig,ax=plt.subplots(figsize=figsize); ax.set_xlim(0,100); ax.set_ylim(0,ylim); ax.axis('off'); return fig,ax
def rb(ax,x,y,w,h,fc,ec,lw=1.0): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.2,rounding_size=1.1',fc=fc,ec=ec,lw=lw))
def ar(ax,x1,y1,x2,y2,c=C['grey'],ls='-',ms=8): ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=ms,lw=1,color=c,ls=ls))

# ---------------- Fig 1
fig,ax=mk((7.3,3.7),52)
ax.text(0.5,50.2,'Registered chain: EEG → decoder → intent map → controller → safety → simulator → task → metrics',fontsize=7.2,fontweight='bold',va='top')
ax.text(0.5,46.4,'Numbered green badges = registered gates 1–6 (all passed).  Red = interface elements whose timing was not validated.',fontsize=6.3,va='top',color=C['ink'])
n=7; gap=1.3; w=(100-gap*(n-1)-1)/n; y=22; h=21
spec=[('EEG\nsource','PhysioNet\nEEGMMIDB R04\nS001–S020\n15 MI epochs\nper subject','G1',0),
      ('Frozen\ndecoders','M1 / M2 / M3\nstrict LOSO\nno target\ncalibration','G2',0),
      ('Intent\nmap','T1 → OPEN\nT2 → CLOSE\nabstract\nlabels only','',1),
      ('Decision\nengine','conf. ≥ 0.75\n≥ 3 consistent\nwindows\ndwell ≥ 0.08 s','G3',1),
      ('Safety +\ncontrol','rate limit\njoint limits\nstale input\n0.30 s','',0),
      ('MuJoCo\ntask','pick-and-place\ntask clock\ntimeout 8.0 s','G4',1),
      ('Metrics','success\n(primary)\nerror, path,\ncorrections','G5 G6',0)]
xs=[0.5+i*(w+gap) for i in range(n)]
for i,(x,(t,s,g,red)) in enumerate(zip(xs,spec)):
    rb(ax,x,y,w,h,'#FFF4F2' if red else C['light'],C['bad'] if red else '#B8C1CC',1.2 if red else 1.0)
    ax.text(x+w/2,y+h-1.5,t,ha='center',va='top',fontsize=6.9,fontweight='bold',color=C['ink'],linespacing=1.15)
    ax.text(x+w/2,y+h-9.2,s,ha='center',va='top',fontsize=5.7,color=C['ink'],linespacing=1.3)
    if g:
        for j,gg in enumerate(g.split()):
            cx=x+2.2+j*3.6; cy=y+h+0.2
            ax.add_patch(Circle((cx,cy),1.55,fc=C['good'],ec='white',lw=0.8,zorder=5)); ax.text(cx,cy-0.05,gg[1],ha='center',va='center',fontsize=5.8,color='white',fontweight='bold',zorder=6)
    if i<n-1: ar(ax,x+w+0.15,y+h/2,xs[i+1]-0.15,y+h/2,ms=7)
# callout
cx0=xs[2]; cx1=xs[5]+w
rb(ax,cx0,1.5,cx1-cx0,15,'#FFF4F2',C['bad'],1.2)
ax.text(cx0+1.2,15.2,'Validity gap: temporal compatibility (no registered gate)',fontsize=6.6,fontweight='bold',color=C['bad'],va='top')
ax.text(cx0+1.2,11.4,'•  one decoder output per 8.2-s trial (15 outputs, ≈ 120 s)\n•  engine needs ≥ 4 consecutive confident same-label windows\n•  task clock expires 8.0 s after the first event\n→  only 2 of 15 outputs are seen before the task has already failed',fontsize=6.0,va='top',color=C['ink'],linespacing=1.4)
for i in (2,3,5):
    xm=xs[i]+w/2; ax.plot([xm,xm],[y-0.3,16.9],ls='--',lw=0.9,color=C['bad'])
fig.savefig('figs/fig1_architecture.png'); plt.close(fig)

# ---------------- Fig 2
fig,ax=mk((7.3,4.6),64)
def fb(x,y,w,h,txt,fc=C['light'],ec='#B8C1CC',fs=6.0,bold=False,lw=1.0):
    rb(ax,x,y,w,h,fc,ec,lw); ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=fs,fontweight='bold' if bold else 'normal',color=C['ink'],linespacing=1.35)
ax.text(0.5,63,'A   Registered confirmatory pathway (protocol P6-C1-MI-R04-v1.0)',fontsize=7.4,fontweight='bold',va='top')
bw=22.5; bx=[0.5,25.7,50.9,76.0]
fb(bx[0],47,bw,10,'20 subjects × 15 epochs\n= 300 labelled epochs\n(PhysioNet R04, MI)')
fb(bx[1],47,bw,10,'3 frozen decoders\nstrict LOSO, no calibration\n→ 60 held-out traces')
fb(bx[2],47,bw,10,'Quality order frozen\nfrom source-CV only\n(M1 > M3 > M2)')
fb(bx[3],47,bw,10,'Fixture gate: 1 / 1\nCOMPLETE (dense 0.1-s\nsynthetic stream)',fc='#EAF6EF',ec=C['good'],lw=1.3)
for i in range(3): ar(ax,bx[i]+bw+0.2,52,bx[i+1]-0.2,52,ms=7)
fb(8,31,38,9,'Primary replay\n60 runs  →  0 / 60 successes',fc='#FFF4F2',ec=C['bad'],bold=True,lw=1.3)
fb(54,31,38,9,'Independent rerun\n60 runs  →  0 / 60 successes',fc='#FFF4F2',ec=C['bad'],bold=True,lw=1.3)
ar(ax,63,46.6,27,40.4); ar(ax,89,46.6,73,40.4)
fb(18,15.5,64,9,'Registered inference: success endpoint degenerate (0 / 20 per model).\nSuccess test not run; continuous endpoints analysed as exploratory.')
ar(ax,27,30.6,40,24.6); ar(ax,73,30.6,60,24.6)
ax.plot([0.5,99.5],[12.2,12.2],color='#B8C1CC',lw=0.8,ls='--')
ax.text(0.5,11.2,'B   Post-hoc validity diagnostics added in this revision (outside the registered inference)',fontsize=7.4,fontweight='bold',color=C['blue'],va='top')
dw=23.4; dx=[0.5,25.6,50.7,75.8]
fb(dx[0],0.8,dw,7.6,'D1  Re-execution of the\n60 archived runs: metrics\nidentical in 60 / 60',fc='#EEF4FB',ec=C['blue'])
fb(dx[1],0.8,dw,7.6,'D2  Oracle negative control\n(true labels, conf. 1.0):\n0 / 20 successes',fc='#EEF4FB',ec=C['blue'])
fb(dx[2],0.8,dw,7.6,'D3  Event-timeline audit:\n2 / 15 events inside window;\n171 / 207 transitions post-failure',fc='#EEF4FB',ec=C['blue'])
fb(dx[3],0.8,dw,7.6,'S1  Timeout removed:\n0 / 60 decoders, 0 / 20 oracle;\nmilestones differ by decoder',fc='#EEF4FB',ec=C['blue'])
fig.savefig('figs/fig2_evidence_flow.png'); plt.close(fig)
print('ok')
