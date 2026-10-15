from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
P6_SCRIPTS = ROOT / "p6" / "c_mi_r04_primary" / "scripts"
sys.path.insert(0, str(P6_SCRIPTS))

from p6_mi_core import CONTROL_MAPPING_ID, MODELS, control_label, features, fit_source_model  # noqa: E402


def test_p6_c_mapping_is_fixed_abstract_interface() -> None:
    assert CONTROL_MAPPING_ID.endswith("_v1")
    assert control_label("T1") == "OPEN"
    assert control_label("T2") == "CLOSE"


def test_p6_c_feature_shapes_preserve_model_family() -> None:
    rng = np.random.default_rng(1701)
    epochs = rng.normal(size=(6, 64, 400)).astype(np.float32)
    assert features(epochs, "M1").shape == (6, 57)
    assert features(epochs, "M2").shape == (6, 114)
    assert features(epochs, "M3").shape == (6, 171)


def test_p6_c_source_model_fits_without_target_data() -> None:
    rng = np.random.default_rng(1701)
    train_x = rng.normal(size=(24, 64, 400)).astype(np.float32)
    train_y = np.array([1, 2] * 12)
    for model_id in MODELS:
        model, score = fit_source_model(train_x, train_y, model_id)
        assert model is not None
        assert 0.0 <= score <= 1.0
