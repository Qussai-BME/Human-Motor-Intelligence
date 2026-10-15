# HUMAN MOTOR INTELLIGENCE RESEARCH STACK
## Master Integration, Research Infrastructure & Product Specification
### Version 1.0 — August 2026

> **Purpose:** Integrate and extend the user's existing research platforms into one coherent research ecosystem without rebuilding the mature platforms from scratch.

---

## 0. EXECUTIVE DIRECTIVE

This specification defines the umbrella layer around four existing systems:

- **MyoControl** — biosignal / motor-intent decoding
- **MyoAdapt** — cross-subject generalisation and domain-adaptation research infrastructure
- **BioSignal-FM V4** — multimodal biosignal representation and research framework
- **MyoSim V1.x** — software-only intent-to-physical-control simulation

The goal is NOT to merge these repositories into one monolith.

The goal is to build a **research ecosystem** that connects them through narrow, versioned contracts and adds a reusable research-infrastructure layer.

Canonical research story:

```text
BIOSIGNAL
   ↓
REPRESENTATION
   ↓
GENERALISATION
   ↓
MOTOR INTENT
   ↓
CONTROL
   ↓
PHYSICAL INTERACTION
```

Mapped to projects:

```text
MyoControl   → Decode
MyoAdapt     → Generalise
BioSignal-FM → Represent / Transfer / Multimodal
MyoSim       → Act / Simulate
```

The umbrella layer adds:

```text
Research Registry
Benchmarking
Experiment Provenance
Artifact Management
Cross-project Adapters
Reproducible Reports
Integrated Demonstrations
```

It must remain a **thin orchestration/infrastructure layer**, not a replacement for the four projects.

---

# 1. PRIMARY SCIENTIFIC QUESTION

The central research question for the overall program is:

> **How can biomedical AI decode human motor intent robustly across individuals without subject-specific calibration?**

Secondary questions:

1. How can biosignal representations generalise across unseen subjects?
2. When does conventional domain alignment fail, and why?
3. Can learned representations reduce subject-specific information while preserving motor-intent information?
4. Can the same representation principles transfer from EMG to EEG?
5. Can EEG and EMG provide complementary information for motor-intent decoding?
6. Can decoded intent translate into stable, safe, useful physical control?
7. How should biosignal research be benchmarked so that accuracy claims remain reproducible and meaningful?

The umbrella platform must support answering these questions rather than simply demonstrating software features.

---

# 2. CURRENT STATE — DO NOT REBUILD THE MATURE PLATFORMS

The following are existing artifacts and must be treated as the implementation baseline:

## 2.1 BioSignal-FM V4

Current state: **pre-publication release / ready for final publicization**.

Use it as the multimodal biosignal framework baseline.

Do not rebuild it from scratch.

Primary capabilities include:

- canonical signal contracts
- modality registry
- EMG / EEG / ECG support
- ECoG/iEEG experimental path
- preprocessing
- encoders
- representation learning
- fusion architecture
- task abstractions
- evaluation
- provenance / manifests
- research protocols

## 2.2 MyoSim V1.x

Current state: **ready / public-release preparation**.

Use it as the simulation/control baseline.

Do not rebuild it from scratch.

Primary capabilities include:

- intent replay
- confidence / temporal decision logic
- state machine
- controller abstraction
- safety layer
- MuJoCo primary backend
- robot model abstraction
- tasks and benchmarks
- deterministic replay
- provenance

## 2.3 MyoAdapt v2.x

Current state: **mature EMG adaptation research platform**.

Keep independent.

Do not merge wholesale into BioSignal-FM or the umbrella platform.

Relevant capabilities include:

- LOSO / LODO
- EMG preprocessing / representations
- MiniROCKET
- CORAL / TCA / Euclidean Alignment
- adversarial adaptation
- Lite-DAN
- calibration analysis
- drift / electrode-shift studies
- reproducibility
- ONNX / deployment paths

## 2.4 MyoControl

Current state: **mature research artifact associated with earlier EMG decoding work**.

Keep independent.

