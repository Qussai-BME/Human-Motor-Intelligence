# P6 Final Status

**Status: SCIENTIFICALLY COMPLETE (C1 registered replay, post-hoc audit, C2 registered follow-up).**

## C1 (registered replay, protocol `P6-C1-MI-R04-v1.0`)
PhysioNet EEGMMIDB R04 unilateral fist motor imagery, S001–S020, strict LOSO, frozen M1/M2/M3 quality order, fixed abstract T1/T2 → OPEN/CLOSE mapping, model-independent MyoSim fixture (1/1), 60 primary and 60 rerun runs. Decoder-conditioned task success was **0/60** in both passes; the registered primary endpoint is non-discriminative. The C1 decoders were at chance (pooled accuracy 0.497–0.510; all p ≥ 0.77).

## Audit of C1 (post-hoc, `p6/c1_audit`)
The audit shows that the C1 endpoint could not be reached by any decoder: an oracle stream (true labels, confidence 1.0) also scored 0/20; the 8.0-s task clock ended after 2 of 15 decoder outputs; the decision engine needs at least four consecutive confident same-label windows and can end an executing command only through an explicit rest event; 171 of 207 controller transitions followed task failure. The exploratory command-correction contrast (Friedman p = 0.0005) arose entirely after task termination and tracked decoder confidence; **that interpretation is withdrawn**. C1 results are retained unchanged as the archived record.

## C2 (registered follow-up, protocol `P6-C2-EPISODE-v1.0`, frozen 2026-10-07 23:46 UTC)
An episode-level interface with cue-locked REST and a cue-correct endpoint (oracle 100/100; C1-format oracle 0/100); an emulated decoder ladder (54 cells × 500); real decoders D1–D5 on 105 subjects (4,725 epochs; 19,750 episodes); controller-parameter sensitivity (25,600 episodes). Principal findings: success rises steeply with emulated accuracy (logit slope 14.8 per unit accuracy), but an over-confident chance-level decoder succeeds in 23.0% of episodes; calibrated decoders overtake over-confident ones only above an accuracy of about 0.8; real zero-calibration decoders (balanced accuracy 0.53–0.60) obtained success (0.8–22.9% raw, 0% Platt-scaled) in proportion to gate passage (Spearman ρ = 0.95) and not accuracy (ρ = 0.24); above a chance-matched floor their benefit was at most 0.4 percentage points at the registered gate.

## Retained baselines and boundaries
R03 remains an engineering/preflight motor-execution baseline only. Raw EEG is not redistributed. A fresh end-to-end rerun requires external retrieval of EEGMMIDB and a compatible MyoSim/MuJoCo environment (see `p6/c2_episode/README.md`). All results are non-clinical, offline, simulation-only.
