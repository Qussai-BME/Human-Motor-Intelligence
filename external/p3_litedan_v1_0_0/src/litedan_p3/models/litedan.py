from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class GradientReversalFn(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx,
        x: torch.Tensor,
        lambda_: float,
    ) -> torch.Tensor:
        ctx.lambda_ = float(lambda_)
        return x.view_as(x)

    @staticmethod
    def backward(
        ctx,
        grad_output: torch.Tensor,
    ):
        return (
            -ctx.lambda_ * grad_output,
            None,
        )


def gradient_reverse(
    x: torch.Tensor,
    lambda_: float,
) -> torch.Tensor:
    return GradientReversalFn.apply(
        x,
        lambda_,
    )


class LiteDANNet(nn.Module):
    def __init__(
        self,
        n_features: int,
        n_classes: int,
        n_domains: int,
        hidden_dim: int = 56,
        dropout: float = 0.30,
    ):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(
                n_features,
                128,
            ),
            nn.BatchNorm1d(
                128,
            ),
            nn.ReLU(),
            nn.Dropout(
                dropout,
            ),
            nn.Linear(
                128,
                hidden_dim,
            ),
            nn.BatchNorm1d(
                hidden_dim,
            ),
            nn.ReLU(),
            nn.Dropout(
                dropout,
            ),
        )

        self.classifier = nn.Sequential(
            nn.Linear(
                hidden_dim,
                32,
            ),
            nn.ReLU(),
            nn.Dropout(
                dropout,
            ),
            nn.Linear(
                32,
                n_classes,
            ),
        )

        self.domain_classifier = nn.Sequential(
            nn.Linear(
                hidden_dim,
                32,
            ),
            nn.ReLU(),
            nn.Dropout(
                dropout,
            ),
            nn.Linear(
                32,
                n_domains,
            ),
        )

    def forward(
        self,
        x: torch.Tensor,
        lambda_: float = 0.0,
    ):
        z = self.encoder(x)

        class_logits = self.classifier(
            z,
        )

        domain_logits = self.domain_classifier(
            gradient_reverse(
                z,
                lambda_,
            ),
        )

        return (
            class_logits,
            domain_logits,
        )

    def parameter_count(self) -> int:
        return sum(
            p.numel()
            for p in self.parameters()
            if p.requires_grad
        )


@dataclass
class TrainingHistory:
    epoch: int
    lambda_: float
    total_loss: float
    class_loss: float
    domain_loss: float


