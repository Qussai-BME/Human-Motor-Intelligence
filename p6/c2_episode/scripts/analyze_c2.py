#!/usr/bin/env python3
import json,math,os,sys
from pathlib import Path
import numpy as np,pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.contingency_tables import mcnemar
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import confint_proportions_2indep
OUT=Path(os.environ.get('C2_OUT',str(Path(__file__).resolve().parents[1]))); RES=OUT/'results'; FIG=OUT/'figures';FIG.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.size':9,'figure.dpi':110,'savefig.dpi':300,'axes.spines.top':False,'axes.spines.right':False})
COL={'cal':'#0072B2','flat':'#D55E00'}
def exact(k,n):
 return [0.0 if k==0 else float(stats.beta.ppf(.025,k,n-k+1)),1.0 if k==n else float(stats.beta.ppf(.975,k+1,n-k))]
def holm(ps):
 ix=np.argsort(ps); adj=np.empty(len(ps)); prev=0
 for rank,i in enumerate(ix):
  val=min(1,(len(ps)-rank)*ps[i]);prev=max(prev,val);adj[i]=prev
 return adj.tolist()
def ca_test(success,total,scores):
 success=np.asarray(success,dtype=float); total=np.asarray(total,dtype=float);scores=np.asarray(scores,dtype=float)
 N=total.sum();P=success.sum();q=scores
 mean=(total*q).sum()/N
 var=(P/N)*(1-P/N)*((total*(q-mean)**2).sum())
 z=(success@q-P*mean)/math.sqrt(var) if var>0 else 0
 return {'z':float(z),'p_one_sided_increasing':float(stats.norm.sf(z)),'p_two_sided':float(2*stats.norm.sf(abs(z)))}
D=pd.read_csv(RES/'emulator_episodes.csv'); D['success']=D.cue_correct_success.astype(int)
cell_rows=[]
for (q,reg,rho),g in D.groupby(['q','regime','rho'],sort=True):
 k=int(g.success.sum());n=len(g);tk=int(g.task_completion.sum());fk=int(g.false_grasp.sum());cell_rows.append({'q':float(q),'regime':reg,'rho':float(rho),'n':n,'successes':k,'rate':k/n,'exact95':exact(k,n),'task_completion_successes':tk,'task_completion_rate':tk/n,'task_completion_exact95':exact(tk,n),'false_grasp_successes':fk,'false_grasp_rate':fk/n,'false_grasp_exact95':exact(fk,n),'miss_rate':float(g.miss.mean())})
H={}
# H-E1: calibrated rho=1 dose response.
g=D[(D.regime=='cal')&(D.rho==1.0)]; gg=g.groupby('q').success.agg(['sum','count']); H['H-E1']={'cochran_armitage':ca_test(gg['sum'],gg['count'],gg.index),'logistic_slope':{}}
fit=smf.glm('success ~ q',data=g,family=sm.families.Binomial()).fit();H['H-E1']['logistic_slope']={'estimate':float(fit.params['q']),'ci95':[float(x) for x in fit.conf_int().loc['q']],'p_one_sided_positive':float(stats.norm.sf(fit.tvalues['q'])),'model':'binomial GLM success ~ q'}
H['H-E1']['supported']=H['H-E1']['cochran_armitage']['p_one_sided_increasing']<.05 and fit.params['q']>0
# H-E2
h2=[]
for q,reg,req,op in [(1.,'cal',.99,'>='),(.5,'cal',.01,'<='),(.5,'flat',.10,'lower_CI_gt')]:
 x=D[(D.q==q)&(D.regime==reg)&(D.rho==1.)];k=int(x.success.sum());n=len(x);ci=exact(k,n)
 ok=(k/n>=req) if op=='>=' else ((k/n<=req) if op=='<=' else ci[0]>req)
 h2.append({'q':q,'regime':reg,'n':n,'successes':k,'rate':k/n,'exact95':ci,'criterion':f'{op} {req}','pass':bool(ok)})
