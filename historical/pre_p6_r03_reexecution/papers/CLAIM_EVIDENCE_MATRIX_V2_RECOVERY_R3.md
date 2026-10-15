# Claim–Evidence Matrix — V2 Recovery R3

| ID | Claim | Evidence source | Evidence status | Permitted use | Explicit limitation |
|---|---|---|---|---|---|
| C1 | P4 is a strict zero-calibration external binary-MI validation | P4 R1 protocol, validation, manifest, Q1 manuscript | COMPLETE | Methods/result description | External validation, not direct replication |
| C2 | P4 has a non-null Friedman model effect | P4 `statistics_macro_f1.json` | COMPLETE | Omnibus inference | No pairwise contrast survives Holm |
| C3 | P4 compact CNN has the highest descriptive mean macro-F1 | P4 subject result/statistics artefacts | COMPLETE | Descriptive table text | No confirmed pairwise superiority |
| C4 | P5 is a 24-subject amended Jeong MI-only validation | R2_001, second-source check, P5 manifest | COMPLETE | Methods/result description | Not original 25-subject dataset and not Cho2017 replication |
| C5 | P5 transparent fusion rules do not establish gain over EEG-only | P5 pairwise Holm results | COMPLETE | Primary conclusion | Does not judge all fusion methods/tasks |
| C6 | EEG/early/late conditions exceeded EMG-only in selected Holm-adjusted contrasts | P5 pairwise statistics | COMPLETE | Qualified within-source result | No causal account of EMG ordering |
| C7 | R2 P6 produced a real initial-state factor | P6 patch/capability tests/20 state records | COMPLETE | Systems methods/result | Two bounded simulator offsets only |
| C8 | R2 P6 fixture failed all 20 declared state repeats | P6 run records/statistics/rerun | COMPLETE | Fixture outcome | Not a decoder-quality or biomedical result |
| C9 | R2 P6 replay is `synthetic-demo` / `example-decoder-v1` | R3 replay-identity hard stop | COMPLETE | Mandatory correction | Does not establish any model/decoder mapping |
| C10 | Worst/mid/best decoder-quality comparison exists | None—traces absent | BLOCKED | Not usable | R3 was not executed; no condition comparison/statistics |
| C11 | P6 establishes a decoder-quality dose-response | None | BLOCKED | Not usable | Requires authentic frozen traces and preregistration amendment |
| C12 | P3 contributes a completed programme result | External Lite-DAN v1.0.0 archive, P3 manuscript, registry, 657 fold files, and results-to-paper audit | COMPLETE | Qualified programme result | Accepted as externally archived evidence; not independently rerun in this umbrella environment |
| C13 | Programme enables clinical/prosthetic deployment | None | UNSUPPORTED | Not usable | Requires clinical, hardware, safety, and human factors evidence |

## Governance Rule

A claim may appear in a manuscript abstract, synthesis, release note, or public-facing summary only if its matrix status is **COMPLETE** and its limitation is printed or linked in the same context. `BLOCKED`, `PENDING`, and `UNSUPPORTED` entries must remain visible as gaps rather than being dropped from the programme narrative.

## References

[1]: ../audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "R3 P6 Replay Identity Hard Stop"
[2]: P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md "P4 Q1 Manuscript"
[3]: P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md "P5 Q1 Manuscript"
[4]: P6_INITIAL_STATE_ROBUSTNESS_AND_DECODER_QUALITY_STATUS_V2_RECOVERY_R3_Q1.md "P6 Q1 Manuscript"

P4–P6 evidence classifications reflect the programme’s retained audit and manuscript records.[1] [2] [3] [4]


## FINAL MASTER SPEC P4/P5 HARDENING ADDITIONS

