# V2 Protocol Lock — Recovery R1

**Status:** Locked before renewed external P4 acquisition  
**Scope:** P4 OpenBMI harmonized external validation only  
**Does not modify:** Frozen V1 or V1.1 results, manuscripts, result paths, or claims

## Reason for Recovery Namespace

The sandbox reset removed the prior V2 execution worktree and external derived caches. The previous P4 cache was reported as D1-passed before the reset, but no P4 model result had been accepted. Recovery R1 therefore begins a fresh external acquisition under a distinct namespace. It must not be called an archival restoration, a reanalysis of a prior completed result, or a direct replication of BCI Competition IV-2a.

The source baseline archive is recorded in `audit/V2_SANDBOX_RESET_RECOVERY.md`. This protocol is the binding execution record for newly acquired data.

## P4 Research Question and Evidence Boundary

The question is whether a fixed, strict zero-calibration subject-level LOSO EEG decoding evaluation can be observed on an independent binary motor-imagery dataset. The candidate is NEMAR OpenBMI/KU-MI derivative `nm000338` v1.0.5, source DOI `10.82901/nemar.nm000338`, supporting data DOI `10.5524/100542`, distributed under GPL-3.0.

> This is a **harmonized external validation**, not a direct replication. Scores from this binary dataset will not be numerically ranked against the four-class BCI Competition IV-2a result. Any eventual cross-dataset discussion is limited to protocol-qualified qualitative pattern comparison.

## Locked Data and Preprocessing Boundary

| Item | Locked value |
|---|---|
| Subjects | `sub-1` through `sub-54` |
| Session | `ses-1` |
| Recording files | `acq-train_run-1` and `acq-test_run-4` BDF plus matching event TSV |
| Target labels | `left_hand`, `right_hand`; 50 per label per recording |
| Channels | 62 named channels after excluding exactly `EMG1`–`EMG4` |
| Source sampling | 1000 Hz |
| Fixed preprocessing | 8–30 Hz fourth-order bandpass, 0.5–3.5 s post-event epoch, factor-8 deterministic decimation to 125 Hz |
| Derived cache expected shape | `(200, 62, 375)` per subject; merged class counts `[100, 100]` |
| Raw-data handling | Download one recording at a time only under `<LOCAL_WORKSPACE>/hmi_data/raw/v2_recovery_r1_openbmi_nm000338`; hash/receipt; cache derived data outside repository; delete all temporary raw BDF and TSV files in `finally` |

## Locked Analysis Boundary

The inference unit is subject. For every fold, all 53 other subjects are used for model/scaler fitting and the held-out subject is used only for prediction and subject-level metrics. There is no target-subject calibration, target-subject hyperparameter selection, or target-subject model selection.

| Fixed condition | Representation / classifier | Fit scope |
|---|---|---|
| `eeg-linear-v1` | Six deterministic time blocks; per-channel mean/std; standardised logistic regression | Training subjects only |
| `eeg-lda-v1` | Same time summaries; standardised shrinkage LDA | Training subjects only |
| `eeg-spectral-v1` | Fixed 8–12, 12–20, 20–30 Hz FFT-power summaries; standardised logistic regression | Training subjects only |
| `eeg-linear-svm-v1` | Same fixed spectral summaries; standardised LinearSVC | Training subjects only |
| `eeg-lightweight-cnn-tcn-v1` | Fixed compact 1D CNN, six epochs, dynamic cache-derived 62 input channels and two outputs | Training subjects only |

No hyperparameter search, representation-learning extension, or extra model family is permitted in this run.

## Metrics and Interpretation

The primary endpoint is subject-level **macro-F1**. Accuracy and balanced accuracy are secondary descriptive endpoints. The binary class balance permits a **nominal binary reference for accuracy**. Macro-F1 is not mechanically equated with an exact chance value; its interpretation will state metric and class assumptions explicitly. All confidence intervals and pairwise tests, if executed after model completion, use subject-level observations only with multiplicity correction for the predeclared comparisons.

## Gates and Stop Conditions

| Gate | Required evidence | Failure action |
|---|---|---|
| D1 | Hash/size verification of cache/provenance; no raw BDF/EDF in cache | Stop model execution |
| D2 | All 54 caches have exact shapes, 62 channels, 125 Hz derived rate | Stop model execution |
| D3 | Every subject exposes both locked labels | Stop model execution |
| D4 | 54-subject LOSO/no-calibration/protocol ID agreement | Stop model execution |
| D5 | Explicit audit of fold isolation, scaler/model fit scope, no target selection, and raw-data boundary | Stop model execution |

If authoritative source access, subject identity, labels, timing, channels, license, cache receipt, or leakage controls fail, the run stops. No participant is silently dropped and no fallback dataset/model is substituted.

## P5 Status

P5 Jeong2020 execution is outside this protocol and is **blocked** by `audit/V2_P5_JEONG_AVAILABILITY_HARD_STOP.md`; its incomplete source cohort may not be converted into a result by this P4 recovery work.
