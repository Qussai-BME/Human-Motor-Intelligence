> **Current P6 state (2026-10-11): C1 (registered replay, 0/60), its post-hoc audit (endpoint unreachable by design) and the C2 registered follow-up are complete. See `P6_FINAL_STATUS.md` and `papers/P6_SUPERSESSION_NOTICE.md`.**

# Human Motor Intelligence — Public Release 1.2.0

**Release date:** 2026-10-11  
**Author:** Qussai Adlbi

This release supersedes the earlier interim-state narrative. Superseded materials remain under `historical/` rather than competing with the current status.

## Included evidence

| Area | Current disposition |
|---|---|
| Programme integration | Released infrastructure: contracts, registry, provenance, adapters, benchmark/report surfaces, CLI. |
| P1-P3 | Preserved with their documented source/evidence boundaries. |
| P4 | External OpenBMI validation package with protocol-specific interpretation. |
| P5 | External Jeong2020 amended fusion package with protocol-specific interpretation. |
| P6 R2 | MyoSim systems/integration evidence retained separately. |
| P6 R03 | Real-data exploratory motor-execution EEG-to-MyoSim evidence: 60 traces, 60 primary task artefacts, paired statistics. |

## P6 disposition

P6 is reported as C1 (registered motor-imagery replay), a post-hoc audit of C1, and the C2 registered follow-up.

- **C1:** R04 motor imagery, S001–S020, strict LOSO, fixture 1/1, 60 + 60 runs, task success 0/60; decoders at chance. T1/T2 → OPEN/CLOSE is an abstract software mapping.
- **Audit:** the C1 endpoint was unreachable by design (oracle 0/20; 2 of 15 outputs inside the 8.0-s task window; 171/207 controller transitions after failure). The exploratory command-correction contrast is withdrawn.
- **C2:** episode-level interface (oracle 100/100), emulated ladder (27,000), real decoders on 105 subjects (19,750), sensitivity (25,600). Control success follows confidence-gate passage (ρ = 0.95) rather than accuracy (ρ = 0.24); above a chance-matched floor, zero-calibration decoders gain at most 0.4 percentage points at the registered gate.

R03 remains an engineering/preflight motor-execution baseline only.

## Publication discipline

Describe P6 as an audited, registered, non-clinical simulation study of how decoder confidence and accuracy relate to control success in a confidence-gated controller. Do not describe it as clinical validation, online-BCI evaluation or a universal law relating decoder quality to control utility.
