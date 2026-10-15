# Final Project Report — Human Motor Intelligence Public Release 1.1.0

**Author:** Qussai Adlbi  
**Report date:** 2026-10-05

Canonical P6 report: `papers/paper_6/P6_C1_MANUSCRIPT.md`

## Executive summary

Human Motor Intelligence is released as a thin research-integration and evidence-governance layer around a six-paper programme. The release preserves child-project boundaries and makes provenance, protocols, retained outputs, limitations, and reproducibility status inspectable.

The current package is technically and scientifically release-ready within its declared scope. P1 is a submitted/frozen record; P2 was revised after supervisor review (manuscript v2; corrected archive v2.0.0 supersedes v1.0.0); P3 is preserved as qualified external evidence; P4 and P5 have their registered external-validation records; P6 C1 is complete with a non-discriminative downstream task-success endpoint. The retained R03 stream is engineering baseline evidence only.

## P6 C1 current status

C1 is the active P6 scientific study. It uses EEGMMIDB R04 motor imagery, strict S001–S020 LOSO evaluation, the frozen M1/M2/M3 decoder family, an abstract registered control mapping, a mandatory model-independent MyoSim fixture gate, run-level provenance, and a full rerun requirement. The code and protocol are complete; no C1 numerical result is inserted before real execution.

## P6 retained engineering evidence

R03 (motor execution) is retained only as an engineering/preflight baseline.

## P6 current evidence

**C1.** Three models (M1/M2/M3) in strict LOSO on R04 motor-imagery data from 20 subjects; quality order frozen from source-CV; fixture 1/1; 60 primary and 60 rerun MyoSim runs; task success 0/60; decoders at chance (pooled accuracy 0.497–0.510).

**Audit.** The C1 success endpoint was unreachable by design: oracle 0/20; 2 of 15 outputs inside the 8.0-s task window; an executing command can end only via REST; 171/207 controller transitions after failure. The exploratory command-correction contrast is withdrawn.

**C2.** Episode-level replay with cue-correct endpoint (oracle 100/100). Emulated ladder (27,000 episodes): slope 14.8 per unit accuracy; over-confident chance-level floor 23.0%; calibration crossover near q = 0.8. Real decoders (105 subjects; 19,750 episodes): success tracks confidence-gate passage (ρ = 0.95), not accuracy (ρ = 0.24); at the registered gate zero-calibration decoders gain at most 0.4 percentage points above a chance-matched floor.

## Interpretation

P6 should be read as an audited study showing that, in a confidence-gated controller, success rates confound accuracy with confidence behaviour; they must be reported against oracle ceilings and chance-matched floors. It must not be generalised to clinical control, prostheses, online users or a universal relationship between decoder quality and downstream utility.

## Engineering release status

Canonical release manifest, deterministic current filenames, citation metadata, portable runners (environment variables, no workstation paths), optional-dependency-aware tests (44 pass, 2 optional skipped without MyoSim), raw C2 archives with SHA-256, and explicit data/dependency boundaries. Superseded snapshots remain in `historical/`.
