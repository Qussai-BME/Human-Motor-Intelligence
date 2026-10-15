import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _REPO=_HERE.parents[2]; _OUT=_HERE.parent/'outputs'
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
os.chdir(_OUT)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from figstyle import *
fig,ax=plt.subplots(figsize=(7.3,4.7)); ax.set_xlim(0,100); ax.set_ylim(0,66); ax.axis('off')
def rb(x,y,w,h,fc,ec,lw=1.0): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.2,rounding_size=1',fc=fc,ec=ec,lw=lw))
ax.text(0.5,65,'A   Endpoint-validity checks',fontsize=7.4,fontweight='bold',va='top')
rows=[('V1','Manipulation check','Does the decoder-quality gradient exist?','fail','All three decoders at chance (p ≥ 0.77); M3 − M2 = 0.0003'),
      ('V2','Floor control','Does a null decoder sit at the floor?','warn','Not registered; floor is reached by every condition'),
      ('V3','Ceiling control','Can a perfect stream reach the endpoint?','fail','Oracle 0 / 20 (fixture passed only at 0.1-s cadence)'),
      ('V4','Timing compatibility','Cadence × controller rule × task clock','fail','8.2 s per output vs 8.0-s clock; needs ≥ 4 windows'),
      ('V5','Endpoint variability','Can the primary endpoint vary at all?','fail','0 / 60 successes: degenerate by construction'),
      ('V6','Metric validity','Metrics computed inside the task window?','fail','171 / 207 controller transitions occur after failure')]
col={'fail':C['bad'],'warn':'#D9A021','pass':C['good']}; sym={'fail':'✕','warn':'!','pass':'✓'}
y0=57
for i,(k,t,q,st,ev) in enumerate(rows):
    y=y0-i*8.9
    rb(0.5,y-6.6,47,7.8,C['light'],'#B8C1CC')
    ax.add_patch(Circle((3.6,y-2.7),2.0,fc=col[st],ec='white',lw=0.8)); ax.text(3.6,y-2.8,sym[st],ha='center',va='center',fontsize=7.5,color='white',fontweight='bold')
    ax.text(7.2,y-0.2,f'{k}  {t}',fontsize=6.6,fontweight='bold',va='top',color=C['ink'])
    ax.text(7.2,y-2.7,q,fontsize=5.5,va='top',color='#4A5560')
    ax.text(7.2,y-4.8,ev,fontsize=5.5,va='top',color=col[st] if st!='warn' else '#8A6A10')
ax.text(0.5,3.5,'✕ failed in C1    ! not tested in C1',fontsize=6.0,color=C['ink'])
ax.text(52,65,'B   Proposed follow-up (C2)',fontsize=7.4,fontweight='bold',va='top')
ax.text(52,61.8,'design proposal — not executed in this study',fontsize=6.2,style='italic',color=C['bad'],va='top')
bx=52; bw=47
def step(y,h,title,body,fc='#EEF4FB',ec=C['blue']):
    rb(bx,y,bw,h,fc,ec); ax.text(bx+1.5,y+h-1.3,title,fontsize=6.4,fontweight='bold',va='top',color=C['ink']); ax.text(bx+1.5,y+h-4.0,body,fontsize=5.6,va='top',color=C['ink'],linespacing=1.35)
step(49,9.2,'1  Episode = grasp trial (T2) + release trial (T1)','same subject, drawn from the held-out trials; success needs\nboth commands decoded, confirmed and executed in order')
step(38,9.2,'2  Windowed stream at control rate','sliding 0.1-s windows across the 2.5-s imagery epoch\n(≥ 25 outputs per trial) so the unchanged controller can confirm')
step(27,9.2,'3  Episode-scoped task clock','clock starts at the episode, not at the recording; events\nafter COMPLETE/FAILED are discarded and not scored')
step(14.8,10.2,'4  Arms with built-in controls','oracle (ceiling) · label-shuffled (floor) · M1–M3 ·\nat least one decoder with a genuine quality advantage\n(manipulation check passed before any task run)')
step(5.2,8.4,'5  Registered analysis','paired subject-level success (exact CIs, McNemar / GLMM)\nwith episodes nested in subjects; sample size by simulation')
for yy in (49,38,27,14.8): ax.add_patch(FancyArrowPatch((bx+bw/2,yy+0.1),(bx+bw/2,yy-1.8),arrowstyle='-|>',mutation_scale=7,lw=0.9,color=C['grey']))
fig.savefig('figs/fig10_validity_framework.png'); plt.close(fig)
print('ok')
