from __future__ import annotations

from itertools import combinations
from typing import Sequence

import numpy as np
from scipy import signal, stats
from scipy.linalg import solve, toeplitz

SCHEMA_VERSION = "current_618_v1"
EXPECTED_RAW_FEATURES = 618

TD_NAMES = [
    "MAV", "RMS", "WL", "Var", "IEMG", "log_MAV", "log_RMS", "log_VAR",
    "AAC", "TKEO", "Skew", "Kurt", "TM3", "TM4", "TM5", "V_order",
    "log_Det", "SSI", "ZCR", "SSC", "WAMP", "MYOP",
]
AR_NAMES = [f"AR_{i}" for i in range(4)]
HIST_NAMES = [f"Hist_{i}" for i in range(10)]
HJOR_NAMES = ["Activity", "Mobility", "Complexity"]
FREQ_NAMES = ["MNF", "MDF", "PeakF", "SpEntropy", "Band_20_150", "Band_150_350", "Band_350_450"]


def _safe_skew(x: np.ndarray) -> float:
    return float(stats.skew(x)) if np.std(x) > 1e-12 else 0.0


def _safe_kurt(x: np.ndarray) -> float:
    return float(stats.kurtosis(x)) if np.std(x) > 1e-12 else 0.0


def ar4(x: np.ndarray) -> list[float]:
    x = np.asarray(x, dtype=np.float64)
    x = x - x.mean()
    n = len(x)
    if n <= 4 or np.allclose(x, 0):
        return [0.0] * 4
    r = np.array([np.dot(x[: n - k], x[k:]) / n for k in range(5)])
    if abs(r[0]) < 1e-12:
        return [0.0] * 4
    try:
        coeff = solve(toeplitz(r[:4]), -r[1:5], assume_a="sym")
        return coeff.tolist() if np.all(np.isfinite(coeff)) else [0.0] * 4
    except Exception:
        return [0.0] * 4


def td_features(x: np.ndarray, threshold: float) -> list[float]:
    x = np.asarray(x, dtype=np.float64)
    dx = np.diff(x)
    ax = np.abs(x)
    var = float(np.var(x))
    mav = float(np.mean(ax))
    rms = float(np.sqrt(np.mean(x * x)))
    tkeo = float(np.mean(np.abs(x[1:-1] ** 2 - x[:-2] * x[2:]))) if len(x) >= 3 else 0.0
    centred = x - x.mean()
    return [
        mav,
        rms,
        float(np.sum(np.abs(dx))),
        var,
        float(np.sum(ax)),
        np.log1p(mav),
        np.log1p(rms),
        np.log1p(var),
        float(np.mean(np.abs(dx))) if len(dx) else 0.0,
        tkeo,
        _safe_skew(x),
        _safe_kurt(x),
        float(np.mean(centred ** 3)) if len(x) >= 3 else 0.0,
        float(np.mean(centred ** 4)) if len(x) >= 4 else 0.0,
        float(np.mean(centred ** 5)) if len(x) >= 5 else 0.0,
        float(np.mean(np.abs(x) ** 3) ** (1 / 3)) if len(x) else 0.0,
        float(np.exp(np.mean(np.log(ax[ax > 0])))) if np.any(ax > 0) else 0.0,
        float(np.sum(x * x)),
        float(np.mean(np.abs(x) > threshold)),
        float(np.mean((dx[:-1] * dx[1:]) < 0)) if len(dx) >= 2 else 0.0,
        float(np.sum(np.abs(dx) > threshold)),
        float(np.mean(ax > threshold)),
    ]


def histogram_features(x: np.ndarray) -> list[float]:
    ax = np.abs(x)
    maximum = float(ax.max()) if len(ax) else 0.0
    if maximum <= 1e-12:
        return [1.0] + [0.0] * 9
    counts, _ = np.histogram(ax, bins=10, range=(0, maximum + 1e-12))
    return (counts / max(counts.sum(), 1)).astype(float).tolist()


