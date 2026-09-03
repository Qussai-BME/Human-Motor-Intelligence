"""Optional MNE-facing EEG edge adapter for authorized external research data.

This module contains no BCI dataset files and no benchmark result. It exposes a
protocol-declared preprocessing and epoching pathway that accepts a caller-owned
MNE Raw object, then emits umbrella `SignalRecord` metadata references. MNE is
imported only when this optional pathway is invoked.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import isfinite
from typing import Any

from research_core.contracts import EvidenceClass, SignalRecord
from research_core.contracts.base import ContractValidationError, validate_identifier, validate_non_empty, validate_uri_or_path

from .common import AdapterError, provenance_from_export


ADAPTER_ID = "mne-eeg-edge"
ADAPTER_VERSION = "1.0.0"


@dataclass(frozen=True, slots=True)
class EEGPreprocessingSpec:
    """Explicit, protocol-owned EEG preprocessing choices; no hidden defaults."""

    eeg_channels: tuple[str, ...]
    reference: str | tuple[str, ...]
    l_freq_hz: float | None
    h_freq_hz: float | None
    notch_freq_hz: tuple[float, ...] = ()
    resample_hz: float | None = None
    reject_by_annotation: bool = True

    def __post_init__(self) -> None:
        channels = tuple(validate_non_empty(channel, "eeg_channels entry") for channel in self.eeg_channels)
        if not channels or len(set(channels)) != len(channels):
            raise AdapterError("eeg_channels must be non-empty and unique")
        object.__setattr__(self, "eeg_channels", channels)
        if isinstance(self.reference, str):
            if self.reference not in {"average", "none"}:
                raise AdapterError("reference must be 'average', 'none', or an explicit channel tuple")
        else:
            reference = tuple(validate_non_empty(channel, "reference channel") for channel in self.reference)
            if not reference:
                raise AdapterError("explicit reference channel tuple must not be empty")
            object.__setattr__(self, "reference", reference)
        for field_name in ("l_freq_hz", "h_freq_hz", "resample_hz"):
            value = getattr(self, field_name)
            if value is not None and (not isfinite(float(value)) or float(value) <= 0):
                raise AdapterError(f"{field_name} must be positive when supplied")
            if value is not None:
                object.__setattr__(self, field_name, float(value))
        if self.l_freq_hz is not None and self.h_freq_hz is not None and self.l_freq_hz >= self.h_freq_hz:
            raise AdapterError("l_freq_hz must be less than h_freq_hz")
        notch = tuple(float(value) for value in self.notch_freq_hz)
        if any(not isfinite(value) or value <= 0 for value in notch):
            raise AdapterError("notch_freq_hz entries must be positive finite values")
        object.__setattr__(self, "notch_freq_hz", notch)


@dataclass(frozen=True, slots=True)
class EEGEpochSpec:
    """Explicit event/epoch semantics required by an EEG protocol."""

    event_id: Mapping[str, int]
    tmin_seconds: float
    tmax_seconds: float
    baseline: tuple[float | None, float | None] | None = None

    def __post_init__(self) -> None:
        if not self.event_id:
            raise AdapterError("event_id mapping must not be empty")
        event_ids: dict[str, int] = {}
        for label, code in self.event_id.items():
            normalized = validate_identifier(str(label), "event_id label")
            if not isinstance(code, int) or isinstance(code, bool):
                raise AdapterError("event_id codes must be integers")
            event_ids[normalized] = code
        object.__setattr__(self, "event_id", event_ids)
        if not isfinite(self.tmin_seconds) or not isfinite(self.tmax_seconds) or self.tmin_seconds >= self.tmax_seconds:
            raise AdapterError("epoch tmin_seconds must be finite and less than tmax_seconds")
        if self.baseline is not None:
            if len(self.baseline) != 2:
                raise AdapterError("baseline must contain exactly two bounds")
            lower, upper = self.baseline
            if lower is not None and not isfinite(lower):
                raise AdapterError("baseline lower bound must be finite or None")
            if upper is not None and not isfinite(upper):
                raise AdapterError("baseline upper bound must be finite or None")
            if lower is not None and upper is not None and lower > upper:
                raise AdapterError("baseline lower bound must not exceed upper bound")


def epoch_signal_records_from_mne(
    raw: Any,
    events: Any,
    *,
    preprocessing: EEGPreprocessingSpec,
    epoching: EEGEpochSpec,
    recording_uri: str,
    signal_id_prefix: str,
    subject_id: str,
    session_id: str,
    dataset_id: str,
    dataset_version: str,
    license_id: str,
    origin: EvidenceClass = EvidenceClass.REAL,
) -> tuple[SignalRecord, ...]:
    """Apply declared MNE steps and return canonical references for each retained epoch.

    The caller owns the input Raw object and resulting data storage. `recording_uri`
    must identify the authorized external recording/epoch store. This adapter
    never copies data into the registry or marks an experiment benchmark eligible.
    """
    try:
        import mne  # type: ignore[import-not-found]
    except ImportError as exc:
        raise AdapterError("MNE is required for EEG preprocessing; install the optional EEG environment") from exc
    if origin is not EvidenceClass.REAL:
        raise AdapterError("MNE EEG edge path is for authorized real-data execution; synthetic work should use contract fixtures")
    try:
        validated_uri = validate_uri_or_path(recording_uri, "recording_uri")
        work = raw.copy().pick(list(preprocessing.eeg_channels))
        if preprocessing.reference == "average":
            work.set_eeg_reference("average", projection=False)
        elif preprocessing.reference != "none":
            work.set_eeg_reference(list(preprocessing.reference), projection=False)
        if preprocessing.notch_freq_hz:
            work.notch_filter(list(preprocessing.notch_freq_hz))
        if preprocessing.l_freq_hz is not None or preprocessing.h_freq_hz is not None:
            work.filter(preprocessing.l_freq_hz, preprocessing.h_freq_hz)
        if preprocessing.resample_hz is not None:
            work.resample(preprocessing.resample_hz)
        epochs = mne.Epochs(
            work,
            events,
            event_id=dict(epoching.event_id),
            tmin=epoching.tmin_seconds,
            tmax=epoching.tmax_seconds,
            baseline=epoching.baseline,
            preload=True,
            reject_by_annotation=preprocessing.reject_by_annotation,
            verbose=False,
        )
    except Exception as exc:  # MNE exposes several data-format-specific exception types.
        raise AdapterError(f"MNE preprocessing/epoching failed: {exc}") from exc
    provenance = provenance_from_export(
        {
            "origin": "real",
            "source_dataset_id": dataset_id,
            "dataset_version": dataset_version,
            "source_uri": validated_uri,
            "license_id": license_id,
            "details": {
                "benchmark_eligible": False,
                "mne_adapter": ADAPTER_ID,
                "preprocessing_must_be_registered": True,
            },
        },
        adapter_id=ADAPTER_ID,
        adapter_version=ADAPTER_VERSION,
    )
    sample_count = len(epochs.times)
    channel_names = tuple(str(name) for name in epochs.ch_names)
    sampling_rate = float(epochs.info["sfreq"])
    records: list[SignalRecord] = []
    for index, event_code in enumerate(epochs.events[:, 2]):
        label = next((name for name, code in epoching.event_id.items() if code == int(event_code)), "unknown")
        records.append(
            SignalRecord(
                signal_id=f"{validate_identifier(signal_id_prefix, 'signal_id_prefix')}-epoch-{index:04d}",
                modality="eeg",
                sampling_rate_hz=sampling_rate,
                channel_names=channel_names,
                sample_count=sample_count,
                provenance=provenance,
                data_uri=f"{validated_uri}#epoch={index}",
                units=("V",),
                subject_id=subject_id,
                session_id=session_id,
                recording_id=signal_id_prefix,
                task_id=label,
                window_id=f"epoch-{index:04d}",
                annotations={
                    "event_code": int(event_code),
                    "event_label": label,
                    "preprocessing_spec": {
                        "reference": preprocessing.reference,
                        "l_freq_hz": preprocessing.l_freq_hz,
                        "h_freq_hz": preprocessing.h_freq_hz,
                        "notch_freq_hz": preprocessing.notch_freq_hz,
                        "resample_hz": preprocessing.resample_hz,
                    },
                    "epoch_spec": {
                        "tmin_seconds": epoching.tmin_seconds,
                        "tmax_seconds": epoching.tmax_seconds,
                        "baseline": epoching.baseline,
                    },
                },
            )
        )
    if not records:
        raise AdapterError("MNE epoching retained zero epochs; no signal records were created")
    return tuple(records)