| ID | Claim | Class | Evidence source | Permitted use | Limitation |
|---|---|---|---|---|---|
| C14 | Temporal and spectral representations exceeded covariance-only log-Euclidean representation in paired P4 subject-level macro-F1 comparisons | A — directly demonstrated | `results/extensions/v2-cpu-q1-upgrade-r3-004/p4_representation_ablation_loso/statistics.json`; final hardening statistics | P4 primary representation conclusion | OpenBMI protocol, fixed feature family and LDA; not a universal Riemannian claim |
| C15 | Static fusion provided measurable robustness beyond EEG-only under 20% EEG feature zeroing | E — unsupported | Final P5 hardening analysis | Must not be claimed | Descriptive difference was negligible and paired Wilcoxon was non-significant |
| C16 | Confidence-selective fusion retained more degraded performance than EEG-only | E — unsupported | Final P5 hardening analysis | Must not be claimed | Degraded aggregate and paired values matched EEG-only |
| C17 | The current entropy-derived confidence heuristic was not validated as a reliability-aware improvement | B — strongly supported | P5 calibration statistics and strict corruption analysis | Qualified negative result | Cohort- and protocol-specific; calibrated learned reliability remains open |
| C18 | P4 calibration quality is not estimable from retained artifacts | A — directly demonstrated | Final hardening audit; absence of P4 probabilities/decision scores | State as reproducibility limitation | Future runner must persist fold-local probabilities or scores |
| C19 | P5 20% EEG zeroing is physical electrode or clinical hardware robustness | E — unsupported | Protocol definition | Must not be claimed | It is feature-cache degradation only |

These additions are governed by `audit/FINAL_P4_P5_Q1_HARDENING_DOSSIER_R3.md` and `audit/final_p4_p5_hardening_statistics_r3_001.json`.


## P3 EXTERNAL EVIDENCE ACCEPTANCE

| Item | Status | Evidence | Boundary |
|---|---|---|---|
| P3 package identity | ACCEPTED | Zenodo DOI `10.5281/zenodo.22768799`; downloaded archive SHA-256 `b382a40aa9a40556a6169ca805fc92c1d75a94e6d982b845ca489dd37c158f14` | Public archive identity, not a new rerun |
| Experimental coverage | ACCEPTED | 27 condition/cohort summaries and 657 subject-level fold records | No raw NinaPro recordings or feature caches redistributed |
| Protocol | ACCEPTED | `external/p3_litedan_v1_0_0/configs/protocol_v1_1.yaml` and registry | Strict zero-calibration LOSO as reported by P3 |
| P6 decoder-quality bridge | NOT SATISFIED | P3 has classification folds, not MyoSim intent traces with quality-condition mapping | P6 R3 hard stop remains active |
| Authorship/provenance | PRESERVED | P3 archive retains its upstream `docs/DATA_PROVENANCE.md` and citation metadata | No provenance disclosure was removed or falsified |


## PUBLIC-DATA REOPENING ADDITIONS
| ID | Claim | Class | Evidence source | Permitted use | Limitation |
|---|---|---|---|---|---|
| C20 | A CPU-first LOSO decoder can produce authenticated offline traces from 20 public PhysioNet subjects | A — directly demonstrated | `p6/results/LOSO_RESULTS.json`, dataset and trace manifests | Methods and qualified systems description | One dataset/run and transparent baseline; not clinical evidence |
| C21 | Three decoder configurations provide a weak, non-monotonic held-out quality contrast | A — directly demonstrated | `QUALITY_SUMMARY.json`, `PAIRED_STATISTICS.json` | Qualified negative/neutral result | Not a universal dose-response law |
| C22 | Authenticated OPEN/CLOSE traces are consumable by MyoSim V1 replay | A — directly demonstrated | `MYOSIM_REPLAY_VALIDATION.json` | Offline integration evidence | Three S001 replay-contract runs; zero commands released under temporal gating |
| C23 | Historical pre-reopening P6 R3 hard stop is closed | E — unsupported | None | Must not be claimed | The historical gate remains preserved; only the separate reopening is complete |
