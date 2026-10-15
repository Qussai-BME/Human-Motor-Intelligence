#!/usr/bin/env python3
import csv,gzip,hashlib,itertools,json,math,os,sys,time
from pathlib import Path
import numpy as np,pandas as pd,yaml
_C2=Path(__file__).resolve().parents[1]; _REPO=_C2.parents[1]
OUT=Path(os.environ.get('C2_OUT',_C2)); PROJ=_REPO; PROTO=_C2; REF=_C2/'scripts'
sys.path.insert(0,str(REF))
from c2_runner import run,write
from c2_emulator_pilot import build,window_seq,draw_output
from c2_analytic_hold import expect
from myosim.core.config import load_config
if not (OUT/'registry/FREEZE_MANIFEST.json').exists(): raise SystemExit('No successful preflight freeze; refusing to run WP2.')

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def result_from(events,cfg=None):
 r,log=run(events) if cfg is None else run(events,cfg=cfg); invalid=bool(r.get('invalid_state_detected',False)); attempts=0
 if invalid:
  attempts=1;first_log=log;r,log=run(events) if cfg is None else run(events,cfg=cfg);log=first_log+log;invalid=bool(r.get('invalid_state_detected',False))
 tm=r['task_metrics']; onset=[x['timestamp_s'] for x in r['task_transitions'] if x['reason']=='decoded_grasp_command']; onset=onset[0] if onset else None
 false=any(2.0<=t<4.0 and st=='EXECUTING' and cmd=='CLOSE' for t,l,st,cmd,ts in log)
 complete=tm['final_state']=='COMPLETE'; cue=bool(complete and onset is not None and 4.0<=onset<=5.5 and not false)
 if invalid:cue=False
 return r,log,dict(task_completion=bool(complete),false_grasp=bool(false),miss=bool(onset is None),cue_correct_success=cue,grasp_onset=onset,completion_time_s=tm.get('completion_time_s'),final_error_m=tm.get('final_error_m'),released_command_count=r.get('control_metrics',{}).get('released_command_count'),invalid_state_detected=invalid,invalid_state_reruns=attempts)
def save_run(arm,eid,events,log,row):
 rp=OUT/f'replay_csv/{arm}/{eid}.csv';rp.parent.mkdir(parents=True,exist_ok=True);write(events,rp);row['csv_sha256']=sha(rp)
 # Compact event records; write one gzip member per run into arm-level log stream.
 lp=OUT/f'logs/{arm}_events.csv.gz';lp.parent.mkdir(parents=True,exist_ok=True)
 with open(lp,'ab') as raw:
  with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as gz:
   import io
   txt=io.TextIOWrapper(gz,encoding='utf-8',newline='')
   w=csv.writer(txt);w.writerow(['episode_id','timestamp_s','label','controller_state','released_command','task_state'])
   for t,l,st,cmd,ts in log:w.writerow([eid,t,l,st,cmd,ts])
   txt.flush();txt.detach()
 return row

def append_result(path,row):
 path=OUT/f'results/{path}';path.parent.mkdir(parents=True,exist_ok=True)
 exists=path.exists()
 with path.open('a',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(row));
  if not exists:w.writeheader()
  w.writerow(row)

excl=OUT/'results/EXCLUSIONS.csv'
if not excl.exists():excl.write_text('arm,episode_id,reason,attempts\n')

