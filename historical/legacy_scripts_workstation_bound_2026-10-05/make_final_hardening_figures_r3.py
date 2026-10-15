from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path('<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1')
data=json.loads((ROOT/'results/extensions/v2-final-q1-hardening-r3-001/final_hardening_statistics.json').read_text())
out=ROOT/'results/extensions/v2-final-q1-hardening-r3-001/figures'; out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':180})
# P4 paired differences
c=data['p4_representation']['comparisons']; labs=[f"{x['left']}\nvs\n{x['right']}" for x in c]; vals=[x['mean_difference'] for x in c]; lo=[x['bootstrap_95_ci_mean_difference'][0] for x in c]; hi=[x['bootstrap_95_ci_mean_difference'][1] for x in c]
fig,ax=plt.subplots(figsize=(8,4.5)); x=np.arange(len(vals)); ax.errorbar(x,vals,yerr=[np.array(vals)-lo,np.array(hi)-np.array(vals)],fmt='o',color='#245a78',ecolor='#245a78',capsize=5); ax.axhline(0,color='#777',lw=.8); ax.set_xticks(x,labs); ax.set_ylabel('Mean paired macro-F1 difference'); ax.set_title('P4 representation triangulation — subject-level paired differences'); ax.grid(axis='y',alpha=.2); fig.tight_layout(); fig.savefig(out/'p4_representation_paired_differences.png',bbox_inches='tight'); plt.close(fig)
# P5 clean/degraded
s=data['p5_clean_train_corrupted_test']['summary']; labs=[x['condition'].replace('_',' ').title() for x in s]; clean=[x['clean_mean_macro_f1'] for x in s]; deg=[x['degraded_mean_macro_f1'] for x in s]; x=np.arange(len(s)); w=.36
fig,ax=plt.subplots(figsize=(8,4.5)); ax.bar(x-w/2,clean,w,label='Clean',color='#245a78'); ax.bar(x+w/2,deg,w,label='20% EEG feature zeroing',color='#b66a3c'); ax.set_xticks(x,labs,rotation=20,ha='right'); ax.set_ylabel('Mean subject-level macro-F1'); ax.set_title('P5 clean-train / corrupted-test robustness'); ax.legend(frameon=False); ax.grid(axis='y',alpha=.2); fig.tight_layout(); fig.savefig(out/'p5_clean_vs_degraded_robustness.png',bbox_inches='tight'); plt.close(fig)
print(*sorted(str(p) for p in out.glob('*.png')),sep='\n')
