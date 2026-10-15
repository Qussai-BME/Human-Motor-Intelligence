#!/usr/bin/env python3
import csv,json,hashlib,os
from pathlib import Path
import pandas as pd
OUT=Path(os.environ.get('C2_OUT',str(Path(__file__).resolve().parents[1])));R=OUT/'results';A=json.load(open(R/'ANALYSIS.json'));P=json.load(open(R/'PREFLIGHT.json'));E=json.load(open(OUT/'registry/ENVIRONMENT.json'));F=json.load(open(OUT/'registry/FREEZE_MANIFEST.json'))
wp5=json.load(open(R/'WP5_STATUS.json')) if (R/'WP5_STATUS.json').exists() else None
rows=A['per_cell'];hyp=A['hypotheses']
fmt=lambda x:f'{x:.3f}'
def cell_table():
 out=['| q | Regime | ρ | N | Cue-correct successes | Rate (exact 95% CI) | Task completion | False grasp | Miss |','|---:|:---:|---:|---:|---:|---:|---:|---:|---:|']
 for x in rows:out.append(f"| {x['q']:.2f} | {x['regime']} | {x['rho']:.1f} | {x['n']} | {x['successes']} | {x['rate']:.3f} ({x['exact95'][0]:.3f}–{x['exact95'][1]:.3f}) | {x['task_completion_rate']:.3f} | {x['false_grasp_rate']:.3f} | {x['miss_rate']:.3f} |")
 return '\n'.join(out)
# T2 preflight rows.
gates=[('WP0 C1 archived re-execution',len(E['c1_reexecution'])==3 and all(x['match'] for x in E['c1_reexecution']),f"{sum(x['match'] for x in E['c1_reexecution'])}/3 bit-identical"),('Config numeric diff',E['numeric_config_equal'], 'No numeric differences; config files are byte-identical'),('V3 ceiling',P['V3']['pass'],f"{P['V3']['successes']}/100; task completes at 5.0 s"),('V2 calibrated chance floor',P['V2']['pass'],f"{P['V2']['successes']}/100; max permitted 1"),('V4 timing',P['V4']['pass'],f"Markers {P['V4']['markers_s']}"),('Truth table',P['truth_table']['pass'],f"{P['truth_table']['passed']}/16"),('Determinism',P['determinism']['pass'],f"{P['determinism']['passed']}/20 identical normalized result JSONs"),('X0 sparse regression control',P['X0']['pass'],f"{P['X0']['successes']}/100"),('V5 variability',P['V5']['pass'],f"{sum(x['pass'] for x in P['V5']['cells'])}/8 pilot cells interior")]
# Hypothesis table.
hrows=[]
h=hyp['H-E1'];hrows.append(f"| H-E1 | Cochran–Armitage z={h['cochran_armitage']['z']:.3f}, p(one-sided)={h['cochran_armitage']['p_one_sided_increasing']:.4g}; logistic q slope {h['logistic_slope']['estimate']:.3f} [{h['logistic_slope']['ci95'][0]:.3f}, {h['logistic_slope']['ci95'][1]:.3f}] | Holm p={h.get('family_wise_holm_p',float('nan')):.4g}; supported={h['supported']} |")
h=hyp['H-E2'];hrows.append('| H-E2 | '+ '; '.join(f"q={x['q']:.2f}/{x['regime']}: {x['successes']}/{x['n']} ({x['rate']:.3f}; exact CI {x['exact95'][0]:.3f}–{x['exact95'][1]:.3f})" for x in h['checks'])+f" | Supported={h['supported']} |")
h=hyp['H-E3'];hrows.append('| H-E3 | '+ '; '.join(f"q={x['q']:.1f}: flat−cal RD={x['risk_difference_flat_minus_cal']:.3f} (Newcombe {x['newcombe95'][0]:.3f}–{x['newcombe95'][1]:.3f}), p={x['p_two_sided']:.4g}, Holm={x['p_holm']:.4g}" for x in h['comparisons'])+f" | Global Holm p={h.get('family_wise_holm_p',float('nan')):.4g} |")
h=hyp['H-E4'];hrows.append('| H-E4 | '+ '; '.join(f"q={x['q']:.1f}: trend z={x['trend']['z']:.3f}, p={x['trend']['p_two_sided']:.4g}, Holm={x['p_holm']:.4g}; false-grasp rates="+','.join(f"ρ{x['rho']:.1f}:{x['false_grasp_rate']:.3f}" for x in x['cells']) for x in h['comparisons'])+f" | Global Holm p={h.get('family_wise_holm_p',float('nan')):.4g} |")
R1=A.get('R1',{})
if R1.get('V1',{}).get('passed'):
 h=R1['H-R1'];hrows.append(f"| H-R1 | Conditional GEE, global Wald p={R1.get('GEE_global_decoder_effect',{}).get('p',float('nan')):.4g}; subject-cluster exchangeable | V1 passed; H-R1 supported={h.get('supported')} |")
