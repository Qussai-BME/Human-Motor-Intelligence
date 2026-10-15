# PROTOCOL P6-C2-EPISODE-v1.0
## Episode-level replay study of decoder quality, calibration and persistence versus simulated control utility

**Owner:** Qussai Adlbi · **Status:** DRAFT FOR EXECUTION (freeze → hash → run) · **Supersedes:** nothing (C1 remains the archived confirmatory record) · **Prepared:** 2026-10-08

This document is written for an autonomous executing agent. Follow it literally. Where it says MUST, deviation requires stopping and asking the owner. Where it says MAY, use judgement and log the choice.

---

## 0. Operating rules for the executing agent

1. **Freeze before you run.** Complete WP0, then compute SHA-256 of this file, `c2_design.yaml`, `config/p6_c2_mysim.yaml` and the reference code, and write them to `registry/FREEZE_MANIFEST.json` **before generating any decoder-conditioned or emulated outcome** (WP1 pre-flight outputs are allowed; they are engineering checks).
2. **Do not change the controller.** MyoSim v0.1.5 at commit `67ee74e3230b068b5db760efa15da3669e315eb3`, and every numeric parameter in `config/p6_c2_mysim.yaml`, are identical to C1 (confidence 0.75, 3 windows, dwell 0.08 s, stale-input 0.30 s, task timeout 8.0 s, target radius 0.08 m). A `diff` against the C1 config MUST show no numeric change. Do not edit MyoSim source.
3. **No outcome-driven changes.** Parameters in §3 and the analysis in §7 are fixed. If a gate fails, apply the stop rule in §9; do not tune parameters until a gate passes.
4. **Everything is logged.** Every run writes its replay CSV, per-event log, result JSON and a manifest row. No run is discarded; failed or invalid runs are listed in `results/EXCLUSIONS.csv` with the reason.
5. **Report honestly.** Null and unexpected results are reported with the same prominence as expected ones. Post-hoc analyses are labelled `POST_HOC` and kept in a separate file.
6. **Ask when blocked.** Missing data (EEGMMIDB), missing packages or ambiguous instructions → stop and report to the owner with the exact error. Do not substitute data or methods silently.
7. **No clinical language.** This is a software simulation of a controller. No prosthetic, patient, medical-device or online-BCI claims in any output.

---

## 1. Rationale (why C2 exists)

C1 (decoder → intent replay → MyoSim) returned 0/60 task successes, but an audit showed the endpoint was unreachable by construction:

| C1 defect | Evidence | C2 remedy |
|---|---|---|
| One decoder output per 8.2-s trial vs task clock 8.0 s → only 2 of 15 events reach the task | 840/840 gaps > 8.0 s | Episode-scoped stream at 0.1-s cadence (§3) |
| Engine needs ≥ 4 consecutive confident same-label windows; oracle streams never exceed 2 | Oracle 0/20; max run 2 | Sample-and-hold windows so a confident output persists ≥ 10 windows |
| Release needs REST/RELEASE; two-class decoders never emit REST, and a released command can only be ended by an explicit REST (HOLD returns to the same label) | Controller source (`state_machine.py`) | Cue-locked scheduled REST windows between trials |
| Decoders were at chance (all p ≥ 0.77); M2 ≈ M3 | Manuscript §4.2 | Controlled accuracy ladder (emulator) + manipulation check for real decoders |
| Metrics computed after task failure | 171/207 transitions post-failure | Episode scoring only inside the episode window |
| No floor/ceiling control | — | Oracle (ceiling), chance arms (floor), sparse-cadence regression control X0 |

**Primary question.** Under the registered controller, how does cue-correct episode success depend on decoder *accuracy*, *confidence calibration* and *temporal persistence*, and where do real zero-calibration EEG decoders fall on that curve?

---

## 2. Design overview