Use only through explicit adapters/contracts.

---

# 3. NON-NEGOTIABLE ARCHITECTURE PRINCIPLE

Do NOT create:

```text
MegaRepo/
    MyoControl/
    MyoAdapt/
    BioSignal-FM/
    MyoSim/
    shared-giant-framework/
```

where all projects become tightly coupled.

Instead:

```text
Existing repositories
        │
        │ versioned contracts
        ↓
Thin integration layer
        │
        ↓
Research Registry / Benchmark Engine
        │
        ├── experiments
        ├── artifacts
        ├── reports
        ├── integrated demos
        └── future commercial MVP
```

The repositories remain independently runnable.

The integration layer may depend on them through adapters, APIs, package interfaces, or exported artifacts — never by reaching into internal implementation details.

---

# 4. MASTER SYSTEM ARCHITECTURE

```text
                   ┌──────────────────────────────┐
                   │      RESEARCH REGISTRY      │
                   │ datasets / models / runs    │
                   │ protocols / artifacts       │
                   └──────────────┬───────────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ↓                ↓                ↓
          BioSignal-FM        MyoAdapt        MyoControl
                 │                │                │
                 └────────────────┼────────────────┘
                                  ↓
                         VERSIONED INTENT /
                         REPRESENTATION CONTRACTS
                                  │
                                  ↓
                               MyoSim
                                  │
                                  ↓
                       PHYSICAL TASK OUTCOMES
                                  │
                                  ↓
                       BENCHMARK / REPORT ENGINE
```

The Research Registry is the system of record for **experiments and artifacts**, not for raw datasets.

Raw research datasets remain external / local / licensed appropriately.

---

# 5. CORE UMBRELLA COMPONENTS

The new umbrella repository should contain only cross-project infrastructure.

Recommended name (working name):

`biosignal-research-platform`

or, if a better public name is selected later:

`human-motor-intelligence`

Do not finalize branding before technical scope is proven.

Core packages:

```text
src/
  research_core/
    contracts/
    registry/
    experiments/
    artifacts/
    provenance/
    protocols/
    benchmarks/
    reporting/
    adapters/
    orchestration/
    cli/
```

Optional later:

```text
ui/
dashboard/
api/
```

Do not build a dashboard until the underlying registry and reports are stable.

---

# 6. CONTRACT LAYER

The highest-value technical component is the contract layer.

It must define stable, versioned, minimal interfaces for:

## 6.1 Signal

Conceptual fields:

- data
- sampling_rate
- channel_names
- timestamps / time basis
- modality
- subject_id
- session_id
- task metadata
- annotations
- provenance

## 6.2 Representation

Conceptual fields:

- representation tensor/vector
- modality
- encoder/model identifier
- model version
- input provenance
- dimensionality
- timestamp/window mapping when applicable

## 6.3 Intent

Conceptual fields:

- label or intent vector
- confidence
- timestamp
- source model/version
- modality provenance
- subject/session provenance

## 6.4 Control Command

Conceptual fields:

- timestamp
- mode
- actuator/joint targets
- originating intent
- validity/provenance

## 6.5 Experiment

Minimum fields:

- experiment_id
- protocol_id
- dataset_id
- dataset_version
- modality
- subject split
- model
- model version
- seed
- configuration hash
- code commit
- environment
- metrics
- artifact references
- status

All contracts must be versioned.

Breaking changes require an explicit version bump.

---

# 7. RESEARCH REGISTRY

Build a lightweight registry, not a heavy distributed system.

The registry must answer:

> What experiment was run, on what data, under what protocol, with what model, producing which artifacts and metrics?

Core entities:

```text
Dataset
Protocol
Model
Experiment
Run
Artifact
Report
Benchmark
Project
```

Relationships:

```text
Dataset + Protocol + Model + Configuration
                    ↓
                 Run
                    ↓
        Metrics + Artifacts + Report
```

Store metadata in structured local files initially (JSON/YAML/SQLite where justified).

Do not introduce a large database unless scale requires it.

---

# 8. DATASET REGISTRY

