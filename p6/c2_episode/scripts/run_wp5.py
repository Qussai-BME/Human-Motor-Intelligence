#!/usr/bin/env python3
"""Registered P6-C2 WP5. Starts only after the emulator and sensitivity arms finish."""
import concurrent.futures,hashlib,json,math,os,subprocess,sys,time,urllib.request
from pathlib import Path
import numpy as np,pandas as pd,mne
from scipy.signal import welch,butter,sosfiltfilt
from scipy.integrate import trapezoid
from sklearn.base import clone
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import balanced_accuracy_score
from sklearn.covariance import OAS
from mne.decoding import CSP
from pyriemann.estimation import Covariances
from pyriemann.tangentspace import TangentSpace
_C2=Path(__file__).resolve().parents[1]; _REPO=_C2.parents[1]
OUT=Path(os.environ.get('C2_OUT',_C2));DATA=Path(os.environ.get('EEGMMIDB_DIR',str(_C2/'data_eegmmidb')));PROJ=_REPO;REF=_C2/'scripts';sys.path.insert(0,str(REF))
from c2_runner import run,write
from c2_emulator_pilot import build
if not (OUT/'results/sensitivity_episodes.csv').exists():raise SystemExit('WP7 not complete; WP5 must run last.')
DATA.mkdir(parents=True,exist_ok=True); runs=['R04','R08','R12']
# Fetch only requested runs from the official no-auth S3 mirror, with PhysioNet fallback.
# Remote Content-Length prevents a killed prior transfer from being mistaken for a complete EDF.
def remote_size(url):
 req=urllib.request.Request(url,method='HEAD')
 with urllib.request.urlopen(req,timeout=30) as resp:return int(resp.headers['Content-Length'])
def getfile(s,r):
 p=DATA/f'S{s:03d}'/f'S{s:03d}{r}.edf';p.parent.mkdir(parents=True,exist_ok=True)
 rel=f'eegmmidb/1.0.0/S{s:03d}/S{s:03d}{r}.edf';urls=[f'https://physionet-open.s3.amazonaws.com/{rel}',f'https://physionet.org/files/{rel}'];notes=[]
 for url in urls:
  try:expected=remote_size(url)
  except Exception as e:notes.append(f'HEAD {url}: {e}');continue
  if p.exists() and p.stat().st_size==expected:return p,None
  tmp=p.with_suffix('.edf.part');tmp.unlink(missing_ok=True)
  try:
   q=subprocess.run(['curl','-fL','--retry','3','--retry-delay','1','--retry-connrefused','--connect-timeout','30','--max-time','240','--silent','--show-error','--output',str(tmp),url],capture_output=True,text=True,timeout=300)
   if q.returncode==0 and tmp.exists() and tmp.stat().st_size==expected:tmp.replace(p);return p,None
   notes.append(f'GET {url}: curl exit {q.returncode}; bytes={tmp.stat().st_size if tmp.exists() else 0}/{expected}; {q.stderr[-300:]}')
  except Exception as e:notes.append(f'GET {url}: {e}')
  tmp.unlink(missing_ok=True)
 return None,' | '.join(notes)
jobs=[(s,r) for s in range(1,110) for r in runs]; errors=[];done=0
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
 futs={ex.submit(getfile,s,r):(s,r) for s,r in jobs}
 for fut in concurrent.futures.as_completed(futs):
  s,r=futs[fut];p,e=fut.result();done+=1
  if e:errors.append({'subject':f'S{s:03d}','run':r,'error':e})
  else:print(f'WP5 download {done}/{len(jobs)}: S{s:03d}{r} ({p.stat().st_size} bytes)',flush=True)
if errors:
 (OUT/'results/WP5_DOWNLOAD_ERRORS.json').write_text(json.dumps(errors,indent=2))
 (OUT/'results/WP5_STATUS.json').write_text(json.dumps({'status':'BLOCKED_DOWNLOAD','errors':len(errors),'examples':errors[:12]},indent=2))
 raise SystemExit(f'WP5 blocked: {len(errors)} EDF downloads failed; other arms remain complete.')