| Arm | Content | Role | Runs |
|---|---|---|---|
| **X0** | Oracle episodes in the *C1 sparse format* (8.2-s spacing, no REST) | Regression control: must score 0 (proves the checklist detects the C1 defect) | 100 |
| **E** | Emulated decoders: accuracy q × confidence regime × persistence ρ | **Primary confirmatory** dose–response | 54 cells × 500 = 27,000 |
| **S** | Controller-parameter sensitivity of the E curve | Exploratory (pre-specified) | ≤ 25,600 |
| **R0** | C1 decoders M1–M3 (existing traces) on the C2 interface | Descriptive; expected ≈ floor | 3 × 140 = 420 |
| **R1** | New real decoders D1–D5 (larger training pool) on the C2 interface | Confirmatory **only if** manipulation check V1 passes (§6.3) | ≈ 8 variants × 2,300 |
| **W** | Windowed decoders (optional) | Exploratory | optional |

Every episode is **deterministic given its label/confidence sequence** (MyoSim physics has no stochasticity; re-running the same CSV gives identical output). Randomness lives only in the emulator draws and the real-decoder predictions. Consequently episodes are independent Bernoulli trials within an emulator cell.

---

## 3. Fixed interface specification

### 3.1 Episode template (time grid Δ = 0.1 s, 70 windows, 7.0 s)

| Segment | Windows (index) | Time (s) | Label stream | Confidence |
|---|---|---|---|---|
| A. Warm-up | 0–19 | 0.0–1.9 | `REST` | 0.99 |
| B. **Decoy trial** (true class T1 → `OPEN`) | 20–29 | 2.0–2.9 | decoder output held for 10 windows | decoder |
| C. Gap | 30–39 | 3.0–3.9 | `REST` | 0.99 |
| D. **Grasp trial** (true class T2 → `CLOSE`) | 40–49 | 4.0–4.9 | decoder output held for 10 windows | decoder |
| E. Tail | 50–69 | 5.0–6.9 | `REST` | 0.99 |

Rationale (verified in pilot): the scripted approach is reached at ≈ 1.6 s, so the grasp gate is open during the decoy trial (a false confident `CLOSE` therefore causes a real premature grasp); a confirmed `CLOSE` in segment D executes at ≈ 4.3 s, transport is reached at ≈ 4.9 s and the object is released in the target at ≈ 5.0 s; the whole episode fits inside the unchanged 8.0-s task clock.

**REST assumption (A1, must be stated in every report):** REST windows are *cue-locked and scheduled by the protocol*, not decoded (synchronous paradigm). The controller can leave `EXECUTING` only through an explicit REST, and the two-class decoders have no REST output.

**Persistence rule.** `rho = 1.0` is pure sample-and-hold (one decoder output per trial repeated for 10 windows). For `rho < 1`, each window after the first repeats the previous window's (label, confidence) with probability `rho` and otherwise redraws independently from the decoder.

### 3.2 Replay CSV schema (identical to C1 / `CsvIntentReplay`)

`timestamp_s,label,confidence,source_subject,modality,model_version,window_id`
Labels ∈ {`REST`,`OPEN`,`CLOSE`}; confidence ∈ [0.5, 1.0] for decoder windows, 0.99 for scheduled REST; timestamps strictly increasing at 0.1 s, formatted `%.3f`; `window_id` zero-padded 4-digit.

### 3.3 Scoring (computed from the per-event log, never from MyoSim metrics alone)

Let `grasp_onset` be the timestamp of the task transition with reason `decoded_grasp_command`.

* **`task_completion`** = final task state is `COMPLETE`.
* **`false_grasp`** = at any event with 2.0 ≤ t < 4.0 the controller state is `EXECUTING` and the released command is `CLOSE`.
* **`miss`** = no `decoded_grasp_command` transition at all.
* **`cue_correct_success` (PRIMARY ENDPOINT)** = `task_completion` ∧ `grasp_onset` ∈ [4.0, 5.5] ∧ ¬`false_grasp`.

Secondary: `task_completion`, `false_grasp`, `miss`, `grasp_onset`, `completion_time_s`, `final_error_m`, `released_command_count`. Reference implementation: `reference_code/c2_runner.py` (`run`, `episode`) and `reference_code/c2_emulator_pilot.py` (`build`, `score`). Edit the two path constants at the top of `c2_runner.py` (`MYO`, `P6`) for your machine.

