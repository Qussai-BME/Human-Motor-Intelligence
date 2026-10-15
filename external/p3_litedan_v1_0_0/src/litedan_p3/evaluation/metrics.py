from __future__ import annotations

import numpy as np
from sklearn.metrics import accuracy_score, cohen_kappa_score, confusion_matrix, f1_score, recall_score


def compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    rest_label: int = 0,
    class_labels: np.ndarray | None = None,
) -> dict:

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    observed_labels = np.unique(
        np.concatenate([y_true, y_pred])
    )

    if class_labels is not None:
        class_labels = np.asarray(class_labels, dtype=int)
        fixed_labels = np.unique(class_labels)
    else:
        fixed_labels = observed_labels

    labels = observed_labels
    active_labels = labels[labels != rest_label]

    missing_test_labels = sorted(
        set(fixed_labels.tolist()) - set(np.unique(y_true).tolist())
    )

    rest_present = bool(np.any(y_true == rest_label))
    active_mask = y_true != rest_label

    result = {
        "accuracy": float(
            accuracy_score(y_true, y_pred)
        ),

        # Primary macro-F1: only labels represented in this test subject.
        "macro_f1": float(
            f1_score(
                y_true,
                y_pred,
                labels=labels,
                average="macro",
                zero_division=0,
            )
        ),

        # Secondary fixed-label-space diagnostic.
        "macro_f1_fixed41": float(
            f1_score(
                y_true,
                y_pred,
                labels=fixed_labels,
                average="macro",
                zero_division=0,
            )
        ),

        "kappa": float(
            cohen_kappa_score(
                y_true,
                y_pred,
                labels=labels,
            )
        ),

        "rest_recall": float(
            recall_score(
                y_true,
                y_pred,
                labels=[rest_label],
                average="macro",
                zero_division=0,
            )
        ) if rest_present else float("nan"),

        "n_samples": int(len(y_true)),

        "labels": [
            int(x) for x in labels.tolist()
        ],

        "fixed_labels": [
            int(x) for x in fixed_labels.tolist()
        ],

        "missing_test_labels": missing_test_labels,
    }
    if np.any(active_mask):
        active_true = y_true[active_mask]
        active_pred = y_pred[active_mask]

        result["active_only_accuracy"] = float(
            accuracy_score(active_true, active_pred)
        )

        result["active_only_macro_f1"] = float(
            f1_score(
                active_true,
                active_pred,
                labels=active_labels,
                average="macro",
                zero_division=0,
            )
        )

        result["inflation_pp"] = 100.0 * (
            result["accuracy"]
            - result["active_only_accuracy"]
        )

        result["active_labels"] = [
            int(x) for x in active_labels.tolist()
        ]

        result["confusion_matrix_active"] = confusion_matrix(
            active_true,
            active_pred,
            labels=active_labels,
        ).tolist()

    else:
        result["active_only_accuracy"] = float("nan")
        result["active_only_macro_f1"] = float("nan")
        result["inflation_pp"] = float("nan")
        result["active_labels"] = []
        result["confusion_matrix_active"] = []
    result["confusion_matrix"] = confusion_matrix(
        y_true,
        y_pred,
        labels=labels,
    ).tolist()

    return result