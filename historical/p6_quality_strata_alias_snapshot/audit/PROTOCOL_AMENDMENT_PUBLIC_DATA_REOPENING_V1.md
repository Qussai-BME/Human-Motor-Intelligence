# P6 R3 Public-Data Reopening — Prospective Protocol Amendment

**Responsible author:** Qussai Adlbi  
**Protocol ID:** `p6-r3-public-data-reopening-v1`  
**Status:** Executed on real public recordings; separate namespace from the historical P6 R3 hard stop.

## Scientific purpose

This amendment defines a new, prospective public-data study to obtain authenticated decoder traces from openly accessible human recordings. It does not retroactively satisfy or overwrite the historical P6 R3 gate, whose missing trace provenance remains documented in the original namespace.

## Source and cohort

The source is the PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0 (DOI `10.13026/C28G6P`). The downloaded cohort contains subjects S001–S020, run R03, 64 EEG channels sampled at 160 Hz. R03 is the unilateral fist motor-imagery run with T1/T2 event annotations. Source files, byte sizes, and SHA-256 digests are recorded in `audit/DATASET_MANIFEST.json`.

## Fixed preprocessing

For each T1/T2 event, the decoder window is the recorded interval from 1.0 s to 3.5 s after the event onset. No target-subject data are used for fitting, scaling, feature selection, model selection, or calibration. Features are log-relative Welch band powers from the fixed EEG channel subset 8–64 (one-based montage indexing represented by zero-based code indices 7–63), with 4–40 Hz total-power normalization.

## Three decoder conditions

Three model families were fixed before held-out evaluation: a single 8–30 Hz band-power family with logistic regression regularization `C=0.1`; a two-band 8–12/13–30 Hz family with `C=1.0`; and the same two-band family with the fixed central-channel asymmetry augmentation and `C=2.0`. Each fold fits preprocessing and the classifier on the source subjects only.

The quality labels are assigned from mean three-fold source-only balanced accuracy: lowest source score = `quality_worst`, middle source score = `quality_middle`, highest source score = `quality_best`. The held-out outcomes are not used to assign these labels. The mapping is recorded in `results/QUALITY_MAPPING.json`.

## Trace contract

Every trace contains timestamp, predicted label, confidence, source subject, modality, model version, held-out window identifier, ground-truth label, and correctness. The quality-stratum traces are byte-identical copies of the raw decoder outputs. No labels, confidence values, timestamps, or predictions were edited after inference.

## Analysis

The primary held-out unit is subject. The primary metric is subject-level balanced accuracy. Pairwise condition comparisons use paired Wilcoxon signed-rank tests and a deterministic 20,000-resample subject bootstrap for the mean paired difference. These public-data results are decoder-validation evidence and simulator-input provenance; they are not clinical evidence and do not establish a universal decoder-quality dose response.