### 3.4 Truth table to reproduce (Appendix A)

Under `rho = 1.0`, with `pass = confidence ≥ 0.75`, a cue-correct success occurs **iff** the grasp trial outputs `CLOSE` with `pass` and the decoy trial does **not** output `CLOSE` with `pass`. The 16 configurations in Appendix A MUST be reproduced exactly in WP1.

---

## 4. Work packages

### WP0 — Environment and provenance
1. Clone `github.com/Qussai-BME/MyoSim`, check out `67ee74e3230b068b5db760efa15da3669e315eb3`; Python ≥ 3.12; `mujoco` ≥ 3.3 (<4); numpy, scipy, pandas, matplotlib, pyyaml, statsmodels, scikit-learn; `pyriemann` and `mne` for WP5.
2. Re-execute the C1 fixture and three archived C1 decoder replays (M1_S001, M3_S015, fixture) and confirm success, path length, final error and command corrections are **bit-identical** to the C1 archive. Failure → STOP.
3. Record: Python/MuJoCo/numpy versions, CPU, `git rev-parse HEAD`, SHA-256 of config and all inputs → `registry/ENVIRONMENT.json`.
4. Diff `config/p6_c2_mysim.yaml` against the C1 config; commit the (empty) numeric diff to `registry/CONFIG_DIFF.txt`.

### WP1 — Pre-flight validity gates (engineering; no decoder outcomes)
All of the following MUST pass before WP2. Record each in `results/PREFLIGHT.json`.

| Gate | Test | Pass criterion |
|---|---|---|
| **V3 ceiling** | 100 oracle episodes (decoy `OPEN` conf 1.0; grasp `CLOSE` conf 1.0) | `cue_correct_success` = 100/100; `completion` at ≈ 5.0 s |
| **V2 floor (calibrated chance)** | 100 episodes, q = 0.5, calibrated (conf ≡ 0.5) | `cue_correct_success` ≤ 1/100 |
| **V4 timing** | Cadence 0.1 s < stale-input 0.30 s; episode 7.0 s < task timeout 8.0 s; approach, grasp, transport, release timestamps within ±0.2 s of §3.1 | all true |
| **Truth table** | 16 hold configurations (Appendix A) | all 16 outcomes identical |
| **Determinism** | Re-run 20 random episodes twice | byte-identical result JSON |
| **X0 regression control** | 100 oracle episodes in the *C1 sparse format* (one decoder output per 8.2-s trial, 15 events, no REST) | `cue_correct_success` = 0/100 (shows the C1 defect is detectable) |
| **V5 variability** | Pilot cells q ∈ {0.6, 0.7, 0.8, 0.9} × cal/flat, 100 episodes each | no cell is 0% or 100% except as listed in Appendix B |

### WP2 — Emulator dose–response (Arm E) — PRIMARY CONFIRMATORY

**Grid (54 cells):** accuracy `q ∈ {0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 1.00}` × regime `{cal, flat}` × persistence `rho ∈ {1.0, 0.8, 0.5}`; **N = 500 episodes per cell**.

**Decoder emulators** (per trial, true class y, `other` = the opposite class):

* `cal` (calibrated): draw `m=(q−0.5)/0.5`; `c = 0.5 + 0.5·Beta(4m, 4(1−m))` (degenerate: `c=0.5` if m=0, `c=1.0` if m=1); output `y` with probability `c`, else `other`. Accuracy = q; P(correct | c) = c.
* `flat` (uninformative, over-confident — mimics C1 M2/M3): `c = 0.5 + 0.5·Beta(2.8, 1.2)` (mean confidence 0.85, independent of correctness); output `y` with probability `q`.
* Decoy trial true class = `OPEN`; grasp trial true class = `CLOSE`.