class LiteDAN:
    """CPU-oriented domain-generalisation model with subject IDs as source domains."""

    def __init__(
        self,
        n_features: int,
        n_classes: int,
        n_domains: int,
        *,
        hidden_dim: int = 56,
        dropout: float = 0.30,
        epochs: int = 80,
        batch_size: int = 512,
        learning_rate: float = 1e-3,
        weight_decay: float = 1e-4,
        lambda_schedule: Literal[
            "gradual",
            "fixed",
            "none",
        ] = "gradual",
        lambda_max: float = 1.0,
        device: str = "cpu",
        seed: int = 42,
        early_stopping_patience: int | None = 15,
    ):
        if (
            device != "cpu"
            and torch.cuda.is_available() is False
        ):
            raise ValueError(
                "Requested non-CPU device, "
                "but CUDA is unavailable"
            )

        if lambda_schedule not in {
            "gradual",
            "fixed",
            "none",
        }:
            raise ValueError(
                "lambda_schedule must be "
                "gradual/fixed/none"
            )

        self.n_features = n_features
        self.n_classes = n_classes
        self.n_domains = n_domains

        self.hidden_dim = hidden_dim
        self.dropout = dropout

        self.epochs = epochs
        self.batch_size = batch_size

        self.learning_rate = (
            learning_rate
        )
        self.weight_decay = (
            weight_decay
        )

        self.lambda_schedule = (
            lambda_schedule
        )
        self.lambda_max = lambda_max

        self.device = torch.device(
            device
        )

        self.seed = seed

        self.early_stopping_patience = (
            early_stopping_patience
        )

        self.classes_: (
            np.ndarray | None
        ) = None

        self.domain_ids_: (
            np.ndarray | None
        ) = None

        self.net: (
            LiteDANNet | None
        ) = None

        self.history: list[
            TrainingHistory
        ] = []

    def lambda_at(
        self,
        epoch_zero_based: int,
    ) -> float:
        if self.lambda_schedule == "none":
            return 0.0

        if self.lambda_schedule == "fixed":
            return float(
                self.lambda_max
            )

        p = (
            epoch_zero_based
            / max(
                self.epochs - 1,
                1,
            )
        )

        return float(
            self.lambda_max
            * (
                2.0
                / (
                    1.0
                    + math.exp(
                        -10.0 * p
                    )
                )
                - 1.0
            )
        )

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        domains: np.ndarray,
    ) -> "LiteDAN":
        X = np.asarray(
            X,
            dtype=np.float32,
        )

        y = np.asarray(y)

        domains = np.asarray(
            domains,
        )

        if (
            len(X) != len(y)
            or len(X) != len(domains)
        ):
            raise ValueError(
                "X, y and domains must have equal length"
            )

        if len(
            np.unique(y)
        ) < 2:
            raise ValueError(
                "At least two training classes "
                "are required"
            )

        if len(
            np.unique(domains)
        ) < 2:
            raise ValueError(
                "At least two source subjects/domains "
                "are required"
            )

        self.classes_ = np.unique(
            y
        )

        self.domain_ids_ = np.unique(
            domains
        )

        class_map = {
            value: idx
            for idx, value in enumerate(
                self.classes_
            )
        }

        domain_map = {
            value: idx
            for idx, value in enumerate(
                self.domain_ids_
            )
        }

        y_idx = np.asarray(
            [
                class_map[value]
                for value in y
            ],
            dtype=np.int64,
        )

        d_idx = np.asarray(
            [
                domain_map[value]
                for value in domains
            ],
            dtype=np.int64,
        )

        torch.manual_seed(
            self.seed
        )

        self.net = LiteDANNet(
            self.n_features,
            len(
                self.classes_
            ),
            len(
                self.domain_ids_
            ),
            self.hidden_dim,
            self.dropout,
        ).to(
            self.device
        )

        optimizer = torch.optim.Adam(
            self.net.parameters(),
            lr=self.learning_rate,
            weight_decay=self.weight_decay,
        )

        class_loss_fn = (
            nn.CrossEntropyLoss()
        )

        domain_loss_fn = (
            nn.CrossEntropyLoss()
        )

        dataset = TensorDataset(
            torch.from_numpy(X),
            torch.from_numpy(y_idx),
            torch.from_numpy(d_idx),
        )

        generator = (
            torch.Generator()
            .manual_seed(
                self.seed
            )
        )

        loader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            shuffle=True,
            generator=generator,
        )

        self.history = []

        best_loss = float(
            "inf"
        )

        stale = 0

        self.net.train()

        for epoch in range(
            self.epochs
        ):
            lambda_ = self.lambda_at(
                epoch
            )

            total = 0.0
            class_total = 0.0
            domain_total = 0.0
            batches = 0

            for (
                xb,
                yb,
                db,
            ) in loader:

                xb = xb.to(
                    self.device
                )

                yb = yb.to(
                    self.device
                )

                db = db.to(
                    self.device
                )

                optimizer.zero_grad(
                    set_to_none=True
                )

                (
                    class_logits,
                    domain_logits,
                ) = self.net(
                    xb,
                    lambda_,
                )

                class_loss = (
                    class_loss_fn(
                        class_logits,
                        yb,
                    )
                )

                if lambda_ > 0:
                    domain_loss = (
                        domain_loss_fn(
                            domain_logits,
                            db,
                        )
                    )
                else:
                    domain_loss = (
                        class_loss.new_zeros(
                            ()
                        )
                    )

                loss = (
                    class_loss
                    + domain_loss
                )

                loss.backward()

                optimizer.step()

                total += float(
                    loss.item()
                )

                class_total += float(
                    class_loss.item()
                )

                domain_total += float(
                    domain_loss.item()
                )

                batches += 1

            record = TrainingHistory(
                epoch=epoch + 1,
                lambda_=lambda_,
                total_loss=(
                    total
                    / max(
                        batches,
                        1,
                    )
                ),
                class_loss=(
                    class_total
                    / max(
                        batches,
                        1,
                    )
                ),
                domain_loss=(
                    domain_total
                    / max(
                        batches,
                        1,
                    )
                ),
            )

            self.history.append(
                record
            )

            if (
                self.early_stopping_patience
                is not None
            ):
                current = (
                    record.total_loss
                )

                if (
                    current
                    < best_loss - 1e-7
                ):
                    best_loss = current
                    stale = 0

                else:
                    stale += 1

                    if (
                        stale
                        >= self.early_stopping_patience
                    ):
                        break

        return self

    def _check_fitted(
        self,
    ) -> None:
        if (
            self.net is None
            or self.classes_ is None
        ):
            raise RuntimeError(
                "Model has not been fitted"
            )

    def predict(
        self,
        X: np.ndarray,
    ) -> np.ndarray:
        self._check_fitted()

        self.net.eval()

        tensor = (
            torch.from_numpy(
                np.asarray(
                    X,
                    dtype=np.float32,
                )
            ).to(
                self.device
            )
        )

        with torch.no_grad():
            logits, _ = self.net(
                tensor,
                0.0,
            )

        return self.classes_[
            logits.argmax(
                dim=1
            ).cpu().numpy()
        ]

    def predict_proba(
        self,
        X: np.ndarray,
    ) -> np.ndarray:
        self._check_fitted()

        self.net.eval()

        tensor = (
            torch.from_numpy(
                np.asarray(
                    X,
                    dtype=np.float32,
                )
            ).to(
                self.device
            )
        )

        with torch.no_grad():
            logits, _ = self.net(
                tensor,
                0.0,
            )

        return (
            torch.softmax(
                logits,
                dim=1,
            )
            .cpu()
            .numpy()
        )

    def embed(
        self,
        X: np.ndarray,
    ) -> np.ndarray:
        self._check_fitted()

        self.net.eval()

        tensor = (
            torch.from_numpy(
                np.asarray(
                    X,
                    dtype=np.float32,
                )
            ).to(
                self.device
            )
        )

        with torch.no_grad():
            return (
                self.net.encoder(
                    tensor
                )
                .cpu()
                .numpy()
            )

    def parameter_count(
        self,
    ) -> int:
        self._check_fitted()

        return self.net.parameter_count()