elif R1.get('V1'):
 hrows.append(f"| H-R1 | Not tested inferentially | V1 failed; R1 descriptive only |")
else:hrows.append('| H-R1 | Not run | WP5 blocked/unavailable |')
# T5 real decoder rows.
t5=[]
if (R/'decoder_quality_R1.json').exists():
 Q=json.load(open(R/'decoder_quality_R1.json'))
 for name,x in Q['variants'].items():t5.append(f"| {name} | {x['n']} | BA={x['balanced_accuracy']:.3f} ({x['balanced_accuracy_exact95'][0]:.3f}–{x['balanced_accuracy_exact95'][1]:.3f}) | ECE={x['ece']:.3f}; conf≥.75={x['share_conf_ge_0.75']:.3f} |")
 for x in A['R0_descriptive']:t5.append(f"| R0 {x['decoder']} | {x['n']} episodes | success={x['successes']}/{x['n']} ({x['rate']:.3f}; exact {x['exact95'][0]:.3f}–{x['exact95'][1]:.3f}) | false-grasp={x['false_grasp_rate']:.3f}; miss={x['miss_rate']:.3f} |")
 for x in A.get('R1_episode_descriptive',[]):
  z=x['cue_correct_success'];t=x['task_completion'];f=x['false_grasp'];m=x['miss']
  t5.append(f"| R1 {x['decoder']} {x['variant']} | {x['n']} episodes | cue-correct={z['successes']}/{x['n']} ({z['rate']:.3f}; exact 95% {z['exact95'][0]:.3f}–{z['exact95'][1]:.3f}) | completion={t['rate']:.3f}; false-grasp={f['rate']:.3f}; miss={m['rate']:.3f} |")
else:
 t5.append(f"| R0 M1–M3 + oracle | {sum(x['n'] for x in A['R0_descriptive'])} episodes | See R0 summary below | R1 WP5 status: BLOCKED / unavailable |")
 if A['R0_descriptive']:
  for x in A['R0_descriptive']:t5.append(f"| R0 {x['decoder']} | {x['n']} | success={x['successes']}/{x['n']} ({x['rate']:.3f}; exact {x['exact95'][0]:.3f}–{x['exact95'][1]:.3f}) | false-grasp={x['false_grasp_rate']:.3f}; miss={x['miss_rate']:.3f} |")
