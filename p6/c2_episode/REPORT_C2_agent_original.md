# P6-C2-EPISODE-v1.0 — Results report

**Study status:** WP0–WP4 and WP7 executed in the registered order; WP5 status: **completed; V1 CONFIRMATORY**.  
**Protocol:** `P6-C2-EPISODE-v1.0` (frozen). **No controller or protocol parameters were tuned.**  
**Analysis endpoint:** cue-correct episode success. All results are deterministic software simulation/replay evidence, not clinical or online-BCI evidence.

## 1. Pre-flight validity

| Gate | Result | Evidence |
|---|:---:|---|
| WP0 C1 archived re-execution | PASS | 3/3 bit-identical |
| Config numeric diff | PASS | No numeric differences; config files are byte-identical |
| V3 ceiling | PASS | 100/100; task completes at 5.0 s |
| V2 calibrated chance floor | PASS | 0/100; max permitted 1 |
| V4 timing | PASS | Markers {'approach_reached': 1.6, 'decoded_grasp_command': 4.3, 'transport_reached': 4.9, 'object_released_in_target': 5.0} |
| Truth table | PASS | 16/16 |
| Determinism | PASS | 20/20 identical normalized result JSONs |
| X0 sparse regression control | PASS | 0/100 |
| V5 variability | PASS | 8/8 pilot cells interior |

The MyoSim C1 fixture and M1_S001/M3_S015 archived replays reproduced their archived task success, completion time, path length, final error, and command-correction values exactly (see `registry/ENVIRONMENT.json`). The C2 and C1 controller config files are byte-identical; numeric diff is empty. The C2 oracle reaches approach at 1.6 s, decoded grasp at 4.3 s, transport at 4.9 s, and target release/completion at 5.0 s.

## 2. Design, arms and counts (T1)

| Arm | Role | Planned | Executed |
|---|---|---:|---:|
| X0 | C1 sparse regression control | 100 | 100 |
| E | 9 q levels × 2 confidence regimes × 3 persistence levels; 500/cell | 27,000 | 27000 |
| R0 | C1 M1–M3 and paired oracle, 140 each | 560 | 560 |
| S | 4 q × 2 regimes × 4 thresholds × 4 confirmation windows; 200/cell | 25,600 | 25600 |
| R1 | New EEG decoders, conditional on EEGMMIDB integrity and V1 | ≈23,000 | 19750 |
| W | Optional windowed analysis | Optional | Not run |

Counts and cell estimates are recorded in `ANALYSIS.json`; every run has its own replay CSV, result JSON and manifest row, with per-episode event logs in gzip streams.

## 3. Emulator dose–response (WP2/WP3)

Primary endpoint estimates are shown with exact Clopper–Pearson 95% intervals. Analytic hold predictions were compared with all 18 rho=1 emulator cells; see `results/ANALYTIC_CROSSCHECK.json`.

