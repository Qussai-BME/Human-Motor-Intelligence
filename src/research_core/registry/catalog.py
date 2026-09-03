"""Curated registry seed catalog.

Entries record only verified public metadata or declared engineering boundaries.
They never download data or imply that a listed dataset has been benchmarked.
"""

from __future__ import annotations

from dataclasses import replace

from research_core.contracts import ContractRecord

from .models import (
    BenchmarkDefinition,
    DatasetAccess,
    DatasetDefinition,
    ModelDefinition,
    ProjectDefinition,
    ProtocolDefinition,
    ProtocolStatus,
    RegistryDefinition,
    StatisticalUnit,
)
from .store import LocalResearchRegistry, StoredEntry


SOURCE_NOTES = "docs/DATASET_SOURCE_NOTES.md"


def project_entries() -> tuple[ProjectDefinition, ...]:
    """Return ownership-boundary entries for the umbrella and mature systems."""
    return (
        ProjectDefinition(
            entity_id="human-motor-intelligence",
            name="Human Motor Intelligence Research Stack",
            role="Thin contract, registry, benchmark, provenance, adapter, and reporting infrastructure.",
            repository_reference=".",
            license_id="Apache-2.0",
            integration_boundary="Owns only cross-project infrastructure; does not vendor or replace child systems.",
        ),
        ProjectDefinition(
            entity_id="biosignal-fm-v4",
            name="BioSignal-FM V4",
            role="Multimodal biosignal representation and protocol-aware research framework.",
            repository_reference="external/BioSignal-FM-V4",
            license_id="Apache-2.0",
            integration_boundary="Exports canonical signal/representation/provenance artifacts; implementation remains independent.",
        ),
        ProjectDefinition(
            entity_id="myoadapt-v2",
            name="MyoAdapt v2",
            role="EMG cross-subject generalisation, adaptation, evaluation, and reproducibility platform.",
            repository_reference="https://github.com/Qussai-BME/MyoAdapt",
            license_id="Apache-2.0",
            integration_boundary="Exports manifests, result artifacts, and model/dataset cards; Paper 3 is import-only and execution-locked.",
        ),
        ProjectDefinition(
            entity_id="myocontrol-v05",
            name="MyoControl",
            role="EMG motor-intent decoder and deployment baseline.",
            repository_reference="https://github.com/Qussai-BME/myocontrol",
            license_id="MIT",
            integration_boundary="Provides serialized decoder predictions; feature, training, edge, and UI implementations remain independent.",
        ),
        ProjectDefinition(
            entity_id="myosim-v011",
            name="MyoSim V1.1",
            role="Software-only replay-to-virtual-prosthetic-control simulation baseline.",
            repository_reference="external/MyoSim-V1.1",
            license_id="Apache-2.0",
            integration_boundary="Receives validated discrete intent events and emits simulator-owned task/control/provenance artifacts.",
        ),
    )


