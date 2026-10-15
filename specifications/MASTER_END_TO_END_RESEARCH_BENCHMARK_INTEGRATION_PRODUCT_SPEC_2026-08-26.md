HUMAN MOTOR INTELLIGENCE

MASTER END-TO-END RESEARCH, BENCHMARK, INTEGRATION & PRODUCT SPECIFICATION

Project Owner: Qussai Adlbi
Project Type: Research ecosystem / scientific integration platform / benchmark infrastructure / future product foundation
Status: Active research program; existing implementation is the architectural baseline
Specification Role: SINGLE SOURCE OF TRUTH for the umbrella project
Primary Principle: Do not rebuild mature child projects. Connect, validate, benchmark, demonstrate, and productize them.

---

0. EXECUTIVE DIRECTIVE

Build and complete Human Motor Intelligence as the coherent research ecosystem around Qussai Adlbi's biomedical-AI research trajectory.

The system must transform existing independent research projects into one scientifically coherent, reproducible and externally demonstrable research program without collapsing them into a monolithic repository.

The target ecosystem is:

BIOSIGNAL
   ↓
REPRESENTATION
   ↓
GENERALISATION
   ↓
MOTOR INTENT
   ↓
ADAPTATION
   ↓
CONTROL
   ↓
PHYSICAL INTERACTION
   ↓
MEASURABLE OUTCOME

The central scientific question is:

«How can biomedical AI decode human motor intent robustly across individuals, modalities, sessions and eventually physical systems, without requiring subject-specific calibration?»

The ecosystem must answer progressively:

1. Can motor information be decoded from biosignals?
2. Can it generalise to unseen subjects?
3. Why do domain-adaptation methods succeed or fail?
4. Can learned representations improve subject invariance?
5. Can these principles transfer from EMG to EEG?
6. Can EMG and EEG provide complementary information?
7. Can decoded intent drive stable simulated physical control?
8. Does better offline decoding actually produce better functional control?
9. Can the resulting research infrastructure become useful to other researchers?

This repository is the integration and research-orchestration layer.

It is NOT:

- a replacement for MyoControl;
- a replacement for MyoAdapt;
- a replacement for BioSignal-FM;
- a replacement for MyoSim;
- a giant shared-codebase;
- a generic biomedical framework.

---

1. CURRENT CHILD PROJECTS

Treat the following as existing independent systems.

1.1 MyoControl

Role:

«Motor-intent decoding / mature EMG research artifact.»

Use through explicit versioned interfaces.

Do not duplicate its internals.

---

1.2 MyoAdapt

Role:

«Cross-subject generalisation and domain-adaptation research infrastructure.»

Relevant research capabilities include:

- LOSO / LODO evaluation;
- EMG preprocessing;
- feature/representation analysis;
- MiniROCKET;
- CORAL;
- TCA;
- Euclidean Alignment;
- adversarial adaptation;
- Lite-DAN;
- calibration analysis;
- drift/electrode-shift studies;
- reproducibility;
- deployment-oriented interfaces.

Keep independent.

---

1.3 BioSignal-FM

Role:

«Multimodal biosignal representation-learning and research platform.»

Current architecture:

signal
 ↓
modality adapter
 ↓
modality-specific processing
 ↓
representation
 ↓
task/fusion layers

Core modalities:

- EMG;
- EEG;
- ECG.

Experimental:

- ECoG/iEEG.

Long-term:

- multimodal representation;
- transfer;
- missing-modality robustness;
- reusable biosignal intelligence.

Do not call it a scientifically validated foundation model unless evidence supports actual foundation-model properties.

---

1.4 MyoSim

Role:

«Decoder-independent software-only virtual physical-control simulation.»

Canonical chain:

Intent
 ↓
Decision Engine
 ↓
Controller
 ↓
Safety
 ↓
Physics
 ↓
Robot / Prosthetic Model
 ↓
Task
 ↓
Metrics

Keep independent.

---

2. NON-NEGOTIABLE ARCHITECTURE

Never build:

human-motor/
    myocontrol/
    myoadapt/
    biosignal/
    myosim/

as copied or tightly coupled source trees.

