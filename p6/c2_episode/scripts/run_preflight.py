#!/usr/bin/env python3
import csv, hashlib, json, os, platform, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
import scipy, matplotlib, yaml, statsmodels, sklearn, mujoco, mne, pyriemann
_C2=Path(__file__).resolve().parents[1]; _REPO=_C2.parents[1]
ROOT=_REPO; PROJ=_REPO; PROTO=_C2; OUT=Path(os.environ.get('C2_OUT',_C2)); REF=_C2/'scripts'
sys.path.insert(0,str(REF))
from c2_runner import run, episode
from c2_emulator_pilot import build, score, window_seq, draw_output
from c2_analytic_hold import expect

for p in ['registry','config','replay_csv/X0','replay_csv/E','replay_csv/R0','logs','results','figures']:
 (OUT/p).mkdir(parents=True,exist_ok=True)
sh=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

# WP0: environment/provenance, frozen controller comparison and archived C1 fixture/replay reproduction.
myo=Path(os.environ.get('MYOSIM_DIR',str(_REPO.parent/'myosim_repo'))); commit=os.popen(f'git -C {myo} rev-parse HEAD').read().strip()
assert commit=='67ee74e3230b068b5db760efa15da3669e315eb3',commit
cfg_c2=PROTO/'config/p6_c2_mysim.yaml'; cfg_c1=PROJ/'p6/c_mi_r04_primary/configs/p6_mi_r04_mysim.yaml'
# Compare numeric tokens in both configs, as required; also retain full textual diff.
import re,difflib
num=lambda s:re.findall(r'(?<![A-Za-z])[-+]?\d+(?:\.\d+)?',s)
a=cfg_c1.read_text(); b=cfg_c2.read_text(); numeric_equal=num(a)==num(b)
(OUT/'registry/CONFIG_DIFF.txt').write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='C1',tofile='C2')) if a!=b else 'Empty diff: C2 config is byte-identical to C1 config; no numeric parameter changes.\n')
# Re-execution of C1 archived fixture and named traces.
base=PROJ/'p6/c_mi_r04_primary'
checks=[]
for name,src,archive in [
 ('fixture',base/'replay_csv/fixture/pick_place_replay.csv',base/'results/myosim/fixture/pick_place_replay.json'),
 ('M1_S001',base/'replay_csv/decoder/M1_S001.csv',base/'results/myosim/decoder/M1_S001.json'),
 ('M3_S015',base/'replay_csv/decoder/M3_S015.csv',base/'results/myosim/decoder/M3_S015.json')]:
 rows=list(csv.DictReader(src.open()))
 events=[(float(r['timestamp_s']),r['label'],float(r['confidence'])) for r in rows]
 got,_=run(events); old=json.load(archive.open()); gm=got['task_metrics']; om=old['task_metrics']
 keys=['success','completion_time_s','path_length_m','final_error_m','command_corrections']
 comparisons={k:gm[k]==om[k] for k in keys}
 checks.append(dict(name=name,match=all(comparisons.values()),comparisons=comparisons,observed={k:gm[k] for k in keys},archived={k:om[k] for k in keys}))
if not numeric_equal or not all(x['match'] for x in checks):
 (OUT/'results/STOP_REPORT.md').write_text(json.dumps(dict(reason='WP0 C1 re-execution or config numeric diff failed',numeric_config_equal=numeric_equal,checks=checks),indent=2))
 raise SystemExit('STOP: WP0 failed')
env={'python':platform.python_version(),'platform':platform.platform(),'cpu':platform.processor(),'cpu_count':os.cpu_count(),'myosim_commit':commit,'myosim_version':'0.1.5','packages':{'numpy':np.__version__,'scipy':scipy.__version__,'pandas':pd.__version__,'matplotlib':matplotlib.__version__,'pyyaml':yaml.__version__,'statsmodels':statsmodels.__version__,'scikit_learn':sklearn.__version__,'mujoco':mujoco.__version__,'mne':mne.__version__,'pyriemann':pyriemann.__version__},'sha256':{'config_c1':sh(cfg_c1),'config_c2':sh(cfg_c2),'c1_fixture_csv':sh(base/'replay_csv/fixture/pick_place_replay.csv')},'c1_reexecution':checks,'numeric_config_equal':numeric_equal}
(OUT/'registry/ENVIRONMENT.json').write_text(json.dumps(env,indent=2))

# WP1 validity gates.
gates={}
# V3 ceiling: fixed oracle sequence, 100/100.
oracle=build([('OPEN',1.)]*10,[('CLOSE',1.)]*10)
oracle_score=[score(oracle) for _ in range(100)]
gates['V3']={'n':100,'successes':sum(x['cue_correct'] for x in oracle_score),'completion_times':sorted(set(x['grasp_onset'] for x in oracle_score)),'pass':all(x['cue_correct'] for x in oracle_score)}
# V2 calibrated chance: c=.5; no confident activation expected.
rng=np.random.default_rng(2026100802)
floor=[]
for i in range(100):
 d=window_seq(rng,'OPEN',.5,'cal',1.,10); g=window_seq(rng,'CLOSE',.5,'cal',1.,10)
 d=[(lab,.5) for lab,c in d];g=[(lab,.5) for lab,c in g]
 floor.append(score(build(d,g)))
