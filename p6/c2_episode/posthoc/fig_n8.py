import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _C2=_HERE.parent; _REPO=_C2.parents[1]; _OUT=_HERE/'outputs'
sys.path.insert(0,str(_REPO/'p6'/'c1_audit'/'scripts'))
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
RAW=_P(os.environ.get('C2_RAW',str(_C2)))
os.chdir(_OUT)
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from figstyle import *
fig,ax=plt.subplots(figsize=(7.3,3.7)); ax.set_xlim(0,100); ax.set_ylim(0,58); ax.axis('off')
def rb(x,y,w,h,fc,ec): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.2,rounding_size=1',fc=fc,ec=ec,lw=1))
rows=[('V1','Manipulation check','fail','Chance level; M3 − M2 = 0.0003','warn','Best BA 0.596; spread 0.53–0.60'),
      ('V2','Floor control','warn','Not tested','warn','Floor: 0% calibrated, 23% over-confident'),
      ('V3','Ceiling control','fail','Oracle 0 / 20','pass','Oracle 100 / 100'),
      ('V4','Timing compatibility','fail','8.2 s per output vs 8.0-s clock','pass','Episode 7.0 s < 8.0-s clock'),
      ('V5','Endpoint variability','fail','0 / 60 successes','pass','Success spans 0–100%'),
      ('V6','Metric validity','fail','171 / 207 transitions post-failure','pass','Scored inside episode window')]
col={'fail':C['bad'],'warn':'#D9A021','pass':C['good']}; sym={'fail':'✕','warn':'!','pass':'✓'}
ax.text(1,56,'Check',fontsize=7,fontweight='bold'); ax.text(26,56,'C1 (sparse replay)',fontsize=7,fontweight='bold'); ax.text(63,56,'C2 (episode replay)',fontsize=7,fontweight='bold')
for i,(k,t,s1,e1,s2,e2) in enumerate(rows):
    y=50-i*8.2
    rb(0.5,y-3.3,24,7.2,C['light'],'#B8C1CC'); ax.text(2,y+0.6,k,fontsize=7,fontweight='bold'); ax.text(6.5,y+0.6,t,fontsize=6.1,va='center')
    for x0,s,e in ((26,s1,e1),(63,s2,e2)):
        rb(x0-1,y-3.3,35.5,7.2,'white',col[s]); ax.add_patch(Circle((x0+2,y+0.2),1.9,fc=col[s],ec='white')); ax.text(x0+2,y+0.1,sym[s],ha='center',va='center',fontsize=7.5,color='white',fontweight='bold'); ax.text(x0+5,y+0.2,e,fontsize=5.7,va='center')
ax.text(0.5,0.4,'✕ failed    ! partial / not tested    ✓ passed',fontsize=6.2)
fig.savefig('figs/N8_validity_checks.png'); plt.close(fig)
