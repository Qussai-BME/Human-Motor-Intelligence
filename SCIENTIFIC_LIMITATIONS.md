# Scientific Limitations — Human Motor Intelligence 1.2.0

These limits apply to P6 (C1, the post-hoc audit and C2). Limits of P1–P5 are in their paper-level records.

## Scope
Offline replay in a deterministic software simulator (MyoSim v0.1.5, MuJoCo) with public healthy-subject EEG (PhysioNet EEGMMIDB). Nothing here establishes online BCI performance, user benefit, hardware safety, prosthetic readiness or clinical efficacy.

## C1
- The registered success endpoint was degenerate (0/60) and, by the audit, unreachable: an oracle stream also failed (0/20), the task clock ended after 2 of 15 outputs, and 171/207 controller transitions followed task failure. C1 therefore says nothing about decoder quality.
- The C1 decoders were at chance (pooled accuracy 0.497–0.510), so the registered quality manipulation did not materialise.
- The exploratory command-correction contrast is **withdrawn**: it arose after task termination and tracks decoder confidence.
- T1/T2 → OPEN/CLOSE is an abstract software mapping, not a physiological or prosthetic semantic validation.

## C2
- REST events are scheduled (synchronous paradigm) and decoder outputs are held across each trial (sample-and-hold); asynchronous operation and sliding-window decoders are outside the confirmatory scope.
- Physics is deterministic: outcomes are determined by label and confidence sequences, i.e. controller-level utility only.
- The emulator assumes Beta-shaped confidence and independent trials and is optimistic relative to real decoders (e.g. D3: success 1.9% versus about 6% for the calibrated emulator at q = 0.6). Accuracies above 0.65 are covered only by emulation: no real decoder exceeded a balanced accuracy of 0.61.
- Real decoders are linear/covariance-based, 2-class, one dataset at 160 Hz. D5 is a within-subject reference evaluated on run R12 only (735 episodes) and is not paired with D1–D4.
- Controller settings were fixed in C1; the sensitivity analysis explores only gate threshold and confirmation windows.
- Post-hoc analyses (chance-matched floor, gate sweep, lookup, independent verification) were defined after outcomes were known and were produced with computational assistance by the author’s team; independent re-execution by others is invited. Confidences are rounded to three decimals in replay files, so 10 of about 29,000 recorded pass flags differ from effective gate passage; simulator outcomes are authoritative.

## Reuse
Cite the claim–evidence matrix (`papers/paper_6/CLAIM_EVIDENCE_MATRIX.md`) rather than the headline numbers alone; do not describe P6 as clinical validation or as a general law relating decoder quality to control utility.