**Seeds.** `master_seed = 20261008`. Cell seed = `master_seed + 1000·cell_index` (cell_index in grid order, `cal` before `flat`, `rho` descending); episode i uses a `numpy.random.default_rng(cell_seed + i)` stream. Persist the seed in each manifest row.

**Execution.** Write each CSV, run MyoSim with the unchanged config, score per §3.3, append to `results/emulator_episodes.csv` (schema §8). Expected throughput ≈ 0.07 s/episode (single core) → ≈ 35 min for the whole arm.

### WP3 — Analytic cross-check (validity of the MC arm)
`reference_code/c2_analytic_hold.py` gives closed-form expected `cue_correct_success` for `rho = 1.0` (Appendix B). For every `rho = 1.0` cell the Monte Carlo estimate MUST lie within 3 standard errors of the analytic value. Failure indicates an implementation error → STOP and debug (do not change the analytic reference).

### WP4 — Arm R0: C1 decoders on the C2 interface (descriptive)
Inputs: `p6/c_mi_r04_primary/traces/{M1,M2,M3}/*_S###.csv` (15 epochs/subject: `ground_truth`, `prediction`, `confidence`). For each subject order T1 (`OPEN`) epochs and T2 (`CLOSE`) epochs by `epoch_index`; pair the k-th T1 with the k-th T2 for k = 1…7 (the 8th epoch of the larger class is unused) → 140 episodes per decoder, identical pairs across M1–M3 and the oracle. Hold each epoch's (`prediction`, `confidence`) for 10 windows. Also run the oracle on the same pairs. Report cue-correct success with exact CIs and false-grasp / miss rates. **No inferential contrast** among M1–M3 (V1 fails for C1 decoders).

### WP5 — Arm R1: real decoders with a genuine quality spread (conditional)

**Data.** PhysioNet EEGMMIDB v1.0.0, runs R04, R08, R12 (imagined left vs right fist; T1 = left, T2 = right), 160 Hz. Integrity check per subject: fs = 160 Hz, 64 channels, exactly 15 imagery events per run, T1/T2 only. Exclude any subject failing the check and list them in `registry/SUBJECT_EXCLUSIONS.csv` (known problem subjects such as S088, S089, S092, S100, S104 are expected to be caught by the check; do not hard-code). If the data are unavailable offline → STOP and request the data from the owner.

**Epoching/features.** Same preprocessing as C1 (`p6/c_mi_r04_primary/scripts/p6_mi_core.py`): epoch 1.0–3.5 s after cue, Welch band power, channel set as in that file; document any deviation.

**Decoders (fixed hyper-parameters; no tuning on test subjects):**

| ID | Pipeline | Type |
|---|---|---|
| D1 | log relative band power 8–30 Hz → standardise → L2-LR (C = 0.1) | zero-calibration |
| D2 | two-band power (8–12, 13–30 Hz) → standardise → L2-LR (C = 1.0) | zero-calibration |
| D3 | CSP (6 filters, 8–30 Hz) → shrinkage LDA | zero-calibration |
| D4 | OAS covariance → tangent space (`pyriemann`) → L2-LR | zero-calibration |
| D5 | within-subject CSP + shrinkage LDA, trained on the subject's first two imagery runs (R04, R08), tested on R12 | calibrated reference (NOT zero-calibration; label as such) |

**Validation.** Zero-calibration decoders: 5-fold *grouped-by-subject* cross-validation (every subject held out exactly once; fixed fold assignment from `master_seed`). Each decoder is evaluated in two confidence variants: `raw` (model probability) and `plt` (Platt scaling fitted **only on the training-fold subjects**). That gives 4 × 2 zero-calibration variants + D5 (raw, plt).

**Manipulation check V1 (gate for confirmatory R1 claims).** Compute per-variant pooled balanced accuracy with exact 95% CI over all held-out epochs. R1 is *confirmatory* only if **both**: (P1) the best zero-calibration decoder has pooled BA ≥ 0.58 with lower exact CI > 0.55; (P2) the best and worst zero-calibration decoders differ in epoch-level accuracy by a subject-cluster bootstrap 95% CI (10,000 resamples) that excludes 0. Otherwise R1 is reported descriptively, the deviation is declared, and the owner is notified (§9).

