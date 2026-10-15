# V2 Dataset and Experiment Selection Matrix — Recovery R1

## Decision Standard

A candidate may be scientifically attractive yet ineligible when source coverage, license, subject identity, target definition, LOSO compatibility, or provenance fails. The programme selects a candidate only when both value and execution integrity pass.

| Candidate / action | Paper | Scientific fit | Dataset/protocol evidence | Cost and risk | Decision | Final status |
|---|---|---|---|---|---|---|
| NEMAR OpenBMI `nm000338` v1.0.5 | P4 | Large independent binary MI cohort; supports subject-level zero-calibration LOSO | 54 subjects; `ses-1`; 62 non-EMG channels; two selected acquisitions; binary labels; GPL-3.0; D1–D5 viable | Sequential BDF processing required; no direct score comparison with BCI IV-2a | **MUST DO** | Executed as external validation; D1–D5 and exact rerun pass |
| NEMAR Jeong `nm000311` v1.0.2 | P5 | Synchronized EEG/EMG, 11 upper-limb MI classes, independent of Cho2017 | Nominally 25 participants/three sessions/71 channels/CC0; actual sidecar audit shows `sub-23` lacks run-2 and twist labels | Invalid locked 25-subject all-11-class cohort; subject removal/subsetting would drift scope | **MUST DO conditional on coverage** | Hard stop before BDF/model run |
| BCI Competition IV-2b | P4 | Additional EEG dataset possible | Small cohort and sparse montage offer little external/statistical gain for current question | Scope inflation, limited modality value | Reject | Not pursued |
| Deep/representation fusion extension | P5 | Could be a distinct methodological project | Not necessary for transparent-fusion question | Changes research identity; uncontrolled architecture search | Reject | Not pursued |
| More generic biomedical datasets | P4/P5 | Quantity only without a focused question | Protocol comparability uncertain | Sample-count-only expansion | Reject | Not pursued |
| Repeated real replay with initial-state/seed factor | P6 | Highest potential evidence expansion if independent variation exists | MyoSim audit found seed has no state/task/replay variation | Pseudo-replication risk | **MUST DO conditional on valid factor** | Hard stop |

## P4 Selection Result

OpenBMI met the pre-execution source, license, subject, label, and compatibility criteria. The resulting analysis is labelled `external_validation:true` and `direct_replication:false`. Its 54-subject external result is separate from frozen BCI IV-2a paths and claims.

## P5 Selection Result

Jeong2020 was scientifically appropriate but operationally ineligible under the locked cohort after event-sidecar audit. The correct response was to stop. A later re-selection requires a new amendment before execution, not a hidden replacement cohort.

## P6 Selection Result

P6 did not require another biomedical dataset. Its priority was real replay evidence with valid independent variation. The existing runtime cannot support that claim through its current seed/reset interface, so no repeat run is selected.

## Sources

[1] [NEMAR OpenBMI `nm000338`](https://doi.org/10.82901/nemar.nm000338)  
[2] [NEMAR Jeong `nm000311`](https://doi.org/10.82901/nemar.nm000311)  
[3] [OpenBMI source paper](https://doi.org/10.1093/gigascience/giz002)  
[4] [Jeong source paper](https://doi.org/10.1093/gigascience/giaa098)
