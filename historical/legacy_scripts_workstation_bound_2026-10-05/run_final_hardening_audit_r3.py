from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path
ROOT=Path('<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1')

def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def load(p): return json.loads(p.read_text())
def check(name, ok, detail): print(json.dumps({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})); return ok

def main():
 checks=[]
 p4=ROOT/'results/extensions/v2-cpu-q1-upgrade-r3-004/p4_representation_ablation_loso'; p4r=ROOT/'results/extensions/v2-cpu-q1-upgrade-r3-004-independent-rerun/p4_representation_ablation_loso'
 p5=ROOT/'results/extensions/v2-cpu-q1-upgrade-r3-003/p5_strict_selective_clean_train_corrupted_test_loso'
 cal=ROOT/'results/extensions/v2-cpu-q1-upgrade-r3-005/p5_clean_loso_calibration'; calr=ROOT/'results/extensions/v2-cpu-q1-upgrade-r3-005-independent-rerun/p5_clean_loso_calibration'
 for a,b,n in [(p4/'subject_level_results.json',p4r/'subject_level_results.json','P4 representation rerun'),(cal/'trial_probabilities.json',calr/'trial_probabilities.json','P5 calibration rerun')]: checks.append(check(n,sha(a)==sha(b),sha(a)))
 rows=load(p4/'subject_level_results.json'); groups={r['condition']:[] for r in rows}
 for r in rows: groups[r['condition']].append(r['subject'])
 checks.append(check('P4 representation subject-level design',set(groups)=={'temporal','spectral','covariance_log'} and all(len(v)==54 and len(set(v))==54 for v in groups.values()),str({k:len(v) for k,v in groups.items()})))
 rows5=load(p5/'subject_level_results.json'); subs=sorted({r['subject'] for r in rows5}); conds=sorted({r['condition'] for r in rows5}); variants=sorted({(r['variant'],r['level_percent']) for r in rows5}); checks.append(check('P5 strict robustness subject-level design',len(subs)==24 and len(conds)==5 and len(variants)==7 and len(rows5)==24*5*7,f'subjects={len(subs)},conditions={len(conds)},variants={len(variants)},rows={len(rows5)}'))
 src=(ROOT/'scripts/run_p5_cpu_q1_strict_r3_003.py').read_text(); checks.append(check('P5 clean-train corrupted-test code boundary','train = [p for p in subjects if p != held]' in src and 'fit(eegtr, ytr)' in src and 'fit(emgtr, ytr)' in src and 'training_is_clean_for_all_test_variants' in src,'train-only fitting and explicit clean-training protocol found'))
 src4=(ROOT/'scripts/run_p4_representation_ablation_r3_004.py').read_text(); checks.append(check('P4 LOSO code boundary','train = [p for p in subjects if p != held]' in src4 and 'fit(xtr, ytr)' in src4 and 'xte = feature_cache[held.stem]' in src4,'held-out subject excluded from fit'))
 stats=load(cal/'calibration_statistics.json'); checks.append(check('P5 calibration conditions',set(x['condition'] for x in stats['conditions'])=={'eeg_only','emg_only','static_mean_fusion','confidence_weighted_fusion','confidence_selective_fusion'},'five predeclared conditions'))
 print(json.dumps({'overall':'PASS' if all(checks) else 'FAIL','checks':len(checks)}))
 return 0 if all(checks) else 2
if __name__=='__main__': raise SystemExit(main())