# WP2: pre-registered 54 x 500 dose-response cells.
resfile=OUT/'results/emulator_episodes.csv'
qs=[.50,.55,.60,.65,.70,.75,.80,.90,1.00]; regimes=['cal','flat']; rhos=[1.,.8,.5]; cell=0; t0=time.time()
existing=pd.read_csv(resfile) if resfile.exists() and resfile.stat().st_size else pd.DataFrame()
for q,reg,rho in itertools.product(qs,regimes,rhos):
 cellseed=20261008+1000*cell; succ=0; saved=existing[existing.cell_index==cell] if len(existing) else pd.DataFrame(); n_saved=len(saved)
 if n_saved>500 or (n_saved and saved.episode_id.duplicated().any()):raise SystemExit(f'Corrupt WP2 checkpoint for cell {cell}')
 if n_saved:succ=int(saved.cue_correct_success.sum())
 for i in range(n_saved,500):
   seed=cellseed+i;rng=np.random.default_rng(seed)
   ds=window_seq(rng,'OPEN',q,reg,rho,10);gs=window_seq(rng,'CLOSE',q,reg,rho,10);events=build(ds,gs)
   r,log,out=result_from(events);succ+=out['cue_correct_success']
   row=dict(episode_id=f'E_c{cell:02d}_{i:04d}',arm='E',q=q,regime=reg,rho=rho,cell_index=cell,seed=seed,decoy_label=ds[0][0],decoy_pass=ds[0][1]>=.75,grasp_label=gs[0][0],grasp_pass=gs[0][1]>=.75,**out)
   row=save_run('E',row['episode_id'],events,log,row);append_result('emulator_episodes.csv',row)
   if out['invalid_state_detected']:append_result('EXCLUSIONS.csv',{'arm':'E','episode_id':row['episode_id'],'reason':'invalid_state_detected_after_rerun' if out['invalid_state_reruns'] else 'invalid_state_detected','attempts':out['invalid_state_reruns']+1})
   # Machine-readable deterministic per-run outcome JSON, no volatile provenance.
   (OUT/f'results/run_json/{row["episode_id"]}.json').parent.mkdir(parents=True,exist_ok=True)
   (OUT/f'results/run_json/{row["episode_id"]}.json').write_text(json.dumps(row,sort_keys=True,separators=(',',':')))
 if n_saved<500:print(f'WP2 cell {cell+1}/54 q={q} {reg} rho={rho} n=500 successes={succ} elapsed={time.time()-t0:.1f}s',flush=True)
 cell+=1

# WP3 analytic agreement for rho=1 cells, including exact binomial standard errors.
df=pd.read_csv(resfile); analytic=[]
for (q,reg),grp in df[df.rho==1.0].groupby(['q','regime']):
 pgrasp,pfalse=expect(float(q),str(reg)); p=pgrasp*(1-pfalse); obs=float(grp.cue_correct_success.mean()); se=float(math.sqrt(p*(1-p)/len(grp))); z=float((obs-p)/se if se else 0)
 analytic.append(dict(q=float(q),regime=str(reg),n=int(len(grp)),observed=obs,analytic=float(p),se=se,z=z,pass_gate=bool(abs(z)<=3 if se else obs==p)))
(OUT/'results/ANALYTIC_CROSSCHECK.json').write_text(json.dumps({'cells':analytic,'pass':bool(all(x['pass_gate'] for x in analytic))},indent=2))
if not all(x['pass_gate'] for x in analytic):
 (OUT/'results/STOP_REPORT.md').write_text('WP3 Monte Carlo vs analytic cross-check failed; no tuning performed.\n'+json.dumps(analytic,indent=2));raise SystemExit('STOP: WP3 failed')

# WP4 R0: existing M1-M3 C1 traces; pair ordered kth T1/T2 epochs, 7 pairs per subject.
r0path=OUT/'results/real_episodes.csv'
if not r0path.exists():
 base=PROJ/'p6/c_mi_r04_primary/traces'; models=['M1','M2','M3'];pairs_by_subject={}
 for subject in range(1,21):
  sid=f'S{subject:03d}';
  def getpairs(model):
   f=base/model/f'{model}_{sid}.csv'; d=pd.read_csv(f)
   t1=d[d.ground_truth=='OPEN'].reset_index(drop=True);t2=d[d.ground_truth=='CLOSE'].reset_index(drop=True)
   return [(t1.iloc[k],t2.iloc[k]) for k in range(7)]
  pairs_by_subject[sid]=getpairs('M1')
 for model in models+['ORACLE']:
  for sid,pairs in pairs_by_subject.items():
   tr=base/'M1'/f'M1_{sid}.csv' if model=='ORACLE' else base/model/f'{model}_{sid}.csv'; dd=pd.read_csv(tr);t1=dd[dd.ground_truth=='OPEN'].reset_index(drop=True);t2=dd[dd.ground_truth=='CLOSE'].reset_index(drop=True)
   for k in range(7):
    a=t1.iloc[k];b=t2.iloc[k]
    dl,dc=('OPEN',1.0) if model=='ORACLE' else (str(a.prediction),float(a.confidence));gl,gc=('CLOSE',1.0) if model=='ORACLE' else (str(b.prediction),float(b.confidence))
    ds=[(dl,dc)]*10;gs=[(gl,gc)]*10;ev=build(ds,gs);r,log,out=result_from(ev);eid=f'R0_{model}_{sid}_{k+1:02d}'
    row=dict(episode_id=eid,arm='R0',decoder=model,variant='existing_trace' if model!='ORACLE' else 'oracle',subject=sid,pair_index=k+1,decoy_label=dl,decoy_confidence=dc,grasp_label=gl,grasp_confidence=gc,**out)
    row=save_run('R0',eid,ev,log,row);append_result('real_episodes.csv',row)
    if out['invalid_state_detected']:append_result('EXCLUSIONS.csv',{'arm':'R0','episode_id':eid,'reason':'invalid_state_detected_after_rerun' if out['invalid_state_reruns'] else 'invalid_state_detected','attempts':out['invalid_state_reruns']+1})
    jf=OUT/f'results/run_json/{eid}.json';jf.parent.mkdir(parents=True,exist_ok=True);jf.write_text(json.dumps(row,sort_keys=True,separators=(',',':')))
  print('WP4 R0 completed',model,flush=True)

