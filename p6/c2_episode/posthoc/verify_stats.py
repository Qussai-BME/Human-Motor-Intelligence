import os, sys
from pathlib import Path as _P
_HERE=_P(__file__).resolve().parent; _C2=_HERE.parent; _REPO=_C2.parents[1]; _OUT=_HERE/'outputs'
sys.path.insert(0,str(_REPO/'p6'/'c1_audit'/'scripts'))
MYOSIM_DIR=_P(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo')))
RAW=_P(os.environ.get('C2_RAW',str(_C2)))
os.chdir(_OUT)
import pandas as pd, numpy as np, json
from scipy import stats
R=str(_C2)+'/'
E=pd.read_csv(R+'results/emulator_episodes.csv'); A=json.load(open(R+'results/ANALYSIS.json'))
out={}
def cp(k,n,a=0.05):
    lo=0.0 if k==0 else stats.beta.ppf(a/2,k,n-k+1); hi=1.0 if k==n else stats.beta.ppf(1-a/2,k+1,n-k); return lo,hi
def ca_trend(ks,ns,scores):
    ks=np.array(ks,float); ns=np.array(ns,float); s=np.array(scores,float); N=ns.sum(); K=ks.sum(); p=K/N
    T=np.sum(s*(ks-ns*p)); var=p*(1-p)*(np.sum(ns*s**2)-np.sum(ns*s)**2/N); return T/np.sqrt(var)
# H-E1
d=E[(E.regime=='cal')&(E.rho==1.0)].groupby('q').cue_correct_success.agg(['sum','size']).reset_index()
out['HE1_z']=float(ca_trend(d['sum'],d['size'],d.q)); 
import statsmodels.api as sm
X=sm.add_constant(E[(E.regime=='cal')&(E.rho==1.0)].q.values); y=E[(E.regime=='cal')&(E.rho==1.0)].cue_correct_success.astype(int).values
m=sm.GLM(y,X,family=sm.families.Binomial()).fit(); out['HE1_slope']=[float(m.params[1]),*[float(x) for x in m.conf_int()[1]]]
# H-E2
for q,reg in [(1.0,'cal'),(0.5,'cal'),(0.5,'flat')]:
    s=E[(E.q==q)&(E.regime==reg)&(E.rho==1.0)].cue_correct_success; out[f'HE2_{reg}_{q}']=[int(s.sum()),len(s),*cp(int(s.sum()),len(s))]
# H-E3
def newcombe(k1,n1,k2,n2):
    def wil(k,n,z=1.959964):
        p=k/n; d=1+z*z/n; c=p+z*z/(2*n); w=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n)); return (c-w)/d,(c+w)/d
    l1,u1=wil(k1,n1); l2,u2=wil(k2,n2); p1,p2=k1/n1,k2/n2; D=p1-p2
    return D-np.sqrt((p1-l1)**2+(u2-p2)**2), D+np.sqrt((u1-p1)**2+(p2-l2)**2)
e3=[]
for q in (0.6,0.7,0.8):
    a=E[(E.q==q)&(E.regime=='flat')&(E.rho==1.0)].cue_correct_success; b=E[(E.q==q)&(E.regime=='cal')&(E.rho==1.0)].cue_correct_success
    k1,k2,n=int(a.sum()),int(b.sum()),500; p=(k1+k2)/(2*n); z=(k1/n-k2/n)/np.sqrt(2*p*(1-p)/n); pv=2*stats.norm.sf(abs(z)); lo,hi=newcombe(k1,n,k2,n)
    e3.append(dict(q=q,flat=k1,cal=k2,rd=(k1-k2)/n,newcombe=[lo,hi],p=pv))
order=np.argsort([e['p'] for e in e3]); 
for r,i in enumerate(order): e3[i]['p_holm']=min(1,(3-r)*e3[i]['p'])
out['HE3']=e3
# crossover: also q 0.9,1.0
for q in (0.75,0.9,1.0):
    a=E[(E.q==q)&(E.regime=='flat')&(E.rho==1.0)].cue_correct_success; b=E[(E.q==q)&(E.regime=='cal')&(E.rho==1.0)].cue_correct_success
    out[f'RD_flat_minus_cal_q{q}']=float(a.mean()-b.mean())
# H-E4
e4=[]
for q in (0.7,0.8,0.9):
    d=E[(E.q==q)&(E.regime=='cal')].groupby('rho').cue_correct_success.agg(['sum','size']).reset_index().sort_values('rho')
    z=ca_trend(d['sum'],d['size'],d.rho); e4.append(dict(q=q,z=float(z),p=float(2*stats.norm.sf(abs(z))),rates={float(r):float(s/n) for r,s,n in zip(d.rho,d['sum'],d['size'])}))
o=np.argsort([e['p'] for e in e4])
for r,i in enumerate(o): e4[i]['p_holm']=min(1,(3-r)*e4[i]['p'])
out['HE4']=e4
# R1 GEE
Rr=pd.read_csv(R+'results/real_episodes.csv'); r1=Rr[(Rr.arm=='R1')&(Rr.variant=='raw')&(Rr.decoder.isin(['D1','D2','D3','D4']))].copy()
r1['y']=r1.cue_correct_success.astype(int)
import statsmodels.formula.api as smf
gee=smf.gee('y ~ C(decoder)',groups='subject',data=r1,family=sm.families.Binomial(),cov_struct=sm.cov_struct.Exchangeable()).fit()
W=gee.wald_test_terms(); out['GEE_wald']=str(W.summary_frame().to_dict())
# McNemar exact pairwise
piv=r1.pivot_table(index=['subject','pair_index'],columns='decoder',values='y',aggfunc='first')
mc=[]
import itertools
for a,b in itertools.combinations(['D1','D2','D3','D4'],2):
    n01=int(((piv[a]==0)&(piv[b]==1)).sum()); n10=int(((piv[a]==1)&(piv[b]==0)).sum()); p=stats.binomtest(min(n01,n10),n01+n10,0.5).pvalue if n01+n10>0 else 1.0
    mc.append(dict(a=a,b=b,n10=n10,n01=n01,p=float(p)))
o=np.argsort([m['p'] for m in mc])
for r,i in enumerate(o): mc[i]['p_holm']=min(1,(6-r)*mc[i]['p'])
out['McNemar']=mc
json.dump(out,open('verified_stats.json','w'),indent=1,default=float)
print(json.dumps({k:out[k] for k in ['HE1_z','HE1_slope','HE2_cal_1.0','HE2_cal_0.5','HE2_flat_0.5','HE3','HE4']},indent=0,default=float)[:2500])
print('agent HE1 z',A['hypotheses']['H-E1']['cochran_armitage']['z'],'slope',A['hypotheses']['H-E1']['logistic_slope']['estimate'])
print(out['GEE_wald'][:300]); print(mc)
