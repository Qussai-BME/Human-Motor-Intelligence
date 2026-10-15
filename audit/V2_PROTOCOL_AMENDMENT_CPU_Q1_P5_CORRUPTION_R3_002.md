# V2 Protocol Amendment — P5 CPU Q1 Corruption and Missing-Modality R3-002

This amendment is a new extension. It does not change P5 R2 frozen outputs.

## Perturbation contract

The P5 derived feature cache has 60 EEG channels represented by two features per channel and seven EMG channels represented by three features per channel. For each held-out subject and each training fold, models are fit on the perturbed training features and evaluated on the identically perturbed held-out features. The corruption is feature-group channel dropout, not a claim about raw-signal hardware failure.

Dropout levels are 0%, 10%, and 20%. The dropped channel indices are deterministic and evenly spaced using `linspace` over the channel index range, rounded to unique indices. All feature columns belonging to a dropped channel are set to zero. No labels or subject identities are changed. The perturbation is applied independently to EEG and EMG in separate arms.

## Conditions

The report retains EEG-only, EMG-only, static mean fusion, and entropy-confidence-weighted fusion. A missing-modality fallback arm sets one modality's posterior to zero and uses the available modality posterior directly; it is explicitly labelled as a fallback rule, not imputation or evidence of physiological recovery.

The primary endpoint is subject-level macro-F1. Trial predictions, modality state, dropout level, and confidence weights are preserved. No post hoc model selection is allowed.

## Boundaries

This study does not establish robustness to raw-channel noise, temporal shift, amplitude scaling, or real hardware failure. Those require separate raw-signal or validated feature-level amendments. No clinical or general fusion claim is permitted.