The registry should support metadata for:

EMG:

- NinaPro DB2
- NinaPro DB3
- NinaPro DB7

EEG:

- BCI Competition IV-2a
- WAY-EEG-GAL

ECG:

- MIT-BIH
- other verified datasets later

ECoG/iEEG:

- future verified datasets

A dataset entry should record:

- name
- modality
- source
- citation
- license/access condition
- sampling rate
- channels
- task
- subjects
- sessions
- label schema
- canonicalization rules
- known limitations

Never embed copyrighted datasets into the repository.

---

# 9. PROTOCOL REGISTRY

A protocol is not merely a model configuration.

Examples:

```text
EMG-LOSO-v1
EEG-LOSO-v1
EEG-MI-v1
EMG-EEG-FUSION-v1
INTENT-TO-CONTROL-v1
```

Each protocol defines:

- split strategy
- train/validation/test semantics
- leakage constraints
- preprocessing
- feature selection
- model selection
- metrics
- statistical unit
- seeds
- hyperparameter policy

This is critical for the user's research because protocol drift was a major issue across earlier EMG work.

---

# 10. BENCHMARK ENGINE

The Benchmark Engine is the most important new feature after the contracts.

It must be able to compare:

- models
- representations
- preprocessing strategies
- adaptation strategies
- modalities
- fusion strategies
- control downstream utility

Example:

```text
Experiment family:
EMG_LOSO_DB7

Models:
XGBoost
MLP
Lite-DAN

Metrics:
accuracy
macro-F1
active-only-F1
rest-recall
```

Output:

- machine-readable table
- publication-ready table
- figure
- statistical comparison
- reproducibility manifest

Never build leaderboards without protocol identity.

---

# 11. STATISTICS

Statistics must operate at the correct unit of inference.

For LOSO research:

> **subject-level**, not window-level, inference.

Support where appropriate:

- Friedman
- Wilcoxon signed-rank
- Holm correction
- effect size
- confidence intervals
- paired comparisons

Do not automatically run every statistical test.

Use the protocol to decide what is valid.

---

# 12. PAPER ASSET GENERATOR

One of the most valuable umbrella capabilities:

Experiment results should produce publication assets automatically.

Example:

```text
Run
 ↓
Aggregate
 ↓
Statistical analysis
 ↓
Table
 ↓
Figure
 ↓
Caption draft
 ↓
Experiment report
```

Generate:

- CSV
- JSON
- Markdown
- LaTeX table
- PNG/SVG/PDF figures where appropriate
- reproducibility manifest

Never generate scientific prose that invents interpretation.

The tool may generate factual summaries from measured outputs, but human review remains mandatory.

---

# 13. PAPER 3 INTEGRATION

Paper 3 is currently in execution lock.

Do not modify its protocol.

The umbrella benchmark engine may later ingest Paper 3 results.

Current Paper 3 protocol remains:

- strict LOSO
- zero calibration
- no target labels
- no target-unlabelled exposure in headline
- training-only scaling
- training-only SelectKBest
- 618 → 308 features
- 41 classes
- source subject IDs as adversarial domains

Do NOT move Paper 3 into the umbrella repository.

Only import its exported experiment manifests/results when available.

---

# 14. EEG RESEARCH TRACK

This is the primary new scientific expansion.

The first target:

**BCI Competition IV-2a**

Pipeline:

```text
BCI IV-2a
   ↓
canonical EEG Signal
   ↓
MNE-based preprocessing adapter
   ↓
epoch/window definition
   ↓
strong baselines
   ↓
strict subject-aware evaluation
   ↓
representation learning
   ↓
analysis
```

Second target:

WAY-EEG-GAL

The goal is NOT immediately to publish.

The goal is to establish a reusable, rigorous EEG research pipeline.

---

# 15. EEG BASELINES

Do not start with a giant transformer.

The initial benchmark should include strong simple baselines.

Possible sequence:

- linear baseline
- LDA where scientifically appropriate
- classical spectral/time-frequency baseline
- lightweight CNN/TCN
- lightweight transformer only when justified
- domain-generalisation baseline

