# HUMAN MOTOR INTELLIGENCE RESEARCH STACK
## V1 Validation, Real-Data Research, Benchmarking & Research-Grade Completion Specification

**Version:** 1.0
**Date:** August 22, 2026
**Authority:** Extends and operationalizes `Human_Motor_Intelligence_Research_Stack_Master_Spec.md`
**Baseline:** Existing `human-motor-intelligence` umbrella repository after Phases A–I
**Objective:** Upgrade the current integration stack from a validated software/integration system into a research-grade, real-data-validated, publication-supporting platform.

---

## 0. PURPOSE

This specification does **not** authorize a rewrite.

The existing Human Motor Intelligence Research Stack is considered the architectural baseline. The objective is to preserve its contracts, adapters, provenance system, registry, benchmark guards, Research-OS CLI, and MyoSim integration while completing the parts that are still scaffolded or synthetic-only.

The current system has already demonstrated:

- versioned cross-project contracts;
- independent repositories with thin adapters;
- provenance and artifact hashing;
- protocol-bound benchmark guards;
- a synthetic, replay-first MyoSim integration;
- an EEG/fusion preparation layer;
- a local Research-OS workflow;
- successful umbrella test/integration checks.

The missing step is **evidence**.

The project must now prove, on real datasets and under registered protocols, that the infrastructure can execute reproducible biosignal experiments and produce auditable scientific outputs.

The target end state is:

> A thin, reproducible research orchestration layer that can register, execute, evaluate, compare, and reproduce real biosignal experiments across EMG/EEG/ECG, with ECoG/iEEG prepared as an experimental modality, while preserving the independence of the mature child repositories.

---

# 1. NON-NEGOTIABLE PRINCIPLES

## 1.1 No rewrite

Do not rebuild:

- BioSignal-FM V4;
- MyoAdapt v2;
- MyoControl;
- MyoSim V1.x.

Do not vendor their source trees.

Do not create a monolithic super-framework.

The umbrella remains thin.

## 1.2 No synthetic scientific claims

Synthetic data may be used for:

- unit tests;
- contract tests;
- deterministic integration;
- development;
- demonstrations.

Synthetic data may NEVER be used to claim:

- real-data accuracy;
- generalization;
- benchmark superiority;
- clinical utility;
- cross-subject performance;
- multimodal scientific benefit.

## 1.3 Real-data claims require provenance

Every real-data experiment must record:

- dataset name;
- dataset version/release identifier where available;
- source URL;
- access/license status;
- subject/session identifiers;
- preprocessing protocol;
- task protocol;
- train/validation/test split;
- random seed;
- model version;
- code commit;
- environment fingerprint;
- configuration hash;
- metrics;
- statistical unit;
- artifact hashes.

If any mandatory provenance is missing, the result is **not benchmark-eligible**.

## 1.4 No hidden protocol changes

A protocol is immutable once registered for a run.

Changing any of the following creates a new protocol version:

- subject split;
- target exposure;
- calibration policy;
- preprocessing window;
- feature-selection rule;
- normalization rule;
- metric definition;
- hyperparameter selection policy;
- dataset subset;
- task labels.

## 1.5 Subject-level inference

For cross-subject experiments, the statistical unit is the subject/fold, not the individual window.

Window-level samples may be used for training and model fitting, but they must not be treated as independent subjects in statistical inference.

## 1.6 No test-set tuning

Outer test subjects must never determine:

- hyperparameters;
- preprocessing choices;
- feature selection rules;
- model selection;
- lambda selection;
- early stopping.

## 1.7 Negative results are valid

The system must support a conclusion such as:

> “The method did not improve the registered baseline under this protocol.”

The purpose is scientific validity, not leaderboard optimization.

---

# 2. CURRENT BASELINE TO PRESERVE

The current umbrella implementation contains, among other elements:

- schema-versioned immutable contracts;
- local registry;
- provenance and artifact verification;
- dataset/protocol/model/project/benchmark cards;
- mapping-only adapters;
- MyoSim intent bridge;
- EEG protocol scaffolds;
- fusion validation scaffolds;
- benchmark eligibility guards;
- report/asset export;
- local Research-OS CLI;
- synthetic end-to-end demonstrator.

All of the above should remain unless a concrete defect is found.

Do not replace a working subsystem simply to make it aesthetically different.

---

# 3. CURRENT GAPS TO CLOSE

