"""Thin artifact- and mapping-based adapters for independently runnable systems."""

from .biosignal_fm import (
    representation_from_biosignal_fm_export,
    signal_from_biosignal_fm_export,
)
from .common import AdapterError
from .eeg import EEGEpochSpec, EEGPreprocessingSpec, epoch_signal_records_from_mne
from .myoadapt import ImportedRunBundle, import_myoadapt_manifest
from .myocontrol import intent_from_myocontrol_prediction
from .myosim import MyoSimIntentPayload, intent_to_myosim_event, intent_to_myosim_payload

__all__ = [
    "AdapterError",
    "EEGEpochSpec",
    "EEGPreprocessingSpec",
    "ImportedRunBundle",
    "MyoSimIntentPayload",
    "epoch_signal_records_from_mne",
    "import_myoadapt_manifest",
    "intent_from_myocontrol_prediction",
    "intent_to_myosim_event",
    "intent_to_myosim_payload",
    "representation_from_biosignal_fm_export",
    "signal_from_biosignal_fm_export",
]