manifest_file=OUT/'registry/EEGMMIDB_MANIFEST.csv';exclusion_file=OUT/'registry/SUBJECT_EXCLUSIONS.csv';store_meta_file=OUT/'registry/EEGMMIDB_STORE_METADATA.json'
prev_manifest_sha=hashlib.sha256(manifest_file.read_bytes()).hexdigest() if manifest_file.exists() else None
need_eeg_arrays=True;cached_store=None
try:
 fm=json.loads((OUT/'results/WP5_FEATURES.json').read_text());cm=json.loads((OUT/'results/WP5_CV_PREDICTIONS.json').read_text());dm=json.loads((OUT/'results/WP5_D5_PREDICTIONS.json').read_text())
 caches_ready=all(p.exists() for p in [OUT/'results/WP5_FEATURES.npz',OUT/'results/WP5_CV_PREDICTIONS.npz',OUT/'results/WP5_D5_PREDICTIONS.npz']) and prev_manifest_sha is not None and all(x.get('manifest_sha256')==prev_manifest_sha for x in [fm,cm,dm]) and int(cm.get('completed_folds',0))==5 and len(dm.get('done_subjects',[]))==int(fm.get('subjects',0))
except Exception:caches_ready=False
if caches_ready:
 md=pd.read_csv(manifest_file)
 def verify_file(row):
  p=Path(str(row['path']))
  if not p.is_file() or p.stat().st_size!=int(row['bytes']):return False
  h=hashlib.sha256()
  with p.open('rb') as f:
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
  return h.hexdigest()==str(row['sha256'])
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:hash_ok=all(ex.map(verify_file,md.to_dict('records')))
 if hash_ok:
  need_eeg_arrays=False
  if store_meta_file.exists():
   sm=json.loads(store_meta_file.read_text())
   if sm.get('manifest_sha256')==prev_manifest_sha:cached_store=sm
  print(f'WP5 cached EEG manifest verified: {len(md)}/{len(md)} SHA-256 entries',flush=True)
 else:print('WP5 cached manifest SHA mismatch; performing full waveform validation.',flush=True)
def extract(path,load_eeg=True):
 raw=mne.io.read_raw_edf(path,preload=load_eeg,verbose='ERROR');picks=mne.pick_types(raw.info,eeg=True,exclude=[]);desc=list(raw.annotations.description);onsets=list(raw.annotations.onset)
 selected=[(float(t),d.strip()) for t,d in zip(onsets,desc) if d.strip() in ('T1','T2')];fs=float(raw.info['sfreq'])
 if fs!=160.0 or len(picks)!=64 or len(selected)!=15 or set(d for _,d in selected)-{'T1','T2'}:
  raise ValueError(f'integrity: fs={fs}, channels={len(picks)}, imagery_events={len(selected)}, labels={set(d for _,d in selected)}')
 eeg=raw.get_data(picks=picks).astype(np.float32) if load_eeg else None;nsamples=eeg.shape[1] if load_eeg else raw.n_times
 ep=[];lab=[];source=[];on=[]
 for t,d in selected:
  a=int(round((t+1.0)*fs));b=int(round((t+3.5)*fs))
  if b>nsamples:raise ValueError(f'epoch truncated at onset {t}')
  if load_eeg:ep.append(eeg[:,a:b])
  lab.append(1 if d=='T1' else 2);source.append(d);on.append(t)
 return (np.asarray(ep,dtype=np.float32) if load_eeg else None),np.asarray(lab,dtype=int),np.asarray(on),source

store={};excluded=[];manifest=[]
if cached_store is not None:
 for subject,rr in cached_store['subjects'].items():store[subject]={r:(None,np.asarray(rr[r]['labels'],dtype=int),np.asarray(rr[r]['onsets'],dtype=float),rr[r]['source']) for r in runs}
 excluded=cached_store['excluded'];manifest=md.to_dict('records');print(f'WP5 event metadata cache loaded: {len(store)} subjects',flush=True)