The completion effort is specifically intended to address:

1. No real EEG benchmark execution.
2. No real multimodal fusion result.
3. No independently verified real-data benchmark for the umbrella layer.
4. Child-suite environment verification incomplete.
5. No complete clean-environment verification matrix.
6. Synthetic demonstrator is not yet paired with a real-data downstream-control experiment.
7. Dataset acquisition and licensing workflows need operationalization.
8. Benchmark reports need automated publication-grade output.
9. Statistical testing needs real subject-level data.
10. EEG/EMG transfer research is not yet executed.
11. Missing-modality experiments are specified but not executed.
12. Artifact lineage must be verified from raw-data acquisition through final report.

---

# 4. REAL-DATA DATASET POLICY

The implementation agent has access to a cloud/runtime environment and may use real datasets when legally and technically accessible.

The agent must:

1. Prefer official or canonical sources.
2. Record source URLs.
3. Record dataset version/release information when available.
4. Record license/access conditions.
5. Never commit raw restricted data to Git.
6. Keep large raw data outside the repository.
7. Keep only small fixtures, manifests, checksums, and derived non-sensitive metadata when permitted.
8. Cache downloaded datasets reproducibly.
9. Verify checksums where the source publishes them or where a stable checksum is generated locally.
10. Document any dataset access limitation.

If a dataset cannot be obtained legally or reproducibly, do NOT fabricate a result. Mark the track blocked and continue other valid tracks.

---

# 5. REAL DATASET TARGETS

## 5.1 EEG — BCI Competition IV Dataset 2a

Primary real-data EEG benchmark.

Use the official dataset description and files.

The official description specifies:

- nine subjects;
- motor imagery;
- four classes;
- 22 EEG channels;
- EOG channels provided for artifact processing;
- 250 Hz sampling;
- training and evaluation sessions.

Official source:

https://www.bbci.de/competition/iv/desc_2a.pdf

Important protocol rule:

Do NOT use EOG channels as classification features.

For the main scientific LOSO benchmark, prefer the publicly labeled training-session data unless the official evaluation labels are independently and legitimately available. Do not treat unlabeled competition evaluation data as a standard supervised test set.

Recommended research protocol:

- subject = outer unit;
- train on all other subjects' labeled training data;
- test on the held-out subject's labeled data under an internally registered LOSO protocol;
- no target calibration;
- no target labels used for model selection;
- training-fold preprocessing only.

Record whether the experiment is:

`BCI2A_LOSO_TRAIN_SESSION_v1`

or another explicitly versioned protocol.

## 5.2 EMG — NinaPro

Use already established local NinaPro availability where legally permitted.

Primary continuity benchmark:

- DB2
- DB3
- DB7

Existing project knowledge includes strict LOSO and the Paper 3 protocol.

Do not alter Paper 3's locked experimental protocol.

The Research Stack may consume Paper 3 exports/manifests, but must never rewrite Paper 3.

Official dataset source:

https://ninapro.hevs.ch/

## 5.3 ECG — PhysioNet / MIT-BIH Arrhythmia

Use as a multimodal validation track, not as a motor-intent dataset.

Official source:

https://physionet.org/content/mitdb/

Primary purpose:

- validate that the framework handles a non-motor physiological modality;
- validate modality-specific preprocessing;
- validate downstream classification/evaluation contracts;
- validate provenance and real-data benchmark generation.

Do not compare ECG accuracy numerically against EMG/EEG accuracy as if tasks were equivalent.

## 5.4 ECoG / iEEG

ECoG/iEEG remains an experimental adapter track.

Use a legally accessible BIDS-compatible or OpenNeuro dataset only if the dataset's license/terms permit the intended use.

Do not force a full ECoG benchmark if a suitable public dataset cannot be obtained quickly and correctly.

The goal is:

- validate adapter architecture;
- validate channel/electrode metadata handling;
- validate provenance;
- validate basic end-to-end parsing;

not to claim ECoG research superiority.

Relevant infrastructure:

https://mne.tools/stable/
https://mne.tools/mne-bids/stable/
https://openneuro.org/

---

# 6. DATA ACQUISITION & INGESTION IMPLEMENTATION

Implement a reproducible data acquisition layer or scripts that generate a dataset manifest containing:

- dataset ID;
- source URL;
- retrieval timestamp;
- release/version if available;
- local storage root;
- file count;
- total size;
- checksums where practical;
- license/access note;
- expected subjects;
- expected modalities;
- expected sampling rates;
- expected channels;
- validation result.