def dataset_entries() -> tuple[DatasetDefinition, ...]:
    """Return dataset cards with provenance and access metadata, never raw datasets."""
    ninapro_common = {
        "source_url": "https://ninapro.hevs.ch/",
        "citation": "Use the database-specific article linked by the official NinaPro portal; see docs/DATASET_SOURCE_NOTES.md.",
        "license_access": DatasetAccess.REGISTRATION_REQUIRED,
        "sampling_rate_hz": 2000.0,
        "channel_description": "Up to 12 Delsys Trigno sEMG channels; source-specific multimodal variables remain external.",
        "session_description": "Dataset-defined exercises/repetitions; preserve source subject, exercise, repetition, and relabelled stimulus identifiers.",
        "label_schema": {"source_of_truth": "official NinaPro dataset variables and cited paper"},
        "canonicalization_rules": (
            "Retain source subject IDs without relabelling.",
            "Register the source label field used, including stimulus versus restimulus where applicable.",
            "Fit all transformations only on protocol-authorized training data.",
        ),
        "version": "official-external-access-2026",
    }
    return (
        DatasetDefinition(
            entity_id="ninapro-db2",
            name="NinaPro DB2",
            modality="emg",
            task_description="Hand-movement classification or regression research with 49 hand movements plus rest context.",
            subject_count=40,
            known_limitations=(
                "Raw data requires external authorized acquisition and is not stored by this repository.",
                "A registered protocol must define the label field, exercises, windowing, and split semantics.",
            ),
            **ninapro_common,
        ),
        DatasetDefinition(
            entity_id="ninapro-db3",
            name="NinaPro DB3",
            modality="emg",
            task_description="Transradial-amputee hand-movement classification or regression research with up to 49 movements plus rest.",
            subject_count=11,
            known_limitations=(
                "The dataset population is small and task/subject availability must be represented in split manifests.",
                "Raw data requires external authorized acquisition and is not stored by this repository.",
            ),
            **ninapro_common,
        ),
        DatasetDefinition(
            entity_id="ninapro-db7",
            name="NinaPro DB7",
            modality="emg",
            task_description="Hand-movement classification or regression research in intact and transradial-amputee participants.",
            subject_count=22,
            known_limitations=(
                "One amputee participant has reduced final-exercise class availability; splits and per-subject labels must preserve this condition.",
                "Raw data requires external authorized acquisition and is not stored by this repository.",
            ),
            **ninapro_common,
        ),
        DatasetDefinition(
            entity_id="bci-competition-iv-2a",
            name="BCI Competition IV Dataset 2a",
            modality="eeg",
            source_url="https://www.bbci.de/competition/iv/",
            citation="BCI Competition IV dataset 2a official description and originating-group citation requirement; see docs/DATASET_SOURCE_NOTES.md.",
            license_access=DatasetAccess.REGISTRATION_REQUIRED,
            sampling_rate_hz=250.0,
            channel_description="22 EEG channels and three EOG channels; record EOG handling explicitly in each protocol.",
            task_description="Four-class cued motor imagery: left hand, right hand, feet, and tongue.",
            subject_count=9,
            session_description="Dataset-defined training/evaluation sessions; a protocol must state whether and how labels are used.",
            label_schema={"classes": ["left_hand", "right_hand", "feet", "tongue"]},
            canonicalization_rules=(
                "Maintain subject and session separation.",
                "Specify epoch boundaries and EOG policy in the protocol.",
                "Fit transformations using training partitions only.",
            ),
            known_limitations=(
                "No dataset files are included; access/citation obligations remain with the researcher.",
                "The registry has no real EEG benchmark result until an authorized run is registered.",
            ),
            version="official-external-access-2026",
        ),
        DatasetDefinition(
            entity_id="way-eeg-gal",
            name="WAY-EEG-GAL",
            modality="eeg",
            source_url="https://doi.org/10.6084/m9.figshare.c.988376.v2",
            citation="Luciw, Jarocka, and Edin (2014), WAY-EEG-GAL collection; see docs/DATASET_SOURCE_NOTES.md.",
            license_access=DatasetAccess.OPEN,
            sampling_rate_hz=None,
            channel_description="32 EEG channels, five EMG channels, event times, kinematics, and force/torque; verify selected release item metadata before use.",
            task_description="Grasp-and-lift trials supporting sensation, intention, and action decoding research.",
            subject_count=12,
            session_description="3,936 total trials; register participant-level availability and alignment choices before fusion work.",
            label_schema={"source_of_truth": "event times and behavioural measures from selected dataset release"},
            canonicalization_rules=(
                "Register the exact Figshare release/item and selected event definition.",
                "Synchronize EEG and EMG using a documented, testable alignment procedure.",
                "Define missing-modality handling before model selection.",
            ),
            known_limitations=(
                "Sampling-rate and item-specific channel metadata must be confirmed from the selected downloaded release before execution.",
                "No EEG–EMG fusion benchmark or transfer claim exists in this repository.",
            ),
            version="figshare-collection-v2",
        ),
        DatasetDefinition(
            entity_id="mit-bih-arrhythmia-v1",
            name="MIT-BIH Arrhythmia Database v1.0.0",
            modality="ecg",
            source_url="https://doi.org/10.13026/C2F305",
            citation="Moody and Mark; MIT-BIH Arrhythmia Database v1.0.0, PhysioNet; see docs/DATASET_SOURCE_NOTES.md.",
            license_access=DatasetAccess.OPEN,
            sampling_rate_hz=360.0,
            channel_description="Two-channel ambulatory ECG excerpts.",
            task_description="Arrhythmia detector evaluation and ECG methodology research.",
            subject_count=47,
            session_description="48 half-hour recordings; record-level splits must remain explicit.",
            label_schema={"source_of_truth": "MIT-BIH annotation files"},
            canonicalization_rules=(
                "Register record-level train/test separation.",
                "Preserve source annotation semantics and record identifiers.",
            ),
            known_limitations=(
                "ECG support is registry-ready; no umbrella ECG benchmark is implemented in the MVP.",
            ),
            version="1.0.0",
        ),
    )


