from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.stats import wilcoxon

ROOT=Path('<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1')
OUT=ROOT/'results/extensions/v2-final-q1-hardening-r3-001'; OUT.mkdir(parents=True,exist_ok=True)
RNG=np.random.default_rng(20260831)

def boot(x, n=10000):
 x=np.asarray(x,float); means=np.mean(x[RNG.integers(0,len(x),size=(n,len(x)))],axis=1)
 return [float(np.quantile(means,.025)),float(np.quantile(means,.975))]
def effect(d): return float(np.mean(d)/np.std(d,ddof=1))
def holm(ps):
    order=np.argsort(ps); adj=np.empty(len(ps),float); running=0.0
    for rank,idx in enumerate(order):
        value=(len(ps)-rank)*float(ps[idx]); running=max(running,value); adj[idx]=min(1.0,running)
    return adj

def p4():
 rows=json.loads((ROOT/'results/extensions/v2-cpu-q1-upgrade-r3-004/p4_representation_ablation_loso/subject_level_results.json').read_text())
 tab={}
 for r in rows: tab.setdefault(r['subject'],{})[r['condition']]=r['macro_f1']
 pairs=[('temporal','spectral'),('temporal','covariance_log'),('spectral','covariance_log')]
 out=[]; raw=[]
 for a,b in pairs:
  subs=sorted(tab); d=np.array([tab[s][a]-tab[s][b] for s in subs]); w=wilcoxon(d,alternative='two-sided',zero_method='wilcox',method='auto')
  raw.append(float(w.pvalue)); out.append({'left':a,'right':b,'n_subjects':len(d),'mean_difference':float(d.mean()),'median_difference':float(np.median(d)),'bootstrap_95_ci_mean_difference':boot(d),'wilcoxon_p_raw':float(w.pvalue),'effect_size_mean_over_sd':effect(d),'positive_difference_subjects':int(np.sum(d>0))})
 adj=holm(raw)
 for r,p in zip(out,adj): r['wilcoxon_p_holm']=float(p)
 return {'comparisons':out,'n_subjects':len(tab),'claim_boundary':'Representation-specific subject-independent evidence under OpenBMI strict zero-calibration LOSO; not a universal statement about Riemannian methods.'}

def p5():
 path=ROOT/'results/extensions/v2-cpu-q1-upgrade-r3-003/p5_strict_selective_clean_train_corrupted_test_loso/subject_level_results.json'; rows=json.loads(path.read_text())
 wanted={'eeg_only','static_mean_fusion','confidence_selective_fusion'}; tab={}
 for r in rows:
  if r['condition'] in wanted and ((r['variant']=='clean' and r['level_percent']==0) or (r['variant']=='eeg_dropout' and r['level_percent']==20)): tab.setdefault(r['subject'],{})[(r['condition'],r['level_percent'])]=r['macro_f1']
 summary=[]; comparisons=[]
 for c in sorted(wanted):
  clean=np.array([tab[s][(c,0)] for s in sorted(tab)]); deg=np.array([tab[s][(c,20)] for s in sorted(tab)]); d=clean-deg; ret=deg/np.where(clean!=0,clean,np.nan)
  summary.append({'condition':c,'n_subjects':len(clean),'clean_mean_macro_f1':float(clean.mean()),'degraded_mean_macro_f1':float(deg.mean()),'mean_degradation_drop':float(d.mean()),'median_degradation_drop':float(np.median(d)),'bootstrap_95_ci_mean_drop':boot(d),'mean_relative_retention':float(np.nanmean(ret)),'median_relative_retention':float(np.nanmedian(ret))})
 for a,b in [('static_mean_fusion','eeg_only'),('confidence_selective_fusion','eeg_only'),('static_mean_fusion','confidence_selective_fusion')]:
  dc=np.array([tab[s][(a,20)]-tab[s][(b,20)] for s in sorted(tab)]); pval=1.0 if np.allclose(dc,0) else float(wilcoxon(dc,method='auto').pvalue); comparisons.append({'degraded_left':a,'degraded_right':b,'n_subjects':len(dc),'mean_difference':float(dc.mean()),'median_difference':float(np.median(dc)),'bootstrap_95_ci_mean_difference':boot(dc),'wilcoxon_p_raw':pval,'effect_size_mean_over_sd':0.0 if np.allclose(dc,0) else effect(dc)})
 return {'summary':summary,'degraded_pairwise_comparisons':comparisons,'primary_robustness_quantity':'clean macro-F1 minus degraded macro-F1','retention_interpretation':'descriptive secondary quantity; not treated as an inferential endpoint','corruption':'20% EEG feature-group zeroing; models trained on clean data only','claim_boundary':'Feature-cache degradation under the evaluated P5 protocol; not physical electrode failure or clinical hardware robustness.'}

result={'p4_representation':p4(),'p5_clean_train_corrupted_test':p5(),'p4_calibration_status':{'status':'not_estimable_from_retained_artifacts','reason':'retained P4 outputs contain labels/predictions but no probability or decision-score artifact; no confidence metric will be reconstructed from hard labels.'},'p4_robustness_status':{'status':'skipped_after_cpu_gate','reason':'previous implementation exceeded practical CPU limits without producing an artifact; specification permits skipping.'}}
(OUT/'final_hardening_statistics.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
