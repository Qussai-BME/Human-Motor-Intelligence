from pathlib import Path
import json
import matplotlib.pyplot as plt
import numpy as np

repo=Path('<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1')
out=repo/'results/extensions/v2-cpu-q1-upgrade-r3-005/figures'; out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':180})

# calibration
p=json.loads((repo/'audit/p5_calibration_statistics_r3_005.json').read_text())['conditions']
labels=[x['condition'].replace('_',' ').title() for x in p]; b=[x['brier_score'] for x in p]; e=[x['ece_10_bin'] for x in p]; acc=[x['accuracy'] for x in p]
fig,ax=plt.subplots(1,3,figsize=(12,3.6)); x=np.arange(len(labels));
for a,v,t in zip(ax,[acc,b,e],['Accuracy','Multiclass Brier (lower is better)','ECE (lower is better)']): a.bar(x,v,color='#245a78'); a.set_xticks(x,labels,rotation=35,ha='right'); a.set_title(t); a.grid(axis='y',alpha=.2)
fig.suptitle('P5 clean LOSO calibration extension (R3-005)'); fig.tight_layout(); fig.savefig(out/'p5_calibration_summary.png',bbox_inches='tight'); plt.close(fig)

# P5 corruption/fallback aggregate if exists
for name in ['p5_strict_corruption','p5_missing_modality_fallback']:
 candidates=list((repo/'results/extensions').glob(f'**/{name}/subject_level_results.json'))
 if not candidates: continue
 rows=json.loads(candidates[0].read_text()); groups={}
 for r in rows:
  k=(r.get('condition') or r.get('variant') or 'unknown',r.get('level_percent',r.get('dropout_percent',0))); groups.setdefault(k,[]).append(r.get('accuracy',r.get('balanced_accuracy')))
 keys=list(groups); vals=[np.mean(groups[k]) for k in keys]; labs=[f'{k[0]}\n{k[1]}%' for k in keys]
 fig,ax=plt.subplots(figsize=(10,4)); ax.bar(np.arange(len(keys)),vals,color='#6c8e23'); ax.set_xticks(np.arange(len(keys)),labs,rotation=45,ha='right'); ax.set_ylabel('Mean subject-level accuracy'); ax.set_title(name.replace('_',' ').title()); ax.grid(axis='y',alpha=.2); fig.tight_layout(); fig.savefig(out/f'{name}.png',bbox_inches='tight'); plt.close(fig)

# P4 representation comparison if available
candidates=list((repo/'results/extensions').glob('**/p4*representation*/*json'))+list((repo/'results/extensions').glob('**/representation*/*json'))
for c in candidates:
 try:
  obj=json.loads(c.read_text())
  rows=obj.get('conditions',obj if isinstance(obj,list) else [])
  if rows and isinstance(rows[0],dict) and 'representation' in rows[0]:
   gs={};
   for r in rows: gs.setdefault(r['representation'],[]).append(r.get('accuracy',r.get('balanced_accuracy')))
   labs=list(gs); vals=[np.mean(gs[k]) for k in labs]; fig,ax=plt.subplots(figsize=(7,4)); ax.bar(labs,vals,color='#9b4d68'); ax.set_ylabel('Mean subject-level accuracy'); ax.set_title('P4 representation ablation'); ax.grid(axis='y',alpha=.2); fig.tight_layout(); fig.savefig(out/'p4_representation_comparison.png',bbox_inches='tight'); plt.close(fig); break
 except Exception: pass
print('\n'.join(str(x) for x in sorted(out.glob('*.png'))))
