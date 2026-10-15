"""Integrity and consistency tests for the P6 C2 episode-level study (p6/c2_episode)."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import tarfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
C2 = ROOT / "p6" / "c2_episode"
C1 = ROOT / "p6" / "c_mi_r04_primary"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_freeze_manifest_matches_frozen_originals() -> None:
    freeze = json.loads((C2 / "registry" / "FREEZE_MANIFEST.json").read_text())
    frozen = C2 / "registry" / "frozen"
    assert freeze["protocol_id"] == "P6-C2-EPISODE-v1.0"
    for rel, digest in freeze["files"].items():
        name = Path(rel).name
        candidate = frozen / (name + ".frozen" if name.endswith(".py") else name)
        assert candidate.exists(), candidate
        assert sha(candidate) == digest, name


def test_top_level_protocol_files_equal_frozen_copies() -> None:
    for name in ("PROTOCOL_C2.md", "c2_design.yaml"):
        assert sha(C2 / name) == sha(C2 / "registry" / "frozen" / name)
    assert sha(C2 / "config" / "p6_c2_mysim.yaml") == sha(C2 / "registry" / "frozen" / "p6_c2_mysim.yaml")


def test_c2_controller_config_is_numerically_identical_to_c1() -> None:
    c2 = yaml.safe_load((C2 / "config" / "p6_c2_mysim.yaml").read_text())
    c1 = yaml.safe_load((C1 / "configs" / "p6_mi_r04_mysim.yaml").read_text())
    for section in ("control", "task", "simulation"):
        assert c2[section] == c1[section], section


def test_portable_reference_code_differs_from_frozen_only_in_path_constants() -> None:
    frozen = (C2 / "registry" / "frozen" / "c2_runner.py.frozen").read_text().splitlines()
    portable = (C2 / "scripts" / "c2_runner.py").read_text().splitlines()
    changed = [
        (a, b) for a, b in zip(frozen, portable[1:], strict=False) if a != b
    ]
    assert len(portable) == len(frozen) + 1  # one added header comment
    assert all(("MYO=" in a or "P6=" in a or a.startswith("import")) for a, _ in changed)


def test_analytic_closed_form_known_values() -> None:
    mod = _load(C2 / "scripts" / "c2_analytic_hold.py", "c2_analytic_hold")
    ok, bad = mod.expect(1.0, "cal")
    assert (ok, bad) == (1.0, 0.0)
    assert mod.expect(0.5, "cal") == (0.0, 0.0)
    ok, bad = mod.expect(0.8, "cal")
    assert abs(ok * (1 - bad) - 0.527) < 2e-3
    ok, bad = mod.expect(0.5, "flat")
    assert abs(ok * (1 - bad) - 0.242) < 2e-3


def test_emulator_design_and_counts() -> None:
    e = pd.read_csv(C2 / "results" / "emulator_episodes.csv")
    assert len(e) == 27_000
    cells = e.groupby(["regime", "q", "rho"]).size()
    assert len(cells) == 54 and set(cells.unique()) == {500}
    assert e.episode_id.is_unique


def test_ceiling_and_floor_cells() -> None:
    e = pd.read_csv(C2 / "results" / "emulator_episodes.csv")
    top = e[(e.regime == "cal") & (e.q == 1.0)]
    assert top.cue_correct_success.all()
    floor = e[(e.regime == "cal") & (e.q == 0.5)]
    assert floor.cue_correct_success.sum() == 0


def test_monte_carlo_agrees_with_closed_form_under_hold() -> None:
    mod = _load(C2 / "scripts" / "c2_analytic_hold.py", "c2_analytic_hold2")
    e = pd.read_csv(C2 / "results" / "emulator_episodes.csv")
    for (reg, q), d in e[e.rho == 1.0].groupby(["regime", "q"]):
        ok, bad = mod.expect(q, reg)
        p = ok * (1 - bad)
        se = max(p * (1 - p), 1e-9) ** 0.5 / len(d) ** 0.5
        assert abs(d.cue_correct_success.mean() - p) < 4 * se + 1e-9, (reg, q)


@pytest.mark.parametrize("fname", ["emulator_episodes.csv", "real_episodes.csv"])
def test_endpoint_definition_is_internally_consistent(fname: str) -> None:
    d = pd.read_csv(C2 / "results" / fname)
    if "arm" in d:
        d = d[d.arm.isin(["R0", "R1"])]
    onset_ok = d.grasp_onset.between(4.0, 5.5)
    expected = d.task_completion.astype(bool) & onset_ok & ~d.false_grasp.astype(bool)
    assert (expected.values == d.cue_correct_success.astype(bool).values).all()


def test_real_episode_counts_and_oracle() -> None:
    r = pd.read_csv(C2 / "results" / "real_episodes.csv")
    assert (r.arm == "R0").sum() == 560 and (r.arm == "R1").sum() == 19_750
    oracle = r[(r.arm == "R0") & (r.decoder == "ORACLE")]
    assert len(oracle) == 140 and oracle.cue_correct_success.all()
    assert (C2 / "results" / "sensitivity_episodes.csv").exists()
    s = pd.read_csv(C2 / "results" / "sensitivity_episodes.csv")
    assert len(s) == 25_600


def test_registered_hypotheses_recorded() -> None:
    a = json.loads((C2 / "results" / "ANALYSIS.json").read_text())
    assert (C2 / "results" / "PREFLIGHT.json").exists()
    assert a["schema"] == "P6-C2-ANALYSIS-v1"
    assert (C2 / "results" / "ANALYTIC_CROSSCHECK.json").exists()
    assert json.loads((C2 / "results" / "ANALYTIC_CROSSCHECK.json").read_text())["pass"] is True


def test_raw_archives_match_recorded_hashes() -> None:
    sums = (C2 / "raw_archives" / "SHA256SUMS.txt").read_text().splitlines()
    assert len(sums) == 4
    for line in sums:
        digest, name = line.split()
        assert sha(C2 / "raw_archives" / name) == digest


def test_oracle_replay_runs_in_myosim_when_available(tmp_path: Path) -> None:
    pytest.importorskip("myosim")
    from myosim.core.config import load_config
    from myosim.experiments.task_runner import PickPlaceExperimentRunner
    from myosim.signals.replay import CsvIntentReplay

    r = pd.read_csv(C2 / "results" / "real_episodes.csv")
    eid = r[(r.arm == "R0") & (r.decoder == "ORACLE")].episode_id.iloc[0]
    with tarfile.open(C2 / "raw_archives" / "P6_C2_replay_csv.tar.gz") as tf:
        member = tf.extractfile(f"replay_csv/R0/{eid}.csv")
        assert member is not None
        csv = tmp_path / f"{eid}.csv"
        csv.write_bytes(member.read())
    cfg = load_config(C2 / "config" / "p6_c2_mysim.yaml")
    result = PickPlaceExperimentRunner(cfg, Path(__import__("myosim").__file__).parents[2]).run(CsvIntentReplay(csv)).to_dict()
    assert result["task_metrics"]["final_state"] == "COMPLETE"
    assert np.isfinite(result["task_metrics"]["path_length_m"])
