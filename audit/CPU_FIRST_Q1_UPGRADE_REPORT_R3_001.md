

## R3-005 P5 Calibration Extension — Completed and Independently Reproduced

The P5 calibration extension was analyzed at the subject/trial level under the frozen clean LOSO protocol. Five conditions were retained: EEG-only, EMG-only, static-mean fusion, confidence-weighted fusion, and confidence-selective fusion. The calibration output was independently regenerated with the same cache, seed, protocol, and runner; the primary and rerun `trial_probabilities.json` files are byte-identical (SHA-256 `9d454e309e6c529bc1466f155884bba7566d4616cdc95db9935e7374782d0378d`, with the full recorded digest in the run manifest).

| Condition | Accuracy | Multiclass Brier | 10-bin ECE | Confidence–correctness point-biserial |
|---|---:|---:|---:|---:|
| EMG-only | 0.095379 | 0.922631 | 0.044483 | 0.014554 |
| Static-mean fusion | 0.112727 | 0.919149 | 0.044729 | -0.008383 |
| EEG-only | 0.114318 | 0.944344 | 0.100162 | -0.004679 |
| Confidence-weighted fusion | 0.110909 | 0.938161 | 0.085202 | -0.006666 |
| Confidence-selective fusion | 0.110909 | 0.948498 | 0.106809 | -0.003529 |

The principal calibration finding is negative for the proposed confidence-aware fusion variants in this cohort: neither confidence-weighted nor confidence-selective fusion improved accuracy relative to the strongest unimodal/fusion alternatives, and both had worse Brier/ECE than static-mean fusion. The confidence–correctness associations were near zero or slightly negative for all fusion conditions. These values are descriptive subject-level/trial-level diagnostics, not evidence that confidence-aware fusion is universally ineffective.

## R3-006 P4 Robustness Gate — Not Released

The clean-train/corrupted-test P4 robustness runner was started using the selected temporal representation but exceeded the CPU execution budget without producing an artifact. It was stopped, and the result is recorded as an execution non-result in `audit/P4_ROBUSTNESS_COMPUTATIONAL_GATE_R3_006.md`. No robustness claim, negative or positive, is made from R3-006. Historical P4 results remain frozen and untouched.