**Episodes.** Per subject and decoder: order T1/T2 epochs chronologically, pair k-th with k-th, hold 10 windows → ≈ 22 pairs/subject (≈ 2,300 episodes/decoder). Pairs are identical across decoders and variants (paired design). Run all variants + oracle.

### WP6 — Arm W: windowed decoders (OPTIONAL, exploratory)
Train D1–D4 on 1.0-s windows; for each epoch take the 10 windows (hop 0.1 s) whose end-times fall in the last 1.0 s of the 2.5-s epoch; stream them unheld. Report as exploratory only.

### WP7 — Arm S: controller-parameter sensitivity (exploratory, pre-specified)
Repeat `rho = 1.0`, q ∈ {0.6, 0.7, 0.8, 0.9} × {cal, flat} with N = 200 for `confidence_threshold ∈ {0.60, 0.70, 0.75, 0.85}` × `confirmation_windows ∈ {1, 2, 3, 5}` (use temporary config copies; hash each; the primary config is untouched). Purpose: quantify how much the accuracy → utility mapping depends on the gate settings.

### WP8 — Analysis, figures, report
Run §7; produce the deliverables in §8 and the report skeleton in §10.

---

## 5. Hypotheses (confirmatory unless marked)

Family-wise α = 0.05 over H-E1…H-E4 and H-R1 (Holm). Exact CIs are Clopper–Pearson.

* **H-E1 (dose–response).** For `cal`, `rho = 1.0`, cue-correct success increases monotonically with q. Test: one-sided Cochran–Armitage trend over the 9 levels, plus logistic slope in q > 0.
* **H-E2 (ceiling/floor structure).** (a) `cal`, q = 1.0: success ≥ 0.99. (b) `cal`, q = 0.5: success ≤ 0.01. (c) `flat`, q = 0.5, `rho = 1.0` (chance, over-confident): lower exact 95% bound **> 0.10**, i.e. an over-confident chance decoder has a non-zero floor (analytic expectation 0.24).
* **H-E3 (calibration effect).** At q ∈ {0.6, 0.7, 0.8}, `rho = 1.0`, success differs between `cal` and `flat` (two-sided two-proportion test, Holm over the 3 comparisons). *Predicted:* `flat > cal` at q ≤ 0.7, parity near q = 0.8, `cal > flat` at q ≥ 0.9 (analytic crossover in [0.75, 0.85]).
* **H-E4 (persistence).** At q ∈ {0.7, 0.8, 0.9}, `cal`, success varies with `rho ∈ {1.0, 0.8, 0.5}` (two-sided Cochran–Armitage trend; Holm over 3 q levels). Direction is *not* predicted (pilot suggests lower persistence gives more chances to confirm); also report `false_grasp`.
* **H-R1 (real decoders; conditional on V1).** Among zero-calibration variants, cue-correct success differs across decoders. Test: GEE logistic (exchangeable, clustered by subject) with decoder as factor; pairwise Holm-adjusted contrasts; paired McNemar on identical episodes as sensitivity.
* **Exploratory (label `EXPLORATORY`):** localisation of each real decoder on the emulator curve (equivalent accuracy `q_eq`, §7.5); calibration effect (`raw` vs `plt`) within decoders; Arm S; Arm W.

---

## 6. Quality gates summary (stop/go)

| Gate | Where | If it fails |
|---|---|---|
| WP0 bit-identical C1 re-execution | WP0 | STOP; report environment diff |
| V3 ceiling = 100/100 | WP1 | STOP; interface cannot reach endpoint |
| V2 floor ≤ 1/100 | WP1 | STOP; scoring bug or leak |
| Truth table (16/16) | WP1 | STOP |
| X0 = 0/100 | WP1 | STOP (checklist insensitive) |
| MC vs analytic within 3 SE (rho = 1) | WP3 | STOP; debug emulator |
| V1 (P1 ∧ P2) | WP5 | R1 descriptive only; notify owner |