else:
 for sid in range(1,110):
  subject=f'S{sid:03d}'
  try:
   rr={r:extract(DATA/subject/f'{subject}{r}.edf',load_eeg=need_eeg_arrays) for r in runs};store[subject]=rr
   for r in runs:
    p=DATA/subject/f'{subject}{r}.edf';manifest.append({'subject':subject,'run':r,'path':str(p.relative_to(DATA)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'fs_hz':160,'channels':64,'imagery_events':15})
  except Exception as e:excluded.append({'subject':subject,'reason':str(e)})
  print(f'WP5 integrity {sid}/109: valid={len(store)} excluded={len(excluded)}',flush=True)
 exclusion_file.write_text('subject,reason\n'+''.join(f'"{x["subject"]}","{x["reason"].replace(chr(34),chr(39))}"\n' for x in excluded))
 manifest_file.write_text(pd.DataFrame(manifest).to_csv(index=False))
 if not need_eeg_arrays:
  sm={'manifest_sha256':hashlib.sha256(manifest_file.read_bytes()).hexdigest(),'excluded':excluded,'subjects':{s:{r:{'labels':rr[r][1].tolist(),'onsets':rr[r][2].tolist(),'source':rr[r][3]} for r in runs} for s,rr in store.items()}}
  store_meta_file.write_text(json.dumps(sm,separators=(',',':')));print('WP5 event metadata cache saved',flush=True)
if not store:
 (OUT/'results/WP5_STATUS.json').write_text(json.dumps({'status':'BLOCKED_INTEGRITY','valid_subjects':0,'excluded_subjects':len(excluded),'reason':'no subjects passed the registered integrity check'},indent=2))
 raise SystemExit('WP5 blocked: no subjects passed the registered integrity check.')
# Combine valid subjects. Test epochs are ordered by subject, run, and cue time.
X=[] if need_eeg_arrays else None;y=[];groups=[];runs_idx=[];source=[];onsets=[];subject_epochs={}
for subject,rr in store.items():
 subject_epochs[subject]={}
 for r in runs:
  ep,lab,on,src=rr[r];subject_epochs[subject][r]={'X':ep,'y':lab,'onsets':on,'source':src}
  if need_eeg_arrays:X.extend(ep)
  y.extend(lab);groups.extend([subject]*len(lab));runs_idx.extend([r]*len(lab));source.extend(src);onsets.extend(on)
if need_eeg_arrays:X=np.asarray(X,dtype=np.float32)
y=np.asarray(y);groups=np.asarray(groups);runs_idx=np.asarray(runs_idx);source=np.asarray(source);onsets=np.asarray(onsets)
# Feature functions mirror C1 Welch relative log power for D1/D2; channels 8-64 (zero-index 7:64).
def band_features(epochs,mode):
 bands=[(8,30)] if mode=='D1' else [(8,12),(13,30)];out=np.empty((len(epochs),57*len(bands)),np.float32)
 for i,ep in enumerate(epochs):
  if i and i%500==0:print(f'WP5 features {mode}: {i}/{len(epochs)}',flush=True)
  row=[]
  for ch in range(7,64):
   f,p=welch(ep[ch],fs=160,nperseg=min(256,ep.shape[-1]));tot=trapezoid(p[(f>=4)&(f<=40)],f[(f>=4)&(f<=40)])+1e-12
   for lo,hi in bands:
    m=(f>=lo)&(f<=hi);row.append(np.log((trapezoid(p[m],f[m])+1e-12)/tot))
  out[i]=row
 return out

# Fixed decoder factories.
def make_model(name):
 if name in ('D1','D2'):
  return Pipeline([('scale',StandardScaler()),('clf',LogisticRegression(C=.1 if name=='D1' else 1.,max_iter=2000,random_state=20261008))])
 if name=='D3':
  return Pipeline([('csp',CSP(n_components=6,reg='ledoit_wolf',log=True,norm_trace=False)),('lda',LinearDiscriminantAnalysis(solver='lsqr',shrinkage='auto'))])
 return Pipeline([('cov',Covariances(estimator='oas')),('tan',TangentSpace(metric='riemann')),('scale',StandardScaler()),('clf',LogisticRegression(C=1.,max_iter=2000,random_state=20261008))])
manifest_sha=hashlib.sha256((OUT/'registry/EEGMMIDB_MANIFEST.csv').read_bytes()).hexdigest()
def save_npz_atomic(path,**arrays):
 tmp=path.with_name(path.name+'.tmp')
 with tmp.open('wb') as f:np.savez_compressed(f,**arrays)
 tmp.replace(path)
def save_json_atomic(path,obj):
 tmp=path.with_name(path.name+'.tmp');tmp.write_text(json.dumps(obj,sort_keys=True));tmp.replace(path)
feat_cache=OUT/'results/WP5_FEATURES.npz';feat_meta=OUT/'results/WP5_FEATURES.json'
if feat_cache.exists() and feat_meta.exists() and json.loads(feat_meta.read_text()).get('manifest_sha256')==manifest_sha:
 with np.load(feat_cache) as z:feat={'D1':z['D1'],'D2':z['D2']}
 print('WP5 feature cache loaded',flush=True)
else:
 if X is None:raise RuntimeError('WP5 feature cache unavailable; full waveform arrays are required.')
 feat={'D1':band_features(X,'D1'),'D2':band_features(X,'D2')}
 save_npz_atomic(feat_cache,D1=feat['D1'],D2=feat['D2']);save_json_atomic(feat_meta,{'manifest_sha256':manifest_sha,'epochs':len(y),'subjects':len(store)})
# D3 fixed 8-30 Hz preprocessing.
sos=butter(4,[8,30],btype='bandpass',fs=160,output='sos');X3=sosfiltfilt(sos,X,axis=-1).astype(np.float32) if X is not None else None
Xdict={'D1':feat['D1'],'D2':feat['D2'],'D3':X3,'D4':X}
all_idx=np.arange(len(y));cv_keys=['D1','D2','D3','D4','D1_plt','D2_plt','D3_plt','D4_plt'];cv_cache=OUT/'results/WP5_CV_PREDICTIONS.npz';cv_meta=OUT/'results/WP5_CV_PREDICTIONS.json'
meta=json.loads(cv_meta.read_text()) if cv_meta.exists() else {}
if cv_cache.exists() and meta.get('manifest_sha256')==manifest_sha and meta.get('keys')==cv_keys:
 with np.load(cv_cache) as z:
  preds={k:z['pred_'+k] for k in cv_keys};probs={k:z['prob_'+k] for k in cv_keys};completed_folds=int(z['completed_folds'])
 fold_assignment=meta.get('fold_assignment',{});print(f'WP5 CV cache loaded: {completed_folds}/5 folds',flush=True)
else:
 preds={k:np.full(len(y),-1,dtype=int) for k in cv_keys};probs={k:np.full((len(y),2),np.nan,dtype=float) for k in cv_keys};completed_folds=0;fold_assignment={}
# Five grouped folds: every subject held out once in a fold.
gkf=GroupKFold(n_splits=5);outer=list(gkf.split(all_idx,y,groups))
for fold,(tr,te) in enumerate(outer):
 fold_assignment.update({str(groups[i]):int(fold) for i in te})
 if fold<completed_folds:continue
 for name in ['D1','D2','D3','D4']:
  model=make_model(name);model.fit(Xdict[name][tr],y[tr]);p=model.predict_proba(Xdict[name][te]);preds[name][te]=model.classes_[p.argmax(axis=1)];probs[name][te]=p
  # Platt calibrator trained exclusively from OOF predictions of outer-training subjects.
  inner=GroupKFold(n_splits=3);oof=np.zeros(len(tr));yo=np.zeros(len(tr),int)
  for itr,iva in inner.split(tr,y[tr],groups[tr]):
   mm=make_model(name);mm.fit(Xdict[name][tr[itr]],y[tr[itr]]);pp=mm.predict_proba(Xdict[name][tr[iva]]);oof[iva]=np.log(np.clip(pp[:,1],1e-6,1-1e-6)/(1-np.clip(pp[:,1],1e-6,1-1e-6)));yo[iva]=(y[tr[iva]]==mm.classes_[1]).astype(int)
  cal=LogisticRegression(C=1e6,max_iter=1000).fit(oof.reshape(-1,1),yo);logit=np.log(np.clip(p[:,1],1e-6,1-1e-6)/(1-np.clip(p[:,1],1e-6,1-1e-6)));p1=cal.predict_proba(logit.reshape(-1,1))[:,1];pp1=np.c_[1-p1,p1]
  probs[name+'_plt'][te]=pp1;preds[name+'_plt'][te]=np.where(p1>=.5,model.classes_[1],model.classes_[0])
  print(f'WP5 CV fold {fold+1}/5 decoder {name} complete',flush=True)
 completed_folds=fold+1
 save_npz_atomic(cv_cache,completed_folds=np.asarray(completed_folds),**{'pred_'+k:v for k,v in preds.items()},**{'prob_'+k:v for k,v in probs.items()})
 save_json_atomic(cv_meta,{'manifest_sha256':manifest_sha,'keys':cv_keys,'completed_folds':completed_folds,'fold_assignment':fold_assignment})
 print(f'WP5 CV fold {fold+1}/5 checkpoint saved',flush=True)
# D5 within-subject runs R04/R08 -> R12; train independent model per subject.
d5_cache=OUT/'results/WP5_D5_PREDICTIONS.npz';d5_meta=OUT/'results/WP5_D5_PREDICTIONS.json';d5done=set()
if d5_cache.exists() and d5_meta.exists() and json.loads(d5_meta.read_text()).get('manifest_sha256')==manifest_sha:
 with np.load(d5_cache) as z:
  d5_raw=z['raw'];d5_plt=z['plt'];d5_pred=z['pred_raw'];d5_predplt=z['pred_plt'];d5done=set(z['done_subjects'].astype(str).tolist())
 print(f'WP5 D5 cache loaded: {len(d5done)}/{len(store)} subjects',flush=True)
else:d5_raw=np.full((len(y),2),np.nan);d5_plt=np.full((len(y),2),np.nan);d5_pred=np.zeros(len(y),int);d5_predplt=np.zeros(len(y),int)
for subject_i,(subject,rr) in enumerate(store.items(),1):
 if subject in d5done:continue
 tridx=np.where((groups==subject)&np.isin(runs_idx,['R04','R08']))[0];te=np.where((groups==subject)&(runs_idx=='R12'))[0]
 xx=np.concatenate([rr['R04'][0],rr['R08'][0]]);yy=np.r_[rr['R04'][1],rr['R08'][1]];xt=rr['R12'][0]
 mm=make_model('D3');mm.fit(sosfiltfilt(sos,xx,axis=-1),yy);pp=mm.predict_proba(sosfiltfilt(sos,xt,axis=-1));d5_raw[te]=pp;d5_pred[te]=mm.classes_[pp.argmax(axis=1)]
 # Training-only calibration via leave-one-run-out models (R04 -> R08 and reverse).
 oof=[];oy=[]
 for train_run,test_run in [('R04','R08'),('R08','R04')]:
  xa,ya=rr[train_run][0],rr[train_run][1];xb,yb=rr[test_run][0],rr[test_run][1]
  cm=make_model('D3');cm.fit(sosfiltfilt(sos,xa,axis=-1),ya);cp=cm.predict_proba(sosfiltfilt(sos,xb,axis=-1));oof.extend(np.log(np.clip(cp[:,1],1e-6,1-1e-6)/(1-np.clip(cp[:,1],1e-6,1-1e-6))));oy.extend((yb==cm.classes_[1]).astype(int))
 pl=LogisticRegression(C=1e6,max_iter=1000).fit(np.asarray(oof).reshape(-1,1),np.asarray(oy));lp=np.log(np.clip(pp[:,1],1e-6,1-1e-6)/(1-np.clip(pp[:,1],1e-6,1-1e-6)));p1=pl.predict_proba(lp.reshape(-1,1))[:,1];d5_plt[te]=np.c_[1-p1,p1];d5_predplt[te]=np.where(p1>=.5,mm.classes_[1],mm.classes_[0])
 d5done.add(subject);save_npz_atomic(d5_cache,raw=d5_raw,plt=d5_plt,pred_raw=d5_pred,pred_plt=d5_predplt,done_subjects=np.asarray(sorted(d5done)))
 save_json_atomic(d5_meta,{'manifest_sha256':manifest_sha,'done_subjects':sorted(d5done)})
 if subject_i%5==0 or subject_i==len(store):print(f'WP5 D5 subject models {subject_i}/{len(store)} complete',flush=True)
probs['D5_raw']=d5_raw;preds['D5_raw']=d5_pred;probs['D5_plt']=d5_plt;preds['D5_plt']=d5_predplt
# Quality metrics and V1 gate; confidence is max class probability.
def ece(ptrue,conf,bins=10):
 pred=conf # use caller's predicted-label correctness with confidence; function below computes bins
 return float('nan')
quality={};zero=[]
for key,p in probs.items():
 valid=np.isfinite(p).all(axis=1)
 if not valid.any():continue
 pv=p[valid];yv=y[valid];pr=preds[key][valid];correct=pr==yv;k=int(correct.sum());n=len(yv);acc=k/n
 from scipy.stats import beta as beta_dist
 class_ci=[]
 for label in (1,2):
  nk=int((yv==label).sum());ck=int(((yv==label)&(pr==label)).sum());class_ci.append([0 if ck==0 else float(beta_dist.ppf(.0125,ck,nk-ck+1)),1 if ck==nk else float(beta_dist.ppf(.9875,ck+1,nk-ck))])
 ci_ba=[float(np.mean([z[0] for z in class_ci])),float(np.mean([z[1] for z in class_ci]))]
 conf=pv.max(axis=1); bins=np.linspace(.5,1,11);eceval=0;reliability=[]
 for lo,hi in zip(bins[:-1],bins[1:]):
  mask=(conf>=lo)&(conf<(hi if hi<1 else hi+1e-9))
  if mask.any():
   eceval+=mask.mean()*abs(correct[mask].mean()-conf[mask].mean())
   reliability.append({'bin_mid':float((lo+hi)/2),'n':int(mask.sum()),'mean_confidence':float(conf[mask].mean()),'accuracy':float(correct[mask].mean())})
 row={'n':n,'correct':k,'pooled_accuracy':acc,'balanced_accuracy':float(balanced_accuracy_score(yv,pr)),'balanced_accuracy_exact95':ci_ba,'balanced_accuracy_ci_method':'average of two exact Clopper-Pearson class limits, Bonferroni simultaneous 95%','class_sensitivity_specificity_exact95':class_ci,'ece':float(eceval),'share_conf_ge_0.75':float((conf>=.75).mean()),'reliability_bins':reliability};quality[key]=row
 if not key.startswith('D5') and not key.endswith('_plt'):zero.append(key)
# Subject-cluster bootstrap best minus worst zero-calibration BA difference, 10,000 resamples.
best=max(zero,key=lambda k:quality[k]['balanced_accuracy']);worst=min(zero,key=lambda k:quality[k]['balanced_accuracy']);subjects=sorted(set(groups));rng=np.random.default_rng(20261008);diff=[]
# Cache deterministic subject scores; each bootstrap still draws the same ordered subjects and averages eligible subject scores equally.
subject_scores={};subject_pos={s:i for i,s in enumerate(subjects)}
for key in [best,worst]:
 p=preds[key];scores=[]
 for s in subjects:
  ix=np.where(groups==s)[0];ix=ix[np.isfinite(probs[key][ix]).all(axis=1)]
  scores.append(balanced_accuracy_score(y[ix],p[ix]) if len(ix) else np.nan)
 subject_scores[key]=np.asarray(scores,dtype=float)
for boot_i in range(10000):
 if boot_i and boot_i%2000==0:print(f'WP5 V1 cluster bootstrap {boot_i}/10000',flush=True)
 pick=rng.choice(subjects,len(subjects),replace=True);vals=[]
 for key in [best,worst]:
  sub_scores=[subject_scores[key][subject_pos[s]] for s in pick if np.isfinite(subject_scores[key][subject_pos[s]])]
  vals.append(float(np.mean(sub_scores)) if sub_scores else np.nan)
 diff.append(vals[0]-vals[1])
bootci=np.nanpercentile(diff,[2.5,97.5]).tolist();v1_p1=quality[best]['balanced_accuracy']>=.58 and quality[best]['balanced_accuracy_exact95'][0]>.55;v1_p2=bootci[0]>0 or bootci[1]<0
quality_payload={'variants':quality,'best_zero_calibration':best,'worst_zero_calibration':worst,'best_vs_worst_subject_cluster_bootstrap_95':bootci,'V1':{'P1':bool(v1_p1),'P2':bool(v1_p2),'passed':bool(v1_p1 and v1_p2),'status':'CONFIRMATORY' if v1_p1 and v1_p2 else 'DESCRIPTIVE_ONLY','bootstrap_resamples':10000,'seed':20261008},'valid_subjects':len(store),'excluded_subjects':excluded,'fold_assignment':fold_assignment}
(OUT/'results/decoder_quality_R1.json').write_text(json.dumps(quality_payload,indent=2))
# R1 trial episodes: pair kth T1 with kth T2 chronologically within each subject across runs.
# Map stored original combined indices via stable order key.
index_by={};idx=0
for subject in store:
 for r in runs:
  ep,lab,on,src=store[subject][r]
  for j in range(len(lab)):index_by[(subject,r,j)]=idx;idx+=1
variants={**{f'{m}_{v}':(m if v=='raw' else m+'_plt') for m in ['D1','D2','D3','D4'] for v in ['raw','plt']},'D5_raw':'D5_raw','D5_plt':'D5_plt'}
target=OUT/'results/real_episodes.csv';existing_ids=set()
if target.exists():
 prior=pd.read_csv(target);prior_n=len(prior)
 for _,pr in prior[prior.arm=='R1'].iterrows():
  eid=str(pr.episode_id)
  if (OUT/f'results/run_json/{eid}.json').exists() and (OUT/f'replay_csv/R1/{eid}.csv').exists():existing_ids.add(eid)
  else:prior=prior[prior.episode_id!=eid]
 if len(prior)!=prior_n:prior.to_csv(target,index=False)
max_new=int(os.environ.get('WP5_MAX_EPISODES','0'));new_done=0
for vname,key in variants.items():
 for subject in store:
  ordered=[];trial_runs=['R12'] if vname.startswith('D5_') else runs
  for r in trial_runs:
   ep,lab,on,src=store[subject][r]
   for j in range(len(lab)):ordered.append((runs.index(r),float(on[j]),r,j,int(lab[j])))
  ordered=sorted(ordered,key=lambda z:(z[0],z[1]));t1=[x for x in ordered if x[4]==1];t2=[x for x in ordered if x[4]==2]
  n=min(len(t1),len(t2))
  for k in range(n):
   eid=f'R1_{vname}_{subject}_{k+1:02d}'
   if eid in existing_ids:continue
   dec=t1[k];gr=t2[k];di=index_by[(subject,dec[2],dec[3])];gi=index_by[(subject,gr[2],gr[3])];pdv=probs[key]
   def pred_conf(ii):
    pp=pdv[ii];cls=preds[key][ii];label='OPEN' if cls==1 else 'CLOSE';return label,float(pp.max())
   dl,dc=pred_conf(di);gl,gc=pred_conf(gi);events=build([(dl,dc)]*10,[(gl,gc)]*10);r,lg=run(events);reruns=0;invalid=bool(r.get('invalid_state_detected',False))
   if invalid:reruns=1;first_log=lg;r,lg=run(events);lg=first_log+lg;invalid=bool(r.get('invalid_state_detected',False))
   tm=r['task_metrics'];onset=[x['timestamp_s'] for x in r['task_transitions'] if x['reason']=='decoded_grasp_command'];onset=onset[0] if onset else None;false=any(2<=t<4 and st=='EXECUTING' and cmd=='CLOSE' for t,l,st,cmd,ts in lg);complete=tm['final_state']=='COMPLETE';cue=bool(complete and onset is not None and 4<=onset<=5.5 and not false and not invalid)
   row={'episode_id':eid,'arm':'R1','decoder':vname.split('_')[0],'variant':'plt' if vname.endswith('_plt') else 'raw','subject':subject,'pair_index':k+1,'decoy_label':dl,'decoy_confidence':dc,'grasp_label':gl,'grasp_confidence':gc,'task_completion':complete,'false_grasp':false,'miss':onset is None,'cue_correct_success':cue,'grasp_onset':onset,'completion_time_s':tm.get('completion_time_s'),'final_error_m':tm.get('final_error_m'),'released_command_count':r.get('control_metrics',{}).get('released_command_count'),'invalid_state_detected':invalid,'invalid_state_reruns':reruns}
   if invalid:
    ep=OUT/'results/EXCLUSIONS.csv';exists=ep.exists()
    with ep.open('a') as ef:
     if not exists:ef.write('arm,episode_id,reason,attempts\n')
     ef.write(f'R1,{eid},invalid_state_detected_after_rerun,{reruns+1}\n')
   rp=OUT/f'replay_csv/R1/{eid}.csv';rp.parent.mkdir(parents=True,exist_ok=True);write(events,rp);row['csv_sha256']=hashlib.sha256(rp.read_bytes()).hexdigest()
   jf=OUT/f'results/run_json/{eid}.json';jf.write_text(json.dumps(row,sort_keys=True,separators=(',',':')))
   lp=OUT/f'logs/R1_events.csv.gz'
   with open(lp,'ab') as raw:
    import gzip,csv,io
    with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as gz:
     t=io.TextIOWrapper(gz,encoding='utf-8',newline='');w=csv.writer(t);w.writerow(['episode_id','timestamp_s','label','controller_state','released_command','task_state']);[w.writerow([eid,*x]) for x in lg];t.flush();t.detach()
   # Commit the results CSV row last so it is a reliable resume checkpoint.
   dfrow=pd.DataFrame([row]);
   if target.exists():dfrow.reindex(columns=pd.read_csv(target,nrows=0).columns).to_csv(target,mode='a',header=False,index=False)
   else:dfrow.to_csv(target,index=False)
   existing_ids.add(eid);new_done+=1
   if max_new and new_done>=max_new:print(f'WP5 chunk complete: {new_done} new episodes; rerun to resume.',flush=True);raise SystemExit(0)
  print(f'WP5 episodes {vname} {subject} n={n} total_new={new_done}',flush=True)
print('WP5 COMPLETE; V1='+quality_payload['V1']['status'],flush=True)
(OUT/'results/WP5_STATUS.json').write_text(json.dumps({'status':'COMPLETED','valid_subjects':len(store),'excluded_subjects':len(excluded),'R1_episode_count':len(existing_ids),'R1_episode_count_source':'unique committed R1 episode_id values in results/real_episodes.csv','V1':quality_payload['V1']},indent=2))
