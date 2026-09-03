from __future__ import annotations

import pytest

from research_core.adapters import AdapterError, EEGEpochSpec, EEGPreprocessingSpec


def test_eeg_preprocessing_spec_requires_explicit_safe_parameters() -> None:
    spec = EEGPreprocessingSpec(
        eeg_channels=("C3", "C4", "Cz"),
        reference="average",
        l_freq_hz=8.0,
        h_freq_hz=30.0,
        notch_freq_hz=(50.0,),
        resample_hz=125.0,
    )
    assert spec.reference == "average"
    assert spec.eeg_channels == ("C3", "C4", "Cz")

    with pytest.raises(AdapterError, match="less than"):
        EEGPreprocessingSpec(
            eeg_channels=("C3",),
            reference="average",
            l_freq_hz=30.0,
            h_freq_hz=8.0,
        )
    with pytest.raises(AdapterError, match="non-empty and unique"):
        EEGPreprocessingSpec(
            eeg_channels=("C3", "C3"),
            reference="average",
            l_freq_hz=None,
            h_freq_hz=None,
        )


def test_eeg_epoch_spec_requires_declared_events_and_valid_time_bounds() -> None:
    epoch = EEGEpochSpec(
        event_id={"left_hand": 1, "right_hand": 2},
        tmin_seconds=0.5,
        tmax_seconds=3.5,
        baseline=None,
    )
    assert epoch.event_id == {"left_hand": 1, "right_hand": 2}

    with pytest.raises(AdapterError, match="less than"):
        EEGEpochSpec(event_id={"left_hand": 1}, tmin_seconds=3.0, tmax_seconds=1.0)
    with pytest.raises(AdapterError, match="must not be empty"):
        EEGEpochSpec(event_id={}, tmin_seconds=0.0, tmax_seconds=1.0)
