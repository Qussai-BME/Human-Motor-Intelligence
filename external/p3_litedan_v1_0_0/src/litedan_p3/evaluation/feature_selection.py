from __future__ import annotations

import numpy as np
from sklearn.feature_selection import f_classif


class SafeSelectKBest:
    """Leakage-safe univariate selector that handles constant training features explicitly."""

    def __init__(self, k: int):
        if k <= 0:
            raise ValueError("k must be positive")
        self.k = int(k)
        self.active_indices_: np.ndarray | None = None
        self.selected_indices_: np.ndarray | None = None
        self.scores_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "SafeSelectKBest":
        X = np.asarray(X, dtype=np.float32)
        if X.ndim != 2:
            raise ValueError("X must be 2-D")
        variances = np.var(X, axis=0)
        active = np.flatnonzero(np.isfinite(variances) & (variances > 1e-12))
        if len(active) == 0:
            raise ValueError("All training features are constant/non-finite")
        scores, _ = f_classif(X[:, active], y)
        scores = np.nan_to_num(scores, nan=-np.inf, posinf=np.finfo(np.float64).max, neginf=-np.inf)
        keep = min(self.k, len(active))
        order = np.argsort(scores, kind="mergesort")[-keep:]
        self.active_indices_ = active
        self.scores_ = scores
        self.selected_indices_ = np.sort(active[order])
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.selected_indices_ is None:
            raise RuntimeError("Selector has not been fitted")
        X = np.asarray(X, dtype=np.float32)
        return X[:, self.selected_indices_]

    def fit_transform(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        return self.fit(X, y).transform(X)

    def get_support(self) -> np.ndarray:
        if self.selected_indices_ is None:
            raise RuntimeError("Selector has not been fitted")
        return self.selected_indices_.copy()