| q | Regime | ρ | N | Cue-correct successes | Rate (exact 95% CI) | Task completion | False grasp | Miss |
|---:|:---:|---:|---:|---:|---:|---:|---:|---:|
| 0.50 | cal | 0.5 | 500 | 0 | 0.000 (0.000–0.007) | 0.000 | 0.000 | 1.000 |
| 0.50 | cal | 0.8 | 500 | 0 | 0.000 (0.000–0.007) | 0.000 | 0.000 | 1.000 |
| 0.50 | cal | 1.0 | 500 | 0 | 0.000 (0.000–0.007) | 0.000 | 0.000 | 1.000 |
| 0.50 | flat | 0.5 | 500 | 127 | 0.254 (0.216–0.295) | 0.584 | 0.330 | 0.416 |
| 0.50 | flat | 0.8 | 500 | 131 | 0.262 (0.224–0.303) | 0.698 | 0.436 | 0.302 |
| 0.50 | flat | 1.0 | 500 | 115 | 0.230 (0.194–0.269) | 0.668 | 0.438 | 0.332 |
| 0.55 | cal | 0.5 | 500 | 6 | 0.012 (0.004–0.026) | 0.014 | 0.002 | 0.986 |
| 0.55 | cal | 0.8 | 500 | 9 | 0.018 (0.008–0.034) | 0.020 | 0.002 | 0.980 |
| 0.55 | cal | 1.0 | 500 | 8 | 0.016 (0.007–0.031) | 0.018 | 0.002 | 0.982 |
| 0.55 | flat | 0.5 | 500 | 139 | 0.278 (0.239–0.320) | 0.590 | 0.312 | 0.410 |
| 0.55 | flat | 0.8 | 500 | 168 | 0.336 (0.295–0.379) | 0.688 | 0.352 | 0.312 |
| 0.55 | flat | 1.0 | 500 | 151 | 0.302 (0.262–0.344) | 0.692 | 0.390 | 0.308 |
| 0.60 | cal | 0.5 | 500 | 21 | 0.042 (0.026–0.063) | 0.048 | 0.006 | 0.952 |
| 0.60 | cal | 0.8 | 500 | 38 | 0.076 (0.054–0.103) | 0.098 | 0.022 | 0.902 |
| 0.60 | cal | 1.0 | 500 | 31 | 0.062 (0.043–0.087) | 0.070 | 0.008 | 0.930 |
| 0.60 | flat | 0.5 | 500 | 185 | 0.370 (0.328–0.414) | 0.618 | 0.248 | 0.382 |
| 0.60 | flat | 0.8 | 500 | 165 | 0.330 (0.289–0.373) | 0.706 | 0.376 | 0.294 |
| 0.60 | flat | 1.0 | 500 | 163 | 0.326 (0.285–0.369) | 0.636 | 0.310 | 0.364 |
| 0.65 | cal | 0.5 | 500 | 48 | 0.096 (0.072–0.125) | 0.126 | 0.030 | 0.874 |
| 0.65 | cal | 0.8 | 500 | 99 | 0.198 (0.164–0.236) | 0.228 | 0.030 | 0.772 |
| 0.65 | cal | 1.0 | 500 | 72 | 0.144 (0.114–0.178) | 0.172 | 0.028 | 0.828 |
| 0.65 | flat | 0.5 | 500 | 213 | 0.426 (0.382–0.471) | 0.664 | 0.238 | 0.336 |
| 0.65 | flat | 0.8 | 500 | 181 | 0.362 (0.320–0.406) | 0.648 | 0.286 | 0.352 |
| 0.65 | flat | 1.0 | 500 | 178 | 0.356 (0.314–0.400) | 0.652 | 0.296 | 0.348 |
| 0.70 | cal | 0.5 | 500 | 124 | 0.248 (0.211–0.288) | 0.266 | 0.018 | 0.734 |
| 0.70 | cal | 0.8 | 500 | 157 | 0.314 (0.274–0.357) | 0.376 | 0.062 | 0.624 |
| 0.70 | cal | 1.0 | 500 | 133 | 0.266 (0.228–0.307) | 0.328 | 0.062 | 0.672 |
| 0.70 | flat | 0.5 | 500 | 266 | 0.532 (0.487–0.576) | 0.690 | 0.158 | 0.310 |
| 0.70 | flat | 0.8 | 500 | 224 | 0.448 (0.404–0.493) | 0.726 | 0.278 | 0.274 |
| 0.70 | flat | 1.0 | 500 | 216 | 0.432 (0.388–0.477) | 0.704 | 0.272 | 0.296 |
| 0.75 | cal | 0.5 | 500 | 217 | 0.434 (0.390–0.479) | 0.492 | 0.058 | 0.508 |
| 0.75 | cal | 0.8 | 500 | 219 | 0.438 (0.394–0.483) | 0.502 | 0.064 | 0.498 |
| 0.75 | cal | 1.0 | 500 | 203 | 0.406 (0.363–0.450) | 0.478 | 0.072 | 0.522 |
| 0.75 | flat | 0.5 | 500 | 294 | 0.588 (0.543–0.632) | 0.712 | 0.124 | 0.288 |
| 0.75 | flat | 0.8 | 500 | 275 | 0.550 (0.505–0.594) | 0.734 | 0.184 | 0.266 |
| 0.75 | flat | 1.0 | 500 | 242 | 0.484 (0.439–0.529) | 0.688 | 0.204 | 0.312 |
| 0.80 | cal | 0.5 | 500 | 309 | 0.618 (0.574–0.661) | 0.676 | 0.058 | 0.324 |
| 0.80 | cal | 0.8 | 500 | 293 | 0.586 (0.541–0.630) | 0.684 | 0.098 | 0.316 |
| 0.80 | cal | 1.0 | 500 | 268 | 0.536 (0.491–0.580) | 0.630 | 0.094 | 0.370 |
| 0.80 | flat | 0.5 | 500 | 332 | 0.664 (0.621–0.705) | 0.770 | 0.106 | 0.230 |
| 0.80 | flat | 0.8 | 500 | 299 | 0.598 (0.554–0.641) | 0.736 | 0.138 | 0.264 |
| 0.80 | flat | 1.0 | 500 | 270 | 0.540 (0.495–0.584) | 0.690 | 0.150 | 0.310 |
| 0.90 | cal | 0.5 | 500 | 458 | 0.916 (0.888–0.939) | 0.942 | 0.026 | 0.058 |
| 0.90 | cal | 0.8 | 500 | 414 | 0.828 (0.792–0.860) | 0.898 | 0.070 | 0.102 |
| 0.90 | cal | 1.0 | 500 | 388 | 0.776 (0.737–0.812) | 0.846 | 0.070 | 0.154 |
| 0.90 | flat | 0.5 | 500 | 409 | 0.818 (0.781–0.851) | 0.864 | 0.046 | 0.136 |
| 0.90 | flat | 0.8 | 500 | 380 | 0.760 (0.720–0.797) | 0.830 | 0.070 | 0.170 |
| 0.90 | flat | 1.0 | 500 | 336 | 0.672 (0.629–0.713) | 0.762 | 0.090 | 0.238 |
| 1.00 | cal | 0.5 | 500 | 500 | 1.000 (0.993–1.000) | 1.000 | 0.000 | 0.000 |
| 1.00 | cal | 0.8 | 500 | 500 | 1.000 (0.993–1.000) | 1.000 | 0.000 | 0.000 |
| 1.00 | cal | 1.0 | 500 | 500 | 1.000 (0.993–1.000) | 1.000 | 0.000 | 0.000 |
| 1.00 | flat | 0.5 | 500 | 470 | 0.940 (0.915–0.959) | 0.940 | 0.000 | 0.060 |
| 1.00 | flat | 0.8 | 500 | 460 | 0.920 (0.893–0.942) | 0.920 | 0.000 | 0.080 |
| 1.00 | flat | 1.0 | 500 | 418 | 0.836 (0.801–0.867) | 0.836 | 0.000 | 0.164 |

