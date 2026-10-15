# EEG Research Track and Multimodal Preparation

## Current Status

The umbrella layer now contains a **validated EEG research foundation scaffold**. It includes an explicit MNE-facing edge adapter, EEG preprocessing and epoch specification objects, BCI Competition IV-2a dataset/protocol metadata, an ordered baseline plan, and a fusion-input validation scaffold. It does **not** contain BCI IV-2a raw data, an executed EEG training run, a real-data results table, a representation-transfer result, or an EEG–EMG fusion result.

> **Scientific boundary:** The implementation supports running a rigorous EEG study after authorized data are provided. It does not establish that EEG decoding works, that an EMG representation transfers to EEG, or that fusion improves motor-intent decoding.

## EEG Adapter Design

`EEGPreprocessingSpec` and `EEGEpochSpec` require the researcher to state choices that are often hidden in scripts: EEG channels, reference, passband/notch/resample parameters, annotation rejection, event IDs, epoch boundaries, and baseline. The optional `epoch_signal_records_from_mne` function imports MNE only when invoked with a caller-owned authorized `Raw` object and event array. It applies the declared steps and returns metadata-only `SignalRecord` references; it never writes raw data into the registry.

| Input / choice | Required state | Why it is explicit |
|---|---|---|
| Authorized external recording | Caller-owned MNE `Raw`, external `recording_uri` | Raw data remains licensed/local and outside Git. |
| Participant and session | Required identifiers | Supports subject-aware splits and provenance. |
| EEG channel selection | Required list | Prevents silent differences in channel availability. |
| Reference | `average`, `none`, or named channels | Referencing is a scientific preprocessing choice. |
| Filter/notch/resampling | Explicit values or intentional absence | Avoids implicit signal transformation. |
| Event IDs and epoch window | Required event mapping and declared time range | Locks task semantics before evaluation. |
| Evidence status | Authorized real data only at MNE edge; benchmark eligibility remains false by default | Dataset access does not alone make a benchmark claim. |

The implementation follows MNE’s documented approach of explicit continuous-data preprocessing and event-based epoch construction; MNE itself is optional at the package boundary. [1]

## BCI Competition IV-2a Foundation Study

The registered `eeg-loso-v1` protocol and `configs/eeg/bci_iv_2a_loso.yaml` establish a draft, subject-aware study path. The official source describes dataset 2a as four-class motor imagery with 22 EEG and three EOG channels at 250 Hz from nine participants, subject to source citation/access conditions. [2]

The baseline order deliberately begins with simple models and representations before lighter neural models or domain-generalisation work.

| Order | Baseline plan | Status | Gate |
|---:|---|---|---|
| 1 | `eeg-linear-v1` | Planned | Authorized data, registered preprocessing/epochs, subject-aware split. |
| 2 | `eeg-lda-v1` | Planned | Scientific appropriateness of chosen spatial/spectral features documented. |
| 3 | `eeg-spectral-v1` | Planned | Frequency/window specification locked before held-out evaluation. |
| 4 | `eeg-lightweight-cnn-tcn-v1` | Deferred | Matching simple baselines registered first. |
| 5 | `eeg-lightweight-transformer-v1` | Deferred | Written justification after simpler matched baselines. |
| 6 | `eeg-domain-generalisation-v1` | Planned after unimodal baselines | Strict held-out-participant restrictions remain active. |

No dataset or result has been fabricated merely to populate this table. The required real-data execution remains pending authorized source data.

## EMG-to-EEG Bridge

The architecture can store EMG and EEG `RepresentationRecord` values under the same provenance and experiment registry. That makes transfer studies **possible to register**. It does not make transfer probable or demonstrated. A future transfer study must name its pretraining source, encoder version, downstream task, frozen/tuned parameter policy, subject split, unimodal baselines, and all negative/failed outcomes.

## EEG–EMG Fusion Preparation

The `emg-eeg-fusion-v1` protocol, `configs/fusion/emg_eeg_fusion.yaml`, and `FusionStudyPlan` make a future multimodal experiment falsifiable before modeling. The validation scaffold requires modality-specific representation IDs, matched subject/session metadata, explicit time windows, alignment tolerance, and all three robustness conditions: both present, EEG missing, and EMG missing.

The WAY-EEG-GAL catalog entry is appropriate for future multimodal planning because its public collection describes EEG, EMG, timing, kinematic, and force information from grasp-and-lift trials. It still requires exact release-item verification, alignment declaration, and an authorized registered run before it can support a result. [3]

| Required future comparison | Current implementation state |
|---|---|
| EEG-only | Protocol/scaffold ready; no result. |
| EMG-only | Protocol/scaffold ready; no matched WAY-EEG-GAL result. |
| EEG + EMG | Alignment/fusion plan validation ready; no fusion model/result. |
| Missing EEG | Required condition declared and input validation ready; no robustness result. |
| Missing EMG | Required condition declared and input validation ready; no robustness result. |

## Known Limits and Next Valid Step

The MNE optional dependency was not installed or exercised against a real EEG recording because no authorized BCI IV-2a or WAY-EEG-GAL data were provided. The next valid step is to provide an authorized local dataset location and a deliberate preprocessing/epoch decision; the adapter can then be invoked, each run registered, and only afterward can baseline training/evaluation be considered.

## References

[1] [MNE-Python 1.12.1 — Filtering and Resampling Data](https://mne.tools/stable/auto_tutorials/preprocessing/30_filtering_resampling.html)

[2] [BCI Competition IV — Dataset 2a Official Description](https://www.bbci.de/competition/iv/)

[3] [WAY-EEG-GAL — Springer Nature Figshare Collection](https://doi.org/10.6084/m9.figshare.c.988376.v2)