H['H-E2']={'checks':h2,'supported':all(x['pass'] for x in h2)}
from scipy.stats import binomtest
pe2=[float(binomtest(int(D[(D.q==q)&(D.regime==reg)&(D.rho==1.)].success.sum()),500,p=base,alternative=alt).pvalue) for q,reg,base,alt in [(1.,'cal',.99,'greater'),(.5,'cal',.01,'less'),(.5,'flat',.10,'greater')]]
H['H-E2']['component_p_one_sided']=pe2;H['H-E2']['family_p_intersection_union']=max(pe2)
# E3 calibration effect; Fisher exact; Holm, risk difference CI.
e3=[]
for q in [.6,.7,.8]:
 a=D[(D.q==q)&(D.regime=='cal')&(D.rho==1.)].success.astype(int);b=D[(D.q==q)&(D.regime=='flat')&(D.rho==1.)].success.astype(int)
 table=[[int(a.sum()),len(a)-int(a.sum())],[int(b.sum()),len(b)-int(b.sum())]]
 expected=np.outer(np.asarray([len(a),len(b)])/ (len(a)+len(b)),np.asarray([int(a.sum()+b.sum()),len(a)+len(b)-int(a.sum()+b.sum())]))
 if expected.min()<5: odds,p=stats.fisher_exact(table,alternative='two-sided');test='Fisher exact fallback'
 else: _,p=sm.stats.proportions_ztest([int(b.sum()),int(a.sum())],[len(b),len(a)],alternative='two-sided');test='two-proportion z, continuity-free'
 lo,hi=confint_proportions_2indep(int(b.sum()),len(b),int(a.sum()),len(a),method='newcomb')
 e3.append({'q':q,'cal_successes':int(a.sum()),'flat_successes':int(b.sum()),'risk_difference_flat_minus_cal':float(b.mean()-a.mean()),'newcombe95':[float(lo),float(hi)],'test':test,'p_two_sided':float(p)})
adj=holm([x['p_two_sided'] for x in e3]);
for x,p in zip(e3,adj):x['p_holm']=p;x['significant_holm_0.05']=p<.05
H['H-E3']={'comparisons':e3,'supported':any(x['significant_holm_0.05'] for x in e3)}
H['H-E3']['family_p_bonferroni_global']=min(1.,3*min(x['p_two_sided'] for x in e3))
# H-E4 persistence, by q.
e4=[]
for q in [.7,.8,.9]:
 x=D[(D.q==q)&(D.regime=='cal')];g=x.groupby('rho').success.agg(['sum','count']).sort_index(ascending=False)
 # increasing persistence scores 1,.8,.5
 tr=ca_test(g['sum'],g['count'],g.index)
 e4.append({'q':q,'trend':tr,'cells':[{'rho':float(r),'n':int(rw['count']),'successes':int(rw['sum']),'false_grasp_rate':float(x[x.rho==r].false_grasp.mean())} for r,rw in g.iterrows()]})
adj=holm([x['trend']['p_two_sided'] for x in e4]);
for x,p in zip(e4,adj):x['p_holm']=p;x['significant_holm_0.05']=p<.05
H['H-E4']={'comparisons':e4,'supported':any(x['significant_holm_0.05'] for x in e4)}
H['H-E4']['family_p_bonferroni_global']=min(1.,3*min(x['trend']['p_two_sided'] for x in e4))
# Descriptive global model and likelihood-ratio interaction tests.
D['q2']=D.q**2;D['rho_cat']=D.rho.astype(str)
full=smf.glm('success ~ (q + q2) * regime * rho_cat',data=D,family=sm.families.Binomial()).fit()
red=smf.glm('success ~ q + q2 + regime + rho_cat',data=D,family=sm.families.Binomial()).fit()
lr=max(0,2*(full.llf-red.llf));df=max(1,int(full.df_model-red.df_model));H['global_descriptive_model']={'formula':'success ~ (q + q²) × regime × rho','llr_interactions':lr,'df':df,'p':float(stats.chi2.sf(lr,df)),'AIC':float(full.aic),'claim_status':'descriptive only'}
# R0 descriptive counts and exact CIs.
r0path=RES/'real_episodes.csv';r0out=[]
if r0path.exists():
 R=pd.read_csv(r0path);R=R[R.arm=='R0']
 for model,g in R.groupby('decoder'):
  k=int(g.cue_correct_success.sum());n=len(g);r0out.append({'decoder':model,'n':n,'successes':k,'rate':k/n,'exact95':exact(k,n),'false_grasp_rate':float(g.false_grasp.mean()),'miss_rate':float(g.miss.mean())})
