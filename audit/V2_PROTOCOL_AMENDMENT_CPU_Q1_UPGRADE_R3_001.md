# V2 Protocol Amendment — CPU-First Q1 Upgrade R3-001

## Scope

This amendment registers new prospective extension namespaces for P4 and P5. It does not alter frozen V2 Recovery R1/R2 outputs, configurations, statistics, or manuscript claims.

## P4 extension

The P4 extension uses the existing 54-subject OpenBMI-derived epoch caches. The outer evaluation remains subject-wise LOSO. For every held-out subject, all representation parameters are estimated from training subjects only. The tested representation conditions are: (i) log-Euclidean covariance features with a fixed LDA classifier, and (ii) covariance-whitened alignment followed by the same log-Euclidean features and LDA. Covariance matrices are computed per epoch from demeaned channel-by-time arrays with fixed diagonal regularization. Matrix logarithms/exponentials use symmetric eigendecomposition with a fixed eigenvalue floor. No hyperparameter search is performed. No held-out subject contributes to fitting a reference covariance or classifier.

The primary endpoint is subject-level macro-F1. Accuracy and balanced accuracy are retained as secondary endpoints. Trial predictions are stored for the new namespace so calibration and robustness work is not inferred from aggregate metrics.

## P5 extension

The P5 extension uses the existing 24-subject amended Jeong feature caches and the same subject-wise LOSO boundary. EEG-only and EMG-only LDA models are fit on training subjects. Confidence-weighted late fusion combines the two held-out posterior vectors using a prespecified confidence based on normalized predictive entropy; weights are normalized per trial and default to equal weights if both confidences are numerically zero. The comparison includes EEG-only, EMG-only, static mean fusion, and confidence-weighted fusion. No model selection or confidence rule tuning is performed.

The primary endpoint is subject-level macro-F1. Per-trial probabilities, predictions, and confidence weights are retained for future calibration and modality-corruption analyses. No causal mechanism claim is permitted.

## Reproducibility

The extension uses deterministic NumPy/scikit-learn operations, a fixed random seed where a solver requires it, the recorded environment, and new primary/rerun namespaces. Each run emits protocol, environment, provenance, trial predictions, subject-level results, summary statistics, and a manifest. An independent rerun must match the primary subject-level output byte-for-byte before any manuscript update.

## Explicitly deferred

P4 cross-dataset evaluation, P4 calibration/robustness perturbations, P5 modality corruption, P5 missing-modality fallback, P5 calibration, and Paper 2 kernel-reduction remain separate amendments until their exact perturbation/evidence contracts are registered. P3 and P6 R3 remain independent external gates.