Raw data remain external to the Git repository.

The repository stores manifests, not large raw datasets.

---

# 7. DATA VALIDATION GATES

Before any experiment:

### Gate D1 — File integrity

- all expected files present;
- readable;
- checksum verified or locally recorded;
- no silent truncation.

### Gate D2 — Schema validation

- channels;
- sampling rate;
- data dimensions;
- events;
- subject identifiers;
- session identifiers.

### Gate D3 — Label validation

- class inventory;
- missing labels;
- unexpected labels;
- class counts;
- subject-specific missing classes.

### Gate D4 — Protocol validation

- expected sessions;
- expected subject count;
- split rules;
- calibration exposure.

### Gate D5 — Leakage audit

Prove that no outer-test subject information leaks into preprocessing or training.

---

# 8. REAL EEG EXPERIMENT TRACK

This is the first mandatory real-data research track.

## EEG-0 — Data ingest

BCI IV-2a real data loaded and validated.

## EEG-1 — Classical baseline

Implement/reuse a strong, transparent baseline such as:

- LDA with appropriate EEG features;
- CSP/FBCSP-style baseline if implemented in a separate validated module;
- another standard baseline only if its protocol is clearly documented.

Do not over-engineer.

## EEG-2 — Spectral baseline

Power/spectral feature baseline with training-fold feature selection.

## EEG-3 — Lightweight deep baseline

One lightweight CNN/TCN baseline.

## EEG-4 — Representation baseline

One lightweight learned representation model.

## EEG-5 — Domain generalisation baseline

A subject-invariant/adversarial baseline only after the non-adversarial baselines are validated.

## EEG-6 — Full LOSO

Run across all available labeled subjects.

## EEG-7 — Statistics

Report subject-level:

- accuracy;
- macro-F1 where meaningful;
- balanced accuracy where meaningful;
- per-subject performance;
- confidence intervals where justified;
- pairwise comparisons only when pre-registered/appropriate.

Do not use accuracy alone.

---

# 9. EEG PROTOCOL RULES

For every EEG pipeline:

- filtering parameters must be fixed before outer test evaluation;
- channel selection must be training-only if data-driven;
- normalization must be training-only;
- feature selection must be training-only;
- PCA must be fitted on training data only;
- CSP/FBCSP must be fitted on training data only;
- hyperparameters must be selected without using the outer test subject;
- EOG channels must not become classification features in BCI IV-2a main benchmark;
- no post-hoc tuning based on held-out subjects.

Every transform must have a provenance record.

---

# 10. EMG RESEARCH-INTEGRATION TRACK

The umbrella platform should validate that it can consume real EMG outputs without changing Paper 3.

Use:

- Paper 3 manifests where available;
- MyoAdapt real-data run manifests where legally reproducible;
- BioSignal-FM real-data exports where available.

Produce:

`REAL_EMG_INTEGRATION_REPORT.md`

with:

- source experiment;
- dataset;
- protocol;
- model;
- subject-level metrics;
- provenance;
- artifacts;
- eligibility classification.

This report must distinguish:

- imported real result;
- independently reproduced result;
- synthetic result;
- external claim not reproduced.

---

# 11. ECG VALIDATION TRACK

Run a minimal real ECG task using an official PhysioNet dataset.

Requirements:

- real data;
- clearly defined task;
- subject-aware split where the dataset permits it;
- preprocessing provenance;
- baseline;
- metrics;
- artifact report.

The purpose is architectural multimodality validation, not a new ECG paper.

---

# 12. ECoG VALIDATION TRACK

Only if a suitable dataset is available under compatible terms.

Implement:

- adapter;
- metadata parsing;
- electrodes/coordinates handling;
- signal contract conversion;
- small real-data smoke validation.

No benchmark claim required.

---

# 13. MULTIMODAL EEG–EMG TRACK

This is the main research expansion after the unimodal EEG baseline is validated.

## Question

> Does combining central neural and peripheral muscular signals improve subject-generalizable motor-intent decoding compared with either modality alone?

This question must be treated as research, not an automatic claim of benefit.

Implement:

A. EEG-only
B. EMG-only
C. Early fusion
D. Mid-level representation fusion
E. Late fusion
F. Missing-EEG condition
G. Missing-EMG condition