# WP7 pre-registered sensitivity (128 cells x 200); temporary config copies, primary untouched.
sfile=OUT/'results/sensitivity_episodes.csv'
cfg0=yaml.safe_load((PROTO/'config/p6_c2_mysim.yaml').read_text());cell=0;t0=time.time();s_existing=pd.read_csv(sfile) if sfile.exists() and sfile.stat().st_size else pd.DataFrame();cell_limit=int(os.environ.get('WP7_CELL_LIMIT','128'));cells_done=0
for q,reg,threshold,nconf in itertools.product([.6,.7,.8,.9],['cal','flat'],[.60,.70,.75,.85],[1,2,3,5]):
 if cells_done>=cell_limit:break
 saved=s_existing[s_existing.cell_index==cell] if len(s_existing) else pd.DataFrame();n_saved=len(saved)
 if n_saved>200 or (n_saved and saved.episode_id.duplicated().any()):raise SystemExit(f'Corrupt WP7 checkpoint for cell {cell}')
 if n_saved<200:
  cfg=yaml.safe_load(yaml.safe_dump(cfg0));cfg['control']['confidence_threshold']=threshold;cfg['control']['confirmation_windows']=nconf
  cf=OUT/f'config/S_c{cell:03d}.yaml';cf.parent.mkdir(parents=True,exist_ok=True);cf.write_text(yaml.safe_dump(cfg,sort_keys=False));cfhash=sha(cf);loaded=load_config(cf)
  seedbase=20261008+200000+1000*cell;ok=int(saved.cue_correct_success.sum()) if n_saved else 0
  for i in range(n_saved,200):
   seed=seedbase+i;rng=np.random.default_rng(seed);ds=window_seq(rng,'OPEN',q,reg,1.,10);gs=window_seq(rng,'CLOSE',q,reg,1.,10);ev=build(ds,gs)
   # Use the frozen runner with only the predeclared temporary sensitivity config.
   rr,lg,out=result_from(ev,loaded);tm=rr['task_metrics'];on=out['grasp_onset'];false=out['false_grasp'];complete=out['task_completion'];cue=out['cue_correct_success'];ok+=cue
   row=dict(episode_id=f'S_c{cell:03d}_{i:04d}',arm='S',q=q,regime=reg,threshold=threshold,confirmation_windows=nconf,cell_index=cell,seed=seed,task_completion=complete,false_grasp=false,miss=out['miss'],cue_correct_success=cue,grasp_onset=on,completion_time_s=tm.get('completion_time_s'),final_error_m=tm.get('final_error_m'),released_command_count=rr.get('control_metrics',{}).get('released_command_count'),invalid_state_detected=out['invalid_state_detected'],invalid_state_reruns=out['invalid_state_reruns'],config_sha256=cfhash)
   save_run('S',row['episode_id'],ev,lg,row);append_result('sensitivity_episodes.csv',row)
   if out['invalid_state_detected']:append_result('EXCLUSIONS.csv',{'arm':'S','episode_id':row['episode_id'],'reason':'invalid_state_detected_after_rerun' if out['invalid_state_reruns'] else 'invalid_state_detected','attempts':out['invalid_state_reruns']+1})
   jf=OUT/f'results/run_json/{row["episode_id"]}.json';jf.parent.mkdir(parents=True,exist_ok=True);jf.write_text(json.dumps(row,sort_keys=True,separators=(',',':')))
  print(f'WP7 cell {cell+1}/128 q={q} {reg} thr={threshold} conf={nconf} success={ok}/200',flush=True)
  cells_done+=1
 cell+=1
total_cells=int(s_existing.cell_index.nunique()) if len(s_existing) else 0
if sfile.exists() and sfile.stat().st_size:total_cells=pd.read_csv(sfile).cell_index.nunique()
print(f'WP2/WP3/WP4 processed; WP7 cumulative complete cells={total_cells}/128; this invocation={cells_done}; cell_limit={cell_limit}',flush=True)