## 4. Registered hypothesis tests (T4)

| Hypothesis | Test/result | Registered conclusion |
|---|---|---|
| H-E1 | Cochran–Armitage z=46.309, p(one-sided)=0; logistic q slope 14.798 [13.953, 15.643] | Holm p=0; supported=True |
| H-E2 | q=1.00/cal: 500/500 (1.000; exact CI 0.993–1.000); q=0.50/cal: 0/500 (0.000; exact CI 0.000–0.007); q=0.50/flat: 115/500 (0.230; exact CI 0.194–0.269) | Supported=True |
| H-E3 | q=0.6: flat−cal RD=0.264 (Newcombe 0.217–0.310), p=4.758e-26, Holm=1.427e-25; q=0.7: flat−cal RD=0.166 (Newcombe 0.107–0.223), p=3.661e-08, Holm=7.321e-08; q=0.8: flat−cal RD=0.004 (Newcombe -0.058–0.066), p=0.8991, Holm=0.8991 | Global Holm p=4.282e-25 |
| H-E4 | q=0.7: trend z=0.900, p=0.3684, Holm=0.3684; false-grasp rates=ρ1.0:0.062,ρ0.8:0.062,ρ0.5:0.018; q=0.8: trend z=-2.571, p=0.01013, Holm=0.02026; false-grasp rates=ρ1.0:0.094,ρ0.8:0.098,ρ0.5:0.058; q=0.9: trend z=-6.101, p=1.054e-09, Holm=3.161e-09; false-grasp rates=ρ1.0:0.070,ρ0.8:0.070,ρ0.5:0.026 | Global Holm p=6.323e-09 |
| H-R1 | Conditional GEE, global Wald p=3.576e-50; subject-cluster exchangeable | V1 passed; H-R1 supported=True |

Protocol-wide Holm adjustment is reported in `ANALYSIS.json` for all confirmatory hypotheses eligible for testing. H-R1 is included only if the V1 gate passes. Within-family E3/E4 Holm adjustments are also reported.

## 5. Real decoders and control utility (T5)