def protocol_entries() -> tuple[ProtocolDefinition, ...]:
    """Return explicitly governed protocols. Paper 3 is intentionally excluded."""
    return (
        ProtocolDefinition(
            entity_id="emg-loso-v1",
            name="EMG LOSO",
            version="1.0.0",
            modalities=("emg",),
            split_strategy="leave-one-subject-out",
            train_validation_test_semantics="One subject is held out for testing; all fitting, selection, tuning, and calibration operate only within designated training-side partitions.",
            leakage_constraints=(
                "No held-out subject windows contribute to scaler fitting.",
                "No held-out subject windows contribute to feature selection or hyperparameter selection.",
                "No target labels are available to adaptation unless a separately named protocol explicitly allows it.",
                "Statistics aggregate at subject level, never at window level.",
            ),
            preprocessing={"owner": "source project configuration", "fit_scope": "training_only"},
            feature_selection={"owner": "source project configuration", "fit_scope": "training_only"},
            model_selection={"policy": "training-side validation only"},
            metrics=("accuracy", "macro_f1", "active_only_f1", "rest_recall"),
            statistical_unit=StatisticalUnit.SUBJECT,
            seeds=(42,),
            hyperparameter_policy="Freeze before testing or select only with training-side validation; record all resolved settings.",
            status=ProtocolStatus.ACTIVE,
            limitations=(
                "This generic protocol does not alter or substitute Paper 3's locked protocol.",
                "Dataset-specific class availability and label choices must be recorded per run.",
            ),
        ),
        ProtocolDefinition(
            entity_id="eeg-loso-v1",
            name="EEG LOSO",
            version="1.0.0",
            modalities=("eeg",),
            split_strategy="leave-one-subject-out",
            train_validation_test_semantics="A held-out participant contributes no fitting, selection, normalization, or model-choice information.",
            leakage_constraints=(
                "Fit preprocessing and normalization on training participants only.",
                "Define epochs/windows before inspection of held-out participant labels.",
                "Aggregate inferential statistics at participant level.",
                "Do not infer cross-subject transfer from a synthetic smoke run.",
            ),
            preprocessing={"adapter": "MNE-based edge adapter", "fit_scope": "training_only", "status": "planned"},
            feature_selection={"policy": "baseline-specific and training_only"},
            model_selection={"policy": "training-side validation only"},
            metrics=("accuracy", "macro_f1", "balanced_accuracy"),
            statistical_unit=StatisticalUnit.SUBJECT,
            seeds=(42,),
            hyperparameter_policy="Begin with predeclared linear/LDA/spectral baselines; introduce complex models only with registered justification.",
            status=ProtocolStatus.DRAFT,
            limitations=(
                "No authorized BCI IV-2a execution or real EEG benchmark is registered yet.",
            ),
        ),
        ProtocolDefinition(
            entity_id="eeg-mi-v1",
            name="EEG Motor Imagery",
            version="1.0.0",
            modalities=("eeg",),
            split_strategy="dataset-defined-subject-aware",
            train_validation_test_semantics="Train/validation/test semantics must be instantiated per dataset and preserved in each run manifest.",
            leakage_constraints=(
                "Preprocessing fitting scope must be declared.",
                "Subject/session split policy must be declared before evaluation.",
                "No pooled-window inference is reported as participant-level evidence.",
            ),
            preprocessing={"adapter": "MNE-based edge adapter", "status": "planned"},
            feature_selection={"policy": "registered per baseline"},
            model_selection={"policy": "registered per run"},
            metrics=("accuracy", "macro_f1", "balanced_accuracy"),
            statistical_unit=StatisticalUnit.SUBJECT,
            seeds=(42,),
            hyperparameter_policy="Register selected baseline configuration before final evaluation.",
            status=ProtocolStatus.DRAFT,
            limitations=("This scaffold does not itself define a completed EEG benchmark.",),
        ),
        ProtocolDefinition(
            entity_id="emg-eeg-fusion-v1",
            name="EMG EEG Fusion",
            version="1.0.0",
            modalities=("emg", "eeg"),
            split_strategy="participant-aware-synchronized",
            train_validation_test_semantics="All modality alignment, split, and missingness decisions are fixed before final evaluation.",
            leakage_constraints=(
                "Synchronize modalities using only declared timing data.",
                "Fit each modality-specific preprocessing stage only on training data.",
                "Evaluate EEG-only, EMG-only, fused, missing-EEG, and missing-EMG conditions under matching splits.",
                "Use participant or protocol-defined trial as the statistical unit, never raw windows by default.",
            ),
            preprocessing={"alignment": "explicit adapter required", "fit_scope": "training_only"},
            feature_selection={"policy": "per-modality training_only"},
            model_selection={"policy": "matched unimodal and fusion baselines required"},
            metrics=("task_performance", "robustness_missing_eeg", "robustness_missing_emg"),
            statistical_unit=StatisticalUnit.SUBJECT,
            seeds=(42,),
            hyperparameter_policy="Do not claim fusion benefit or transfer until matched experiments are registered.",
            status=ProtocolStatus.DRAFT,
            limitations=("This is a research scaffold, not evidence of cross-modal transfer or robustness.",),
        ),
        ProtocolDefinition(
            entity_id="intent-to-control-v1",
            name="Intent to Control Replay",
            version="1.0.0",
            modalities=("emg",),
            split_strategy="deterministic-replay",
            train_validation_test_semantics="No model fitting occurs in the simulator stage; a versioned intent stream is replayed through MyoSim.",
            leakage_constraints=(
                "Retain fixed intent sequence, label map, replay timestamps, and simulator configuration hashes.",
                "Do not bypass MyoSim confidence, temporal, state-machine, safety, or target-generation logic.",
                "Report simulator outputs as replay evidence, not clinical or live-hardware performance.",
            ),
            preprocessing={"owner": "upstream decoder or replay bundle"},
            feature_selection={"owner": "upstream decoder"},
            model_selection={"owner": "upstream decoder"},
            metrics=("task_success_rate", "command_latency", "false_activations", "command_stability", "trajectory_smoothness", "completion_time", "failure_rate"),
            statistical_unit=StatisticalUnit.TASK_TRIAL,
            seeds=(42,),
            hyperparameter_policy="Simulator/control configuration is fixed and hashed per replay run.",
            status=ProtocolStatus.ACTIVE,
            limitations=(
                "The first integration is replay-first and software-only.",
                "No live hardware, clinical safety, or decoder-accuracy equivalence claim is permitted.",
            ),
        ),
    )


