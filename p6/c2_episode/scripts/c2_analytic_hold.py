"""Closed-form expected cue-correct success under sample-and-hold (rho = 1.0).
cue_correct = P(grasp trial: predicted CLOSE and conf >= 0.75) * (1 - P(decoy trial: predicted CLOSE and conf >= 0.75))
Confidence models (conf on [0.5, 1]; scaled Beta with concentration 4):
  'cal'  : mean-fraction m=(q-0.5)/0.5, P(correct | conf=c) = c            -> accuracy q
  'flat' : mean-fraction m=0.7 (mean conf 0.85) independent of correctness; P(correct)=q
"""
import numpy as np, json
from scipy import integrate, stats
def conf_pdf(m):
    a,b=4*m,4*(1-m); return lambda c: stats.beta.pdf((c-0.5)/0.5,a,b)/0.5
def expect(q,cal):
    if cal=='cal':
        m=(q-0.5)/0.5
        if m<=1e-9: return 0.0,0.0
        if m>=1-1e-9: return 1.0,0.0
        f=conf_pdf(m)
        return (integrate.quad(lambda c:c*f(c),0.75,1.0)[0], integrate.quad(lambda c:(1-c)*f(c),0.75,1.0)[0])
    f=conf_pdf(0.7); pp=integrate.quad(f,0.75,1.0)[0]; return q*pp,(1-q)*pp
if __name__=='__main__':
    rows=[]
    for cal in ('cal','flat'):
        for q in (0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.9,1.0):
            ok,bad=expect(q,cal); rows.append(dict(cal=cal,q=q,p_grasp=ok,p_false_grasp=bad,cue_correct=ok*(1-bad)))
    json.dump(rows,open('c2_analytic_hold.json','w'),indent=1); print(json.dumps(rows,indent=1))
