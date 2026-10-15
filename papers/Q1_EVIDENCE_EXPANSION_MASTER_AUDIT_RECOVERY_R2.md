# Q1 Evidence Expansion Master Audit — V2 Recovery R2

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


**Programme:** Human Motor Intelligence  
**Version:** V2.0 Recovery R2  
**Purpose:** Auditable programme-level integration of the six-paper evidence expansion after P5 external validation and P6 declared-state repeat execution.  
**Core question:** How can biomedical AI decode human motor intent robustly across individuals without subject-specific calibration?

## Executive Determination

Recovery R2 preserves the frozen V1/V1.1 evidence layer and adds separately versioned evidence only. P4 remains the completed R1 OpenBMI external EEG validation. P5 is now completed as an amended, source-availability-qualified 24-subject Jeong2020 external MI fusion validation. P6 is now completed as a 20-state real-replay **simulation systems** study after a narrowly scoped, predeclared initial-state perturbation capability passed baseline and safety gates. P3 remains unavailable and retains its mandatory pending-value marker.

| Paper | Research identity | Current status | Admissible claim class |
|---|---|---|---|
| P1 | Rest-class metric inflation in zero-calibration cross-subject sEMG | Author-supplied manuscript integrated | Source-grounded author evidence |
| P2 | MiniROCKET representation/domain-adaptation mechanism analysis | Author-supplied manuscript integrated | Source-grounded, representation-specific evidence |
| P3 | Companion EMG work | Pending author package | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** |
| P4 | Strict zero-calibration EEG MI | Completed R1 OpenBMI external validation | External, protocol-qualified EEG evidence |
| P5 | Transparent EEG–EMG fusion under LOSO | Completed R2 Jeong2020 amended-cohort validation | External, protocol-qualified multimodal evidence |
| P6 | Real replay control robustness | Completed R2 declared-state repeat study | Simulation systems evidence, not biomedical validation |

## Tiering, Origin, and Preservation Rules

| Evidence layer | Status | Non-negotiable rule |
|---|---|---|
| V1/V1.1 Tier A | Frozen | Never overwrite, rerun into a legacy result path, or silently reinterpret. |
| V2 Recovery R1 Tier B | Completed | Retains P4 OpenBMI evidence and documented original P5/P6 hard stops. |
| V2 Recovery R2 Tier B | Completed additions | P5 and P6 use new namespaces, amended protocols, result artefacts, and independent reruns. |
| Synthetic controlled corruption | Separate | Remains `origin=synthetic_controlled_corruption`, `benchmark_eligible=false`, and cannot be presented as biomedical evidence. |

The change from an R1 hard stop to an R2 execution is explicit rather than retrospective. P5 proceeded only after a second-source check established the availability limitation for `sub-23` and a pre-feature-extraction cohort amendment. P6 proceeded only after an unperturbed compatibility baseline, a source-visible runtime extension, and a declared-state preflight demonstrated actual seed-to-state variability.

## Dataset and Capability Decision Record

| Candidate/action | Decision | Rationale | Resulting evidence |
|---|---|---|---|
| OpenBMI / NEMAR `nm000338` P4 | Executed in R1 | External binary MI, 54 subjects, feasible strict LOSO, source/provenance/license checks passed | 54-subject external EEG validation |
| Jeong2020 / NEMAR `nm000311` P5 at original 25 subjects | Stopped in R1 | `sub-23` lacked a required run in the NEMAR derivative | No R1 score; hard stop retained |
| Jeong2020 amended 24-subject cohort | Executed in R2 | Second-source check confirmed the missing acquisition; exclusion and balanced event cap were fixed before extraction/model fitting | 24-subject all-11-class MI external fusion validation |
| Deep fusion or target calibration P5 | Rejected | Would alter the transparent zero-calibration paper identity | Not executed |
| Seed-labelled deterministic P6 repeats | Rejected in R1 | A seed label alone did not vary physical/task state | No pseudo-replication |
| Declared bounded P6 initial-state factor | Executed in R2 | Minimal code path records a real seed-to-state mapping while holding replay/controller/task fixed | 20-state simulation systems cohort |

## P4: External EEG Validation — Retained R1 Result

