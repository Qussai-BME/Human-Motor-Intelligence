#!/usr/bin/env python3
"""Audit all Jeong2020 `ses-0` event TSVs before signal extraction.

The audit retrieves only small event sidecars and records coverage failures without
silently excluding a subject. It writes no raw recordings and cannot produce model
results. Its output supports a prospective cohort decision after data availability
has been assessed.
"""
from __future__ import annotations

import csv
import json
import time
from collections import Counter
from io import StringIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "https://data.nemar.org/nm000311/v1.0.2"
LABELS = (
    "reach_forward", "reach_backward", "reach_left", "reach_right", "reach_up", "reach_down",
    "grasp_cup", "grasp_ball", "grasp_card", "twist_pronation", "twist_supination",
)
REPO = Path("<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1")


def fetch(url: str) -> list[dict[str, str]]:
    """Fetch one TSV with bounded retries; do not substitute a failed response."""
    failure: Exception | None = None
    for attempt in range(1, 6):
        try:
            request = Request(url, headers={"User-Agent": "HMI-V2-research-stack/1.0"})
            with urlopen(request, timeout=120) as response:
                text = response.read().decode("utf-8")
            return list(csv.DictReader(StringIO(text), delimiter="\t"))
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            failure = exc
            if isinstance(exc, HTTPError) and exc.code == 404:
                break
            if attempt < 5:
                time.sleep(2 ** (attempt - 1))
    raise RuntimeError(f"source retrieval failed: {url}: {failure}")


def main() -> None:
    subjects: dict[str, dict[str, object]] = {}
    for index in range(1, 26):
        subject = f"sub-{index}"
        counts: Counter[str] = Counter()
        runs: dict[str, dict[str, int]] = {}
        errors: list[str] = []
        for run in range(3):
            url = f"{BASE}/{subject}/ses-0/eeg/{subject}_ses-0_task-imagery_run-{run}_events.tsv"
            try:
                rows = fetch(url)
            except RuntimeError as exc:
                errors.append(str(exc))
                continue
            run_counts = Counter(str(row["trial_type"]) for row in rows)
            unexpected = sorted(set(run_counts) - set(LABELS))
            if unexpected:
                errors.append(f"{subject} run {run} has unexpected labels: {unexpected}")
            counts.update(run_counts)
            runs[str(run)] = dict(sorted(run_counts.items()))
        missing_labels = sorted(set(LABELS) - set(counts))
        if missing_labels:
            errors.append(f"missing labels across observed runs: {missing_labels}")
        complete = not errors and set(counts) == set(LABELS)
        subjects[subject] = {
            "status": "complete" if complete else "incomplete",
            "total_trials": sum(counts.values()),
            "class_counts": {label: int(counts[label]) for label in LABELS},
            "runs": runs,
            "all_labels_present": set(counts) == set(LABELS),
            "errors": errors,
        }
        print(f"audited {subject}: {sum(counts.values())} events; status={subjects[subject]['status']}", flush=True)
    complete_subjects = [subject for subject, value in subjects.items() if value["status"] == "complete"]
    incomplete_subjects = [subject for subject, value in subjects.items() if value["status"] != "complete"]
    vectors = {
        tuple(subjects[subject]["class_counts"][label] for label in LABELS)
        for subject in complete_subjects
    }
    payload = {
        "dataset": "nm000311-v1.0.2",
        "session": "ses-0",
        "labels": list(LABELS),
        "subjects": subjects,
        "complete_subjects": complete_subjects,
        "incomplete_subjects": incomplete_subjects,
        "unique_class_count_vectors_complete_subjects": [list(vector) for vector in sorted(vectors)],
        "recommended_fixed_cap_per_class_complete_subjects": min(
            min(subjects[subject]["class_counts"].values()) for subject in complete_subjects
        ) if complete_subjects else None,
    }
    target = REPO / "audit/jeong_ses0_event_inventory.json"
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "target": str(target),
        "complete_subjects": complete_subjects,
        "incomplete_subjects": incomplete_subjects,
        "unique_class_count_vectors_complete_subjects": payload["unique_class_count_vectors_complete_subjects"],
        "recommended_fixed_cap_per_class_complete_subjects": payload["recommended_fixed_cap_per_class_complete_subjects"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
