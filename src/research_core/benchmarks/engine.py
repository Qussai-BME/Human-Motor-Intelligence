"""Protocol-governed benchmark aggregation with subject-level inference defaults."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from math import isfinite, sqrt
from statistics import mean, stdev
from typing import Any

from research_core.contracts import ExperimentRecord, ensure_real_benchmark_records
from research_core.contracts.base import ContractValidationError, json_safe, validate_identifier


class BenchmarkError(RuntimeError):
    """Raised for invalid, incomparable, or scientifically ineligible benchmark inputs."""


@dataclass(frozen=True, slots=True)
class SubjectMetricObservation:
    """A single measured metric at the protocol-defined subject inference unit."""

    run_id: str
    protocol_id: str
    dataset_id: str
    model_id: str
    subject_id: str
    metric_name: str
    value: float

    def __post_init__(self) -> None:
        for field_name in ("run_id", "protocol_id", "dataset_id", "model_id", "subject_id", "metric_name"):
            object.__setattr__(self, field_name, validate_identifier(getattr(self, field_name), field_name))
        numeric = float(self.value)
        if not isfinite(numeric):
            raise BenchmarkError("subject metric value must be finite")
        object.__setattr__(self, "value", numeric)


@dataclass(frozen=True, slots=True)
class ModelMetricSummary:
    """A descriptive summary across subjects, not an unqualified scientific conclusion."""

    model_id: str
    metric_name: str
    subject_count: int
    mean: float
    standard_deviation: float | None
    subject_values: tuple[tuple[str, float], ...]

    def to_dict(self) -> dict[str, Any]:
        return json_safe(asdict(self))  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """A protocol-identified benchmark result bundle suitable for factual assets."""

    benchmark_id: str
    protocol_id: str
    dataset_id: str
    metric_name: str
    summaries: tuple[ModelMetricSummary, ...]
    comparison_notes: tuple[str, ...]
    statistics: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return json_safe(asdict(self))  # type: ignore[return-value]


class BenchmarkEngine:
    """Aggregate imported run measurements only where the protocol permits comparison."""

    @staticmethod
    def summarize(
        *,
        benchmark_id: str,
        experiments: tuple[ExperimentRecord, ...],
        observations: tuple[SubjectMetricObservation, ...],
        metric_name: str,
    ) -> BenchmarkResult:
        """Create a subject-level descriptive benchmark with optional valid tests.

        The function does not fit models, manufacture observations, pool raw
        windows, or declare significance merely because values are available.
        It requires real-data eligible experiment records and exact protocol,
        dataset, and metric agreement.
        """
        try:
            eligible_runs = ensure_real_benchmark_records(experiments)
        except ContractValidationError as exc:
            raise BenchmarkError(str(exc)) from exc
        if not observations:
            raise BenchmarkError("at least one subject-level observation is required")
        benchmark_id = validate_identifier(benchmark_id, "benchmark_id")
        metric_name = validate_identifier(metric_name, "metric_name")
        protocol_ids = {run.protocol_id for run in eligible_runs}
        dataset_ids = {run.dataset_id for run in eligible_runs}
        if len(protocol_ids) != 1:
            raise BenchmarkError("benchmark aggregation requires exactly one protocol_id")
        if len(dataset_ids) != 1:
            raise BenchmarkError("benchmark aggregation requires exactly one dataset_id")
        protocol_id = next(iter(protocol_ids))
        dataset_id = next(iter(dataset_ids))
        allowed_runs = {run.run_id: run for run in eligible_runs}
        grouped: dict[str, dict[str, float]] = defaultdict(dict)
        participating_run_ids: set[str] = set()
        for observation in observations:
            if observation.metric_name != metric_name:
                raise BenchmarkError("all observations must use the requested metric_name")
            if observation.protocol_id != protocol_id or observation.dataset_id != dataset_id:
                raise BenchmarkError("observation protocol_id and dataset_id must match registered runs")
            if observation.run_id not in allowed_runs:
                raise BenchmarkError(f"observation references unknown or ineligible run {observation.run_id}")
            run = allowed_runs[observation.run_id]
            if observation.model_id != run.model_id:
                raise BenchmarkError("observation model_id must match its registered run")
            if observation.subject_id in grouped[observation.model_id]:
                raise BenchmarkError(
                    "one subject-level value per model is required; aggregate windows upstream under the protocol"
                )
            grouped[observation.model_id][observation.subject_id] = observation.value
            participating_run_ids.add(observation.run_id)
        unused_runs = set(allowed_runs) - participating_run_ids
        if unused_runs:
            raise BenchmarkError(
                "each supplied experiment must contribute observations; omit unrelated runs or add their subject-level values"
            )
        summaries: list[ModelMetricSummary] = []
        for model_id, subject_values in sorted(grouped.items()):
            values = list(subject_values.values())
            summaries.append(
                ModelMetricSummary(
                    model_id=model_id,
                    metric_name=metric_name,
                    subject_count=len(values),
                    mean=mean(values),
                    standard_deviation=stdev(values) if len(values) > 1 else None,
                    subject_values=tuple(sorted(subject_values.items())),
                )
            )
        comparison_notes = BenchmarkEngine._comparison_notes(grouped)
        statistics = BenchmarkEngine._optional_statistics(grouped)
        return BenchmarkResult(
            benchmark_id=benchmark_id,
            protocol_id=protocol_id,
            dataset_id=dataset_id,
            metric_name=metric_name,
            summaries=tuple(summaries),
            comparison_notes=comparison_notes,
            statistics=statistics,
        )

    @staticmethod
    def _comparison_notes(grouped: dict[str, dict[str, float]]) -> tuple[str, ...]:
        """Describe comparability without treating unequal folds as paired evidence."""
        subject_sets = {model_id: set(values) for model_id, values in grouped.items()}
        if len(subject_sets) < 2:
            return (
                "Only one model is present; no inter-model statistical comparison was attempted.",
                "Values are aggregated at the subject level.",
            )
        first_set = next(iter(subject_sets.values()))
        if all(subjects == first_set for subjects in subject_sets.values()):
            return (
                "All compared models have matched subject-level observations.",
                "Paired comparison may be considered only if the registered protocol authorizes it.",
            )
        return (
            "Compared models do not share an identical subject set.",
            "No paired statistical comparison was attempted; inspect protocol and coverage before inference.",
        )

    @staticmethod
    def _optional_statistics(grouped: dict[str, dict[str, float]]) -> dict[str, Any]:
        """Run only a conservative Friedman test when inputs are paired and SciPy is installed."""
        if len(grouped) < 3:
            return {
                "status": "not_run",
                "reason": "Friedman requires at least three matched model conditions; no automatic alternate test selected.",
            }
        common_subjects = set.intersection(*(set(values) for values in grouped.values()))
        if not common_subjects or any(set(values) != common_subjects for values in grouped.values()):
            return {
                "status": "not_run",
                "reason": "Friedman requires identical paired subject coverage across all compared models.",
            }
        try:
            from scipy.stats import friedmanchisquare  # type: ignore[import-not-found]
        except ImportError:
            return {
                "status": "not_run",
                "reason": "SciPy is not installed; no statistical result was generated.",
            }
        ordered_subjects = sorted(common_subjects)
        arrays = [[values[subject] for subject in ordered_subjects] for _, values in sorted(grouped.items())]
        statistic, p_value = friedmanchisquare(*arrays)
        return {
            "status": "computed",
            "test": "friedman",
            "subjects": len(ordered_subjects),
            "models": [model_id for model_id, _ in sorted(grouped.items())],
            "statistic": float(statistic),
            "p_value": float(p_value),
            "interpretation": "Descriptive test output only; protocol-authorized post-hoc analysis and human review remain required.",
        }