The benchmark must reveal whether more complex models genuinely add value.

---

# 16. EMG → EEG RESEARCH BRIDGE

After the EEG baseline exists, build a cross-modal research study layer.

Question:

> Can representation-learning principles developed for cross-subject EMG generalisation transfer to EEG motor decoding?

Do NOT claim transfer before testing it.

Potential experiments:

```text
EMG pretrained representation
        ↓
    transfer?
        ↓
EEG downstream task
```

and:

```text
EEG pretrained representation
        ↓
    transfer?
        ↓
EMG downstream task
```

These are future experiments, not immediate requirements.

---

# 17. EEG–EMG FUSION TRACK

Future multimodal study:

```text
EEG → encoder ─┐
               ├→ fusion → task
EMG → encoder ─┘
```

Test:

- EEG only
- EMG only
- EEG + EMG
- missing EEG
- missing EMG

Metrics should include both task performance and robustness under modality loss.

This is a likely future paper.

---

# 18. MYOSIM INTEGRATION

MyoSim remains independent.

The umbrella platform creates an adapter:

```text
Intent Contract
    ↓
MyoSim Adapter
    ↓
MyoSim
```

The first integration should NOT require live hardware.

Start with:

```text
replayed intent
    ↓
MyoSim
    ↓
virtual prosthesis
```

Then:

```text
BioSignal-FM / MyoControl output
    ↓
adapter
    ↓
MyoSim
```

The adapter must remain thin.

---

# 19. DIGITAL-TWIN / END-TO-END DEMONSTRATOR

Build one integrated demonstrator.

Preferred flow:

```text
EMG / replayed intent
        ↓
MyoControl or compatible decoder
        ↓
Intent Contract
        ↓
MyoSim
        ↓
Virtual Prosthetic Hand
        ↓
Task
        ↓
Outcome metrics
```

Later:

```text
EEG decoder
        ↓
Intent Contract
        ↓
MyoSim
```

The demonstrator must be deterministic and replayable.

The purpose is scientific communication and downstream utility, not marketing.

---

# 20. CONTROL UTILITY METRICS

This is a high-value research opportunity.

Do not evaluate a decoder only with classification accuracy.

Compare decoder outputs using:

- task success rate
- command latency
- false activations
- command stability
- trajectory smoothness
- completion time
- failure rate

This allows a future research question:

> Does better signal decoding necessarily produce better physical control?

This may become a strong paper direction.

---

# 21. COMMERCIAL MVP — RESEARCH OPERATING SYSTEM

If the research infrastructure is mature enough, create a lightweight professional MVP.

Working concept:

> Biosignal Research OS

Do not build it as a generic SaaS.

Core user:

- graduate student
- biosignal researcher
- biomedical AI lab
- neuroengineering lab

Core workflow:

```text
Dataset
  ↓
Protocol
  ↓
Model
  ↓
Run
  ↓
Metrics
  ↓
Statistics
  ↓
Figures / Tables / Report
```

Potential features:

- experiment registry
- reproducible configurations
- benchmark comparison
- paper asset export
- model cards
- dataset cards
- run manifests
- team notes
- artifact storage

Do NOT implement yet:

- billing
- SaaS accounts
- payment
- cloud infrastructure
- multi-tenant architecture
- telemetry

First prove that researchers actually want the workflow.

---

# 22. COMMERCIALIZATION STRATEGY

The product should be positioned eventually as:

> Reproducible experiment infrastructure for biosignal and biomedical AI research.

Potential business models later:

- hosted research workspace
- lab/team licenses
- enterprise/private deployment
- benchmark services
- premium collaboration
- managed compute
- consulting / custom research infrastructure

Do not implement pricing or billing in this sprint.

---

# 23. PUBLIC RESEARCH SHOWCASE

Build a showcase layer only after the underlying experiments are stable.

Show:

- architecture
- benchmark
- demo
- reproducibility manifest
- paper relationship
- limitations

Avoid:

