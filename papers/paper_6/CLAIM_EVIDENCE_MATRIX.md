# P6 Claim–Evidence Matrix (C1, audit, C2)

| Claim | Verdict | Evidence |
|---|---|---|
| The registered C1 chain executed completely and reproducibly | Supported | Six gates; primary = rerun; audit D1 bit-identical |
| C1 decoders carried above-chance information | Not supported | Pooled accuracy 0.497–0.510; all binomial p ≥ 0.77 |
| C1 success of 0/60 informs on decoder quality | Not supported | Oracle also 0/20; 2 of 15 outputs inside the task window |
| C1 decoders differ in downstream command corrections | **Withdrawn** | 0/64 corrections before task end; tracks confidence |
| The C2 interface can reach the endpoint | Supported | Oracle 100/100; C1-format oracle 0/100 |
| Control success rises with accuracy for calibrated decoders (emulator) | Supported | H-E1 slope 14.8 per unit accuracy (13.95–15.64) |
| An over-confident chance-level decoder has a substantial floor | Supported | 23.0% (19.4–26.9%); closed form 24.2% |
| Calibration changes success, with crossover near q = 0.8 | Supported | H-E3: +26.4, +16.6, +0.4 points at q = 0.6, 0.7, 0.8 |
| Real zero-calibration decoders differ in control success | Supported, but confidence-driven | H-R1; gate-pass ρ = 0.95 vs accuracy ρ = 0.24 |
| Real zero-calibration decoders give accuracy-attributable utility at the registered gate | Negligible | Excess −1.9 to +0.4 points (D3 −0.2, CI −2.3 to 1.3) |
| Within-subject calibration gives accuracy-attributable utility | Weakly supported | D5 +5.9 points (1.1 to 11.2); one run, unpaired episodes |
| Results apply to online BCI, prostheses or patients | Not supported | Offline replay, simulator, healthy-subject data |
