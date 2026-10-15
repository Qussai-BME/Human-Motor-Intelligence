# Six-Paper Research Synthesis — V2 Recovery R2

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


## Programme Question and Evidence Architecture

The programme investigates how biomedical AI can decode motor intent across individuals without subject-specific calibration. Its evidence is intentionally heterogeneous: sEMG benchmark behaviour, representation-specific adaptation analysis, a pending companion work, external EEG decoding, external EEG–EMG fusion, and replay-based systems robustness. Therefore, no single metric, dataset, or simulator endpoint can answer the programme question alone.

| Paper | Contribution | Strongest permitted inference | Principal boundary |
|---|---|---|---|
| P1 | Rest-class metric inflation audit across three sEMG databases | Overall accuracy can materially overstate active-class performance under class imbalance | Dataset sizes and class policies constrain generalization |
| P2 | MiniROCKET cross-subject adaptation analysis | The tested PPV representation/adaptation path has a measured failure mode | Not an argument against all adaptation methods |
| P3 | Companion EMG study | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** | No result, method, or claim may be supplied before author evidence arrives |
| P4 | OpenBMI external zero-calibration EEG MI validation | Fixed subject-independent EEG pipelines decode binary MI above nominal binary reference in this protocol | External validation, not direct replication or universal calibration-free estimate |
| P5 | Jeong2020 external all-11-class MI fusion validation | Fixed transparent fusion rules did not outperform EEG-only after Holm in this amended cohort | Does not rank fusion approaches generally or explain EMG behaviour |
| P6 | Declared-state real-replay simulation cohort | Fixed replay/control did not complete the fixed task under the declared simulated initial-state distribution | Simulation systems result; no decoder dose response or biomedical outcome |

## Cross-Paper Findings

P1 and P2 establish a disciplined sEMG foundation. P1 shows why rest-inclusive summary metrics require active-class checks and class-aware reporting. P2 identifies a representation-specific numerical mechanism in its tested MiniROCKET adaptation setting; neither paper authorizes a generic claim that calibration-free sEMG is impossible or that all domain adaptation fails.

P4 demonstrates that subject-held-out binary MI decoding is feasible on a second external EEG source under a locked transparent/comparator model family. The OpenBMI result is not directly rankable against BCI IV-2a because the cohorts, sessions, acquisition, channels, preprocessing, epochs, and class setup differ. Its main contribution is external protocol-qualified robustness evidence, not a universal performance ceiling.

P5 adds a harder all-11-class multimodal MI setting. In this amended 24-subject Jeong cohort, EEG-only LDA had mean macro-F1 0.0813, early fusion 0.0754, late fusion 0.0805, and EMG-only 0.0484. The omnibus condition effect did not translate into a Holm-supported fusion-over-EEG advantage. This does not conflict with literature that reports fusion gains under different architectures, label selections, calibration policies, or modalities; it limits the claim to the tested transparent pipeline and source.

P6 adds a systems-level caution. Exact replay success at a single unperturbed state was not robust to the declared distribution of simulator initial forearm positions: 0/20 perturbed states completed the task, despite no invalid dynamics. The result supports inclusion of task success/failure and state-coverage artefacts in replay studies. Because decoder output was fixed, it provides no evidence that decoder quality caused the failures and cannot be pooled with synthetic decoder-corruption experiments.

## Integrated Interpretation

> Robust cross-subject motor-intent research requires evidence at multiple boundaries: class policy, representation geometry, external source shift, modality/task selection, and closed-loop state sensitivity. Each boundary can change observed performance without identifying a single causal mechanism.

The programme can therefore claim a methodologically rigorous research stack: frozen historical evidence, source-grounded EMG manuscripts, external EEG and multimodal validations, and an auditable simulation robustness study. It cannot claim a modality-universal solution, universal zero-calibration performance, a mechanistic explanation for P5 modality ordering, or a clinically valid P6 conclusion.

## Evidence Gaps and Next Gates

P3 remains the immediate documentary gap. Future P5 work requires a new protocol and a source-complete cohort or a separately justified new external dataset; it must not re-use the R2 result to tune features/models. Future P6 work should separate initial-state robustness from decoder-quality manipulation, retain explicit state provenance, and validate any simulator-to-human claim with appropriate real-world evidence. Any new study must use a new evidence namespace, prospectively fixed endpoints, source/license verification, leakage controls, and an independent rerun.
