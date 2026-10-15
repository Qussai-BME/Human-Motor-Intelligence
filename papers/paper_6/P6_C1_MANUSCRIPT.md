> **SUPERSEDED (v1.2.0).** C1-only draft. See `../P6_SUPERSESSION_NOTICE.md` (the current manuscript text is not distributed in this archive).

# P6 — From Decoder Quality to Downstream Control Utility
## C1 Motor-Imagery EEG → MyoSim Study

**Study status:** scientifically complete. The primary endpoint was prespecified; its observed outcome was non-discriminative. R03 remains engineering/preflight baseline only.

### Abstract
**Background.** P6 tested whether frozen cross-subject EEG decoder-quality differences remain observable after translation into a simulated control task.

**Methods.** We evaluated M1/M2/M3 under strict LOSO on PhysioNet EEGMMIDB R04 unilateral fist motor imagery (S001–S020). Epochs were 1.0–3.5 s after event onset. Source-training 3-fold balanced accuracy froze the quality order before task analysis (M2 low, M3 mid, M1 high). T1/T2 were mapped through the preregistered abstract interface T1→OPEN and T2→CLOSE; this mapping is not a physiological equivalence claim. A model-independent fixture was required before 60 primary and 60 rerun decoder-conditioned MyoSim runs.

**Results.** The R04 decoder stage produced 60 primary and 60 rerun traces. The fixture completed (1/1). Decoder-conditioned task success was 0/60 for primary and 0/60 for rerun, for every model; thus the primary endpoint was degenerate and could not discriminate quality. Subject-level exploratory statistics for continuous endpoints, effect sizes, and bootstrap CIs are in `FINAL_STATISTICS.json`.

**Conclusion.** Under this fixed MyoSim configuration, decoder predictions reached the complete control chain but did not complete the task. P6 does not support a decoder-quality-to-task-success claim.

## 1. Introduction
P6 is the translation step from offline decoder evidence to a fixed simulated control task. The earlier R03 study is motor execution and is retained only as an engineering baseline, not motor-imagery evidence.

## 2. Hypothesis and estimand
The registered estimand was paired subject-level task success across M1/M2/M3, with continuous secondary endpoints. Trial-level pseudoreplication was prohibited.

## 3. Dataset and protocol
The dataset was PhysioNet EEGMMIDB v1.0.0 R04. Each of S001–S020 contributed 15 usable T1/T2 epochs. Strict LOSO prevented held-out-subject exposure during fitting, feature processing, or quality ranking.

## 4. Decoder and quality freeze
M1 broad-band, M2 band-pair, and M3 band-pair-asymmetry retained the registered feature families and hyperparameters. The source-only quality means were M1 0.505179, M2 0.465274, and M3 0.465607. The mapping was frozen before MyoSim outcomes were inspected.

## 5. Intent-to-control translation
T1→OPEN and T2→CLOSE were fixed abstract control labels under `P6_C1_R04_T1_TO_OPEN_T2_TO_CLOSE_ABSTRACT_v1`. They are interface labels, not claims about physiology or prosthetic equivalence.

## 6. Downstream control task
The chain was EEG → decoder → intent contract → controller → safety → MyoSim → task → metrics. The model-independent fixture reached COMPLETE. All 60 primary and 60 rerun decoder-conditioned runs produced run-level JSON artifacts with provenance; none reached task success.

## 7. Statistical analysis
Inference was paired at subject level across 20 subjects. Task success was reported descriptively because it was 0/20 in every condition. Continuous endpoint analyses are exploratory and include paired Friedman tests, Kendall's W, effect sizes, and bootstrap CIs.

## 8. Results
The R04 decoder stage and full replay chain executed successfully. The primary endpoint was non-discriminative: M1, M2, and M3 each had 0/20 successful subject runs in both primary and rerun.

### Downstream endpoint summary

| Endpoint | M1 | M2 | M3 | Friedman p | Kendall W | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| Final error (m), mean | 0.122753 | 0.122753 | 0.122753 | 0.6065 | 0.025 | No detectable omnibus difference |
| Path length (m), mean | 0.504376 | 0.504415 | 0.504520 | 0.1146 | 0.108 | No detectable omnibus difference |
| Command corrections, mean | 0.00 | 1.05 | 2.15 | 0.0005 | 0.380 | Exploratory model-level difference; no task success |
| Grasp stability steps, mean | 0.00 | 0.00 | 0.00 | — | — | Constant endpoint; inferential test not applicable |

The rerun reproduced these run-level task metrics exactly. Secondary results, paired effect sizes, and bootstrap confidence intervals are recorded in `FINAL_STATISTICS.json`. The command-correction difference is interpreted as exploratory because the primary success endpoint was degenerate and the registered study was designed around task success.

## 9. Discussion
The fixture result separates simulator/task capability from decoder-conditioned failure. The observed result is a genuine negative/non-discriminative systems finding under the locked configuration, not evidence that the decoder families are physiologically invalid. Because no decoder condition completed the task, the study cannot establish that source-only quality translates into task success. The exploratory command-correction analysis shows model-level differences, but those differences did not produce task completion and therefore do not establish a monotonic decoder-quality-to-utility relationship.

## 10. Limitations
This is a software simulation, not online human control, a physical prosthesis, or clinical validation. The R04 cohort and fixed task are limited. The abstract T1/T2 mapping is deliberately non-physiological. The primary success endpoint was degenerate, so secondary statistics are exploratory. Raw EDF files are not redistributed; their SHA-256 provenance is recorded in `audit/DATASET_MANIFEST.json`.

## 11. Conclusion
P6 C1 completed the registered R04 LOSO and full replay workflow with complete primary/rerun provenance. The fixture was valid, but decoder-conditioned task success was 0/60 for all models. The appropriate conclusion is a non-discriminative negative downstream result, with no general, clinical, or prosthetic efficacy claim.

## 12. Data availability and references

The raw EEG recordings are from the PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0 (DOI 10.13026/C28G6P) and are not redistributed in this package. The release records source-file SHA-256 values and the exact R04 provenance required to retrieve and verify the source records.

**References**
1. Schalk G, McFarland DJ, Hinterberger T, Birbaumer N, Wolpaw JR. BCI2000: A General-Purpose Brain-Computer Interface (BCI) System. *IEEE Transactions on Biomedical Engineering*. 2004;51(6):1034–1043.
2. Schalk G. EEG Motor Movement/Imagery Dataset. PhysioNet, version 1.0.0, 2009. DOI: 10.13026/C28G6P.
