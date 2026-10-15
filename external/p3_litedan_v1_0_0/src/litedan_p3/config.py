from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import hashlib
import json

import yaml


@dataclass(frozen=True)
class DatasetConfig:
    name: str
    subdir: str | None = None
    exercise: list[int] | None = None
    expected_subjects: int | None = None
    expected_classes: int | None = None
    notes: str = ""


@dataclass(frozen=True)
class ProtocolConfig:
    strict_zero_calibration: bool = True
    target_unlabelled_exposure: bool = False
    fs: int = 2000
    window_ms: int = 400
    overlap: float = 0.50
    lowcut_hz: float = 20.0
    highcut_hz: float = 450.0
    notch_hz: float = 50.0
    rest_label: int = 0
    min_window_purity: float = 0.0
    feature_k: int = 308
    max_train_samples: int | None = 60000
    max_train_samples_per_subject: int | None = 2500


@dataclass(frozen=True)
class FeatureConfig:
    implementation: str = "current_618_v1"
    include_ar: bool = True
    include_histogram: bool = True
    include_hjorth: bool = True
    include_frequency: bool = True
    include_interchannel_corr: bool = True
    n_channels_expected: int = 12


@dataclass(frozen=True)
class ModelConfig:
    hidden_dim: int = 56
    dropout: float = 0.30
    epochs: int = 80
    batch_size: int = 512
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    lambda_max: float = 1.0
    lambda_schedule: str = "gradual"
    device: str = "cpu"
    early_stopping_patience: int | None = 15


@dataclass(frozen=True)
class BaselineConfig:
    xgboost: dict[str, Any] = field(default_factory=dict)
    lda: dict[str, Any] = field(default_factory=dict)
    linear_svc: dict[str, Any] = field(default_factory=dict)
    random_forest: dict[str, Any] = field(default_factory=dict)
@dataclass(frozen=True)
class RunConfig:
    seed: int = 42
    output_root: Path = Path("results")
    artifact_root: Path = Path("artifacts")
    data_root: Path = Path("data/ninapro")
    protocol: ProtocolConfig = field(default_factory=ProtocolConfig)
    features: FeatureConfig = field(default_factory=FeatureConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    baselines: BaselineConfig = field(default_factory=BaselineConfig)
    datasets: dict[str, DatasetConfig] = field(default_factory=dict)


def _dataset_configs(raw: dict[str, Any]) -> dict[str, DatasetConfig]:
    out: dict[str, DatasetConfig] = {}
    for name, cfg in raw.items():
        cfg = cfg or {}
        out[name] = DatasetConfig(
            name=name,
            subdir=cfg.get("subdir", name),
            exercise=(
    None
    if cfg.get("exercise") is None
    else [int(x) for x in cfg.get("exercise")]
    if isinstance(cfg.get("exercise"), (list, tuple))
    else [int(cfg.get("exercise"))]
),
            expected_subjects=cfg.get("expected_subjects"),
            expected_classes=cfg.get("expected_classes"),
            notes=cfg.get("notes", ""),
        )
    return out


def load_config(path: str | Path) -> RunConfig:
    path = Path(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return RunConfig(
        seed=int(raw.get("seed", 42)),
        output_root=Path(raw.get("output_root", "results")),
        artifact_root=Path(raw.get("artifact_root", "artifacts")),
        data_root=Path(raw.get("data_root", "data/ninapro")),
        protocol=ProtocolConfig(**raw.get("protocol", {})),
        features=FeatureConfig(**raw.get("features", {})),
        model=ModelConfig(**raw.get("model", {})),
        baselines=BaselineConfig(**raw.get("baselines", {})),
        datasets=_dataset_configs(raw.get("datasets", {})),
    )


def canonical_dict(cfg: RunConfig) -> dict[str, Any]:
    return {
        "seed": cfg.seed,
        "output_root": str(cfg.output_root),
        "artifact_root": str(cfg.artifact_root),
        "data_root": cfg.data_root.as_posix(),
        "protocol": cfg.protocol.__dict__,
        "features": cfg.features.__dict__,
        "model": cfg.model.__dict__,
        "baselines": cfg.baselines.__dict__,
        "datasets": {k: v.__dict__ for k, v in cfg.datasets.items()},
    }


def config_hash(cfg: RunConfig) -> str:
    blob = json.dumps(canonical_dict(cfg), sort_keys=True, default=str).encode()
    return hashlib.sha256(blob).hexdigest()[:12]


def cache_input_hash(cfg: RunConfig, entry: DatasetConfig) -> str:
    """Fingerprint only inputs that define extracted feature-cache contents.

    Model and output settings are deliberately excluded: changing a classifier must
    not make a valid raw-feature cache appear stale, whereas any extraction protocol,
    feature schema, data-root, or dataset-entry change must do so.
    """
    payload = {
        "data_root": cfg.data_root.as_posix(),
        "dataset": entry.__dict__,
        "protocol": cfg.protocol.__dict__,
        "features": cfg.features.__dict__,
    }
    blob = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]