---

## 7. Statistical analysis plan

7.1 **Per-cell estimates.** Success proportion with exact 95% CI for every cell and endpoint (primary: `cue_correct_success`).
7.2 **Trend tests (H-E1, H-E4).** Cochran–Armitage (`statsmodels` or hand-coded; document), plus logistic regression `success ~ q` (H-E1) with Wald CI for the slope.
7.3 **Calibration contrasts (H-E3).** Two-sided two-proportion z-tests with continuity-free exact (Fisher) fallback when any expected count < 5; Holm adjustment; report risk difference with Newcombe 95% CI.
7.4 **Global model (descriptive).** Logistic GLM `success ~ (q + q²) × regime × rho`; report likelihood-ratio tests for interactions; no confirmatory claim from this model.
7.5 **Equivalent accuracy for real decoders.** For each R1 variant compute its observed cue-correct success `s` and its calibration summary (ECE, share of events with conf ≥ 0.75); select the emulator regime (`cal` or `flat`) with the closest ECE; invert the emulator curve (`rho = 1.0`) by linear interpolation to obtain `q_eq` with a bootstrap 95% CI. Label EXPLORATORY.
7.6 **Real-decoder inference (H-R1).** GEE logistic, exchangeable correlation, cluster = subject; pairwise contrasts with Holm; sensitivity: McNemar on identical episodes; report absolute success differences with subject-cluster bootstrap 95% CIs (10,000 resamples, seed `master_seed`).
7.7 **Power (planned).** With N = 500 per emulator cell and α = 0.05/12, power to detect a risk difference of 0.15 near p = 0.5 is ≈ 0.97; 0.10 → ≈ 0.62; exact CI half-width ≤ 0.058 at p = 0.5 (n = 300 gives ≈ 0.81 / 0.34; hence N = 500).
7.8 **Missing/invalid runs.** Any run with `invalid_state_detected` = true is re-run once; if it recurs it is kept as `invalid` and counted as a non-success, and listed in EXCLUSIONS.csv. Never silently dropped.

---

## 8. Deliverables and file schemas

```
P6_C2_RESULTS/
  registry/  FREEZE_MANIFEST.json  ENVIRONMENT.json  CONFIG_DIFF.txt  SUBJECT_EXCLUSIONS.csv
  config/    p6_c2_mysim.yaml  (+ S-arm temporary configs with hashes)
  replay_csv/{X0,E,R0,R1,W}/...            # every CSV actually run
  logs/      per-episode event logs (parquet or csv.gz)
  results/
    PREFLIGHT.json
    emulator_episodes.csv     # episode_id,arm,q,regime,rho,cell_index,seed,decoy_label,decoy_pass,grasp_label,grasp_pass,
                              # task_completion,false_grasp,miss,cue_correct_success,grasp_onset,completion_time_s,
                              # final_error_m,released_command_count,csv_sha256
    real_episodes.csv         # episode_id,arm,decoder,variant,subject,pair_index,... same outcome columns
    decoder_quality_R1.json   # pooled BA, exact CI, ECE, share conf>=0.75 per variant; V1 verdict
    ANALYSIS.json             # every statistic named in §7 with p, CI, test name
    EXCLUSIONS.csv
  figures/    (300 dpi PNG + PDF) — see below
  REPORT_C2.md
```

**Required figures** (match the manuscript style: colour-blind-safe palette, panel letters, exact CIs): F1 interface timeline (episode template with approach/grasp/transport/release markers from a real run); F2 emulator dose–response (cue-correct and task completion vs q; cal vs flat; three rho panels; ceiling/floor annotated); F3 calibration crossover (risk difference flat − cal vs q with CIs); F4 persistence effect and false-grasp rate; F5 real-decoder quality (pooled BA with exact CIs; reliability); F6 real decoders on the emulator curve (`q_eq`); F7 sensitivity heat-maps (Arm S); F8 X0 regression control vs C2 oracle (the C1 defect, shown).

