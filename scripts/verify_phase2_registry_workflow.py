"""Verify the master-spec Phase 2 local registry gate without scientific execution.

The workflow registers a deliberately synthetic, metadata-only experiment in a
fresh temporary registry. It proves deterministic identity, separate experiment
and run views, append-only events, and integrity validation. It is explicitly
not benchmark eligible and does not load data, fit a model, or produce a result.
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from research_core.contracts import ExperimentRecord, RunStatus
from research_core.registry import LocalResearchRegistry
from research_core.registry.catalog import seed_registry


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="hmi-phase2-registry-") as temporary:
        root = Path(temporary) / "registry"
        registry = LocalResearchRegistry(root)
        seeded = seed_registry(registry)
        completed = datetime.now(timezone.utc).isoformat()
        experiment = ExperimentRecord(
            experiment_id="phase2-synthetic-experiment-v1",
            run_id="phase2-synthetic-run-0001",
            project_id="human-motor-intelligence",
            protocol_id="eeg-loso-v1",
            dataset_id="bci-competition-iv-2a",
            dataset_version="metadata-only-fixture-v1",
            modality="eeg",
            subject_split="synthetic-subject-a-held-out",
            model_id="registry-fixture-model",
            model_version="1.0.0",
            seed=20260826,
            configuration_hash="0" * 64,
            status=RunStatus.SUCCEEDED,
            completed_at_utc=completed,
            environment={"purpose": "registry-phase-gate", "raw_data_loaded": False},
            metrics={},
            metadata={
                "synthetic": True,
                "benchmark_eligible": False,
                "purpose": "phase2_registry_registration_and_replay_only",
            },
        )
        first_experiment, first_run = registry.register_experiment_run(
            experiment,
            event_context={"phase": "master-spec-phase-2", "evidence_class": "synthetic"},
        )
        events_after_first = root.joinpath("events.jsonl").read_text(encoding="utf-8").splitlines()
        second_experiment, second_run = registry.register_experiment_run(
            experiment,
            event_context={"phase": "master-spec-phase-2", "evidence_class": "synthetic"},
        )
        events_after_second = root.joinpath("events.jsonl").read_text(encoding="utf-8").splitlines()
        stored_experiment = registry.get("experiment", experiment.experiment_id)
        stored_run = registry.get("run", experiment.run_id)
        report = {
            "status": "pass",
            "purpose": "synthetic_metadata_registry_only",
            "seeded_catalog_entries": len(seeded),
            "experiment_entity_id": stored_experiment.entity_id,
            "run_entity_id": stored_run.entity_id,
            "experiment_hash": first_experiment.content_hash,
            "run_hash": first_run.content_hash,
            "idempotent_experiment_hash": first_experiment.content_hash == second_experiment.content_hash,
            "idempotent_run_hash": first_run.content_hash == second_run.content_hash,
            "event_count_after_first_registration": len(events_after_first),
            "event_count_after_replay": len(events_after_second),
            "idempotent_event_log": len(events_after_first) == len(events_after_second),
            "synthetic": stored_experiment.document["metadata"]["synthetic"],
            "benchmark_eligible": stored_experiment.document["metadata"]["benchmark_eligible"],
            "raw_data_loaded": stored_experiment.document["environment"]["raw_data_loaded"],
        }
        if not all(
            (
                report["idempotent_experiment_hash"],
                report["idempotent_run_hash"],
                report["idempotent_event_log"],
                report["synthetic"],
                not report["benchmark_eligible"],
                not report["raw_data_loaded"],
            )
        ):
            raise RuntimeError(json.dumps(report, sort_keys=True))
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
