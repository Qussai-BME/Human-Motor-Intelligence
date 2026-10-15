#!/usr/bin/env python3
import hashlib,json,os,shutil,subprocess,time
from pathlib import Path
_C2=Path(__file__).resolve().parents[1];OUT=Path(os.environ.get('C2_OUT',str(_C2)));PROTO=_C2;REG=OUT/'registry'
# Include the registered reference code and the exact local orchestration scripts used.
(REG/'reference_code').mkdir(parents=True,exist_ok=True)
(OUT/'scripts').mkdir(parents=True,exist_ok=True)
for name in ['c2_runner.py','c2_emulator_pilot.py','c2_analytic_hold.py']:
 shutil.copy2(PROTO/'reference_code'/name,REG/'reference_code'/name)
for name in ['run_preflight.py','run_main_arms.py','run_wp5.py','analyze_c2.py','build_report.py','finalize_package.py']:
 shutil.copy2(PROTO/name,OUT/'scripts'/name)
if not (OUT/'REPORT_C2.md').exists() or not (OUT/'ANALYSIS.json').exists():raise SystemExit('Required REPORT_C2.md / ANALYSIS.json missing')
# Full output SHA-256 inventory (the inventory cannot include its own digest).
manifest_path=REG/'OUTPUT_MANIFEST.json';files=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p!=manifest_path:
  h=hashlib.sha256()
  with p.open('rb') as f:
   for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
  files.append({'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':h.hexdigest()})
manifest={'schema':'P6-C2-OUTPUT-MANIFEST-v1','created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'file_count':len(files),'files':files,'manifest_self_hash_note':'OUTPUT_MANIFEST.json is intentionally excluded from its own file list; its SHA-256 is supplied in OUTPUT_MANIFEST.sha256.'}
manifest_path.write_text(json.dumps(manifest,indent=2))
selfhash=hashlib.sha256(manifest_path.read_bytes()).hexdigest();(REG/'OUTPUT_MANIFEST.sha256').write_text(f'{selfhash}  OUTPUT_MANIFEST.json\n')
# Zip at a low compression level to avoid spending substantial time recompressing already-small artifacts.
zip_path=ROOT/'P6_C2_RESULTS.zip';zip_path.unlink(missing_ok=True)
subprocess.run(['zip','-q','-1','-r',str(zip_path),OUT.name],cwd=ROOT,check=True)
print(json.dumps({'folder':str(OUT),'zip':str(zip_path),'output_files_hashed':len(files),'zip_bytes':zip_path.stat().st_size,'manifest_sha256':selfhash},indent=2))