# S summaries.
sp=RES/'sensitivity_episodes.csv';sout=[]
if sp.exists():
 S=pd.read_csv(sp)
 for keys,g in S.groupby(['q','regime','threshold','confirmation_windows']):
  q,reg,thr,nconf=keys;sout.append({'q':float(q),'regime':reg,'threshold':float(thr),'confirmation_windows':int(nconf),'n':len(g),'successes':int(g.cue_correct_success.sum()),'rate':float(g.cue_correct_success.mean()),'false_grasp_rate':float(g.false_grasp.mean())})
R1={};qeq=[]
if (RES/'decoder_quality_R1.json').exists() and r0path.exists():
 Q=json.load(open(RES/'decoder_quality_R1.json'));Rall=pd.read_csv(r0path);R1df=Rall[(Rall.arm=='R1')&(Rall.decoder.isin(['D1','D2','D3','D4']))&(Rall.variant=='raw')].copy()
 R1['V1']=Q['V1'];R1['quality']=Q['variants']
 if Q['V1']['passed'] and len(R1df):
  from statsmodels.genmod.cov_struct import Exchangeable
  from patsy import dmatrix
  import itertools as it
  gee=smf.gee('cue_correct_success ~ C(decoder)',groups='subject',data=R1df,family=sm.families.Binomial(),cov_struct=Exchangeable()).fit()
  models=['D1','D2','D3','D4'];design=dmatrix('C(decoder)',pd.DataFrame({'decoder':models}),return_type='dataframe');contrasts=[]
  for a,b in it.combinations(models,2):
   v=(design.iloc[models.index(a)]-design.iloc[models.index(b)]).to_numpy();tt=gee.t_test(v);contrasts.append({'a':a,'b':b,'log_odds_difference':float(np.ravel(tt.effect)[0]),'p':float(np.ravel(tt.pvalue)[0])})
  wald=gee.wald_test(np.eye(len(gee.params))[1:]);R1['GEE_global_decoder_effect']={'wald_chi2':float(np.asarray(wald.statistic).squeeze()),'df':int(len(gee.params)-1),'p':float(np.asarray(wald.pvalue).squeeze())}
  adjusted=holm([x['p'] for x in contrasts]);
  for x,pv in zip(contrasts,adjusted):x['p_holm']=pv;x['significant_holm_0.05']=pv<.05
  R1['GEE']={'formula':'cue_correct_success ~ C(decoder)','family':'binomial','covariance':'exchangeable','cluster':'subject','n':len(R1df),'decoder_contrasts':contrasts,'model_summary':str(gee.summary())}
  raw=R1df[R1df.variant=='raw'];pairs=[]
  for a,b in it.combinations(models,2):
   wide=raw.pivot_table(index=['subject','pair_index'],columns='decoder',values='cue_correct_success',aggfunc='first').dropna(subset=[a,b]);tb=[[int(((wide[a]==1)&(wide[b]==1)).sum()),int(((wide[a]==1)&(wide[b]==0)).sum())],[int(((wide[a]==0)&(wide[b]==1)).sum()),int(((wide[a]==0)&(wide[b]==0)).sum())]]
   pval=float(mcnemar(tb,exact=True).pvalue);pairs.append({'a':a,'b':b,'n_pairs':int(len(wide)),'mcnemar_p_exact':pval})
  adj=holm([x['mcnemar_p_exact'] for x in pairs]);
  for x,pv in zip(pairs,adj):x['p_holm']=pv
  R1['McNemar_sensitivity']=pairs
  # Subject-cluster bootstrap absolute paired differences (raw variants), 10,000 draws.
  subj=sorted(raw.subject.unique());rng=np.random.default_rng(20261008);boot={f'{a}-{b}':[] for a,b in it.combinations(models,2)}
  subj_means=raw.groupby(['subject','decoder']).cue_correct_success.mean().unstack()
  for _ in range(10000):
   draw=rng.choice(subj,len(subj),replace=True)
   for a,b in it.combinations(models,2):
    vals=(subj_means.loc[draw,a]-subj_means.loc[draw,b]).dropna();boot[f'{a}-{b}'].append(float(vals.mean()) if len(vals) else 0.)
  R1['subject_cluster_bootstrap_risk_differences']={k:{'ci95':np.percentile(v,[2.5,97.5]).tolist(),'resamples':10000,'seed':20261008} for k,v in boot.items()}
 for vname,row in Q['variants'].items():
  subset=R1df[(R1df.decoder==vname.split('_')[0])&(R1df.variant==('plt' if vname.endswith('_plt') else 'raw'))]
  if not len(subset):continue
  ece_real=row['ece'];s=float(subset.cue_correct_success.mean());candidates=[]
  for reg in ['cal','flat']:
   for qq in sorted(D.q.unique()):
    # Registered emulator reliability target: calibrated ECE≈0; flat ECE≈|q−mean(conf)|, mean(conf)=0.85.
    target_ece=0.0 if reg=='cal' else abs(float(qq)-.85);em=D[(D.q==qq)&(D.regime==reg)&(D.rho==1.)].cue_correct_success.mean();candidates.append((abs(target_ece-ece_real),reg,float(qq),float(em)))
  reg=min(candidates)[1];curve=sorted([(x['q'],x['rate']) for x in cell_rows if x['regime']==reg and x['rho']==1],key=lambda z:z[0]);qx=np.asarray([x[0] for x in curve]);sy=np.asarray([x[1] for x in curve]);order=np.argsort(sy);q_est=float(np.interp(s,sy[order],qx[order]));subjects_v=sorted(subset.subject.unique());rngv=np.random.default_rng(20261008);qboot=[]
  smat=subset.groupby('subject').cue_correct_success.mean()
  for _ in range(10000):
   bs=rngv.choice(subjects_v,len(subjects_v),replace=True);ss=float(np.mean([smat.loc[z] for z in bs]));qboot.append(float(np.interp(ss,sy[order],qx[order])))
  qeq.append({'variant':vname,'observed_success':s,'ece':ece_real,'share_conf_ge_0.75':row['share_conf_ge_0.75'],'selected_emulator_regime':reg,'q_eq':q_est,'bootstrap95':np.percentile(qboot,[2.5,97.5]).tolist(),'resamples':10000,'seed':20261008,'status':'EXPLORATORY'})
  R1['H-R1']={'status':'tested' if Q['V1']['passed'] else 'descriptive_only','supported':bool(Q['V1']['passed'] and R1.get('GEE_global_decoder_effect',{}).get('p',1.)<.05),'note':'R1 inferential contrasts are conditional on V1.'}
 R1['q_eq']=qeq