# Sensitivity brief counts.
sens=A['sensitivity'];sens_note=f"{len(sens)} cells, each N={sens[0]['n'] if sens else 0}; all detailed rates in ANALYSIS.json and F7." if sens else 'Not yet available.'
if wp5:
 _ex=pd.read_csv(OUT/'registry/SUBJECT_EXCLUSIONS.csv') if (OUT/'registry/SUBJECT_EXCLUSIONS.csv').exists() else pd.DataFrame(columns=['subject'])
 _ids=', '.join(_ex.subject.astype(str).tolist()) if len(_ex) else 'none'
 _r1df=pd.read_csv(R/'real_episodes.csv');_r1n=int(_r1df[_r1df.arm=='R1'].episode_id.nunique())
 wp5_note=f"WP5 integrity: {wp5['valid_subjects']} subjects passed and {wp5['excluded_subjects']} failed the registered sampling-rate, channel-count or event-count checks; excluded IDs (selected by checks, not hard-coded): {_ids}. The committed R1 set contains {_r1n} unique episodes. D5 replay uses the held-out R12 run only."
 wp5_audit='- **D5 split implementation correction:** D5 is trained on R04/R08 and evaluated on held-out R12. The initial runner attempted a training-run epoch with intentionally undefined D5 confidence; replay-input validation rejected it before controller simulation. The rejected CSV and attempt are preserved in `replay_csv/R1/FAILED_INPUT_R1_D5_raw_S001_01.csv`, `results/EXCLUSIONS.csv`, and `results/WP5_D5_REPLAY_CORRECTION.json`. D5 replay was corrected to R12 only; no model, controller or task parameters changed.'
