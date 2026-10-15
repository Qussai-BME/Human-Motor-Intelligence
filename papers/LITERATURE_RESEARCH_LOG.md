# V2 Literature and Live-Source Research Log

**Status:** Reconstructed after sandbox reset; sources were opened directly on 2026-08-23 (GMT+3).  
**Use rule:** This log records source context and comparability boundaries. It does not substitute for protocol artefacts or create a claim without a cited result file.

## Source-Handling Note

NEMAR pages identify derivative versions, licensing, and related identifiers. Their high-level prose description is explicitly labelled on-page as AI-generated and potentially erroneous. Dataset-specific participant coverage, BDF channel handling, event labels, and trial totals in this programme are therefore grounded in the programme's sidecar/schema audit and cache provenance, not in that prose alone.

| ID | Source | Directly checked facts used in V2 | Relevance / limitation |
|---|---|---|---|
| L1 | Lee et al., *EEG dataset and OpenBMI toolbox for three BCI paradigms* (2019) [1] | The article describes 54 healthy participants, two sessions, binary MI, 62 EEG electrodes, auxiliary arm EMG, and substantial MI variability. | Authoritative source descriptor for P4. Its reported analyses are not the Recovery R1 LOSO protocol and must not be used as a numerical comparator. |
| L2 | NEMAR `nm000338` v1.0.5 [2] | Records derivative DOI, v1.0.5 availability, GPL-3.0 license, two sessions, 62-channel 10–05 montage, 1000 Hz, and derivation links to OpenBMI source data and article. | Official derivative metadata; the V2 cache/provenance and sidecar checks establish the exact run/event handling. |
| L3 | Jeong et al. multimodal upper-limb source descriptor (2020) [3] | Linked as the original publication for the selected multimodal dataset. | Source context only; it does not repair a missing derivative file. |
| L4 | NEMAR `nm000311` v1.0.2 [4] | Records derivative DOI, CC0-1.0, 25 participants, three sessions, 71 recorded channels, 1000 Hz, and original publication relation. | The complete event-sidecar audit supersedes its high-level availability statement for P5 feasibility: `sub-23/ses-0` has no run-2 file and misses twist labels. |
| L5 | Halme & Parkkonen (2018) [5] | Cross-subject EEG MI work illustrates that subject-independent performance depends strongly on feature/model/training design. | Contextual counterweight: a null pairwise outcome in one locked protocol cannot establish universal weakness of zero-calibration EEG decoding. |
| L6 | Dong et al. (2023) [6] | Reviews/assesses approaches for inter-subject MI decoding. | Contextual; architecture, selection, and adaptation boundaries differ from Recovery R1. |
| L7 | Pritchard et al. (2025) [7] | Reports subject-independent multimodal decoding/fusion gains under a distinct hierarchical/CASH-style methodological setting. | Counterclaim context for P5: the current source-coverage stop cannot be rewritten as a claim that multimodal fusion is universally unhelpful. |
| L8 | Pan et al. (2024) [8] and Skomrock et al. (2018) [9] | Motivate task-level success, time, and failure endpoints beyond time-bin classifier accuracy in myocontrol evaluations. | Contextual support for P6 endpoint design only; no repeat P6 result exists because valid independent simulator variation was absent. |

## Research Conclusions Allowed by These Sources

The opened sources support the selection rationale for a large external binary MI dataset and the original relevance of a synchronized multimodal dataset. They also support conservative interpretation: performance and fusion claims vary with task, cohort, architecture, data partitioning, and adaptation policy. The sources **do not** override the exact data-availability hard stop in P5 or the deterministic-runtime hard stop in P6.

## References

[1] [Lee et al. (2019), *GigaScience*](https://doi.org/10.1093/gigascience/giz002)  
[2] [NEMAR `nm000338`, v1.0.5](https://doi.org/10.82901/nemar.nm000338)  
[3] [Jeong et al. (2020), *GigaScience*](https://doi.org/10.1093/gigascience/giaa098)  
[4] [NEMAR `nm000311`, v1.0.2](https://doi.org/10.82901/nemar.nm000311)  
[5] [Halme & Parkkonen (2018), *Scientific Reports*](https://doi.org/10.1038/s41598-018-28295-z)  
[6] [Dong et al. (2023), *Brain Sciences*](https://doi.org/10.3390/brainsci13071109)  
[7] [Pritchard et al. (2025), *Journal of Neural Engineering*](https://doi.org/10.1088/1741-2552/ade1f9)  
[8] [Pan et al. (2024), *Frontiers in Human Neuroscience*](https://doi.org/10.3389/fnhum.2024.1429130)  
[9] [Skomrock et al. (2018), *Frontiers in Neuroscience*](https://doi.org/10.3389/fnins.2018.00763)

## R3 Q1-Standard Related-Work Addendum

| ID | Source opened directly | Fact used in Q1 manuscript | Comparability boundary |
|---|---|---|---|
| L10 | Zheng et al. (2025), *Cross-Subject Motor Imagery EEG Decoding with Domain Generalization* [10] | Uses a deep domain-generalization design with source-domain invariant representation learning for unseen MI-EEG subjects. | It uses a materially different architecture/training procedure from P4’s fixed transparent comparator family; it is contextual, not a score comparator. |
| L11 | Kueper et al. (2024), *Avoidance of specific calibration sessions* [11] | Demonstrates that avoiding a dedicated calibration session can be framed as cross-task transfer in a rehabilitation-oriented setting. | Its target task, healthy cohort, transfer source, and movement-intention design differ from P4’s strict subject-held-out binary MI LOSO. |
| L12 | Pritchard et al. (2025), *An investigation of multimodal EMG-EEG fusion strategies* [12] | Studies subject-independent multimodal gesture classification with automated model selection and a hierarchical approach, reporting fusion gains in its own setting. | It supplies a direct counterweight to any general P5 anti-fusion claim; its CASH/hierarchical methodology is not the fixed LDA design. |
| L13 | Li et al. (2025), *Fusion of EEG and EMG signals for detecting pre-movement intention* [13] | Evaluates a connectivity-based EEG–EMG method for sit/stand intent with healthy and SCI participants. | Task, population, window, connectivity features, and validation context differ from P5 MI-only all-11-class LOSO. |
| L14 | Roots et al. (2020), *Fusion Convolutional Neural Network for Cross-Subject EEG Motor Imagery Classification* [14] | Illustrates deep multi-branch cross-subject EEG fusion on another dataset. | EEG-only architecture/data splits differ from P5 multimodal transparent LDA protocol; it is context only. |

### R3 Addendum References

[10] [Zheng et al. (2025), *Bioengineering*](https://doi.org/10.3390/bioengineering12050495)  
[11] [Kueper et al. (2024), *Scientific Reports*](https://doi.org/10.1038/s41598-024-65910-8)  
[12] [Pritchard et al. (2025), *Journal of Neural Engineering*](https://doi.org/10.1088/1741-2552/ade1f9)  
[13] [Li et al. (2025), *Frontiers in Neuroscience*](https://doi.org/10.3389/fnins.2025.1532099)  
[14] [Roots et al. (2020), *Computers*](https://doi.org/10.3390/computers9030072)