family_p={'H-E1':H['H-E1']['cochran_armitage']['p_one_sided_increasing'],'H-E2':H['H-E2']['family_p_intersection_union'],'H-E3':H['H-E3']['family_p_bonferroni_global'],'H-E4':H['H-E4']['family_p_bonferroni_global']}
if R1.get('V1',{}).get('passed') and 'GEE_global_decoder_effect' in R1:family_p['H-R1']=R1['GEE_global_decoder_effect']['p']
fkeys=list(family_p);fadj=holm([family_p[k] for k in fkeys]);H['family_wise_Holm']={k:{'unadjusted_p':family_p[k],'holm_p':v,'significant_0.05':v<.05} for k,v in zip(fkeys,fadj)}
for k in ['H-E1','H-E2','H-E3','H-E4']:
 if k in H['family_wise_Holm']:
  H[k]['family_wise_holm_p']=H['family_wise_Holm'][k]['holm_p'];H[k]['supported']=bool(H[k].get('supported',False) and H['family_wise_Holm'][k]['significant_0.05'])
if 'H-R1' in R1:
 R1['H-R1']['family_wise_holm_p']=H['family_wise_Holm'].get('H-R1',{}).get('holm_p');R1['H-R1']['supported']=bool(R1['H-R1'].get('supported',False) and H['family_wise_Holm'].get('H-R1',{}).get('significant_0.05',False))
