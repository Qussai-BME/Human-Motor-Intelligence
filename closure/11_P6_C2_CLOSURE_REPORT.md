# Closure Report — P6 C1 audit and C2 follow-up (2026-10-11)

## Scope
Records the post-hoc audit of C1 and the execution, verification and release of the registered follow-up C2 (`P6-C2-EPISODE-v1.0`).

## Audit of C1
Endpoint unreachable by design (oracle 0/20; 2 of 15 outputs inside the 8.0-s task window; executing commands endable only via REST; 171/207 controller transitions after failure). Exploratory command-correction contrast withdrawn. Archived C1 results unchanged. Reproducible from `p6/c1_audit`.

## C2 execution
Protocol frozen 2026-10-07 23:46 UTC (hash manifest; controller configuration byte-identical to C1). Pre-flight passed (oracle 100/100; X0 0/100; calibrated chance 0/100; truth table 16/16; determinism). Episodes: emulator 27,000; sensitivity 25,600; R0 560; R1 19,750 (105 subjects; S088, S092, S100, S104 excluded by the integrity check). One documented deviation: the D5 episode builder was corrected before any D5 outcome entered the analysis (`results/WP5_D5_REPLAY_CORRECTION.json`).

## Independent verification
Protocol/config hashes match; 300 sampled episodes re-run through MyoSim with 0 mismatches; all confirmatory statistics recomputed (identical); emulator agrees with the closed form (max |z| = 1.08); the analysis re-run reproduces `ANALYSIS.json`.

## Corrections to the agent’s original report
H-R1 is formally supported but confidence-driven (gate-pass ρ = 0.95 vs accuracy ρ = 0.24); D1–D3 raw are calibrated but unconfident, D4/D5 raw over-confident; q_eq is interpretable only for D3 and D4; task completion overstates success; D5 is unpaired (735 episodes); replay confidences are rounded to three decimals.

## Disposition
P6 is scientifically complete as C1 + audit + C2. Remaining open items (not required for release): a stronger decoder (balanced accuracy ≥ 0.70), a second dataset, a real-confidence-resampling emulator, asynchronous/decoded-rest operation.
