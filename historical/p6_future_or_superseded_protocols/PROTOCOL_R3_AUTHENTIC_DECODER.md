> **HISTORICAL / SUPERSEDED RECORD:** This document records an earlier pre-reopening state. It is retained for provenance only. Current P6 disposition is documented in `P6_FINAL_STATUS.md` and `closure/10_FINAL_CLOSURE_REPORT.md`.

# P6 R3 Authentic Decoder Protocol — Pre-execution Register

**Status:** REGISTERED AS A GATED PROTOCOL TEMPLATE; CONFIRMATORY EXECUTION NOT AUTHORISED.

## Question
Does measured variation in authentic, cross-subject decoder output quality translate into variation in downstream MyoSim task/control performance?

## Required evidence before execution

1. At least one identifiable frozen decoder/checkpoint and compatible source input set.
2. Timestamped output traces with source subject/fold/session, class mapping, confidence semantics, preprocessing, latency, and checksums.
3. Permission to use source data/model outputs for local replay and public release of derived metadata.
4. Three or more quality values or a justified multi-variant design established independently of downstream task outcomes.
5. Trace gates A–D passed and an immutable trace manifest produced.

## Locked analysis intent

The primary unit must be the independent trace/held-out source unit, not repeated seeds treated as human subjects. The primary endpoint must be declared before confirmatory runs and should be task success or a predeclared control-performance measure. Secondary endpoints may include completion time, invalid commands, timeout/failure state, and trajectory/error metrics. Repeated initial states are repeated simulations, not independent people.

Quality strata must be assigned using a decoder-quality metric defined before examining task outcomes. Source-subject identity, class distribution, and trace length must be recorded as potential confounders. The phrase “dose-response” is prohibited unless a measured quality range and justified model support it.

## Exclusions and stopping

- Exclude only malformed or technically invalid traces under predeclared rules, retaining them in the audit log.
- Stop before confirmatory inference if provenance, compatibility, or reproducibility gates fail.
- Do not create artificial worst/mid/best traces by editing labels, confidence, timing, or error rates.

## Statistical plan to be completed after trace acceptance

Select a paired or hierarchical analysis appropriate to the number of independent traces and repeated simulation states; report effect sizes, uncertainty, missing/failed runs, and multiplicity correction. A power/precision assessment must be based on accepted trace-level evidence before the number of confirmatory runs is finalised.

**Current scientific disposition:** inconclusive about decoder-quality-to-control utility because the prerequisite authentic trace contrast is unavailable, not because a nonsignificant decoder-quality experiment was observed.
