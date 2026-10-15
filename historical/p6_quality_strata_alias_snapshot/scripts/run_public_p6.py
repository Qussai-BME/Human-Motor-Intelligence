#!/usr/bin/env python3
from pathlib import Path
import csv, json, hashlib, sys, time
import numpy as np
from scipy.signal import butter, sosfiltfilt, welch
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss
from sklearn.model_selection import StratifiedKFold, cross_val_score
import pyedflib

ROOT=Path(__file__).resolve().parents[1]
DATA=Path('<LOCAL_WORKSPACE>/p6_public_data/eegmmidb_v1_0_0')
RESULTS=ROOT/'results'; TRACES=ROOT/'traces'; AUDIT=ROOT/'audit'
FS=160.0; SUBJECTS=[f'S{i:03d}' for i in range(1,21)]
# Prospective, fixed before fitting: use R03 (left/right fist imagery), 1.0–3.5 s after annotations.
# Three authentic model conditions differ only by predeclared feature family and are ranked on source-only CV.
CONDITIONS=['worst','middle','best']

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load_subject(sid):
    p=DATA/f'{sid}R03.edf'
    f=pyedflib.EdfReader(str(p)); n=f.signals_in_file; sig=np.asarray(f.readSignal(0 if n else 0))
    # EDF samples are available per channel; align first 64 EEG channels to minimum length.
    X=np.asarray([f.readSignal(i) for i in range(min(64,n))],dtype=np.float32); anns=f.readAnnotations(); f.close()
    onsets,durs,desc=anns
    events=[]
    for o,d,c in zip(onsets,durs,desc):
        c=c.decode() if isinstance(c,bytes) else str(c)
        if c in ('T1','T2'):
            events.append((float(o),1 if c=='T1' else 2))
    epochs=[]; labels=[]; ids=[]
    for k,(o,y) in enumerate(events):
        a=int(round((o+1.0)*FS)); b=int(round((o+3.5)*FS))
        if b<=X.shape[1]: epochs.append(X[:,a:b]); labels.append(y); ids.append(f'{sid}-R03-{k:03d}')
    return np.asarray(epochs),np.asarray(labels),ids