All protocols must define the exact evaluation split.

---

# 14. MULTIMODAL FUSION RULES

The default conceptual architecture is:

    EEG → EEG Encoder ──┐
                        │
    EMG → EMG Encoder ──┼→ Fusion → Task Head
                        │
    ECG → optional ─────┘

Do not force ECG into the motor-intent fusion experiment unless the scientific question warrants it.

Fusion methods should be evaluated separately.

Do not report “multimodal improvement” unless the same subject split, task, and label semantics are used for all comparisons.

---

# 15. MISSING-MODALITY ROBUSTNESS

Run controlled experiments:

- full EEG+EMG;
- EEG only;
- EMG only;
- modality dropped at random if method supports it.

Measure:

- degradation from full modality set;
- robustness;
- subject-level variance;
- failure modes.

Do not fabricate missing data.

Use actual modality absence or a documented simulation method.

---

# 16. MOTOR INTENT → PHYSICAL CONTROL EXPERIMENT

Upgrade the current synthetic MyoSim demonstrator to include a real-data downstream control experiment when technically possible.

Pipeline:

real biosignal dataset
    ↓
validated decoder / representation
    ↓
IntentRecord
    ↓
MyoSim
    ↓
safe controller
    ↓
prosthetic task

Do not claim clinical control.

Primary research question:

> Does a difference in signal-decoding performance translate into a difference in downstream simulated motor-control utility?

Compare at least two decoder conditions where scientifically justified.

Possible metrics:

- task success rate;
- task completion time;
- command latency;
- false activation rate;
- command reversals;
- trajectory stability;
- safety interventions.

This experiment is a systems study, not a clinical trial.

---

# 17. DECODING VS CONTROL UTILITY

Create a report that explicitly separates:

### Recognition quality

accuracy / macro-F1 / balanced accuracy / calibration where appropriate.

### Control utility

task success / latency / stability / false activations.

Do not assume the model with the highest classifier accuracy is necessarily the best controller.

This comparison should become one of the strongest systems-level outputs of the stack.

---

# 18. RESEARCH REGISTRY EXTENSION

Extend the registry with first-class real-data experiment support.

Required cards:

- DatasetCard
- ProtocolCard
- ModelCard
- ExperimentCard
- ProjectCard
- BenchmarkCard
- ArtifactCard
- RunCard

Every completed real-data experiment must be queryable from the local Research-OS CLI.

Example conceptual queries:

```text
list datasets
list protocols
list real experiments
show experiment <id>
compare runs <id1> <id2>
show artifacts <run>
verify manifest <run>
export report <run>
```

---

# 19. BENCHMARK ENGINE — RESEARCH-GRADE REQUIREMENTS

The benchmark engine must enforce:

1. same dataset;
2. same protocol;
3. compatible task;
4. compatible label space;
5. subject-level observations;
6. real-data eligibility;
7. identical evaluation definitions;
8. documented missing-data policy;
9. documented calibration policy;
10. documented hyperparameter-selection policy.

It must reject comparisons that violate these conditions.

---

# 20. BASELINE POLICY

Every new learned method must be compared with at least one transparent strong baseline.

For EEG:

- LDA/CSP-type classical baseline where appropriate;
- lightweight deep baseline.

For EMG:

- established classical baseline;
- existing Paper 3 / MyoAdapt baseline when compatible.

For multimodal fusion:

- EEG-only;
- EMG-only;
- simplest fusion baseline.

Never compare a sophisticated method only against a weak baseline.

---

# 21. STATISTICS

For cross-subject studies:

Primary unit:

`subject/fold`

Preferred reports:

- mean ± SD;
- median/IQR when distributions warrant;
- per-subject scores;
- confidence intervals where appropriate;
- paired comparisons because the same subjects are usually evaluated by each condition.

When comparing >2 models/conditions on the same subjects:

- consider Friedman test;
- post-hoc Wilcoxon signed-rank tests;
- Holm correction.

Do not apply tests blindly; confirm assumptions and study design.

Effect sizes should be reported where informative.

Do not treat 20,000 windows from one subject as 20,000 independent experimental units.

---

# 22. METRICS POLICY

The framework must support task-appropriate metrics.

Classification candidates:

- accuracy;
- balanced accuracy;
- macro-F1;
- per-class F1;
- confusion matrix;
- Cohen's kappa where justified;
- calibration metrics where probabilistic outputs matter.

