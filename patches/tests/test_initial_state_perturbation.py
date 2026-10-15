from dataclasses import replace
from pathlib import Path

from myosim.core.config import InitialStatePerturbationConfig, load_config
from myosim.experiments.task_runner import PickPlaceExperimentRunner
from myosim.signals.replay import CsvIntentReplay


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
REPLAY = REPOSITORY_ROOT / "examples" / "intents" / "pick_place_replay.csv"


def _config(seed: int, *, enabled: bool):
    base = load_config(REPOSITORY_ROOT / "configs" / "benchmarks.yaml")
    initial = (
        InitialStatePerturbationConfig(
            enabled=True,
            distribution_id="uniform_forearm_xy_v1",
            forearm_x_offset_range_m=(0.0, 0.020),
            forearm_y_offset_range_m=(-0.015, 0.015),
        )
        if enabled
        else InitialStatePerturbationConfig()
    )
    return replace(base, run=replace(base.run, seed=seed), initial_state=initial)


def test_disabled_initial_state_factor_is_inert() -> None:
    result = PickPlaceExperimentRunner(_config(20260822, enabled=False), REPOSITORY_ROOT).run(CsvIntentReplay(REPLAY))
    assert result.initial_state["enabled"] is False
    assert result.initial_state["distribution_id"] == "none"
    assert result.initial_state["initial_joint_offsets"] == {}
    assert result.task_metrics.success


def test_declared_seeds_produce_distinct_bounded_initial_states() -> None:
    first = PickPlaceExperimentRunner(_config(20260901, enabled=True), REPOSITORY_ROOT).run(CsvIntentReplay(REPLAY))
    second = PickPlaceExperimentRunner(_config(20260902, enabled=True), REPOSITORY_ROOT).run(CsvIntentReplay(REPLAY))
    for result in (first, second):
        offsets = result.initial_state["initial_joint_offsets"]
        assert 0.0 <= offsets["forearm_x"] <= 0.020
        assert -0.015 <= offsets["forearm_y"] <= 0.015
        assert result.initial_state["enabled"] is True
        assert result.initial_state["distribution_id"] == "uniform_forearm_xy_v1"
        assert result.initial_state["initial_named_joint_positions"]["forearm_x"] == offsets["forearm_x"]
        assert result.initial_state["initial_named_joint_positions"]["forearm_y"] == offsets["forearm_y"]
    assert first.initial_state["initial_joint_offsets"] != second.initial_state["initial_joint_offsets"]
    assert first.initial_state["initial_qpos"] != second.initial_state["initial_qpos"]
