# Six-Paper Research Synthesis — V2 Recovery R3

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


## Purpose and Current-State Interpretation

The Human Motor Intelligence programme is organized around robust motor-intent decoding across people, modalities, and deployment layers. R3 preserves the programme trajectory while making its evidence boundaries operational: source-grounded EMG work (P1–P2), an externally archived P3 evidence package, external EEG/EEG–EMG validations (P4–P5), and simulator systems methodology (P6). The programme does **not** currently establish a clinical or device-ready end-to-end system.

## Six-Paper Map

| Paper | Question | Evidence tier | Current answer | Boundary |
|---|---|---|---|---|
| P1 | EMG representation/decoding question | Frozen source-grounded | Retained in `EMG_SERIES_MASTER_EVIDENCE.md` | No new result inferred here |
| P2 | EMG generalisation/robustness question | Frozen source-grounded | Retained in `EMG_SERIES_MASTER_EVIDENCE.md` | No pooling with later cohorts |
| P3 | Learned adaptation | External Lite-DAN archive | Qualified complete | Not independently rerun in umbrella; no MyoSim trace bridge |
| P4 | Can fixed pipelines decode binary MI with no target calibration? | External validation | Yes at an OpenBMI protocol-qualified level; model comparison omnibus is non-null but pairwise superiority is unresolved after Holm | Not BCI IV-2a replication or clinical proof |
| P5 | Do fixed transparent EEG–EMG fusion rules improve all-11-class MI LOSO? | Amended external validation | No Holm-supported gain over EEG-only in this Jeong MI-only cohort | Not general fusion failure/mechanism |
| P6 | Are replay-driven simulator outcomes robust to a declared initial-state factor, and can decoder quality be compared? | Systems evidence + hard stop | The fixture failed across 20 bounded states; decoder-quality comparison remains unexecuted | No real-decoder/biomedical claim |

## Cross-Paper Findings

The completed external evaluations separate two defensible claims. P4 shows that a zero-calibration LOSO protocol can be tested transparently across 54 OpenBMI subjects without target-subject fitting. P5 shows that a fixed LDA early/late fusion set must not be presumed superior simply because it uses an added EMG modality; within its amended source cohort, the EEG-only contrast does not survive Holm adjustment. These results are complementary but intentionally not numerically pooled because their datasets, label spaces, preprocessing, and study questions differ.[1] [2]

P6 serves a different role. It establishes a method for making initial-state perturbation a real, auditable simulator factor rather than an inert random seed. Its all-failure result is visible and reproducible. However, the identity of the replay input invalidates the earlier assumption that it represented a real decoder condition. R3 appropriately stops before constructing a fictional dose-response relationship.[3]

## Integration Logic

| Programme transition | Present support | What remains unproven |
|---|---|---|
| Biosignal processing → cross-subject generalisation | P4/P5 external LOSO evidence | Generalisation across sources, sessions, and clinical populations |
| EEG/EMG → multimodal motor-intent learning | P5 controlled comparison | General fusion superiority or physiological mechanism |
| Decoder output → embodied task simulation | P6 integration-fixture pathway | Connection from a validated real decoder to task success remains **unproven** |
| Simulation → prosthesis/medical robotics | Architectural ambition only | Hardware, safety, clinical and human factors evidence |

## R3 Research Gate

The next valid P6 study begins with authentic frozen trace provenance, not with model fitting or statistical testing. P3 is now integrated as qualified external evidence. P6 remains open only at the authentic decoder-trace gate; until that dependency is supplied, the right output is an interim release, a precise evidence map, and a traceable route to the next registered experiment.

## References

[1]: # "P4 manuscript (text not distributed in this archive)"
[2]: # "P5 manuscript (text not distributed in this archive)"
[3]: P6_INITIAL_STATE_ROBUSTNESS_AND_DECODER_QUALITY_STATUS_V2_RECOVERY_R3_Q1.md "P6 Q1 Manuscript"
[4]: ../audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "R3 P6 Replay Identity Hard Stop"

The P6 conditions for future work are stated in the hard-stop record.[4]
