# Public Review Disclosure — Human Motor Intelligence 1.2.0

This document is the reviewer-facing scope statement for the current public release.

| Area | Reviewer may conclude | Reviewer must not conclude |
|---|---|---|
| Architecture | The umbrella integration layer, contracts, registry, provenance, adapters, and benchmark/report tooling are present. | Child projects were merged or silently reimplemented. |
| P4 | The registered OpenBMI external validation and its rerun/evidence records are preserved. | It is a direct replication of unrelated datasets or a universal EEG claim. |
| P5 | The amended Jeong2020 cohort comparison found no Holm-supported fusion gain under the tested rules. | Multimodal fusion never helps or a causal mechanism was proved. |
| P6 | A registered offline EEGMMIDB-to-MyoSim study (C1), its post-hoc audit and a registered follow-up (C2) are present; control success in the confidence-gated controller follows gate passing rather than decoder accuracy. The retained R03 motor-execution record is engineering baseline only. | It is clinical validation, prosthetic validation, online human control, or proof of a general decoder-quality law; R03 is motor imagery. |

## P6 audit facts

**C1** (R04 motor imagery, S001–S020, strict LOSO, frozen quality order, validated fixture): 60 primary and 60 rerun MyoSim run artefacts, task success 0/60 in both passes; decoders at chance. A post-hoc audit (`p6/c1_audit`) shows the endpoint was unreachable by design (oracle 0/20; 2 of 15 outputs inside the task window; executing commands endable only via REST; 171/207 controller transitions after failure); the exploratory command-correction contrast is withdrawn.

**C2** (`p6/c2_episode`, protocol frozen before outcomes): episode-level interface validated by an oracle (100/100) and a C1-format regression control (0/100); emulated ladder (27,000 episodes), real decoders on 105 subjects (19,750 episodes), sensitivity (25,600). Verified independently (300 re-run episodes, 0 mismatches; statistics recomputed). Real zero-calibration decoders gain at most 0.4 percentage points above a chance-matched floor at the registered gate.

R03 is motor execution, retained as engineering/preflight evidence only; its T1/T2 → OPEN/CLOSE mapping is abstract.

## Public claim discipline

The archive is a complete evidence-governed public release and P6 is scientifically complete as C1 + audit + C2 within the stated limits (`SCIENTIFIC_LIMITATIONS.md`). No documentation change can convert motor-execution recordings into motor-imagery evidence, or offline simulator results into clinical evidence.