| Variant | Quality / episodes | Control result | Calibration |
|---|---|---|---|
| D1 | 4725 | BA=0.543 (0.519–0.566) | ECE=0.030; conf≥.75=0.018 |
| D2 | 4725 | BA=0.530 (0.507–0.553) | ECE=0.062; conf≥.75=0.032 |
| D3 | 4725 | BA=0.596 (0.573–0.619) | ECE=0.022; conf≥.75=0.039 |
| D4 | 4725 | BA=0.532 (0.508–0.555) | ECE=0.438; conf≥.75=0.947 |
| D1_plt | 4725 | BA=0.543 (0.520–0.566) | ECE=0.006; conf≥.75=0.002 |
| D2_plt | 4725 | BA=0.530 (0.507–0.553) | ECE=0.003; conf≥.75=0.000 |
| D3_plt | 4725 | BA=0.599 (0.577–0.622) | ECE=0.053; conf≥.75=0.010 |
| D4_plt | 4725 | BA=0.531 (0.508–0.554) | ECE=0.023; conf≥.75=0.000 |
| D5_raw | 1575 | BA=0.609 (0.569–0.648) | ECE=0.301; conf≥.75=0.843 |
| D5_plt | 1575 | BA=0.565 (0.524–0.605) | ECE=0.044; conf≥.75=0.147 |
| R0 M1 | 140 episodes | success=3/140 (0.021; exact 0.004–0.061) | false-grasp=0.021; miss=0.957 |
| R0 M2 | 140 episodes | success=20/140 (0.143; exact 0.089–0.212) | false-grasp=0.193; miss=0.664 |
| R0 M3 | 140 episodes | success=17/140 (0.121; exact 0.072–0.187) | false-grasp=0.300; miss=0.579 |
| R0 ORACLE | 140 episodes | success=140/140 (1.000; exact 0.974–1.000) | false-grasp=0.000; miss=0.000 |
| R1 D1 plt | 2285 episodes | cue-correct=0/2285 (0.000; exact 95% 0.000–0.002) | completion=0.000; false-grasp=0.000; miss=1.000 |
| R1 D1 raw | 2285 episodes | cue-correct=19/2285 (0.008; exact 95% 0.005–0.013) | completion=0.011; false-grasp=0.003; miss=0.989 |
| R1 D2 plt | 2285 episodes | cue-correct=0/2285 (0.000; exact 95% 0.000–0.002) | completion=0.000; false-grasp=0.000; miss=1.000 |
| R1 D2 raw | 2285 episodes | cue-correct=47/2285 (0.021; exact 95% 0.015–0.027) | completion=0.032; false-grasp=0.012; miss=0.968 |
| R1 D3 plt | 2285 episodes | cue-correct=0/2285 (0.000; exact 95% 0.000–0.002) | completion=0.010; false-grasp=0.010; miss=0.990 |
| R1 D3 raw | 2285 episodes | cue-correct=44/2285 (0.019; exact 95% 0.014–0.026) | completion=0.032; false-grasp=0.013; miss=0.968 |
| R1 D4 plt | 2285 episodes | cue-correct=0/2285 (0.000; exact 95% 0.000–0.002) | completion=0.000; false-grasp=0.000; miss=1.000 |
| R1 D4 raw | 2285 episodes | cue-correct=524/2285 (0.229; exact 95% 0.212–0.247) | completion=0.651; false-grasp=0.422; miss=0.349 |
| R1 D5 plt | 735 episodes | cue-correct=82/735 (0.112; exact 95% 0.090–0.137) | completion=0.139; false-grasp=0.027; miss=0.861 |
| R1 D5 raw | 735 episodes | cue-correct=226/735 (0.307; exact 95% 0.274–0.342) | completion=0.665; false-grasp=0.358; miss=0.335 |

WP5 integrity: 105 subjects passed and 4 failed the registered sampling-rate, channel-count or event-count checks; excluded IDs (selected by checks, not hard-coded): S088, S092, S100, S104. The committed R1 set contains 19750 unique episodes. D5 replay uses the held-out R12 run only.

R0 comparisons are descriptive only. If the V1 manipulation check failed, no decoder-quality ordering claim is made and R1 inferential tests are omitted.

## 6. Sensitivity (WP7)

Arm S executed 128 cells, each N=200; all detailed rates in ANALYSIS.json and F7. The primary configuration remained unchanged; each temporary configuration and its SHA-256 is under `config/`.

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
- **D5 split implementation correction:** D5 is trained on R04/R08 and evaluated on held-out R12. The initial runner attempted a training-run epoch with intentionally undefined D5 confidence; replay-input validation rejected it before controller simulation. The rejected CSV and attempt are preserved in `replay_csv/R1/FAILED_INPUT_R1_D5_raw_S001_01.csv`, `results/EXCLUSIONS.csv`, and `results/WP5_D5_REPLAY_CORRECTION.json`. D5 replay was corrected to R12 only; no model, controller or task parameters changed.
- Each emulator episode is deterministic given its label/confidence sequence; random draws follow the registered master seed and cell/episode seed arithmetic.
- MyoSim was run at commit `67ee74e3230b068b5db760efa15da3669e315eb3` (v0.1.5) with the numeric-identical C1/C2 config. MyoSim source was not edited.
- All results are an offline software simulation of a controller. No claims are made about online BCI, patients, prostheses, hardware or clinical benefit.
- Known limits include sample-and-hold trial decisions, parametric independent emulator draws, deterministic physics, and the fixed (not optimized) controller gate settings.

## 10. Reproducibility and provenance

- Python 3.12.3; MyoSim commit `67ee74e3230b068b5db760efa15da3669e315eb3`.
- Input hashes and environment package versions: `registry/ENVIRONMENT.json`.
- Frozen protocol, design, C2 configuration and reference code SHA-256: `registry/FREEZE_MANIFEST.json`.
- Final output hashes: `registry/OUTPUT_MANIFEST.json`.
- No outcome-driven tuning or unregistered parameter changes were performed.
