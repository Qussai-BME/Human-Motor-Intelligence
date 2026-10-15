from __future__ import annotations

import numpy as np


def _stratified_take(indices: np.ndarray, labels: np.ndarray, n_take: int, rng: np.random.Generator) -> np.ndarray:
    if n_take >= len(indices):
        return indices.copy()
    classes = np.unique(labels)
    buckets = []
    base = n_take // len(classes)
    remainder = n_take % len(classes)
    for i, cls in enumerate(classes):
        idx = indices[labels == cls]
        want = min(len(idx), base + (1 if i < remainder else 0))
        if want:
            buckets.append(rng.choice(idx, size=want, replace=False))
    chosen = np.concatenate(buckets) if buckets else np.empty(0, dtype=int)
    if len(chosen) < n_take:
        remaining = np.setdiff1d(indices, chosen, assume_unique=False)
        extra = rng.choice(remaining, size=n_take - len(chosen), replace=False)
        chosen = np.concatenate([chosen, extra])
    return np.sort(chosen)


def stratified_subject_class_indices(
    labels: np.ndarray,
    subjects: np.ndarray,
    max_total: int | None,
    per_subject_cap: int | None,
    seed: int,
) -> np.ndarray:
    """Deterministically sample without replacing subject or class balance first."""
    labels = np.asarray(labels)
    subjects = np.asarray(subjects)
    rng = np.random.default_rng(seed)
    subject_ids = np.unique(subjects)
    selected_by_subject: list[np.ndarray] = []

    for subject in subject_ids:
        idx = np.flatnonzero(subjects == subject)
        cap = len(idx) if per_subject_cap is None else min(len(idx), per_subject_cap)
        selected_by_subject.append(_stratified_take(idx, labels[idx], cap, rng))

    selected = np.concatenate(selected_by_subject) if selected_by_subject else np.empty(0, dtype=int)
    if max_total is not None and len(selected) > max_total:
        # Equal subject allocation, then class stratification inside each subject.
        target_per_subject = max(1, max_total // len(subject_ids))
        refined: list[np.ndarray] = []
        for subject in subject_ids:
            idx = selected[subjects[selected] == subject]
            want = min(len(idx), target_per_subject)
            refined.append(_stratified_take(idx, labels[idx], want, rng))
        selected = np.concatenate(refined) if refined else np.empty(0, dtype=int)
        if len(selected) > max_total:
            selected = rng.choice(selected, size=max_total, replace=False)
    return np.sort(selected.astype(int))
