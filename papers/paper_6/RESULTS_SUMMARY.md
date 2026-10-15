# P6 Results Summary (C1, audit, C2)

Source of truth: `p6/c_mi_r04_primary/results/` (C1), `p6/c1_audit/outputs/` (audit), `p6/c2_episode/results/` and `p6/c2_episode/posthoc/outputs/` (C2). Manuscript text: not distributed in this archive.

## Stage 1 — C1 (registered, `P6-C1-MI-R04-v1.0`)
- R04 motor imagery, S001–S020, strict LOSO, M1/M2/M3 (quality order M1 > M3 > M2 frozen from source-CV: 0.505, 0.466, 0.465).
- Fixture 1/1. **Task success 0/60 (0/20 per model) in the primary run and the rerun**; exact 95% upper bound 6.0% pooled.
- Decoders at chance: pooled accuracy 0.510, 0.497, 0.507 (binomial p 0.77, 0.95, 0.86); Friedman p = 0.65; no subject reached 12/15.

## Stage 2 — audit (post-hoc, descriptive)
- D1 re-execution of the 60 archived runs: bit-identical.
- D2 oracle (true labels, confidence 1.0): **0/20**.
- D3 timeline: every run ended by task timeout at 12.3–12.5 s after 2 of 15 outputs; 840/840 inter-event gaps exceed the 8.0-s clock; 171/207 controller transitions and 64/64 command corrections followed task failure.
- S1 timeout removed: 0/60 decoders, 0/20 oracle (the engine can end an executing command only through an explicit REST).
- The C1 command-correction contrast (Friedman p = 0.0005) is **withdrawn** (artefact; tracks confidence, ρ = 0.51, not accuracy, ρ = −0.03).

## Stage 3 — C2 (registered, `P6-C2-EPISODE-v1.0`)
- Interface: 7.0-s episodes at 0.1-s windows (decoy trial OPEN, grasp trial CLOSE, scheduled REST); endpoint cue-correct success. Pre-flight: oracle 100/100, calibrated chance 0/100, C1-format oracle 0/100, truth table 16/16, determinism 20/20.
- Emulator (54 cells × 500): H-E1 logit slope 14.80 per unit accuracy (95% CI 13.95–15.64); H-E2 ceiling 500/500, calibrated chance 0/500, over-confident chance **115/500 = 23.0%** (19.4–26.9%); H-E3 calibration crossover near q = 0.8 (risk differences over-confident − calibrated +26.4, +16.6, +0.4 points at q = 0.6, 0.7, 0.8; −10.4 at 0.9); H-E4 success rises as persistence falls at q ≥ 0.8 (Holm p = 0.020 and 3 × 10⁻⁹).
- Real decoders (105 subjects, 4,725 epochs; D5 within-subject reference on run R12):

| Variant | BA | ECE | Gate-pass | Cue-correct (k/n) | False grasp | Above chance-matched floor, pp [95% CI] |
|---|---|---|---|---|---|---|
| D1 plt | 0.543 | 0.006 | 0.2% | 0.0% (0/2285) | 0.0% | -0.0 [-0.1, +0.0] |
| D1 | 0.543 | 0.030 | 1.8% | 0.8% (19/2285) | 0.3% | +0.3 [+0.0, +0.6] |
| D2 plt | 0.530 | 0.003 | 0.0% | 0.0% (0/2285) | 0.0% | +0.0 [+0.0, +0.0] |
| D2 | 0.530 | 0.062 | 3.2% | 2.1% (47/2285) | 1.2% | +0.4 [+0.0, +0.8] |
| D3 plt | 0.599 | 0.053 | 1.0% | 0.0% (0/2285) | 1.0% | -1.0 [-2.8, +0.0] |
| D3 | 0.596 | 0.022 | 3.9% | 1.9% (44/2285) | 1.3% | -0.2 [-2.3, +1.3] |
| D4 plt | 0.531 | 0.023 | 0.0% | 0.0% (0/2285) | 0.0% | +0.0 [+0.0, +0.0] |
| D4 | 0.532 | 0.438 | 94.7% | 22.9% (524/2285) | 42.2% | -1.9 [-4.3, +0.5] |
| D5 plt | 0.565 | 0.044 | 14.7% | 11.2% (82/735) | 2.7% | +3.8 [+1.1, +6.7] |
| D5 raw | 0.609 | 0.301 | 84.3% | 30.7% (226/735) | 35.8% | +5.9 [+1.1, +11.2] |

- Across the 10 variants success tracked the share of events passing the 0.75 gate (Spearman ρ = 0.95, p = 3 × 10⁻⁵) and not balanced accuracy (ρ = 0.24, p = 0.50); variants are not independent, so these are descriptive.
- At a relaxed gate of 0.55 the best zero-calibration decoder (D3 raw) gained +4.0 points above its floor (95% CI +0.2 to +8.1); chance-level decoders also gain success when the gate is lowered.

Interpretation: success in a confidence-gated controller measures gate passage as much as accuracy; success rates must be reported against a chance-matched floor and an oracle ceiling. Non-clinical, offline, simulation-only.