Cross-subject biosignal studies should additionally report:

- per-subject performance;
- subject variance;
- worst-subject performance where meaningful.

Do not automatically report every metric for every task.

---

# 23. PAPER-READY REPORT GENERATION

Every completed research run must be able to produce:

- `results.csv`;
- `metrics.json`;
- `protocol.json`;
- `manifest.json`;
- confusion matrix SVG/PNG;
- subject-level results CSV;
- aggregate table CSV;
- LaTeX-ready table;
- Markdown summary;
- machine-readable experiment record.

Every figure/table must embed or reference:

- experiment ID;
- dataset;
- protocol;
- model;
- git commit;
- configuration hash.

---

# 24. REAL-DATA REPORT TEMPLATE

Every real-data experiment produces:

```text
Experiment ID
Dataset
Dataset version
Source URL
License/access
Modality
Task
Subjects
Protocol ID
Calibration policy
Preprocessing
Model
Hyperparameter policy
Seed
Git commit
Environment
Results
Subject-level results
Statistical analysis
Artifact list
Limitations
Eligibility status
```

---

# 25. REPRODUCIBILITY VALIDATION

For at least one representative real experiment per modality track:

Run 1:
full execution

Run 2:
independent replay from the same manifest/configuration

Verify:

- identical or tolerance-equivalent predictions;
- identical metrics;
- identical protocol identity;
- identical artifact lineage;
- reproducible model/version reference.

If exact numerical identity is impossible, document the tolerance and cause.

---

# 26. CLEAN-ENVIRONMENT VALIDATION

Create a validation matrix for every child project:

| Project | install | import | unit tests | integration | real-data smoke | status |
|---|---|---|---|---|---|---|
| BioSignal-FM | required | required | required | required | required where accessible | |
| MyoAdapt | required | required | required | required | required where accessible | |
| MyoControl | required | required | required | required | required where accessible | |
| MyoSim | required | required | required | required | required where accessible | |
| Umbrella | required | required | required | required | required | |

Each failure must be classified as:

- code defect;
- missing dependency;
- blocked dataset;
- environment limitation;
- licensing/access limitation.

Never mark a blocked test as “passed”.

---

# 27. CONTAINER / ENVIRONMENT VERIFICATION

Where practical create a reproducible environment for the umbrella and each child project.

Prefer:

- lockable dependency declarations;
- Python version documentation;
- optional extras per modality;
- CPU-safe defaults;
- minimal-core installation.

Do not require every optional modality to be installed for the core package.

---

# 28. PERFORMANCE

The final system should measure:

- data ingestion time;
- preprocessing time;
- training time;
- inference time;
- memory use where practical;
- artifact generation time.

Do not optimize blindly.

Add profiling only when a bottleneck is demonstrated.

---

# 29. REAL-TIME / STREAMING READINESS

Do not build hardware streaming now.

But contracts should not prevent future streaming.

A future streaming adapter should be conceptually able to emit:

IntentRecord(timestamp, confidence, modality, model_version, ...)

without changing downstream MyoSim or registry contracts.

No network infrastructure is required now.

---

# 30. COMMERCIAL PRODUCT DISCOVERY TRACK

Do not build a full SaaS platform in this phase.

Instead create a small product-readiness layer:

- researcher workflow document;
- user journey;
- one-command experiment execution;
- shareable experiment report;
- exportable artifact package;
- reproducibility bundle.

The potential product hypothesis is:

> A researcher-focused reproducibility and benchmarking workbench for biosignal experiments.

Validate the workflow first.

Do not add:

- billing;
- subscriptions;
- accounts;
- multi-tenant cloud;
- payment processing.

These require separate commercial validation.

---

# 31. SECURITY / DATA GOVERNANCE

Enforce:

- no credentials in manifests;
- URI secret rejection;
- no raw-data commits;
- dataset license record;
- data access notes;
- sanitized reports;
- no accidental subject-identifying metadata in public artifacts.

If a dataset has restrictions, the registry must preserve the restriction status.

---

# 32. SCIENTIFIC CLAIM GUARDRAIL

Automated reports must distinguish:

REAL RESULT
SYNTHETIC RESULT
IMPORTED EXTERNAL RESULT
REPRODUCED RESULT
UNVERIFIED CLAIM

No imported paper number becomes a local benchmark result unless independently reproduced.

---

# 33. EEG RESEARCH OUTPUT STANDARD