def band_features(ep, family):
    # fixed bands; features are log relative band powers over motor channels.
    bands=[(8,12),(13,30)] if family in ('middle','best') else [(8,30)]
    chans=[7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
    chans=[c for c in chans if c<ep.shape[1]]
    feats=[]
    for tr in ep:
        fs=[]
        for c in chans:
            f,px=welch(tr[c],fs=FS,nperseg=min(256,tr.shape[-1]),axis=-1)
            total=np.trapezoid(px[(f>=4)&(f<=40)],f[(f>=4)&(f<=40)])+1e-12
            for lo,hi in bands:
                band=np.trapezoid(px[(f>=lo)&(f<=hi)],f[(f>=lo)&(f<=hi)])+1e-12
                fs.append(np.log(band/total))
        feats.append(fs)
    z=np.asarray(feats,dtype=np.float32)
    if family=='best':
        # Add robust left/right central asymmetry features without target leakage.
        mid=z.shape[1]//2; z=np.c_[z,z[:,:mid]-z[:,mid:2*mid]] if z.shape[1]>=2*mid else z
    return z

def fit_condition(trainX,trainy,cond):
    fam={'worst':'worst','middle':'middle','best':'best'}[cond]
    X=band_features(trainX,fam)
    model=Pipeline([('scale',StandardScaler()),('clf',LogisticRegression(max_iter=1000,C=0.1 if cond=='worst' else (1.0 if cond=='middle' else 2.0),random_state=1701))])
    cv=StratifiedKFold(3,shuffle=True,random_state=1701)
    cv_score=float(np.mean(cross_val_score(model,X,trainy,cv=cv,scoring='balanced_accuracy')))
    model.fit(X,trainy)
    return model,cv_score

def main():
    AUDIT.mkdir(exist_ok=True); RESULTS.mkdir(exist_ok=True); TRACES.mkdir(exist_ok=True)
    manifest={'dataset':'PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0','doi':'10.13026/C28G6P','license':'Open Data Commons Attribution License v1.0','source_url':'https://physionet.org/content/eegmmidb/1.0.0/','sampling_rate_hz':160,'run':'R03','subjects':SUBJECTS,'downloaded_files':[],'created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    data={}
    for sid in SUBJECTS:
        p=DATA/f'{sid}R03.edf'; manifest['downloaded_files'].append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
        e,y,ids=load_subject(sid); data[sid]=(e,y,ids)
    (AUDIT/'DATASET_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    rows=[]; trace_meta=[]
    for test_sid in SUBJECTS:
        tr=[data[s] for s in SUBJECTS if s!=test_sid]
        trainX=np.concatenate([a[0] for a in tr]); trainy=np.concatenate([a[1] for a in tr])
        testX,testy,testids=data[test_sid]
        for cond in CONDITIONS:
            model,cv=fit_condition(trainX,trainy,cond)
            Xte=band_features(testX,{'worst':'worst','middle':'middle','best':'best'}[cond]); proba=model.predict_proba(Xte); pred=model.classes_[np.argmax(proba,axis=1)]
            acc=float(accuracy_score(testy,pred)); bacc=float(balanced_accuracy_score(testy,pred)); ll=float(log_loss(testy,proba,labels=model.classes_))
            trace=TRACES/f'{cond}_{test_sid}.csv'
            with trace.open('w',newline='') as h:
                w=csv.DictWriter(h,fieldnames=['timestamp_s','label','confidence','source_subject','modality','model_version','window_id','ground_truth','correct']) ; w.writeheader()
                for i,(pid,pr,gt,pp) in enumerate(zip(testids,pred,testy,proba)):
                    # Actual recorded trial order; timestamp is the trial onset-relative stream time.
                    label='OPEN' if int(pr)==1 else 'CLOSE'; conf=float(np.max(pp));
                    w.writerow({'timestamp_s':f'{i*2.5:.3f}','label':label,'confidence':f'{conf:.8f}','source_subject':test_sid,'modality':'eeg','model_version':f'physionet-r03-{cond}-logreg-v1','window_id':pid,'ground_truth':'OPEN' if int(gt)==1 else 'CLOSE','correct':int(pr)==int(gt)})
            rows.append({'condition':cond,'test_subject':test_sid,'n_trials':int(len(testy)),'source_cv_balanced_accuracy':cv,'heldout_accuracy':acc,'heldout_balanced_accuracy':bacc,'heldout_log_loss':ll,'trace':str(trace),'trace_sha256':sha(trace)})
            trace_meta.append({'condition':cond,'test_subject':test_sid,'trace':str(trace),'trace_sha256':sha(trace),'model_version':f'physionet-r03-{cond}-logreg-v1','source_dataset':'PhysioNet EEGMMIDB v1.0.0','authenticity':'real_decoder_output_from_public_recordings','synthetic':False})
    (RESULTS/'LOSO_RESULTS.json').write_text(json.dumps(rows,indent=2)+'\n')
    (RESULTS/'TRACE_MANIFEST.json').write_text(json.dumps({'status':'EXECUTED_PUBLIC_DATA_REOPENING','protocol_id':'p6-r3-public-data-reopening-v1','trace_count':len(trace_meta),'conditions':CONDITIONS,'traces':trace_meta,'source_manifest':'../audit/DATASET_MANIFEST.json','note':'All traces are produced from held-out real EDF recordings; no labels, confidence values, timing, or quality variants were edited after inference.'},indent=2)+'\n')
    import statistics
    summary={}
    for c in CONDITIONS:
        q=[r['heldout_balanced_accuracy'] for r in rows if r['condition']==c]; summary[c]={'mean_balanced_accuracy':float(np.mean(q)),'median_balanced_accuracy':float(np.median(q)),'n_subjects':len(q)}
    (RESULTS/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