P4 used NEMAR `nm000338` v1.0.5/OpenBMI as a harmonized external validation, not a direct replication of BCI IV-2a. The analysis retained 62 named EEG channels, used the fixed binary MI protocol and strict subject-held-out LOSO across 54 subjects, and passed D1–D5 before fitting. The external source descriptor is available through [NEMAR](https://doi.org/10.82901/nemar.nm000338), the original data record through [GigaDB](https://doi.org/10.5524/100542), and the acquisition description through [Lee et al.](https://doi.org/10.1093/gigascience/giz002).

| Fixed P4 condition | Mean held-out-subject macro-F1 | Bootstrap 95% CI |
|---|---:|---:|
| Linear | 0.5962 | 0.5694–0.6253 |
| LDA | 0.5980 | 0.5708–0.6278 |
| Linear SVM | 0.6123 | 0.5806–0.6446 |
| Spectral | 0.6130 | 0.5809–0.6459 |
| Compact CNN | 0.6364 | 0.5929–0.6800 |

The locked omnibus test was Friedman χ²=16.16, *p*=0.00281, but none of the ten predeclared paired contrasts survived Holm correction (minimum adjusted *p*=0.1042). The primary and independent-rerun subject-level CSVs matched exactly. P4 therefore supports protocol-locked subject-independent binary MI decoding on this external cohort; it does not justify numerical cross-dataset ranking or a universal claim about zero-calibration EEG.

## P5: Amended Jeong2020 External Fusion Validation — New R2 Result

The R2 P5 cohort contains 24 subjects (`sub-1`–`sub-22`, `sub-24`, `sub-25`), all three `ses-0` MI runs, all eleven labels, and 550 retained trials per subject. `sub-23` is not silently omitted: the source unavailability, independent verification, pre-analysis cohort amendment, and demographic balance record are all retained. The source is [NEMAR `nm000311`](https://doi.org/10.82901/nemar.nm000311), supported by the original [GigaDB record](https://doi.org/10.5524/100788) and [Jeong et al.](https://doi.org/10.1093/gigascience/giaa098). This remains an external validation—not a direct replication or pooled comparison with frozen Cho2017 evidence.

| Fixed P5 condition | Mean held-out-subject macro-F1 | Bootstrap 95% CI |
|---|---:|---:|
| EEG-only LDA | 0.0813 | 0.0719–0.0915 |
| Late-fusion LDA | 0.0805 | 0.0689–0.0936 |
| Early-fusion LDA | 0.0754 | 0.0622–0.0890 |
| EMG-only LDA | 0.0484 | 0.0386–0.0590 |

The P5 omnibus test was Friedman χ²(3)=16.25, *p*=0.00101. Within the six-comparison Holm family, EEG-only, late fusion, and early fusion each exceeded EMG-only (adjusted *p*=0.00103, 0.000762, and 0.00800, respectively). No contrast among EEG-only, late fusion, and early fusion survived Holm adjustment. The 96-row subject-level result was byte-identical in the independent rerun.

> In this amended Jeong MI-only cohort and these transparent LDA pipelines, fusion did not establish a Holm-supported improvement over EEG-only. The result does not show that multimodal fusion is generally ineffective, nor does it establish why EMG-only is lower in this specific setting. Microactivation, strategy, hardware, preprocessing, features, and task differences remain competing untested explanations.

The balanced eleven-class cohort gives a nominal uniform-class reference of 1/11 for accuracy/balanced accuracy, but this reference is not mechanically equivalent to macro-F1 and is not presented as a macro-F1 chance test.

## P6: Declared-State Real-Replay Systems Study — New R2 Result

P6 first reproduced the preserved unperturbed MyoSim benchmark exactly. A minimal extension then sampled only named `forearm_x` and `forearm_y` initial qpos offsets from declared bounded uniform distributions, recorded the realised state in every run, and held the replay file, controller, decoder mapping, task geometry, object/target state, and success logic fixed. Twenty predeclared seeds generated 20 distinct initial qpos states with zero invalid simulation states. A complete independent rerun reproduced the run record byte-for-byte.

| P6 endpoint | R2 result |
|---|---:|
| Task success | 0/20; Wilson 95% CI 0.000–0.161 |
| Task failure | 20/20; Wilson 95% CI 0.839–1.000 |
| Final state | `TRANSPORT` in 20/20 runs |
| Completion time among successes | Undefined: no successful run |
| Mean final planar error | 0.046650 m; bootstrap 95% CI 0.045621–0.047751 m |
| Mean path length | 1.024690 m; bootstrap 95% CI 1.007466–1.042456 m |
| Invalid-state count | 0 |

This is an intentionally unhidden negative systems result. It shows that the fixed replay/controller did not complete the fixed simulator task under the declared 20-state distribution. It is not a human study, clinical result, broad simulator certification, causal mechanism, or decoder-quality dose-response result: decoder replay quality was held constant.

## Required Artefacts and Reproducibility

| Requirement | P4 R1 | P5 R2 | P6 R2 |
|---|---|---|---|
| Immutable protocol/amendment | Pass | Pass | Pass |
| Source/provenance record | Pass | Pass, including second-source `sub-23` check | Replay checksum and code fingerprint |
| Validation gates | D1–D5 pass | D1–D5 pass | Baseline, safety, state-identity, completeness gates pass |
| Unit of analysis | 54 subjects | 24 subjects | 20 declared initial states |
| Primary result artefact | 270 rows | 96 rows | 20 per-run records |
| Statistics | Bootstrap/Friedman/Wilcoxon/Holm | Bootstrap/Friedman/Wilcoxon/Holm | Wilson/Bootstrap descriptive systems endpoints |
| Independent rerun | Exact pass | Exact pass | Exact pass |
| Permitted scope | External EEG validation | External multimodal validation | Simulation systems robustness only |

## Programme-Level Claim Discipline

The programme may now state that transparent cross-subject performance and fusion behaviour are dataset-, task-, modality-, and protocol-dependent. It may not state that one modality or fusion strategy is universally superior, that simple domain adaptation fails in general, that simulator initial-state sensitivity predicts human performance, or that P3 supports any unprovided result. Negative/null findings are retained as results rather than tuned away.

## Integration Decision

P1/P2, P4, P5 R2, and P6 R2 may be integrated into programme synthesis with the tiers and constraints above. P3 must remain pending. P5 and P6 R1 hard-stop files stay part of the audit history; their reopening is described only through R2 amendments. Future work must begin with a new protocol/version rather than modify the R2 cohort, seed list, or conclusions.

## References

[1] [NEMAR OpenBMI dataset `nm000338`](https://doi.org/10.82901/nemar.nm000338)  
[2] [OpenBMI supporting data, GigaDB 100542](https://doi.org/10.5524/100542)  
[3] [Lee et al. (2019), OpenBMI description](https://doi.org/10.1093/gigascience/giz002)  
[4] [NEMAR Jeong2020 dataset `nm000311`](https://doi.org/10.82901/nemar.nm000311)  
[5] [Jeong2020 supporting data, GigaDB 100788](https://doi.org/10.5524/100788)  
[6] [Jeong et al. (2020), multimodal upper-limb data](https://doi.org/10.1093/gigascience/giaa098)