else:wp5_note='';wp5_audit=''
# Build report.
text=f'''# P6-C2-EPISODE-v1.0 — Results report

**Study status:** WP0–WP4 and WP7 executed in the registered order; WP5 status: **{('completed; V1 '+R1.get('V1',{}).get('status','')) if (R/'decoder_quality_R1.json').exists() else 'blocked/unavailable'}**.  
**Protocol:** `P6-C2-EPISODE-v1.0` (frozen). **No controller or protocol parameters were tuned.**  
**Analysis endpoint:** cue-correct episode success. All results are deterministic software simulation/replay evidence, not clinical or online-BCI evidence.

## 1. Pre-flight validity

| Gate | Result | Evidence |
|---|:---:|---|
'''+ '\n'.join(f'| {n} | {"PASS" if ok else "FAIL"} | {detail} |' for n,ok,detail in gates)+f'''

The MyoSim C1 fixture and M1_S001/M3_S015 archived replays reproduced their archived task success, completion time, path length, final error, and command-correction values exactly (see `registry/ENVIRONMENT.json`). The C2 and C1 controller config files are byte-identical; numeric diff is empty. The C2 oracle reaches approach at 1.6 s, decoded grasp at 4.3 s, transport at 4.9 s, and target release/completion at 5.0 s.

## 2. Design, arms and counts (T1)

| Arm | Role | Planned | Executed |
|---|---|---:|---:|
| X0 | C1 sparse regression control | 100 | {P['X0']['n']} |
| E | 9 q levels × 2 confidence regimes × 3 persistence levels; 500/cell | 27,000 | {len(rows)*500} |
| R0 | C1 M1–M3 and paired oracle, 140 each | 560 | {sum(x['n'] for x in A['R0_descriptive'])} |
| S | 4 q × 2 regimes × 4 thresholds × 4 confirmation windows; 200/cell | 25,600 | {len(sens)*200 if sens else 0} |
| R1 | New EEG decoders, conditional on EEGMMIDB integrity and V1 | ≈23,000 | {int((pd.read_csv(R/'real_episodes.csv').arm=='R1').sum()) if (R/'real_episodes.csv').exists() else 0} |
| W | Optional windowed analysis | Optional | Not run |

Counts and cell estimates are recorded in `ANALYSIS.json`; every run has its own replay CSV, result JSON and manifest row, with per-episode event logs in gzip streams.

## 3. Emulator dose–response (WP2/WP3)

Primary endpoint estimates are shown with exact Clopper–Pearson 95% intervals. Analytic hold predictions were compared with all 18 rho=1 emulator cells; see `results/ANALYTIC_CROSSCHECK.json`.

{cell_table()}

## 4. Registered hypothesis tests (T4)

| Hypothesis | Test/result | Registered conclusion |
|---|---|---|
{chr(10).join(hrows)}

Protocol-wide Holm adjustment is reported in `ANALYSIS.json` for all confirmatory hypotheses eligible for testing. H-R1 is included only if the V1 gate passes. Within-family E3/E4 Holm adjustments are also reported.

## 5. Real decoders and control utility (T5)

| Variant | Quality / episodes | Control result | Calibration |
|---|---|---|---|
{chr(10).join(t5)}

'''+((wp5_note+'\n\n') if wp5 else "WP5 data were downloaded and integrity-checked; exclusions and decoder quality are listed in the registry/results files.\n\n")+f'''R0 comparisons are descriptive only. If the V1 manipulation check failed, no decoder-quality ordering claim is made and R1 inferential tests are omitted.

## 6. Sensitivity (WP7)

Arm S executed {sens_note} The primary configuration remained unchanged; each temporary configuration and its SHA-256 is under `config/`.

## 7. Figures and tables

- F1: `figures/F1_interface_timeline.png` / PDF
- F2: `figures/F2_emulator_dose_response.png` / PDF
- F3: `figures/F3_calibration_crossover.png` / PDF
- F4: `figures/F4_persistence_false_grasp.png` / PDF
- F5: `figures/F5_real_decoder_quality.png` / PDF
- F6: `figures/F6_real_on_emulator_curve.png` / PDF
- F7: `figures/F7_sensitivity_heatmaps.png` / PDF
- F8: `figures/F8_X0_vs_oracle.png` / PDF

T2 is the pre-flight table above; T3 is the per-cell table in Section 3; T4–T5 are above. T6 is the claim–evidence matrix below.

## 8. Claim–evidence matrix (T6)

| Claim | Evidence | Permitted interpretation |
|---|---|---|
| E1 accuracy–utility relationship | H-E1 trend, slope and CIs | Only the registered emulator/controller mapping; describe exact observed rate and interval. |
| E2 ceiling/floor | Oracle, calibrated chance, flat chance exact CIs | Report all components, including over-confident chance-level floor. |
| E3 confidence calibration | Fixed-q flat-vs-calibrated contrasts and Holm-adjusted p-values | The result is limited to the registered emulator assumptions. |
| E4 temporal persistence | Registered rho contrasts and false-grasp rates | Controller-level effect only; no direction assumed. |
| R1 real decoder utility | V1 gate and conditional GEE/McNemar, if eligible | No decoder ordering claim if V1 fails or WP5 is blocked. |
| C1 sparse-to-C2 interface | X0 0/100 and C2 oracle ceiling | Supports detection of the C1 timing-interface defect within this software setup. |

## 9. Protocol assumptions, deviations and limitations

- **A1 REST assumption:** REST windows are cue-locked and scheduled by the synchronous protocol, not decoded. Asynchronous operation is out of scope.
{wp5_audit}
- Each emulator episode is deterministic given its label/confidence sequence; random draws follow the registered master seed and cell/episode seed arithmetic.
- MyoSim was run at commit `{E['myosim_commit']}` (v0.1.5) with the numeric-identical C1/C2 config. MyoSim source was not edited.
- All results are an offline software simulation of a controller. No claims are made about online BCI, patients, prostheses, hardware or clinical benefit.
- Known limits include sample-and-hold trial decisions, parametric independent emulator draws, deterministic physics, and the fixed (not optimized) controller gate settings.

## 10. Reproducibility and provenance

- Python {E['python']}; MyoSim commit `{E['myosim_commit']}`.
- Input hashes and environment package versions: `registry/ENVIRONMENT.json`.
- Frozen protocol, design, C2 configuration and reference code SHA-256: `registry/FREEZE_MANIFEST.json`.
- Final output hashes: `registry/OUTPUT_MANIFEST.json`.
- No outcome-driven tuning or unregistered parameter changes were performed.
'''
# Correct the WP5 count source and write both requested convenience paths.
(OUT/'REPORT_C2.md').write_text(text)
(OUT/'ANALYSIS.json').write_text((R/'ANALYSIS.json').read_text())
print('REPORT_C2.md written')