- fake leaderboards
- unsupported “state of the art” claims
- fake users
- fake productivity claims

---

# 24. ROADMAP

## PHASE A — INTEGRATION FOUNDATION

1. Audit all four repositories at the contract level.
2. Define versioned cross-project contracts.
3. Build adapters.
4. Build Research Registry skeleton.
5. Verify no repository becomes tightly coupled to another.

Acceptance:

- existing projects still run independently
- adapters pass contract tests
- registry records a test run

---

## PHASE B — BENCHMARK / EXPERIMENT ENGINE

1. Protocol registry
2. Dataset registry
3. Run manifests
4. artifact references
5. metrics aggregation
6. statistical analysis
7. report generation

Acceptance:

- one complete EMG benchmark run
- reproducible manifest
- figure/table export

---

## PHASE C — MYOSIM INTEGRATION

1. Intent adapter
2. replay integration
3. end-to-end signal/intent → simulator flow
4. control utility metrics
5. deterministic demo

Acceptance:

```text
Intent → MyoSim → Task → Metrics
```

reproducibly.

---

## PHASE D — EEG FOUNDATION PIPELINE

1. BCI IV-2a adapter
2. canonical EEG contract validation
3. preprocessing
4. baselines
5. subject-aware evaluation
6. experiment registry integration
7. report generation

Acceptance:

- one complete reproducible EEG benchmark
- publication-ready results table

---

## PHASE E — MULTIMODAL RESEARCH PREPARATION

1. EEG encoder integration
2. EMG encoder integration
3. fusion interface
4. missing-modality evaluation protocol
5. EEG–EMG benchmark scaffold

No paper claims yet.

---

## PHASE F — DIGITAL-TWIN DEMONSTRATOR

1. decoder adapter
2. intent contract
3. MyoSim integration
4. visual demonstration
5. metrics
6. reproducibility bundle

Acceptance:

A third party can reproduce the demo from the repository and manifest.

---

## PHASE G — RESEARCH OS MVP

Only if Phases A–F are stable.

1. researcher-oriented CLI/UI
2. run comparison
3. protocol selection
4. artifact browsing
5. paper asset export
6. documentation

Do not add cloud infrastructure yet.

---

# 25. SEVEN-DAY UNLIMITED-AGENT SPRINT

The agent has an unusual temporary unlimited-credit window.

Use it for breadth with strict scope control.

Recommended order:

### DAY 1
Full audit + contracts + integration architecture.

### DAY 2
Research Registry + Protocol Registry + Dataset Registry.

### DAY 3
Benchmark engine + reproducible run manifests + report generator.

### DAY 4
MyoSim adapter + deterministic end-to-end demo.

### DAY 5
BCI IV-2a EEG research pipeline.

### DAY 6
EEG–EMG fusion scaffold + missing-modality protocol + integrated documentation.

### DAY 7
Research OS MVP polish + end-to-end validation + demo + documentation.

This is a target schedule, not a promise of completion time.

The agent must stop or defer work when acceptance criteria are met instead of inventing scope.

---

# 26. EXECUTION PRINCIPLES FOR THE AGENT

You are an integration engineer, not a greenfield rewriter.

Rules:

1. Do not rebuild BioSignal-FM.
2. Do not rebuild MyoSim.
3. Do not rewrite MyoAdapt.
4. Do not rewrite MyoControl.
5. Build thin adapters.
6. Keep repositories independently runnable.
7. Prefer contracts over shared internal imports.
8. Prefer provenance over convenience.
9. Prefer reproducibility over flashy UI.
10. Prefer measurable research utility over feature count.
11. Do not claim scientific validation without evidence.
12. Do not fabricate results.
13. Do not silently alter Paper 3 protocol.
14. Do not introduce cloud/commercial infrastructure prematurely.
15. Do not add a feature unless it supports a defined research or product use case.

---

# 27. QUALITY GATES

Each phase must pass:

### Scientific
- protocol is explicit
- no leakage
- metrics appropriate
- claims supported

### Engineering
- typed interfaces
- tests
- clean dependency direction
- documentation
- reproducible config