def model_entries() -> tuple[ModelDefinition, ...]:
    """Return references to reusable model families without checkpoint copies."""
    return (
        ModelDefinition(
            entity_id="myocontrol-classical-decoder",
            name="MyoControl classical EMG decoder",
            version="0.5",
            project_id="myocontrol-v05",
            modalities=("emg",),
            model_family="Classical feature-based classifier",
            source_reference="external/myocontrol-main",
            intended_use="Exported discrete EMG motor-intent prediction for explicit adapter conversion.",
            known_limitations=("Only explicitly mapped labels may feed the MyoSim V1 adapter.",),
        ),
        ModelDefinition(
            entity_id="myoadapt-lite-dan",
            name="MyoAdapt Lite-DAN",
            version="2.0.0",
            project_id="myoadapt-v2",
            modalities=("emg",),
            model_family="Domain-adversarial EMG classifier",
            source_reference="external/myoadapt",
            intended_use="Referenced adaptation baseline for independently executed EMG protocols.",
            known_limitations=("No umbrella reimplementation or unregistered performance claim.",),
        ),
        ModelDefinition(
            entity_id="biosignal-fm-encoder-export",
            name="BioSignal-FM representation encoder export",
            version="4",
            project_id="biosignal-fm-v4",
            modalities=("emg", "eeg", "ecg"),
            model_family="Modality-aware representation encoder",
            source_reference="external/BioSignal-FM-V4",
            intended_use="External representation record producer for research integration.",
            known_limitations=("Not a claim of a validated foundation model or cross-modal transfer result.",),
        ),
    )


def benchmark_entries() -> tuple[BenchmarkDefinition, ...]:
    """Return benchmark family scaffolds. No result is implied by registration."""
    return (
        BenchmarkDefinition(
            entity_id="emg-loso-db7",
            name="EMG LOSO DB7",
            protocol_id="emg-loso-v1",
            dataset_ids=("ninapro-db7",),
            comparison_dimension="model_or_adaptation_strategy",
            description="Protocol-identified EMG LOSO comparison scaffold; populated only by eligible real-data run imports.",
        ),
        BenchmarkDefinition(
            entity_id="eeg-loso-bci-iv-2a",
            name="EEG LOSO BCI IV-2a",
            protocol_id="eeg-loso-v1",
            dataset_ids=("bci-competition-iv-2a",),
            comparison_dimension="baseline_or_representation_strategy",
            description="Draft EEG benchmark scaffold; no real dataset result is registered initially.",
        ),
        BenchmarkDefinition(
            entity_id="emg-eeg-fusion-way-eeg-gal",
            name="EMG EEG Fusion WAY-EEG-GAL",
            protocol_id="emg-eeg-fusion-v1",
            dataset_ids=("way-eeg-gal",),
            comparison_dimension="unimodal_fusion_or_missing_modality_condition",
            description="Draft multimodal study scaffold requiring matched actual-data experiments.",
        ),
    )


def catalog_entries() -> tuple[RegistryDefinition, ...]:
    """Return the complete stable seed catalog in dependency-friendly order."""
    entries = (
        *project_entries(),
        *dataset_entries(),
        *protocol_entries(),
        *model_entries(),
        *benchmark_entries(),
    )
    # A curated release is immutable. Pin its timestamp so seeding the same
    # release remains idempotent and does not masquerade as a metadata revision.
    return tuple(replace(entry, created_at_utc="2026-08-22T00:00:00+00:00") for entry in entries)


def seed_registry(registry: LocalResearchRegistry) -> tuple[StoredEntry, ...]:
    """Idempotently load the baseline catalog into a local registry."""
    return registry.import_many(catalog_entries(), event_context={"source": "built_in_seed_catalog"})