At completion of the EEG track, the project must have:

1. real dataset acquisition/validation evidence;
2. one classical baseline;
3. one lightweight deep baseline;
4. one representation-learning baseline;
5. full subject-level evaluation;
6. complete provenance;
7. statistical summary;
8. publication-ready tables/figures;
9. limitations;
10. reproducibility rerun.

Only then can the project say:

> “The EEG research track has been experimentally validated on BCI IV-2a under protocol X.”

Do not claim general EEG foundation-model superiority from one dataset.

---

# 34. EEG–EMG RESEARCH OUTPUT STANDARD

At completion:

- unimodal EEG baseline;
- unimodal EMG baseline;
- fusion baseline;
- subject-level paired evaluation;
- missing-modality analysis;
- statistical comparison;
- complete provenance;
- reproducible artifacts.

The result may be positive, neutral, or negative.

All three are valid.

---

# 35. CONTROL DEMONSTRATOR RESEARCH OUTPUT STANDARD

For the real-data downstream-control experiment:

- input source identified;
- decoder identified;
- intent mapping explicit;
- no direct decoder-to-physics bypass;
- MyoSim safety intact;
- replay reproducible;
- task success measurable;
- benchmark labelled as systems/control study, not clinical evidence.

---

# 36. FINAL ARCHITECTURE

The completed Human Motor Intelligence Stack should look conceptually like:

```text
                  REAL BIOSIGNAL DATA
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
         EMG            EEG            ECG
          │              │              │
          └───────┬──────┴──────┬───────┘
                  ↓              │
          BioSignal-FM           │
                  ↓              │
          Representation         │
                  ↓              │
          Subject Generalisation │
                  ↓              │
               Intent            │
                  ↓              │
             MyoControl /        │
             MyoAdapt /          │
             Lite-DAN            │
                  ↓              │
            IntentRecord ────────┘
                  ↓
               MyoSim
                  ↓
          Safe simulated control
                  ↓
              Task result
                  ↓
        Research OS / Benchmark
                  ↓
      Tables / Figures / Reports
```

This is a conceptual systems map, not a requirement to make every repository import every other repository.

---

# 37. IMPLEMENTATION PHASES

The agent is authorized to work end-to-end without waiting for approval after every phase.

## Phase J — Real-data acquisition & validation

Deliver:

- dataset manifests;
- source/license records;
- ingestion validation;
- real-data smoke fixtures;
- acquisition audit.

Gate:
No real experiment before D1–D5 pass.

## Phase K — Clean environment matrix

Deliver:

- child-project install/test matrix;
- dependency fixes where required;
- no source changes to children unless explicitly authorized;
- environment blockers documented.

## Phase L — EEG real benchmark

Deliver:

- BCI IV-2a real-data loader;
- LOSO protocol;
- baselines;
- representation baseline;
- real metrics;
- statistics;
- reproducibility rerun;
- publication-ready artifacts.

## Phase M — Real EMG integration

Deliver:

- real Paper 3/MyoAdapt/BioSignal-FM manifest import;
- eligibility audit;
- subject-level reporting;
- provenance.

Do not modify Paper 3.

## Phase N — ECG validation

Deliver:

- real PhysioNet data path;
- baseline;
- metrics;
- report;
- provenance.

## Phase O — Multimodal EEG–EMG

Deliver:

- EEG-only;
- EMG-only;
- fusion;
- missing-modality analysis;
- statistics;
- paper-ready assets.

## Phase P — Real-data MyoSim downstream experiment

Deliver:

- real decoder output → intent contract;
- MyoSim replay;
- control metrics;
- comparative decoder study;
- reproducibility bundle.

## Phase Q — Research-OS publication workflow

Deliver:

- one-command report generation;
- experiment comparison;
- table/figure generation;
- manifest bundle;
- benchmark export.

## Phase R — Final red-team audit

Audit:

- architecture;
- contracts;
- data leakage;
- statistical validity;
- provenance;
- reproducibility;
- dependencies;
- security;
- documentation;
- unsupported claims;
- code quality;
- performance;
- real-data evidence.

## Phase S — Release

Create:

- `FINAL_PROJECT_REPORT.md`;
- `REAL_DATA_VALIDATION_REPORT.md`;
- `BENCHMARK_REPORT.md`;
- `REPRODUCIBILITY_REPORT.md`;
- `CHILD_PROJECT_VALIDATION_MATRIX.md`;
- release changelog;
- verified artifact manifest.

