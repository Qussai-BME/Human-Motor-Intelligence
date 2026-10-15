import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _C2=_HERE.parent; _REPO=_C2.parents[1]; _OUT=_HERE/'outputs'
sys.path.insert(0,str(_REPO/'p6'/'c1_audit'/'scripts'))
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
RAW=_P(os.environ.get('C2_RAW',str(_C2)))
os.chdir(_HERE)
import numpy as np, json, time, itertools
from scipy import stats
from probe import *
DT=0.1; NW,NC,NG,NT=20,10,10,20
T_DECOY=(NW*DT,(NW+NC)*DT); T_GRASP=((NW+NC+NG)*DT,(NW+2*NC+NG)*DT)
def draw_conf(rng,mean_m):  # scaled Beta on [0.5,1], mean_m in [0,1]
    if mean_m<=1e-9: return 0.5
    if mean_m>=1-1e-9: return 1.0
    return 0.5+0.5*rng.beta(4*mean_m,4*(1-mean_m))
def draw_output(rng,y,q,cal):
    other='CLOSE' if y=='OPEN' else 'OPEN'
    if cal=='cal':
        c=draw_conf(rng,(q-0.5)/0.5); ok=rng.random()<c
    else:
        c=draw_conf(rng,0.7); ok=rng.random()<q
    return (y if ok else other),c
def window_seq(rng,y,q,cal,rho,n):
    out=[draw_output(rng,y,q,cal)]
    for _ in range(n-1): out.append(out[-1] if rng.random()<rho else draw_output(rng,y,q,cal))
    return out
def build(decoy_seq,grasp_seq):
    ev=[];t=0.0
    for _ in range(NW): ev.append((t,'REST',0.99)); t+=DT
    for l,c in decoy_seq: ev.append((t,l,c)); t+=DT
    for _ in range(NG): ev.append((t,'REST',0.99)); t+=DT
    for l,c in grasp_seq: ev.append((t,l,c)); t+=DT
    for _ in range(NT): ev.append((t,'REST',0.99)); t+=DT
    return ev
def score(events):
    r,log=run(events); tm=r['task_metrics']; trans=[(x['timestamp_s'],x['reason']) for x in r['task_transitions']]
    onset=[t for t,rs in trans if rs=='decoded_grasp_command']; onset=onset[0] if onset else None
    fa=any((T_DECOY[0]<=t<T_GRASP[0]) and st=='EXECUTING' and cmd=='CLOSE' for t,l,st,cmd,ts in log)
    complete=tm['final_state']=='COMPLETE'
    ok_on= onset is not None and T_GRASP[0]<=onset<=T_GRASP[1]+0.5
    return dict(task_success=bool(complete),false_grasp=bool(fa),grasp_onset=onset,cue_correct=bool(complete and ok_on and not fa))
if __name__=='__main__':
    rng=np.random.default_rng(1701); N=60; rows=[]; t0=time.time()
    for q,cal,rho in itertools.product([0.5,0.6,0.7,0.8,0.9,1.0],['cal','flat'],[1.0,0.8,0.5]):
        res=[]
        for i in range(N):
            ev=build(window_seq(rng,'OPEN',q,cal,rho,NC),window_seq(rng,'CLOSE',q,cal,rho,NC)); res.append(score(ev))
        a=np.mean([r['cue_correct'] for r in res]); b=np.mean([r['task_success'] for r in res]); f=np.mean([r['false_grasp'] for r in res])
        rows.append(dict(q=q,cal=cal,rho=rho,n=N,cue_correct=a,task_success=b,false_grasp=f)); print(q,cal,rho,round(a,3),round(b,3),round(f,3),flush=True)
    json.dump(rows,open('c2_pilot.json','w'),indent=1); print('secs',round(time.time()-t0))
