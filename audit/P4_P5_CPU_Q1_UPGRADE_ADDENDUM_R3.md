

## P5 R3-005 Calibration Extension

The clean LOSO calibration extension was completed and independently reproduced byte-for-byte. Static-mean fusion was the best-calibrated fusion condition in this cohort (Brier 0.919149; ECE 0.044729), while confidence-weighted fusion (Brier 0.938161; ECE 0.085202) and confidence-selective fusion (Brier 0.948498; ECE 0.106809) did not improve calibration or accuracy. Accuracy was 0.110909 for both confidence-aware variants, compared with 0.112727 for static-mean fusion and 0.114318 for EEG-only. The appropriate conclusion is that the present confidence heuristic is not validated as a reliability-aware fusion mechanism in this cohort; the result motivates future calibration learned strictly within training folds rather than supporting deployment claims.

## P4 R3-006 Robustness Gate

P4's clean-train/corrupted-test robustness implementation was initiated but did not complete within the available CPU budget and produced no evidence artifact. It is therefore marked **PENDING COMPUTATIONAL GATE**, not as a positive or negative scientific result. All historical P4 evidence remains frozen.
