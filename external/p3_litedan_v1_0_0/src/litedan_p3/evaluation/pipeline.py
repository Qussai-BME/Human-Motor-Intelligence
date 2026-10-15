from __future__ import annotations

import time
from dataclasses import asdict
from pathlib import Path

import numpy as np
from scipy import linalg
from sklearn.covariance import LedoitWolf
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier

from ..config import RunConfig, config_hash
from ..models.litedan import LiteDAN
from ..utils.repro import set_seed
from ..utils.sampling import stratified_subject_class_indices
from .feature_selection import SafeSelectKBest
from .metrics import compute_metrics


def _matrix_sqrt(matrix: np.ndarray, inverse: bool = False) -> np.ndarray:
    values, vectors = linalg.eigh(matrix)
    values = np.clip(values, 1e-10, None)
    transformed = (1.0 / np.sqrt(values)) if inverse else np.sqrt(values)
    return (vectors * transformed) @ vectors.T


def coral_source_to_reference(
    source: np.ndarray,
    reference: np.ndarray,
    regularization: float = 1e-3,
    reference_transform: np.ndarray | None = None,
) -> np.ndarray:
    """
    Source-only CORAL.

    The transformation is applied to centered source data and
    translated back to the reference-domain mean.

    No target-subject data are used.
    """

    source = np.asarray(
        source,
        dtype=np.float32,
    )

    reference = np.asarray(
        reference,
        dtype=np.float32,
    )

    if source.ndim != 2:
        raise ValueError(
            f"source must be 2-D, got {source.shape}"
        )

    if reference.ndim != 2:
        raise ValueError(
            f"reference must be 2-D, got {reference.shape}"
        )

    if source.shape[1] != reference.shape[1]:
        raise ValueError(
            "source/reference feature dimensions do not match"
        )

    n_features = source.shape[1]

    source_mean = source.mean(
        axis=0,
        dtype=np.float64,
    )

    reference_mean = reference.mean(
        axis=0,
        dtype=np.float64,
    )

    source_centered = (
        source.astype(
            np.float64,
            copy=False,
        )
        - source_mean
    )

    if reference_transform is None:
        reference_centered = (
            reference.astype(
                np.float64,
                copy=False,
            )
            - reference_mean
        )

        reference_cov = (
            LedoitWolf()
            .fit(reference_centered)
            .covariance_
        )

        reference_cov += (
            regularization
            * np.eye(
                n_features,
                dtype=np.float64,
            )
        )

        reference_transform = _matrix_sqrt(
            reference_cov,
            inverse=False,
        )

    source_centered = np.asarray(
        source_centered,
        dtype=np.float64,
        order="C",
    )

    source_cov = (
        LedoitWolf()
        .fit(source_centered)
        .covariance_
    )

    source_cov += (
        regularization
        * np.eye(
            n_features,
            dtype=np.float64,
        )
    )

    source_inverse_sqrt = _matrix_sqrt(
        source_cov,
        inverse=True,
    )

    transformed = (
        source_centered
        @ source_inverse_sqrt
        @ reference_transform
    )

    transformed += reference_mean

    return transformed.astype(
        np.float32,
        copy=False,
    )


def make_xgb(
    cfg: RunConfig,
    seed: int,
) -> XGBClassifier:
    params = dict(
        cfg.baselines.xgboost
    )

    params["random_state"] = seed

    params.setdefault(
        "objective",
        "multi:softprob",
    )

    params.setdefault(
        "eval_metric",
        "mlogloss",
    )

    return XGBClassifier(
        **params
    )


def make_random_forest(
    cfg: RunConfig,
    seed: int,
) -> RandomForestClassifier:
    params = dict(
        cfg.baselines.random_forest
    )

    params["random_state"] = seed

    return RandomForestClassifier(
        **params
    )    