def hjorth_features(x: np.ndarray) -> list[float]:
    x = np.asarray(x, dtype=np.float64)
    d1 = np.diff(x)
    d2 = np.diff(d1)
    v0 = float(np.var(x))
    v1 = float(np.var(d1))
    v2 = float(np.var(d2))
    mobility = np.sqrt(v1 / max(v0, 1e-12)) if v0 > 0 else 0.0
    mobility_d = np.sqrt(v2 / max(v1, 1e-12)) if v1 > 0 else 0.0
    complexity = mobility_d / max(mobility, 1e-12) if mobility > 0 else 0.0
    return [v0, float(mobility), float(complexity)]


def frequency_features(x: np.ndarray, fs: int) -> list[float]:
    f, p = signal.welch(x, fs=fs, nperseg=min(256, len(x)))
    total = float(p.sum())
    if total <= 1e-15:
        return [0.0] * 7
    mean_frequency = float((f * p).sum() / total)
    csum = np.cumsum(p)
    median_frequency = float(f[min(np.searchsorted(csum, total / 2), len(f) - 1)])
    peak_frequency = float(f[np.argmax(p)])
    pnorm = p / (total + 1e-15)
    entropy = float(-(pnorm * np.log2(pnorm + 1e-15)).sum() / max(np.log2(len(pnorm)), 1e-12))
    bands = [float(p[(f >= lo) & (f <= hi)].sum()) for lo, hi in [(20, 150), (150, 350), (350, 450)]]
    return [mean_frequency, median_frequency, peak_frequency, entropy, *bands]


def window_features(window_cts: np.ndarray, fs: int = 2000) -> tuple[np.ndarray, list[str]]:
    w = np.asarray(window_cts, dtype=np.float32)
    if w.ndim != 2 or w.shape[0] != 12:
        raise ValueError(f"Expected window shape [12, samples], got {w.shape}")
    blocks: list[float] = []
    names: list[str] = []
    thresholds: list[float] = []
    for channel in w:
        diff = np.diff(channel)
        thresholds.append(float(np.percentile(np.abs(diff), 5)) if len(diff) else 0.0)

    for ch in range(12):
        x = w[ch].astype(np.float64)
        threshold = max(thresholds[ch], 1e-8)
        values = (
            td_features(x, threshold)
            + ar4(x)
            + histogram_features(x)
            + hjorth_features(x)
            + frequency_features(x, fs)
        )
        blocks.extend(values)
        names.extend([f"ch{ch}_{name}" for name in TD_NAMES + AR_NAMES + HIST_NAMES + HJOR_NAMES + FREQ_NAMES])

    z = w.astype(np.float64) - w.mean(axis=1, keepdims=True)
    sd = w.std(axis=1, keepdims=True)
    sd[sd < 1e-12] = 1.0
    corr = (z / sd) @ (z / sd).T / w.shape[1]
    for i, j in combinations(range(12), 2):
        blocks.append(float(np.clip(corr[i, j], -1.0, 1.0)))
        names.append(f"Corr_{i:02d}_{j:02d}")

    result = np.asarray(blocks, dtype=np.float32)
    if result.shape[0] != EXPECTED_RAW_FEATURES:
        raise RuntimeError(
            f"Feature schema invariant broken: expected {EXPECTED_RAW_FEATURES}, got {result.shape[0]}"
        )
    return result, names


def extract_feature_matrix(windows: np.ndarray, fs: int = 2000, n_jobs: int = 6) -> tuple[np.ndarray, list[str]]:
    from joblib import Parallel, delayed

    windows = np.asarray(windows, dtype=np.float32)
    if windows.ndim != 3 or windows.shape[1] != 12:
        raise ValueError(f"Expected [n_windows, 12, samples], got {windows.shape}")
    rows = Parallel(n_jobs=n_jobs, prefer="threads")(
        delayed(window_features)(window, fs) for window in windows
    )
    if not rows:
        return np.empty((0, EXPECTED_RAW_FEATURES), np.float32), []
    matrix = np.vstack([row[0] for row in rows]).astype(np.float32)
    names = rows[0][1]
    if any(row[1] != names for row in rows[1:]):
        raise RuntimeError("Feature-name schema drift detected across windows")
    return matrix, names