---

# 38. ACCEPTANCE CRITERIA FOR “10/10” STATUS

The stack must NOT be labelled complete until:

### Architecture

- all approved boundaries remain intact;
- no monolith has emerged;
- contracts are versioned;
- adapters remain thin;
- child systems remain independently runnable.

### Real Data

- at least one real dataset has been processed successfully for each claimed active modality;
- EEG has a real BCI IV-2a experiment;
- EMG has a real integration path;
- ECG has a real validation path;
- ECoG has a validated adapter if a legally accessible dataset is available.

### Scientific Evaluation

- subject-level metrics;
- registered protocols;
- leakage audit;
- meaningful baselines;
- statistical comparisons where justified;
- no test tuning;
- reproducibility rerun.

### Multimodal

- EEG-only;
- EMG-only;
- fusion;
- missing-modality condition;
- subject-level comparison.

### Physical control

- real decoder output can reach MyoSim through the Intent contract;
- safety remains active;
- control metrics are reported;
- replay is reproducible.

### Reproducibility

- clean-environment matrix;
- manifests;
- hashes;
- exact protocol identity;
- rerun verification.

### Research output

- publication-ready tables;
- figures;
- experiment manifests;
- machine-readable results;
- complete limitation statements.

### Integrity

- no synthetic result presented as real;
- no imported external number presented as reproduced;
- no clinical claims;
- no unsupported foundation-model claims.

---

# 39. FAILURE POLICY

If a real dataset fails to download:

STOP THAT TRACK.

Document:

- source;
- failure;
- access condition;
- attempted resolution;
- consequence.

Continue independent tracks.

If a baseline fails:

Do not silently replace it.

Document the failure and implement a justified alternative as a new registered condition.

If leakage is detected:

Invalidate affected runs.

Do not repair the result retrospectively.

If reproducibility fails:

Mark the run non-reproducible until fixed.

---

# 40. REQUIRED FINAL ARTIFACT TREE

Conceptually:

```text
human-motor-intelligence/
├── src/
├── tests/
├── configs/
├── datasets/
│   └── manifests/
├── protocols/
├── results/
│   ├── real/
│   ├── synthetic/
│   └── imported/
├── artifacts/
│   ├── figures/
│   ├── tables/
│   ├── reports/
│   └── manifests/
├── reports/
├── docs/
└── audit/
```

Do not place raw restricted datasets in the repository.

---

# 41. REQUIRED FINAL REPORTS

## FINAL_PROJECT_REPORT.md

Overall architecture and status.

## REAL_DATA_VALIDATION_REPORT.md

What real datasets were actually executed, with provenance.

## BENCHMARK_REPORT.md

All benchmark-eligible real experiments.

## REPRODUCIBILITY_REPORT.md

Rerun results and environment verification.

## CHILD_PROJECT_VALIDATION_MATRIX.md

Install/test/integration status for each child repository.

## SCIENTIFIC_LIMITATIONS.md

Explicit limitations and claims that are NOT supported.

---

# 42. CLAIM LANGUAGE AT COMPLETION

Permitted example:

> “The Research Stack was validated on BCI Competition IV Dataset 2a under a registered subject-level LOSO protocol.”

Only if actually executed.

Permitted:

> “We observed X ± Y across subjects under protocol Z.”

Only if produced by the registered experiment.

Not permitted:

> “The platform proves general biosignal intelligence.”

Not permitted:

> “The foundation model generalizes universally.”

Not permitted:

> “Clinical-ready.”

unless future evidence genuinely supports such claims.

---

# 43. FINAL AGENT EXECUTION INSTRUCTION

Work through Phases J–S end-to-end.

Do not ask for approval after every phase.

However, STOP and report immediately if:

- a real architectural contradiction is discovered;
- a legal/data-access blocker prevents a required experiment;
- a safety issue is found;
- a severe leakage risk is detected;
- the specification cannot be satisfied without changing a locked child-project protocol.

Otherwise continue autonomously.

At the end, produce all required reports and a truthful final status.

The objective is NOT to manufacture impressive numbers.

The objective is to turn the existing Human Motor Intelligence Research Stack into a **real-data-validated, reproducible, scientifically defensible research platform** that can generate trustworthy evidence for future papers, demos, collaborations, and eventually product discovery.

# END OF SPECIFICATION
