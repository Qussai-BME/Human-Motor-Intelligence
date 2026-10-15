import json
from pathlib import Path
from scipy.stats import friedmanchisquare
p=Path('<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1/results/extensions/v2-cpu-q1-upgrade-r3-003/p5_strict_selective_clean_train_corrupted_test_loso/subject_level_results.json')
rows=json.loads(p.read_text())
conds=['eeg_only','emg_only','static_mean_fusion','confidence_weighted_fusion','confidence_selective_fusion']
# restrict to clean rows and use macro-F1
by={c:{} for c in conds}
for r in rows:
 if r.get('variant')=='clean' and r.get('level_percent')==0 and r['condition'] in by: by[r['condition']][r['subject']]=r['macro_f1']
subs=sorted(set.intersection(*(set(v) for v in by.values())))
res=friedmanchisquare(*[[by[c][s] for s in subs] for c in conds])
print(json.dumps({'conditions':conds,'n_subjects':len(subs),'chi2':float(res.statistic),'df':len(conds)-1,'p':float(res.pvalue)},indent=2))