**Required tables:** T1 design/arms and counts; T2 pre-flight gates; T3 emulator cell results; T4 hypothesis tests (H-E1…H-R1); T5 real-decoder quality and control success; T6 claim–evidence matrix.

---

## 9. Stop rules and deviation handling

* Any gate in §6 fails → STOP, write `results/STOP_REPORT.md` (what failed, numbers, hypotheses for the cause, no parameter changes), and notify the owner.
* Unexpected controller behaviour (e.g. oracle episode failing in a subset): save the offending CSV and event log; do **not** alter the template.
* Any change to §3 or §5 after freeze is a protocol amendment: stop, describe, and wait for the owner’s written approval; amendments get `P6-C2-v1.1`, a new freeze hash and a note in the report.
* If R1’s V1 fails, continue with all other arms, report R1 descriptively, and list candidate remedies for a later amendment (e.g. stronger architectures, more data) without acting on them.

---

## 10. Report skeleton (`REPORT_C2.md`, to be merged into manuscript §4–5 of P6)

1. Pre-flight validity (table of gates; X0 vs C2 oracle figure).
2. Emulator dose–response: H-E1/H-E2 with exact CIs; ceiling/floor findings (including the chance-level over-confident floor).
3. Calibration and persistence: H-E3, H-E4; false-grasp analysis.
4. Real decoders: quality (V1), control success, `q_eq` placement (if V1 passed) or descriptive-only statement.
5. Sensitivity of the mapping to controller gate settings (Arm S).
6. Deviations, exclusions, software versions, hashes.

**Interpretation rules (what each outcome licenses):**

| Outcome | Licensed statement |
|---|---|
| H-E1 supported | Under this controller and interface, control success rises with decoder accuracy at a rate of … (CI); success ≥ 0.99 requires q = 1.0 with calibrated confidence. |
| H-E2(c) supported | A chance-level, over-confident decoder achieves X% cue-correct success: any control benefit must be assessed against this floor. |
| H-E3 supported | Confidence calibration changes control utility at fixed accuracy; calibrated confidence is advantageous only above q ≈ … |
| H-R1 + V1 passed | Real zero-calibration decoders differ in control utility by …; their equivalent accuracy is … |
| V1 failed | No claim about decoder quality ordering; report accuracy and calibration only. |
| Any outcome | No claim about online BCI, patients, prostheses or clinical benefit. |

---

## 11. Compute and timeline (single core, indicative)

WP0–WP1 ≈ 1–2 h · WP2 ≈ 35 min · WP3 minutes · WP4 ≈ 3 min · WP5 training ≈ 0.5–2 h + runs ≈ 20 min · WP7 ≈ 30 min · WP8 ≈ 1–2 h. Memory < 3 GB.

---

## Appendix A — Truth table for `rho = 1.0` (pilot, MyoSim v0.1.5)

`pass` = confidence ≥ 0.75 (pilot used 0.9 for pass, 0.6 for fail). Outcome = final task state; `cue_correct` per §3.3.

| Decoy label | Decoy pass | Grasp label | Grasp pass | Task state | Grasp onset (s) | cue_correct |
|---|---|---|---|---|---|---|
| OPEN | 0 | OPEN | 0 | WAIT_FOR_GRASP | — | 0 |
| OPEN | 0 | OPEN | 1 | WAIT_FOR_GRASP | — | 0 |
| OPEN | 0 | CLOSE | 0 | WAIT_FOR_GRASP | — | 0 |
| **OPEN** | **0** | **CLOSE** | **1** | COMPLETE | 4.3 | **1** |
| OPEN | 1 | OPEN | 0 | WAIT_FOR_GRASP | — | 0 |
| OPEN | 1 | OPEN | 1 | WAIT_FOR_GRASP | — | 0 |
| OPEN | 1 | CLOSE | 0 | WAIT_FOR_GRASP | — | 0 |
| **OPEN** | **1** | **CLOSE** | **1** | COMPLETE | 4.3 | **1** |
| CLOSE | 0 | OPEN | 0 | WAIT_FOR_GRASP | — | 0 |
| CLOSE | 0 | OPEN | 1 | WAIT_FOR_GRASP | — | 0 |
| CLOSE | 0 | CLOSE | 0 | WAIT_FOR_GRASP | — | 0 |
| **CLOSE** | **0** | **CLOSE** | **1** | COMPLETE | 4.3 | **1** |
| CLOSE | 1 | OPEN | 0 | COMPLETE | 2.3 | 0 (false grasp) |
| CLOSE | 1 | OPEN | 1 | COMPLETE | 2.3 | 0 (false grasp) |
| CLOSE | 1 | CLOSE | 0 | COMPLETE | 2.3 | 0 (false grasp) |
| CLOSE | 1 | CLOSE | 1 | COMPLETE | 2.3 | 0 (false grasp) |

