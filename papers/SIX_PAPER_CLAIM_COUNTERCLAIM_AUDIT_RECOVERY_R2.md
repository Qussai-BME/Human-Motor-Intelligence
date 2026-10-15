# Six-Paper Claim–Counterclaim Audit — V2 Recovery R2

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


This audit governs manuscript wording after R2. A claim is admissible only when its artefact, evidence tier, and limitation are all stated together.

| ID | Candidate programme claim | Status | Supporting evidence | Counterclaim / required qualification |
|---|---|---|---|---|
| C1 | Rest-inclusive cross-subject sEMG accuracy can inflate apparent active-gesture performance. | Supported within P1 datasets | Author-supplied P1; P1 source record | Not a universal inflation magnitude; preserve DB-specific class policy and small-DB caveats. |
| C2 | The tested MiniROCKET PPV representation has a measurable numerical conditioning failure under the evaluated adaptation path. | Supported, representation-specific | Author-supplied P2 | Do not generalize to all time-series representations or all domain-adaptation methods. |
| C3 | P3 provides an additional EMG claim. | Not admissible | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** | No numbers, conclusions, ablations, or solution claims may be inferred. |
| C4 | Fixed zero-calibration EEG models decoded binary MI in an external 54-subject OpenBMI LOSO protocol. | Supported | P4 R1 results, D1–D5, exact rerun | Do not call direct BCI IV-2a replication or rank across datasets numerically. |
| C5 | One P4 model is definitively superior to every other fixed model. | Not supported | P4 Friedman omnibus is non-null | No P4 pairwise contrast survives Holm; report no pairwise superiority. |
| C6 | In the amended Jeong MI-only cohort, EEG-only/early/late conditions exceed EMG-only in the fixed LDA family. | Supported | P5 R2 Wilcoxon/Holm and exact rerun | Applies to 24-subject amended cohort, 11 classes, features, and zero calibration only. |
| C7 | Transparent fusion is generally useless. | Rejected | P5 R2 no fusion-over-EEG Holm result | External literature and other pipeline choices can differ; no general fusion conclusion is identified. |
| C8 | EMG-only is lower because imagery EMG is absent or microactivation causes a particular mechanism. | Rejected | P5 R2 descriptive result only | Microactivation, strategy, montage, preprocessing, and task complexity are unresolved alternatives. |
| C9 | Fixed replay/control is robust over the declared initial-state distribution. | Contradicted in P6 R2 | 0/20 P6 task successes; all `TRANSPORT` | Scope is the declared simulator distribution, not human performance. |
| C10 | Decoder quality caused P6 failures. | Not identified | P6 holds replay decoder stream fixed | The design contains no decoder-quality factor or causal contrast. |
| C11 | P6 proves clinical/prosthetic fragility. | Rejected | P6 MyoSim systems artefacts | No clinical population, physical device, or real-world perturbation was tested. |
| C12 | The programme shows that outcome metrics beyond classifier accuracy matter in control evaluation. | Methodologically supported | P6 task success/failure/final state differ in interpretive value from fixed decoder metrics | This is a systems-method claim, not validation of an endpoint in clinical use. |

## Publication Rule

All status labels above must be preserved in abstract, results, discussion, review, and press-facing summaries. A statistical result must not be promoted above the scope of the corresponding dataset, cohort, model family, or simulator distribution.
