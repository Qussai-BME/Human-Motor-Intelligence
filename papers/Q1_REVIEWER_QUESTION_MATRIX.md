# Q1 Reviewer Question Matrix

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


This matrix is an evidence-response tool, not a claim catalogue. A “blocked” entry is an honest programme result when a source or protocol gate prevented a valid experiment.

| Reviewer question | Evidence answer | Source artefact | Claim boundary / next action |
|---|---|---|---|
| Are P1 metrics distorted by rest windows? | P1 reports a large overall-versus-macro-F1 divergence in the stated DB3 analysis and an active-only contrast. | `EMG_SERIES_MASTER_EVIDENCE.md`; P1 extracted source text | Do not assert universal inflation; retain rest-policy and DB3 limitations. |
| Are P1 groups/algorithms adequately compared? | P1 supplies strict LOSO and reported Friedman results but records small DB3 and modelling caveats. | P1 source extract | Preserve stated caveats; do not retrofit EA/CNN ablations. |
| Does P2 show that domain adaptation fails generally? | No. P2’s mechanism is representation-specific to its MiniROCKET PPV conditioning diagnosis. | `EMG_SERIES_MASTER_EVIDENCE.md` | State scope explicitly; cite adaptation literature context. |
| Can P1 and P2 reported accuracies be directly compared? | No. P1 includes rest in reported overall metrics; P2 excludes rest. | `EMG_SERIES_MASTER_EVIDENCE.md` | Require a harmonized metric policy before numerical comparison. |
| What evidence supports P3? | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** | `EMG_SERIES_MASTER_EVIDENCE.md` | Do not infer an effect, architecture, or conclusion. |
| Is P4 genuinely subject-independent? | Yes for Recovery R1: one held-out subject at a time; classifier/scaler fitting excludes the held-out subject; no target calibration. | P4 `protocol.json`, `validation.json`, `subject_level_results.csv` | Scope is OpenBMI binary MI only. |
| Are P4 data/source/license/provenance adequate? | NEMAR v1.0.5, 54 subjects, receipts/provenance, D1 integrity pass, GPL-3.0 recorded. | P4 manifest; `V2_P4_OPENBMI_EXTERNAL_VALIDATION_AUDIT_RECOVERY_R1.md` | External validation, not direct replication. |
| Is the P4 chance discussion mathematically careful? | The audit uses a nominal binary accuracy reference under exact balance; it does not equate macro-F1 mechanically with chance. | P4 audit; `statistics_macro_f1.json` | Keep accuracy and macro-F1 distinct. |
| Does a P4 model win? | Omnibus Friedman *p*=0.00281; no pairwise comparison survives Holm (minimum adjusted *p*=0.1042). | `statistics_macro_f1.json` | No confirmed pairwise superiority claim. |
| Are P4 results reproducible? | Yes: independent complete rerun produced identical 270-row CSV and matching manifest/protocol checksums. | P4 primary/rerun directories; P4 audit | Rerun is a reproducibility check, not extra evidence subjects. |
| Does P4 directly reproduce BCI IV-2a? | No. Cohort, class structure, recordings, and implementation differ. | P4 protocol and audit | Compare only qualitative protocol-qualified patterns. |
| Did P5 test the full external fusion hypothesis? | No. It stopped before extraction/model fit because source `sub-23` lacks one imagery run and twist labels under the locked 25-subject all-11-class cohort. | `V2_P5_JEONG_AVAILABILITY_HARD_STOP.md`; event inventory | Do not report a P5 external null or use 24 subjects silently. |
| Does P5 establish that fusion is useless? | No. Frozen Cho2017 transparent-fusion null remains dataset/protocol-specific; no new P5 external score exists. | V2 master audit; literature log | Retain transparent-fusion question; do not generalize to all fusion architectures. |
| Why could EMG exceed EEG during imagery? | The programme lists microactivation, quality, preprocessing, task, and participant strategy as hypotheses only. | V2 specification; master audit | No causal attribution without targeted evidence. |
| Did P6 provide 20 independent replays? | No. Runtime inspection showed seed metadata/reset but no seed-dependent state/task/replay variation. | `V2_P6_REPLAY_VARIABILITY_CAPABILITY_HARD_STOP.md` | Do not create pseudo-replication; reopen only with a predeclared valid variation factor. |
| Are synthetic corruption outputs biomedical evidence? | No. They remain controlled synthetic sensitivity material only. | V2 master audit; frozen synthetic path policy | Keep `origin=synthetic_controlled_corruption`, `benchmark_eligible=false`. |
| What is the programme-level clinical implication? | The programme offers auditable evidence about protocol-specific cross-subject decoding and metrics, not clinical efficacy or device readiness. | All paper audits | Avoid patient-benefit, prosthesis-control, or universal generalization claims. |