Oracle episode: approach reached 1.6 s, grasp 4.3 s, transport reached 4.9 s, released in target 5.0 s. Note that `task_completion` alone rewards false grasps (4 of 16 configurations); this is why the primary endpoint is `cue_correct_success`.

## Appendix B — Expected values and pilot (N = 60 per cell, exploratory pilot, emulator only)

Closed-form expected `cue_correct_success` at `rho = 1.0` (`c2_analytic_hold.json`):

| q | cal | flat |
|---|---|---|
| 0.50 | 0.000 | 0.242 |
| 0.55 | 0.018 | 0.284 |
| 0.60 | 0.063 | 0.330 |
| 0.65 | 0.144 | 0.379 |
| 0.70 | 0.256 | 0.432 |
| 0.75 | 0.389 | 0.488 |
| 0.80 | 0.527 | 0.547 |
| 0.90 | 0.781 | 0.676 |
| 1.00 | 1.000 | 0.818 |

Pilot Monte-Carlo agreement (MyoSim, N = 60): cal q = 0.8 → 0.50; cal q = 0.9 → 0.82; flat q = 0.5 → 0.15; flat q = 0.7 → 0.42; flat q = 1.0 → 0.80; cal q = 1.0 → 1.00; cal q = 0.5 → 0.00. For `rho < 1`, pilot success was equal or higher (e.g. cal q = 0.9: 0.82 / 0.85 / 0.92 for rho = 1.0 / 0.8 / 0.5) because redraws give additional chances to confirm; false-grasp rates for the flat regime at chance were 0.33–0.48. Files: `pilot/c2_pilot.json`, `pilot/c2_pilot_dose_response.png`.

## Appendix C — Known limitations to carry into the report

1. REST is scheduled, not decoded (synchronous paradigm, A1); asynchronous operation is out of scope.
2. Sample-and-hold converts a trial-level decision into a sustained stream; Arm W partly addresses sliding-window decoders.
3. MyoSim physics is deterministic, so the experiment measures *controller-level* utility of decoder output statistics; it is not a physical-plant, human-in-the-loop or clinical evaluation.
4. Emulators are parametric (Beta-shaped confidence, independent trials); real decoder errors are correlated within subjects (handled in R1 by subject clustering).
5. Controller gate settings are those of C1; Arm S shows sensitivity but not optimality.
6. EEGMMIDB is a healthy-subject, 2-class, 160-Hz dataset; R1 results do not generalise to patients or other paradigms.
7. All outcomes are pre-specified at the cue-correct level; the composite endpoint depends on the declared scoring windows (§3.3).

## Appendix D — Agent checklist

- [ ] WP0 bit-identical C1 re-execution · [ ] FREEZE_MANIFEST written · [ ] WP1 gates all pass · [ ] WP2 54 × 500 episodes · [ ] WP3 analytic agreement · [ ] WP4 R0 · [ ] WP5 data integrity → decoders → V1 verdict → episodes · [ ] WP7 Arm S · [ ] ANALYSIS.json complete · [ ] 8 figures + 6 tables · [ ] REPORT_C2.md · [ ] hashes of every output in `registry/OUTPUT_MANIFEST.json` · [ ] STOP_REPORT.md only if a gate failed