R1_episode_descriptive=[]
if r0path.exists():
 R1episodes=pd.read_csv(r0path);R1episodes=R1episodes[R1episodes.arm=='R1']
 for (decoder,variant),g in R1episodes.groupby(['decoder','variant'],sort=True):
  n=len(g)
  def ep_rate(col):
   k=int(g[col].astype(bool).sum());return {'successes':k,'rate':k/n,'exact95':exact(k,n)}
  R1_episode_descriptive.append({'decoder':decoder,'variant':variant,'n':n,'cue_correct_success':ep_rate('cue_correct_success'),'task_completion':ep_rate('task_completion'),'false_grasp':ep_rate('false_grasp'),'miss':ep_rate('miss')})
AN={'schema':'P6-C2-ANALYSIS-v1','per_cell':cell_rows,'hypotheses':H,'R0_descriptive':r0out,'R1':R1,'R1_episode_descriptive':R1_episode_descriptive,'sensitivity':sout,'R1_status':'AVAILABLE' if (RES/'decoder_quality_R1.json').exists() else 'BLOCKED_PENDING_WP5_DATA','multiplicity':'Holm, family-wise alpha=.05','intervals':'Clopper-Pearson exact 95% unless explicitly Newcombe','seed':20261008}
(RES/'ANALYSIS.json').write_text(json.dumps(AN,indent=2))
# F1 interface timeline with registered markers.
fig,ax=plt.subplots(figsize=(9,2.4));segments=[(0,2,'Warm-up','REST'),(2,3,'Decoy','decoder'),(3,4,'Scheduled REST','REST'),(4,5,'Grasp','decoder'),(5,7,'Tail','REST')]
for a,b,label,color in [(0,2,'Warm-up','#DDDDDD'),(2,3,'Decoy trial','#E69F00'),(3,4,'REST gap','#DDDDDD'),(4,5,'Grasp trial','#56B4E9'),(5,7,'REST tail','#DDDDDD')]:
 ax.barh(1,b-a,left=a,color=color,edgecolor='black');ax.text((a+b)/2,1,label,ha='center',va='center')
for x,label,y,rotation,ha in [(1.6,'approach',.35,45,'left'),(4.3,'grasp',.35,45,'left'),(4.9,'transport',.43,90,'right'),(5.0,'release',.12,90,'left')]:
 ax.axvline(x,color='#009E73',ls='--');ax.text(x,y,label,rotation=rotation,ha=ha,va='center',fontsize=8)
ax.set(xlim=(0,7),ylim=(0,1.8),xlabel='Time (s)',yticks=[]);ax.set_title('F1. C2 episode schedule and registered controller markers');fig.tight_layout();fig.savefig(FIG/'F1_interface_timeline.png');fig.savefig(FIG/'F1_interface_timeline.pdf');plt.close(fig)
# F2 dose response and F3 calibration crossover / F4 persistence.
fig,axs=plt.subplots(1,3,figsize=(12,3.5),sharey=True)
for ax,rho in zip(axs,[1.,.8,.5]):
 for reg in ['cal','flat']:
  sub=[x for x in cell_rows if x['rho']==rho and x['regime']==reg];sub.sort(key=lambda z:z['q']);x=[z['q'] for z in sub];y=[z['rate'] for z in sub];lo=[z['rate']-z['exact95'][0] for z in sub];hi=[z['exact95'][1]-z['rate'] for z in sub];ax.errorbar(x,y,yerr=[lo,hi],marker='o',label=f'{reg}: cue-correct',color=COL[reg],capsize=2)
  yt=[z['task_completion_rate'] for z in sub];tlo=[z['task_completion_rate']-z['task_completion_exact95'][0] for z in sub];thi=[z['task_completion_exact95'][1]-z['task_completion_rate'] for z in sub];ax.errorbar(x,yt,yerr=[tlo,thi],ls='--',marker='x',alpha=.75,color=COL[reg],label=f'{reg}: task completion (exact CI)',capsize=2)
 ax.set(title=f'ρ = {rho}',xlabel='Emulator accuracy q',ylim=(-.03,1.03));ax.grid(alpha=.2)