Instead:

                         HUMAN MOTOR
                              │
                    RESEARCH REGISTRY
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ↓                     ↓                     ↓
   BioSignal-FM          MyoAdapt              MyoControl
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ↓
                      VERSIONED CONTRACTS
                              ↓
                           MyoSim
                              ↓
                      FUNCTIONAL OUTCOME
                              ↓
                 BENCHMARK / REPORT ENGINE

The umbrella owns:

- contracts;
- registries;
- protocols;
- benchmark orchestration;
- experiment manifests;
- artifact references;
- report generation;
- integration;
- evidence tracking;
- external demonstration.

The child projects own:

- their science;
- their models;
- their preprocessing;
- their internal testing;
- their implementation details.

---

3. CORE SYSTEM COMPONENTS

The umbrella must contain only the following conceptual layers.

3.1 Contract Layer

Defines stable schemas for:

- biosignal metadata;
- experiment;
- protocol;
- model;
- prediction;
- intent;
- control event;
- result;
- artifact;
- provenance.

Every contract must have:

- name;
- semantic version;
- schema;
- validation;
- compatibility rule;
- provenance fields.

---

3.2 Dataset Registry

Register:

- dataset identifier;
- version;
- modality;
- source;
- access/license;
- subjects;
- sessions;
- task;
- label protocol;
- preprocessing version.

The registry stores metadata, NOT restricted raw datasets.

---

3.3 Protocol Registry

Protocols are immutable once executed.

Examples:

EMG-LOSO-v1
EEG-LOSO-v1
EEG-EMG-FUSION-v1
CONTROL-REPLAY-v1

A protocol version must define:

- inclusion criteria;
- split;
- preprocessing;
- normalization;
- calibration;
- target;
- hyperparameter policy;
- metric definitions;
- statistical unit.

Changing one of these creates a new version.

---

3.4 Experiment Registry

Every run receives:

- run ID;
- project;
- dataset;
- protocol;
- model;
- code commit;
- environment;
- seed;
- timestamp;
- configuration hash;
- outputs;
- status.

---

3.5 Artifact Registry

Artifacts include:

- predictions;
- metrics;
- figures;
- tables;
- model files;
- manifests;
- reports;
- logs.

Every artifact must have a provenance reference.

---

4. SCIENTIFIC GOVERNANCE

No experiment can become benchmark evidence unless:

- protocol is registered;
- split is explicit;
- leakage audit passes;
- statistical unit is correct;
- test data are not used for tuning;
- provenance is complete;
- results can be reproduced.

For cross-subject experiments:

«Subject/fold is the statistical unit, not windows.»

Never treat millions of windows as millions of independent biological subjects.

Synthetic data is allowed for:

- development;
- unit testing;
- contract testing;
- deterministic integration.

Synthetic data may NOT support:

- real-world performance claims;
- generalisation claims;
- benchmark superiority;
- clinical utility.

---

5. RESEARCH PROGRAM

The completed program must make the following trajectory explicit.

Chapter 1 — EMG decoding

Question:

«Can motor intent be decoded robustly from peripheral muscular signals?»

Evidence:

- Paper 1;
- Paper 2;
- Paper 3.

---

Chapter 2 — Generalisation

Question:

«What prevents motor-intent models from transferring between subjects?»

Evidence:

- LOSO;
- domain-shift analysis;
- adaptation experiments;
- mechanistic analysis.

---

Chapter 3 — Learned subject-invariant representations

Question:

«Can learned representations outperform or overcome the limitations of conventional alignment?»

Representative method:

- Lite-DAN.

---

Chapter 4 — EEG

Question:

«Can the same generalisation principles transfer from peripheral signals to neural signals?»

Must include:

- EEG preprocessing;
- real-data evaluation;
- subject-aware protocols;
- baselines;
- representation learning.

---

Chapter 5 — EEG–EMG

Question:

«Does combining central neural information and peripheral muscular information improve motor-intent decoding or robustness?»

Must evaluate:

- EEG only;
- EMG only;
- fusion;
- missing modality;
- subject-level comparison.

A negative result is scientifically valid.

---

Chapter 6 — Functional control

Question:

«Does better decoding translate into better physical control?»

Flow:

biosignal
 ↓
decoder
 ↓
IntentRecord
 ↓
Decision Engine
 ↓
controller
 ↓
MyoSim
 ↓
task
 ↓
functional metrics

---

6. HUMAN MOTOR BENCHMARK

