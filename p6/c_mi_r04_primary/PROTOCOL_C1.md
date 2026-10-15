# P6 Protocol C1 — Motor-Imagery EEG → Control-Utility Trace

**Status:** registered implementation; scientific execution complete external R04 EDF acquisition and compatible MyoSim runtime.

## Purpose

P6 asks whether differences in a frozen, subject-independent EEG decoder family survive translation into downstream simulated control utility.

## Design

- Dataset: PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0.
- Primary run: **R04**, unilateral left/right fist **motor imagery**.
- Subjects: S001–S020.
- Evaluation: strict leave-one-subject-out (LOSO), no target-subject calibration/exposure.
- Models: M1, M2, M3, preserving the same feature families and hyperparameters used by the retained R03 engineering baseline.
- Trial window: 1.0–3.5 s after source event onset, unchanged from the retained R03 implementation.
- Quality ordering: frozen from source-training cross-validation only, before any MyoSim task analysis.
- Control interface: T1/T2 are mapped to two **abstract control labels** through a fixed, registered mapping. The mapping is not presented as a physiological equivalence between left/right fist imagery and prosthetic open/close actions.
- Primary downstream unit: subject × model run.
- Trial/event predictions are not treated as independent observations for between-model inference.

## Mandatory gates

1. **Dataset-semantic gate:** every input file must be R04 and every T1/T2 event must be interpreted under the R04 unilateral-fist imagery protocol.
2. **Decoder-freeze gate:** quality ordering must be produced and persisted before any task outcomes are inspected.
3. **Control-fixture gate:** a model-independent, valid intent-control sequence must complete the declared MyoSim task before decoder-conditioned outcomes are interpreted.
4. **Run-level provenance gate:** every decoder trace and every MyoSim run receives an external SHA-256 identity and complete source/configuration provenance.
5. **Replay gate:** a complete rerun must preserve all 60 decoder traces and all 60 MyoSim per-run JSON artifacts.
6. **Statistical gate:** inference is paired at the subject level; trial-level observations are descriptive only unless an explicitly justified hierarchical model is registered.

## Interpretation rule

The study may support a statement about decoder-quality differences translating into downstream utility only if the control fixture is valid and the primary task endpoint is capable of discriminating model conditions. If all conditions fail the task, the endpoint becomes non-discriminative and secondary continuous metrics are the appropriate exploratory evidence.