axs[0].set_ylabel('Cue-correct success (exact 95% CI)');handles,legend_labels=axs[-1].get_legend_handles_labels();fig.legend(handles,legend_labels,loc='lower center',bbox_to_anchor=(.5,.01),ncol=2,frameon=False);fig.suptitle('F2. Emulator dose–response',y=.98);fig.tight_layout(rect=[0,.16,1,.92]);fig.savefig(FIG/'F2_emulator_dose_response.png');fig.savefig(FIG/'F2_emulator_dose_response.pdf');plt.close(fig)
fig,ax=plt.subplots(figsize=(5.5,3.5));
for q in sorted(set(x['q'] for x in cell_rows)):
 c=next((x for x in cell_rows if x['q']==q and x['rho']==1 and x['regime']=='cal'),None);f=next((x for x in cell_rows if x['q']==q and x['rho']==1 and x['regime']=='flat'),None)
 if c and f:
  rd=f['rate']-c['rate'];lo,hi=confint_proportions_2indep(f['successes'],f['n'],c['successes'],c['n'],method='newcomb');ax.errorbar(q,rd,yerr=[[rd-lo],[hi-rd]],fmt='o',color='#CC79A7',capsize=2)
ax.axhline(0,color='black',lw=.8);ax.set(xlabel='q',ylabel='Risk difference (flat − calibrated)',title='F3. Calibration contrast, ρ=1');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(FIG/'F3_calibration_crossover.png');fig.savefig(FIG/'F3_calibration_crossover.pdf');plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(8,3.4));
for q in [.7,.8,.9]:
 sub=[x for x in cell_rows if x['q']==q and x['regime']=='cal'];sub.sort(key=lambda z:-z['rho']);slo=[x['rate']-x['exact95'][0] for x in sub];shi=[x['exact95'][1]-x['rate'] for x in sub];axs[0].errorbar([x['rho'] for x in sub],[x['rate'] for x in sub],yerr=[slo,shi],marker='o',label=f'q={q}',capsize=2);flo=[x['false_grasp_rate']-x['false_grasp_exact95'][0] for x in sub];fhi=[x['false_grasp_exact95'][1]-x['false_grasp_rate'] for x in sub];axs[1].errorbar([x['rho'] for x in sub],[x['false_grasp_rate'] for x in sub],yerr=[flo,fhi],marker='s',label=f'q={q}',capsize=2)
axs[0].set(xlabel='Persistence ρ',ylabel='Cue-correct success',title='Success');axs[0].legend(frameon=False);axs[1].set(xlabel='Persistence ρ',ylabel='False-grasp rate',title='False grasp');axs[1].legend(frameon=False);fig.suptitle('F4. Persistence and false-grasp outcomes');fig.tight_layout();fig.savefig(FIG/'F4_persistence_false_grasp.png');fig.savefig(FIG/'F4_persistence_false_grasp.pdf');plt.close(fig)
# F5/F6 real decoder panel is explicitly marked blocked if files absent.
if (RES/'decoder_quality_R1.json').exists():
 Q=json.load(open(RES/'decoder_quality_R1.json'));items=list(Q['variants'].items());fig,axs=plt.subplots(1,2,figsize=(11,4))
 labels=[x[0] for x in items];ba=[x[1]['balanced_accuracy'] for x in items];lo=[x[1]['balanced_accuracy']-x[1]['balanced_accuracy_exact95'][0] for x in items];hi=[x[1]['balanced_accuracy_exact95'][1]-x[1]['balanced_accuracy'] for x in items]
 axs[0].errorbar(range(len(items)),ba,yerr=[lo,hi],fmt='o',capsize=3,color='#0072B2');axs[0].set_xticks(range(len(items)),labels,rotation=45,ha='right');axs[0].set(ylabel='Pooled balanced accuracy (exact 95% CI)',title='Held-out quality');axs[0].axhline(.5,color='gray',ls='--')
 for name,row in items:
  rb=row['reliability_bins'];axs[1].plot([x['mean_confidence'] for x in rb],[x['accuracy'] for x in rb],marker='o',label=name,alpha=.8)
 axs[1].plot([.5,1],[.5,1],color='black',ls='--');axs[1].set(xlim=(.5,1),ylim=(0,1),xlabel='Mean confidence',ylabel='Accuracy',title='Reliability');axs[1].legend(fontsize=7,ncol=2,frameon=False);fig.suptitle('F5. Real-decoder quality (D5 is within-subject reference)');fig.tight_layout();fig.savefig(FIG/'F5_real_decoder_quality.png');fig.savefig(FIG/'F5_real_decoder_quality.pdf');plt.close(fig)
 qeq_rows=R1.get('q_eq',[]);fig,ax=plt.subplots(figsize=(7,4))
 for reg in ['cal','flat']:
  sub=sorted([x for x in cell_rows if x['rho']==1 and x['regime']==reg],key=lambda z:z['q']);ax.plot([x['q'] for x in sub],[x['rate'] for x in sub],marker='o',label=f'{reg} emulator')
 for x in qeq_rows:ax.errorbar(x['q_eq'],x['observed_success'],xerr=[[x['q_eq']-x['bootstrap95'][0]],[x['bootstrap95'][1]-x['q_eq']]],fmt='s',capsize=2,label=x['variant'])
 ax.set(xlabel='Accuracy / q-equivalent',ylabel='Cue-correct success',title='F6. Real decoders on emulator curve (EXPLORATORY)');ax.legend(fontsize=7,ncol=2,frameon=False);fig.tight_layout();fig.savefig(FIG/'F6_real_on_emulator_curve.png');fig.savefig(FIG/'F6_real_on_emulator_curve.pdf');plt.close(fig)