### Integration
- existing projects still work
- adapters are thin
- no hidden coupling

### Product
- workflow understandable
- no unnecessary UI
- user value is explicit

### Commercial / IP
- license compatibility checked
- no proprietary data committed
- no secrets
- no unsubstantiated commercial claims

---

# 28. TESTING STRATEGY

The umbrella layer must include:

- contract tests
- adapter tests
- integration tests
- reproducibility tests
- benchmark tests
- report-generation tests
- schema/version tests

The umbrella layer must NOT duplicate the full unit-test suites of the child repositories.

---

# 29. OBSERVABILITY

Every orchestration run must expose:

- run ID
- stage
- project
- model
- dataset
- protocol
- status
- error
- duration
- artifact references

Structured logging is required.

---

# 30. SECURITY / DATA GOVERNANCE

Rules:

- no raw clinical/private data in Git
- no credentials
- no hidden uploads
- local-first defaults
- dataset licenses recorded
- provenance preserved
- clear separation of public code and private data

---

# 31. DOCUMENTATION DELIVERABLES

Create:

```text
README.md
ARCHITECTURE.md
CONTRACTS.md
INTEGRATION_GUIDE.md
RESEARCH_PROTOCOLS.md
BENCHMARK_GUIDE.md
REPRODUCIBILITY.md
ROADMAP.md
COMMERCIALIZATION_NOTES.md
```

Do not generate fictional case studies.

---

# 32. FINAL DEMONSTRATION

The final sprint should produce one concise demonstration:

```text
Biosignal / Intent
      ↓
Research contract
      ↓
Decoder
      ↓
MyoSim
      ↓
Virtual Prosthetic Task
      ↓
Metrics
      ↓
Reproducible Report
```

The demo should be explainable in under two minutes.

---

# 33. FINAL SUCCESS CRITERIA

The overall system succeeds when:

1. Existing projects remain independently functional.
2. They can exchange data through versioned contracts.
3. Experiments can be registered and reproduced.
4. EMG and EEG can use the same research infrastructure.
5. A benchmark can generate publication-ready artifacts.
6. A decoder output can reach MyoSim through an adapter.
7. The complete demo is deterministic and replayable.
8. The architecture can later support ECoG/iEEG and multimodal fusion.
9. The system can plausibly become a professional research product.
10. No scientific claim exceeds the available evidence.

---

# 34. FINAL ROLE OF THE AGENT

The agent may implement the entire scope end-to-end during the temporary unlimited-credit window.

However, it must use this sequence:

AUDIT
→ CONTRACTS
→ REGISTRIES
→ ADAPTERS
→ BENCHMARK ENGINE
→ MYOSIM INTEGRATION
→ EEG TRACK
→ MULTIMODAL PREPARATION
→ DIGITAL TWIN DEMO
→ RESEARCH OS MVP
→ FINAL AUDIT

The agent should keep a live:

`IMPLEMENTATION_STATUS.md`

and finish with:

`FINAL_PROJECT_REPORT.md`

containing:

- what was implemented
- what was reused
- what was adapted
- what was not changed
- all repositories touched
- architecture map
- contract versions
- tests
- benchmarks
- demos
- limitations
- future work
- unresolved issues

---

# 35. FINAL NON-NEGOTIABLE PRINCIPLE

This project is not about creating the maximum number of repositories.

It is about creating the maximum amount of **research leverage** from the repositories that already exist.

Do not build another MyoControl.
Do not build another MyoAdapt.
Do not build another BioSignal-FM.
Do not build another MyoSim.

Build the connective tissue that makes them a coherent research and product ecosystem.

The ultimate narrative is:

```text
BIOSIGNAL
   ↓
REPRESENTATION
   ↓
GENERALISATION
   ↓
MOTOR INTENT
   ↓
CONTROL
   ↓
PHYSICAL ACTION
   ↓
MEASURABLE OUTCOME
```

And the central question remains:

> **How can biomedical AI decode human motor intent robustly across individuals without subject-specific calibration?**
```