def make_litedan(cfg: RunConfig, condition: str, n_features: int, n_classes: int, n_domains: int, seed: int) -> LiteDAN:
    schedule = cfg.model.lambda_schedule
    lambda_max = cfg.model.lambda_max
    if condition == "litedan_fixed_0p1":
        schedule, lambda_max = "fixed", 0.1
    elif condition == "litedan_fixed_0p5":
        schedule, lambda_max = "fixed", 0.5
    elif condition == "litedan_fixed_1p0":
        schedule, lambda_max = "fixed", 1.0
    elif condition == "litedan_no_grl":
        schedule, lambda_max = "none", 0.0
    return LiteDAN(
        n_features=n_features,
        n_classes=n_classes,
        n_domains=n_domains,
        hidden_dim=cfg.model.hidden_dim,
        dropout=cfg.model.dropout,
        epochs=cfg.model.epochs,
        batch_size=cfg.model.batch_size,
        learning_rate=cfg.model.learning_rate,
        weight_decay=cfg.model.weight_decay,
        lambda_schedule=schedule,
        lambda_max=lambda_max,
        device=cfg.model.device,
        seed=seed,
        early_stopping_patience=cfg.model.early_stopping_patience,
    )


def fit_predict_fold(
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    test_subject: int,
    condition: str,
    cfg: RunConfig,
    seed: int,
) -> dict:
    """
    Execute one strict LOSO fold.

    Protocol invariants:
    - held-out subject is never used for fitting
    - scaling is fit on training data only
    - SelectKBest is fit on training data only
    - no target-unlabelled exposure in strict mode
    - all classifiers receive the same fold-local representation
    """

    if (
        cfg.protocol.strict_zero_calibration
        and cfg.protocol.target_unlabelled_exposure
    ):
        raise ValueError(
            "strict_zero_calibration cannot be combined "
            "with target_unlabelled_exposure"
        )

    set_seed(seed)

    fold_t0 = time.perf_counter()

    # =========================================================
    # OUTER LOSO SPLIT
    # =========================================================

    train_mask = groups != test_subject
    test_mask = groups == test_subject

    train_idx_full = np.flatnonzero(train_mask)
    test_idx = np.flatnonzero(test_mask)

    if len(test_idx) == 0:
        raise ValueError(
            f"No test samples for subject {test_subject}"
        )

    # =========================================================
    # TRAINING-ONLY SAMPLE CAP
    # =========================================================

    local_idx = stratified_subject_class_indices(
        y[train_idx_full],
        groups[train_idx_full],
        max_total=cfg.protocol.max_train_samples,
        per_subject_cap=cfg.protocol.max_train_samples_per_subject,
        seed=seed,
    )

    train_idx = train_idx_full[local_idx]

    if len(np.unique(y[train_idx])) < 2:
        raise ValueError(
            "Training fold has fewer than two classes "
            "after sampling"
        )

    train_subjects = groups[train_idx]

    classes = np.unique(y[train_idx])

    n_domains = len(
        np.unique(train_subjects)
    )

    # =========================================================
    # TRAINING-ONLY FEATURE SELECTION + SCALING
    #
    # Protocol v1.1 intentionally selects on source-only raw
    # features before fitting the scaler on selected source columns.
    # No target rows are exposed to either fitted transform.
    # =========================================================

    prep_t0 = time.perf_counter()

    k = min(
        cfg.protocol.feature_k,
        X[train_idx].shape[1],
    )

    selector = SafeSelectKBest(k=k)

    X_train_selected = selector.fit_transform(
        X[train_idx],
        y[train_idx],
    ).astype(np.float32)

    X_test_selected = selector.transform(
        X[test_idx]
    ).astype(np.float32)

    scaler = StandardScaler()

    X_train = scaler.fit_transform(
        X_train_selected
    ).astype(np.float32)

    X_test = scaler.transform(
        X_test_selected
    ).astype(np.float32)

    prep_elapsed = (
        time.perf_counter()
        - prep_t0
    )

    # =========================================================
    # COMMON OUTPUT STATE
    # =========================================================

    model = None
    predictions = None
    parameter_count = None
    history = None

    fit_elapsed = 0.0
    predict_elapsed = 0.0
    model_elapsed = 0.0

    # =========================================================
    # XGBOOST
    # =========================================================

    if condition == "xgb":

        model_t0 = time.perf_counter()

        model = make_xgb(
            cfg,
            seed,
        )

        fit_t0 = time.perf_counter()

        model.fit(
            X_train,
            y[train_idx],
            verbose=False,
        )

        fit_elapsed = (
            time.perf_counter()
            - fit_t0
        )

        pred_t0 = time.perf_counter()

        predictions = model.predict(
            X_test
        )

        predict_elapsed = (
            time.perf_counter()
            - pred_t0
        )

        model_elapsed = (
            time.perf_counter()
            - model_t0
        )

    # =========================================================
    # LDA
    # =========================================================

    elif condition == "lda":

        model_t0 = time.perf_counter()

        model = LinearDiscriminantAnalysis(
            **cfg.baselines.lda
        )

        fit_t0 = time.perf_counter()

        model.fit(
            X_train,
            y[train_idx],
        )

        fit_elapsed = (
            time.perf_counter()
            - fit_t0
        )

        pred_t0 = time.perf_counter()

        predictions = model.predict(
            X_test
        )

        predict_elapsed = (
            time.perf_counter()
            - pred_t0
        )

        model_elapsed = (
            time.perf_counter()
            - model_t0
        )

    # =========================================================
    # LINEAR SVC
    # =========================================================

    elif condition == "linear_svc":

        model_t0 = time.perf_counter()

        params = dict(cfg.baselines.linear_svc)
        params["random_state"] = seed
        model = LinearSVC(**params)

        fit_t0 = time.perf_counter()

        model.fit(
            X_train,
            y[train_idx],
        )

        fit_elapsed = (
            time.perf_counter()
            - fit_t0
        )

        pred_t0 = time.perf_counter()

        predictions = model.predict(
            X_test
        )

        predict_elapsed = (
            time.perf_counter()
            - pred_t0
        )

        model_elapsed = (
            time.perf_counter()
            - model_t0
        )

    # =========================================================
    # RANDOM FOREST
    # =========================================================

    elif condition == "random_forest":

        model_t0 = time.perf_counter()

        model = make_random_forest(
            cfg,
            seed,
        )

        fit_t0 = time.perf_counter()

        model.fit(
            X_train,
            y[train_idx],
        )

        fit_elapsed = (
            time.perf_counter()
            - fit_t0
        )

        pred_t0 = time.perf_counter()

        predictions = model.predict(
            X_test
        )

        predict_elapsed = (
            time.perf_counter()
            - pred_t0
        )

        model_elapsed = (
            time.perf_counter()
            - model_t0
        )

    # =========================================================
    # SOURCE-ONLY CORAL + XGBOOST
    # =========================================================

    elif condition == "coral_xgb":

        model_t0 = time.perf_counter()

        reference_subject = int(
            np.unique(train_subjects)[0]
        )

        transformed = np.empty_like(
            X_train
        )
        reference = X_train[
            train_subjects == reference_subject
        ]
            
        if len(reference) == 0:
             raise ValueError(
                 f"No samples found for CORAL reference "
                 f"subject {reference_subject}"
                )
        reference_cov = (
             LedoitWolf()
             .fit(reference)
             .covariance_
         )
        reference_cov = (
             reference_cov
             + 1e-3
            * np.eye(
                X_train.shape[1],
                dtype=reference_cov.dtype,
                )
        )
        reference_transform = _matrix_sqrt(
             reference_cov,
              inverse=False,
              )
        transformed[
            train_subjects
             == reference_subject
             ] = reference
              

        for subject in np.unique(
            train_subjects
        ):
            if subject == reference_subject:
                continue

            idx = np.flatnonzero(
                train_subjects == subject
            )

            transformed[idx] = (
                coral_source_to_reference(
                    X_train[idx],
                    reference,
                    regularization=1e-3,
                    reference_transform=(
                        reference_transform
                        ),
                        
                )
            )

        model = make_xgb(
            cfg,
            seed,
        )

        fit_t0 = time.perf_counter()

        model.fit(
            transformed,
            y[train_idx],
            verbose=False,
        )

        fit_elapsed = (
            time.perf_counter()
            - fit_t0
        )

        pred_t0 = time.perf_counter()

        predictions = model.predict(
            X_test
        )

        predict_elapsed = (
            time.perf_counter()
            - pred_t0
        )

        model_elapsed = (
            time.perf_counter()
            - model_t0
        )

    # =========================================================
    # TRANSDUCTIVE CORAL
    # =========================================================

    elif condition == "coral_target_xgb":

        if cfg.protocol.strict_zero_calibration:
            raise ValueError(
                "coral_target_xgb is transductive and forbidden "
                "in strict zero-calibration mode"
            )

        model_t0 = time.perf_counter()

        source_cov = LedoitWolf().fit(
            X_train
        ).covariance_

        target_cov = LedoitWolf().fit(
            X_test
        ).covariance_

        transform = (
            _matrix_sqrt(
                source_cov,
                inverse=True,
            )
            @ _matrix_sqrt(
                target_cov,
                inverse=False,
            )
        )

        model = make_xgb(
            cfg,
            seed,
        )

        fit_t0 = time.perf_counter()

        model.fit(
            X_train @ transform,
            y[train_idx],
            verbose=False,
        )

        fit_elapsed = (
            time.perf_counter()
            - fit_t0
        )

        pred_t0 = time.perf_counter()

        predictions = model.predict(
            X_test
        )

        predict_elapsed = (
            time.perf_counter()
            - pred_t0
        )

        model_elapsed = (
            time.perf_counter()
            - model_t0
        )

    # =========================================================
    # LITE-DAN
    # =========================================================

    elif condition.startswith("litedan"):

        model_t0 = time.perf_counter()

        model = make_litedan(
            cfg,
            condition,
            X_train.shape[1],
            len(classes),
            n_domains,
            seed,
        )

        class_to_idx = {
            label: i
            for i, label in enumerate(classes)
        }

        y_train_idx = np.asarray(
            [
                class_to_idx[label]
                for label in y[train_idx]
            ],
            dtype=np.int64,
        )

        fit_t0 = time.perf_counter()

        model.fit(
            X_train,
            y_train_idx,
            train_subjects,
        )

        fit_elapsed = (
            time.perf_counter()
            - fit_t0
        )

        pred_t0 = time.perf_counter()

        predicted_idx = model.predict(
            X_test
        )

        predictions = classes[
            predicted_idx
        ]

        predict_elapsed = (
            time.perf_counter()
            - pred_t0
        )

        model_elapsed = (
            time.perf_counter()
            - model_t0
        )

        parameter_count = (
            model.parameter_count()
        )

        history = [
            asdict(row)
            for row in model.history
        ]

    else:
        raise ValueError(
            f"Unknown condition: {condition}"
        )

    # =========================================================
    # METRICS
    # =========================================================

    metrics = compute_metrics(
        y[test_idx],
        predictions,
        rest_label=cfg.protocol.rest_label,
        class_labels=np.arange(41),
    )

    fold_elapsed = (
        time.perf_counter()
        - fold_t0
    )

    return {
        "experiment_status": "COMPLETED",
        "architecture_version": "LDAN-v1.0" if condition.startswith("litedan") else None,
        "code_version": "protocol-v1.1.0",
        "config_hash": config_hash(cfg),
        "feature_schema": cfg.features.implementation,
        "protocol": {
            "strict_zero_calibration": bool(cfg.protocol.strict_zero_calibration),
            "target_unlabelled_exposure": bool(cfg.protocol.target_unlabelled_exposure),
            "preprocessing_order": "outer_LOSO>source_only_SelectKBest>source_only_StandardScaler>fit>held_out_prediction",
        },
        "condition": condition,
        "test_subject": int(test_subject),
        "train_subject_ids": [
            int(subject)
            for subject in sorted(np.unique(groups[train_idx_full]).tolist())
        ],
        "seed": int(seed),

        "n_train": int(
            len(train_idx)
        ),

        "n_train_full": int(
            len(train_idx_full)
        ),

        "n_test": int(
            len(test_idx)
        ),

        "n_train_subjects": int(
            n_domains
        ),

        "n_selected_features": int(
            X_train.shape[1]
        ),

        "selected_feature_indices": (
            selector.get_support().tolist()
        ),

        "prep_seconds": float(
            prep_elapsed
        ),

        "fit_seconds": float(
            fit_elapsed
        ),

        "predict_seconds": float(
            predict_elapsed
        ),

        "model_elapsed_seconds": float(
            model_elapsed
        ),

        "fold_elapsed_seconds": float(
            fold_elapsed
        ),

        "elapsed_seconds": float(
            fold_elapsed
        ),

        "parameter_count": (
            int(parameter_count)
            if parameter_count is not None
            else None
        ),

        "metrics": metrics,

        "history": history,
    }