gates['V2']={'n':100,'successes':sum(x['cue_correct'] for x in floor),'pass':sum(x['cue_correct'] for x in floor)<=1}
# Timing and real oracle event markers.
r,log=run(oracle)
trans=r['task_transitions']; markers={x['reason']:x['timestamp_s'] for x in trans}
gates['V4']={'cadence_below_stale':.1<float(yaml.safe_load(cfg_c2.read_text())['control']['stale_input_timeout_s']),'episode_below_timeout':7.0<float(yaml.safe_load(cfg_c2.read_text())['task']['timeout_s']),'markers_s':markers,'pass':(.1<.30 and 7.0<8.0 and abs(markers.get('approach_reached',-99)-1.6)<=.2 and abs(markers.get('decoded_grasp_command',-99)-4.3)<=.2 and abs(markers.get('transport_reached',-99)-4.9)<=.2)}
# Appendix A exact 16 configurations. Confidence levels match registered pass/fail cutoffs.
truth=[]
for dl in ['OPEN','CLOSE']:
 for dp in [False,True]:
  for gl in ['OPEN','CLOSE']:
   for gp in [False,True]:
    exp=bool(gl=='CLOSE' and gp and not (dl=='CLOSE' and dp))
    got=score(build([(dl,.9 if dp else .6)]*10,[(gl,.9 if gp else .6)]*10))
    truth.append({'decoy':dl,'decoy_pass':dp,'grasp':gl,'grasp_pass':gp,'expected':exp,'actual':got['cue_correct'],'pass':exp==got['cue_correct']})
gates['truth_table']={'n':16,'passed':sum(t['pass'] for t in truth),'cases':truth,'pass':all(t['pass'] for t in truth)}
# Determinism: serialize protocol endpoint/event information (no volatile provenance IDs/timestamps).
rng=np.random.default_rng(2026100803); deterministic=[]
for i in range(20):
 d=window_seq(rng,'OPEN',.65,'flat',.8,10);g=window_seq(rng,'CLOSE',.65,'flat',.8,10);ev=build(d,g)
 def canon():
  rr,ll=run(ev);rr.pop('provenance',None);return json.dumps({'result':rr,'log':ll},sort_keys=True,separators=(',',':'))
 deterministic.append(canon()==canon())
gates['determinism']={'n':20,'passed':sum(deterministic),'pass':all(deterministic)}
# X0 regression control: legacy cadence, 15 events and no REST; task clock expires before later events.
x0=[]
for i in range(100):
 ev=[]
 for j in range(15): ev.append((j*8.2,'CLOSE' if j%2 else 'OPEN',1.0))
 rr,ll=run(ev);tm=rr['task_metrics']; trans0=[x for x in rr['task_transitions'] if x['reason']=='decoded_grasp_command']
 x0.append(bool(tm['final_state']=='COMPLETE' and trans0))
gates['X0']={'n':100,'successes':sum(x0),'pass':sum(x0)==0}
# V5 pilot variability: 8 cells, 100 episodes each; all must be interior (Appendix B exceptions are q=.5/1 only).
v5=[]
for qi,q in enumerate([.6,.7,.8,.9]):
 for cal in ['cal','flat']:
  rng=np.random.default_rng(2026100804+qi*100+(cal=='flat'))
  obs=[score(build(window_seq(rng,'OPEN',q,cal,1.,10),window_seq(rng,'CLOSE',q,cal,1.,10)))['cue_correct'] for _ in range(100)]
  k=sum(obs);v5.append({'q':q,'regime':cal,'n':100,'successes':k,'pass':0<k<100})
gates['V5']={'cells':v5,'pass':all(x['pass'] for x in v5)}
gates['overall_pass']=all(v['pass'] for k,v in gates.items() if k!='overall_pass')
(OUT/'results/PREFLIGHT.json').write_text(json.dumps(gates,indent=2))
if not gates['overall_pass']:
 (OUT/'results/STOP_REPORT.md').write_text('WP1 validity gate failed; no parameter changes made.\n\n'+json.dumps(gates,indent=2))
 raise SystemExit('STOP: WP1 gate failed')

# Freeze inputs and reference code after WP0/WP1; before any decoder-conditioned/emulator study outcome.
files=[PROTO/'PROTOCOL_C2.md',PROTO/'c2_design.yaml',cfg_c2,REF/'c2_runner.py',REF/'c2_emulator_pilot.py',REF/'c2_analytic_hold.py']
manifest={'protocol_id':'P6-C2-EPISODE-v1.0','frozen_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'files':{str(p.relative_to(ROOT)):sh(p) for p in files},'preflight_passed':True,'myosim_commit':commit,'note':'C2 runner path constants MYO and P6 set to the execution workspace; no other reference-code edits.'}
(OUT/'registry/FREEZE_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'WP0':'PASS','WP1':'PASS','freeze':'written','gates':{k:v['pass'] for k,v in gates.items() if isinstance(v,dict) and 'pass' in v}},indent=2))
