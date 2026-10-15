import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _C2=_HERE.parent; _REPO=_C2.parents[1]; _OUT=_HERE/'outputs'
sys.path.insert(0,str(_REPO/'p6'/'c1_audit'/'scripts'))
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
RAW=_P(os.environ.get('C2_RAW',str(_C2)))
os.chdir(_OUT)
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from figstyle import *
fig,ax=plt.subplots(figsize=(7.3,4.4)); ax.set_xlim(0,100); ax.set_ylim(0,62); ax.axis('off')
def bx(x,y,w,h,t,fc=C['light'],ec='#B8C1CC',fs=5.9,bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.2,rounding_size=1',fc=fc,ec=ec,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,fontweight='bold' if bold else 'normal',linespacing=1.35,color=C['ink'])
def ar(x1,y1,x2,y2): ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=7,lw=0.9,color=C['grey']))
ax.text(0.5,61,'Stage 1 · C1 registered replay',fontsize=7.2,fontweight='bold',va='top'); ax.text(36,61,'Stage 2 · post-hoc audit',fontsize=7.2,fontweight='bold',color=C['blue'],va='top'); ax.text(68,61,'Stage 3 · C2 follow-up',fontsize=7.2,fontweight='bold',color=C['good'],va='top')
bx(0.5,46,31,9,'20 subjects × 15 epochs\nM1–M3, strict LOSO → 60 traces')
bx(0.5,31,31,11,'60 primary + 60 rerun runs\nsparse replay, 8.2 s per output\nsuccess 0 / 60',fc='#FFF4F2',ec=C['bad'],bold=True)
bx(0.5,17,31,10,'Endpoint non-discriminative\n(registered interpretation rule)')
ar(16,45.6,16,42.4); ar(16,30.6,16,27.4)
bx(36,46,29,9,'D1  re-execution: 60 / 60 identical',fc='#EEF4FB',ec=C['blue'])
bx(36,35,29,9,'D2  oracle: 0 / 20 successes',fc='#EEF4FB',ec=C['blue'])
bx(36,24,29,9,'D3  timeline: 2 of 15 events in window;\n171 / 207 transitions after failure',fc='#EEF4FB',ec=C['blue'])
bx(36,13,29,9,'S1  timeout removed:\n0 / 60 decoders, 0 / 20 oracle',fc='#EEF4FB',ec=C['blue'])
ar(31.8,22,35.7,28)
bx(68,50,31,5.5,'6 pre-flight checks (all passed)',fc='#EAF6EF',ec=C['good'],bold=True)
arms=[('X0','C1-format oracle · 100 episodes'),('E','emulated · 54 × 500 = 27,000'),('S','gate sensitivity · 25,600'),('R0','M1–M3 + oracle · 560'),('R1','D1–D5, 105 subjects · 19,750')]
for i,(a,t) in enumerate(arms): bx(68,43.6-i*6.7,31,5.6,f'{a}   {t}',fs=5.6)
ar(65.2,30,67.8,45)
ax.plot([0.5,99.5],[10.5,10.5],color='#B8C1CC',lw=0.8,ls='--')
ax.text(0.5,9.4,'Post-hoc analyses after C2 outcomes (P1–P4)',fontsize=7,fontweight='bold',color=C['blue'],va='top')
for i,t in enumerate(['P1  re-run of 300 episodes;\nstatistics recomputed','P2  lookup validated (0 / 300\nmismatches, 3 thresholds)','P3  chance-matched floor and\naccuracy-attributable utility','P4  gate sweep 0.50–0.85\nfor real decoders']):
    bx(0.5+i*25,0.6,24,6.4,t,fc='#EEF4FB',ec=C['blue'],fs=5.3)
fig.savefig('figs/N0_study_map.png'); plt.close(fig)