else:
 for n,title in [('F5_real_decoder_quality','F5. Real-decoder quality (WP5 unavailable)'),('F6_real_on_emulator_curve','F6. Equivalent accuracy (WP5 unavailable)')]:
  fig,ax=plt.subplots(figsize=(7,3));ax.text(.5,.5,'WP5 pending / blocked: EEGMMIDB acquisition and integrity validation',ha='center',va='center',wrap=True);ax.set_axis_off();ax.set_title(title);fig.savefig(FIG/f'{n}.png');fig.savefig(FIG/f'{n}.pdf');plt.close(fig)
# F7 sensitivity heatmap if present.
if sout:
 S=pd.DataFrame(sout);fig,axs=plt.subplots(2,4,figsize=(12,6),sharex=True,sharey=True)
 for ax,(q,reg) in zip(axs.flat,[(q,r) for q in [.6,.7,.8,.9] for r in ['cal','flat']]):
  z=S[(S.q==q)&(S.regime==reg)].pivot(index='threshold',columns='confirmation_windows',values='rate').sort_index(ascending=False);im=ax.imshow(z.to_numpy(),vmin=0,vmax=1,aspect='auto',cmap='viridis');ax.set_title(f'q={q}, {reg}');ax.set_xticks(range(len(z.columns)),z.columns);ax.set_yticks(range(len(z.index)),[f'{v:.2f}' for v in z.index]);ax.set_xlabel('' );ax.set_ylabel('' )
 fig.supxlabel('Confirmation windows',y=.04);fig.supylabel('Confidence threshold',x=.025);fig.suptitle('F7. Sensitivity heatmaps (Arm S)',y=.97);fig.subplots_adjust(left=.08,right=.88,bottom=.14,top=.87,wspace=.18,hspace=.3);cax=fig.add_axes([.91,.2,.022,.62]);fig.colorbar(im,cax=cax,label='cue-correct success');fig.savefig(FIG/'F7_sensitivity_heatmaps.png',bbox_inches='tight');fig.savefig(FIG/'F7_sensitivity_heatmaps.pdf',bbox_inches='tight');plt.close(fig)
# F8 regression control vs ceiling.
fig,ax=plt.subplots(figsize=(5,3.5));x0count=int(json.load(open(RES/'PREFLIGHT.json'))['X0'].get('successes',0));counts=[x0count,100];rates=[x/100 for x in counts];cis=[exact(x,100) for x in counts];ax.bar(['X0 C1 sparse','C2 oracle'],rates,color=['#D55E00','#009E73']);ax.errorbar([0,1],rates,yerr=[[rates[i]-cis[i][0] for i in range(2)],[cis[i][1]-rates[i] for i in range(2)]],fmt='none',ecolor='black',capsize=4);ax.set(ylabel='Cue-correct successes / 100 (exact 95% CI)',ylim=(0,1),title='F8. Regression control vs C2 ceiling');fig.tight_layout();fig.savefig(FIG/'F8_X0_vs_oracle.png');fig.savefig(FIG/'F8_X0_vs_oracle.pdf');plt.close(fig)
print('ANALYSIS_JSON_AND_FIGURES_DONE')