The benchmark is not the same thing as Human Motor.

Human Motor is the research program.

The benchmark is the standardized scientific measurement layer.

Its first version should be:

«Human Motor Cross-Subject Benchmark»

Minimum evaluation dimensions:

- unseen subject;
- unseen session where applicable;
- calibration/no-calibration;
- model family;
- task;
- metric.

Later:

- cross-device;
- cross-task;
- missing modality;
- adaptation budget;
- drift.

Do NOT build every dimension simultaneously.

---

7. BENCHMARK OUTPUT

Every benchmark run should be able to produce:

benchmark/
├── protocol.json
├── dataset_manifest.json
├── run_manifest.json
├── predictions/
├── metrics/
├── statistics/
├── figures/
├── tables/
├── report.md
└── reproducibility.md

Minimum metrics depend on task.

For classification:

- accuracy;
- macro-F1;
- balanced accuracy;
- kappa where appropriate;
- per-subject metrics.

For regression:

- MAE;
- RMSE;
- R²;
- trajectory error.

For control:

- task success;
- completion time;
- command latency;
- false activation;
- stability;
- trajectory smoothness;
- failure rate.

---

8. CONTROL DEMONSTRATOR

The canonical demonstrator is:

EMG / EEG / Replay
        ↓
Decoder
        ↓
Intent Contract
        ↓
MyoSim
        ↓
Virtual Prosthetic / Robot
        ↓
Task
        ↓
Functional Metrics

The demonstrator must be:

- deterministic;
- replayable;
- traceable;
- visually understandable;
- measurable.

It must NOT be described as:

- clinical validation;
- patient-ready;
- medical device validation;
- proof of prosthesis effectiveness.

The correct language is:

- research demonstrator;
- simulated control;
- proof of concept;
- virtual prosthetic control.

---

9. REPRODUCIBILITY

A third party should be able to:

1. install the documented environment;
2. identify the protocol;
3. obtain the permitted dataset;
4. run the experiment;
5. regenerate metrics;
6. regenerate figures;
7. inspect provenance.

No raw protected dataset may be committed.

---

10. RESEARCH OUTPUT ENGINE

Generate:

- paper-ready tables;
- publication figures;
- statistical summaries;
- machine-readable JSON/CSV;
- experiment manifests;
- reproducibility bundles.

Automatically distinguish:

REAL RESULT
SYNTHETIC RESULT
IMPORTED RESULT
REPRODUCED RESULT
UNVERIFIED

Never present an imported number as a locally reproduced result.

---

11. RESEARCH OS / FUTURE COMMERCIAL LAYER

Potential workflow:

Dataset
 ↓
Protocol
 ↓
Experiment
 ↓
Model
 ↓
Run
 ↓
Metrics
 ↓
Statistics
 ↓
Figure/Table
 ↓
Reproducibility Package

This is a product hypothesis, not a guaranteed product.

V1 must NOT include:

- billing;
- subscriptions;
- cloud infrastructure;
- multi-tenancy;
- telemetry.

First prove researcher demand.

---

12. USER WORKFLOWS

The system must support three principal workflows.

Workflow A — Researcher

register dataset
→ select protocol
→ run experiment
→ inspect results
→ reproduce

Workflow B — Paper

registered protocol
→ experiments
→ statistics
→ figures
→ tables
→ report

Workflow C — Demonstration

decoder
→ intent
→ MyoSim
→ task
→ outcome

---

13. CLI

The umbrella should eventually expose commands conceptually equivalent to:

hm doctor
hm dataset list
hm dataset register ...
hm protocol list
hm protocol validate ...
hm experiment run ...
hm experiment reproduce ...
hm benchmark run ...
hm benchmark report ...
hm artifact list ...
hm demo control ...
hm report build ...

Do not create a CLI command until the underlying contract is stable.

---

14. PHASE PLAN

PHASE 0 — Architectural freeze

Audit:

- current repository;
- current contracts;
- current adapters;
- current registries;
- current tests.

Do not rebuild mature projects.

Deliver:

- architecture report;
- gap analysis;
- risk register.

Gate:

Architecture remains compatible with child projects.

---

PHASE 1 — Contract hardening

Deliver:

- versioned schemas;
- validators;
- compatibility tests;
- migration notes.

Gate:

All existing integrations still pass.

---

PHASE 2 — Registry hardening

Deliver:

- dataset registry;
- protocol registry;
- model registry;
- experiment registry;
- artifact registry.

Gate:

A synthetic experiment can be registered and replayed.

---

PHASE 3 — Benchmark engine

Deliver:

- protocol execution;
- metric aggregation;
- statistical layer;
- reporting.

Gate:

One real EMG benchmark can be executed end-to-end.

---

PHASE 4 — EMG research validation

Run existing validated EMG protocols through the orchestration layer.

Do NOT silently modify the paper protocol.

Gate:

Reproduced outputs are explicitly labelled reproduced.

---

PHASE 5 — EEG validation

Deliver:

- real EEG loader;
- subject-aware split;
- baselines;
- representation baseline;
- statistics;
- report.

Gate:

One reproducible EEG experiment.

---

PHASE 6 — Multimodal preparation

Deliver:

- EMG contract;
- EEG contract;
- fusion contract;
- missing-modality protocol.

Gate:

Synthetic fusion path passes.

---

PHASE 7 — MyoSim integration

Deliver:

decoder
→ IntentRecord
→ MyoSim
→ task
→ metrics

Gate:

Deterministic reproducible replay.

---

PHASE 8 — Functional benchmark

Compare decoders using:

- task success;
- latency;
- false activation;
- stability;
- completion time;
- trajectory metrics.

Gate:

At least one complete control benchmark.

---

PHASE 9 — Research showcase

Deliver:

- architecture diagram;
- benchmark;
- demonstration;
- reproducibility package;
- documentation.

Gate:

A technically literate external reviewer can understand the system in <10 minutes.

---

PHASE 10 — Product discovery

Only after evidence exists.

Deliver:

- researcher workflow;
- pain-point hypotheses;
- pilot interface;
- external-user testing;
- willingness-to-pay evidence.

Gate:

Do not commercialize unless external users demonstrate repeated value.

---

15. TESTING

Required:

- schema tests;
- contract tests;
- adapter tests;
- integration tests;
- protocol tests;
- reproducibility tests;
- report-generation tests;
- negative tests;
- leakage guards.

Do NOT duplicate all child-project unit tests.

---

16. SECURITY / DATA GOVERNANCE

Enforce:

- no secrets;
- no raw restricted data;
- license records;
- access metadata;
- sanitized reports;
- no hidden uploads;
- local-first operation.

---

17. OBSERVABILITY

Every run exposes:

- run ID;
- stage;
- project;
- dataset;
- protocol;
- model;
- status;
- duration;
- error;
- artifacts.

---

18. COMMERCIAL/IP BOUNDARY

Potential future commercial assets:

- benchmark infrastructure;
- experiment registry;
- reproducibility engine;
- research reporting;
- lab/team workflow;
- benchmarking service.

Do not claim commercial traction without external users.

Do not add telemetry secretly.

---

19. RELEASE DISCIPLINE

Every release must include:

- semantic version;
- Git commit;
- changelog;
- environment;
- benchmark summary;
- provenance;
- limitations;
- license information;
- reproducibility instructions.

Never overwrite scientific release artifacts.

---

20. DEFINITION OF DONE

Human Motor is complete as a V1 research platform when:

- independent projects remain runnable;
- versioned contracts are stable;
- registry works;
- protocols are immutable/versioned;
- benchmark engine works;
- real EMG evidence is registered;
- real EEG evidence is registered;
- control demonstrator works;
- MyoSim receives real or replayed decoder output;
- functional control metrics exist;
- reproducibility rerun succeeds;
- publication-ready artifacts are generated;
- limitations are explicit;
- no claim exceeds evidence.

The broader program is not required to have clinical hardware.

---

21. FINAL AGENT BEHAVIOUR

The agent must think:

«integrate before rebuilding
measure before claiming
reproduce before publishing
validate before commercializing»

The agent must maintain:

"IMPLEMENTATION_STATUS.md"

and finish with:

"FINAL_PROJECT_REPORT.md"

including:

- architecture;
- contracts;
- phases;
- changes;
- evidence;
- tests;
- benchmarks;
- demonstrations;
- reproducibility;
- limitations;
- commercial hypotheses;
- unresolved risks.

END OF SPECIFICATION