from __future__ import annotations

import argparse
import json
import platform
import time
from pathlib import Path

import numpy as np
import pandas as pd

from .config import RunConfig, cache_input_hash, config_hash, load_config
from .data.ninapro import available_exercises, subject_windows, validate_dataset
from .evaluation.pipeline import fit_predict_fold
from .evaluation.plots import plot_lambda, plot_metric_summary, plot_subject_accuracy
from .evaluation.stats import paired_condition_stats
from .features.hybrid import SCHEMA_VERSION, extract_feature_matrix
from .models.litedan import LiteDAN
from .utils.repro import env_manifest, save_json, set_seed


CONDITIONS = [
    "xgb",
    "lda",
    "linear_svc",
    "random_forest",
    "coral_xgb",
    "coral_target_xgb",
    "litedan",
    "litedan_fixed_0p1",
    "litedan_fixed_0p5",
    "litedan_fixed_1p0",
    "litedan_no_grl",
]


def _dataset(
    cfg: RunConfig,
    db: str,
    exercise_override: list[int] | None = None,
):
    if db not in cfg.datasets:
        raise SystemExit(
            f"Unknown dataset {db}. Available: {', '.join(cfg.datasets)}"
        )

    entry = cfg.datasets[db]

    exercises = (
        exercise_override
        if exercise_override is not None
        else entry.exercise
    )

    if exercises is None:
        raise SystemExit(
            f"Exercise mapping for {db} is unset. "
            "Verify the NinaPro filename/label convention "
            "and configure a list such as [1, 2] before a full run."
        )

    exercises = [int(x) for x in exercises]

    if not exercises:
        raise SystemExit(
            f"Exercise mapping for {db} is empty."
        )

    return entry, exercises


def _dataset_root(cfg: RunConfig, entry) -> Path:
    return cfg.data_root / (entry.subdir or entry.name)


def cmd_doctor(args: argparse.Namespace) -> None:
    import sklearn
    import scipy
    import torch
    import xgboost

    print("Lite-DAN Paper 3 environment")
    print(json.dumps({
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "sklearn": sklearn.__version__,
        "torch": torch.__version__,
        "xgboost": xgboost.__version__,
        "torch_device": args.device,
        "cpu_threads": torch.get_num_threads(),
        "cuda_available": bool(torch.cuda.is_available()),
    }, indent=2))


def cmd_smoke(args: argparse.Namespace) -> None:
    rng = np.random.default_rng(42)
    n, d, c, g = 480, 308, 4, 8
    X = rng.normal(size=(n, d)).astype(np.float32)
    y = np.arange(n) % c
    domains = np.repeat(np.arange(g), n // g)
    model = LiteDAN(
        n_features=d,
        n_classes=c,
        n_domains=g,
        epochs=3,
        batch_size=64,
        device="cpu",
        seed=42,
        early_stopping_patience=None,
    )
    model.fit(X, y, domains)
    pred = model.predict(X[:10])
    assert pred.shape == (10,)
    print(f"SMOKE OK | parameters={model.parameter_count()} | predictions={len(pred)}")


def cmd_validate_data(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    base_root = Path(args.data_root or cfg.data_root)

    entry, exercises = _dataset(
        cfg,
        args.db,
        args.exercise,
    )

    root = base_root / (entry.subdir or entry.name)

    print(
        json.dumps(
            {"available_exercises": available_exercises(root)},
            indent=2,
        )
    )

    report = validate_dataset(
        root,
        exercises,
        entry.expected_subjects,
    )

    print(json.dumps(report, indent=2))

    if not report["n_intersection_subjects"]:
     raise SystemExit("No subject has all required exercises.")

    if not report["subject_count_matches"]:
     raise SystemExit(
        "Dataset subject coverage does not match the configured "
        f"expected count: expected={report['expected_subjects']}, "
        f"intersection={report['n_intersection_subjects']}"
    )
def cmd_prepare(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    base_root = Path(args.data_root or cfg.data_root)

    entry, exercises = _dataset(
        cfg,
        args.db,
        args.exercise,
    )

    root = base_root / (entry.subdir or entry.name)

    coverage = validate_dataset(
        root,
        exercises,
        entry.expected_subjects,
    )
    subjects = coverage["intersection_subjects"]

    if not subjects:
        raise SystemExit(
            f"No subject has every required exercise for {args.db} "
            f"E{','.join(map(str, exercises))} under {root.resolve()}"
        )
    if not coverage["subject_count_matches"]:
        raise SystemExit(
            "Dataset subject coverage does not match the configured expected "
            f"count: expected={coverage['expected_subjects']}, "
            f"intersection={coverage['n_intersection_subjects']}"
        )

    output = cfg.artifact_root / "features" / args.db
    output.mkdir(parents=True, exist_ok=True)
    expected_cache_hash = cache_input_hash(cfg, entry)
    completed: set[int] = set()
    cached_meta: dict[int, dict] = {}



    for path in output.glob("S*.npz"):
     subject = None

     try:
        subject = int(path.stem[1:])
        with np.load(path, allow_pickle=False) as payload:
            features = payload["features"]
            labels = payload["labels"]
            purity = payload["purity"]
            feature_names = payload["feature_names"]
        valid_cache = (
                     features.ndim == 2
            and features.shape[1] == 618
            and labels.ndim == 1
            and purity.ndim == 1
            and feature_names.ndim == 1
            and len(feature_names) == 618
            and np.isfinite(features).all()
            and np.isfinite(purity).all()
            and features.shape[0] == labels.shape[0] == purity.shape[0]
        )
        if not valid_cache:
            print(
                f"recompute DB7 S{subject:02d}: "
                "invalid cached shape"
            )
            continue
        meta_path = output / f"S{subject:02d}.json"
        if meta_path.exists():
            with meta_path.open("r", encoding="utf-8") as f:
                meta = json.load(f)
            if (
                meta.get("db") == args.db
                and int(meta.get("subject", -1)) == subject
                and meta.get("exercises") == exercises
                and int(meta.get("raw_features", -1)) == 618
                and meta.get("feature_schema") == SCHEMA_VERSION
                and meta.get("cache_input_hash") == expected_cache_hash
            ):
                cached_meta[subject] = meta
                completed.add(subject)
            else:
                print(
                    f"recompute DB{args.db} S{subject:02d}: "
                    "metadata mismatch"
                )    
        else:
            print(
                f"recompute DB{args.db} S{subject:02d}: "
                "missing metadata file"
            )        
     except (ValueError, TypeError, OSError, KeyError) as exc:
         label = (f"S{subject:02d}" if subject is not None else path.name)
         print(
             f"recompute DB{args.db} {label}: "
                f"invalid cache ({exc})"
            ) 
    manifest_rows: dict[int, dict] = dict(cached_meta)
    for subject in subjects:
        if subject in completed:
            print(f"skip {args.db} S{subject:02d}: cached")
            continue
        payload = subject_windows(
            root,
            subject,
            exercises,
            cfg.protocol,
        )
        features, names = extract_feature_matrix(
            payload["windows"],
            fs=cfg.protocol.fs,
            n_jobs=6,
        )
        if features.ndim != 2 or features.shape[1] != 618:
            raise RuntimeError(
                f"DB{args.db} S{subject:02d}: "
                f"expected 618 features, got {features.shape}"
            )
                
        np.savez_compressed(
            output / f"S{subject:02d}.npz",
            features=features,
            labels=payload["labels"],
            purity=payload["purity"],
            feature_names=np.asarray(names, dtype=str),
        )        
                                    
        meta = {
            "db": args.db,
            "subject": subject,
            "exercises": exercises,
            "n_windows": int(len(payload["labels"])),
            "raw_features": int(features.shape[1]),
            "feature_schema": SCHEMA_VERSION,
            "cache_input_hash": expected_cache_hash,
            "source_files": sorted(
                set(payload["source_files"])
            ),
        }

        save_json(
            meta,
            output / f"S{subject:02d}.json",
        )

        manifest_rows[subject] = meta

        print(
            f"prepared {args.db} "
            f"S{subject:02d}: {features.shape}"
        )

    save_json(
        {
            "db": args.db,
            "exercises": exercises,
            "subjects": subjects,
            "feature_schema": SCHEMA_VERSION,
            "config_hash": config_hash(cfg),
            "cache_input_hash": expected_cache_hash,
            "summary": [
                manifest_rows[subject]
                for subject in subjects
                if subject in manifest_rows
            ],
                
                
        },
        output / "manifest.json",
    )
def _load_cached(cfg: RunConfig, db: str):
    if db not in cfg.datasets:
        raise ValueError(f"Unknown dataset: {db}")
    entry = cfg.datasets[db]
    directory = cfg.artifact_root / "features" / db
    manifest_path = directory / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing {manifest_path}. Run prepare first.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("db") != db:
        raise ValueError(f"Cache manifest database mismatch: {manifest.get('db')!r} != {db!r}")
    if manifest.get("feature_schema") != SCHEMA_VERSION:
        raise ValueError("Cache manifest feature schema is incompatible with this code version")
    if manifest.get("cache_input_hash") != cache_input_hash(cfg, entry):
        raise ValueError("Cache input fingerprint mismatch; recompute the feature cache in this versioned branch")
    expected_subjects = list(range(1, int(entry.expected_subjects) + 1)) if entry.expected_subjects else None
    if expected_subjects is not None and manifest.get("subjects") != expected_subjects:
        raise ValueError("Cache manifest subject list does not match the configured protocol")
    rows = []
    reference_names = None
    for subject in manifest["subjects"]:
        path = directory / f"S{int(subject):02d}.npz"
        if not path.exists():
            raise FileNotFoundError(f"Missing cached subject file {path}")
        with np.load(path, allow_pickle=False) as payload:
            features = payload["features"]
            labels = payload["labels"]
            purity = payload["purity"]
            names = payload["feature_names"]
        if (
            features.ndim != 2 or features.shape[1] != 618
            or labels.ndim != 1 or purity.ndim != 1
            or names.ndim != 1 or len(names) != 618
            or len(features) != len(labels) or len(features) != len(purity)
            or not np.isfinite(features).all() or not np.isfinite(purity).all()
        ):
            raise ValueError(f"Invalid cached feature artifact: {path}")
        names_list = names.tolist()
        if reference_names is None:
            reference_names = names_list
        elif names_list != reference_names:
            raise ValueError(f"Feature-name ordering differs across cache files: {path}")
        rows.append((int(subject), features, labels))
    X = np.concatenate([row[1] for row in rows], axis=0)
    y = np.concatenate([row[2] for row in rows], axis=0)
    groups = np.concatenate([
        np.full(len(row[2]), row[0], dtype=np.int32) for row in rows
    ])
    if entry.expected_classes is not None and set(np.unique(y).tolist()) != set(range(int(entry.expected_classes))):
        raise ValueError("Dataset-level cache label union does not match the configured class space")
    return X, y, groups, manifest


def cmd_loso(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)

    X, y, groups, manifest = _load_cached(
        cfg,
        args.db,
    )

    all_subjects = sorted(
        int(s)
        for s in np.unique(groups)
    )

    if args.test_subject is not None:
        requested_subject = int(
            args.test_subject
        )

        if requested_subject not in all_subjects:
            raise SystemExit(
                f"Unknown test subject {requested_subject}. "
                f"Available subjects: {all_subjects}"
            )

        subjects = [
            requested_subject
        ]
    else:
        subjects = all_subjects

    output = (
        cfg.output_root
        / args.db
        / args.condition
    )

    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ============================================================
    # LOAD COMPLETED FOLDS
    #
    # This is true resume:
    #   fold_S01.json ... fold_S16.json
    # are reused without retraining.
    # ============================================================

    cached_results: dict[int, dict] = {}

    for subject in subjects:
        fold_path = (
            output
            / f"fold_S{subject:02d}.json"
        )

        if not fold_path.exists():
            continue

        try:
            with fold_path.open(
                "r",
                encoding="utf-8",
            ) as f:
                result = json.load(f)

            cached_subject = int(
                result.get(
                    "test_subject",
                    -1,
                )
            )

            cached_condition = result.get(
                "condition"
            )

            expected_train_subjects = [
                int(source_subject)
                for source_subject in all_subjects
                if int(source_subject) != int(subject)
            ]
            required_metrics = {
                "accuracy", "macro_f1", "macro_f1_fixed41", "kappa",
                "rest_recall", "active_only_accuracy", "active_only_macro_f1", "inflation_pp",
            }
            valid_resume = (
                cached_subject == subject
                and cached_condition == args.condition
                and result.get("experiment_status") == "COMPLETED"
                and result.get("code_version") == "protocol-v1.1.0"
                and result.get("config_hash") == config_hash(cfg)
                and result.get("feature_schema") == cfg.features.implementation
                and result.get("train_subject_ids") == expected_train_subjects
                and result.get("protocol", {}).get("strict_zero_calibration") == bool(cfg.protocol.strict_zero_calibration)
                and result.get("protocol", {}).get("target_unlabelled_exposure") == bool(cfg.protocol.target_unlabelled_exposure)
                and result.get("protocol", {}).get("preprocessing_order") == "outer_LOSO>source_only_SelectKBest>source_only_StandardScaler>fit>held_out_prediction"
                and isinstance(result.get("metrics"), dict)
                and required_metrics.issubset(result["metrics"])
            )
            if valid_resume:
                cached_results[subject] = result
            else:
                print(
                    f"WARNING: ignoring incompatible cached fold S{subject:02d}; rerun required",
                    flush=True,
                )

        except (
            OSError,
            ValueError,
            TypeError,
            json.JSONDecodeError,
        ) as exc:
            print(
                f"WARNING: ignoring invalid cache "
                f"S{subject:02d}: {exc}",
                flush=True,
            )

    # ============================================================
    # BUILD RESULTS FROM CACHE FIRST
    # ============================================================

    rows: list[dict] = []
    histories: list[dict] = []

    def append_result(
        result: dict,
        subject: int,
    ) -> None:
        metrics = result["metrics"]

        rows.append(
            {
                "condition": args.condition,
                "test_subject": int(subject),

                "accuracy": metrics[
                    "accuracy"
                ],

                "macro_f1": metrics[
                    "macro_f1"
                ],

                "macro_f1_fixed41": metrics.get(
                    "macro_f1_fixed41"
                ),

                "rest_recall": metrics[
                    "rest_recall"
                ],

                "active_only_accuracy": metrics[
                    "active_only_accuracy"
                ],

                "active_only_macro_f1": metrics[
                    "active_only_macro_f1"
                ],

                "inflation_pp": metrics[
                    "inflation_pp"
                ],

                "missing_test_labels": str(
                    metrics.get(
                        "missing_test_labels",
                        [],
                    )
                ),

                "n_train": result[
                    "n_train"
                ],

                "n_train_full": result[
                    "n_train_full"
                ],

                "n_test": result[
                    "n_test"
                ],

                "n_selected_features": result[
                    "n_selected_features"
                ],

                "prep_seconds": result[
                    "prep_seconds"
                ],

                "fit_seconds": result[
                    "fit_seconds"
                ],

                "predict_seconds": result[
                    "predict_seconds"
                ],

                "model_elapsed_seconds": result[
                    "model_elapsed_seconds"
                ],

                "fold_elapsed_seconds": result[
                    "fold_elapsed_seconds"
                ],

                "parameter_count": result[
                    "parameter_count"
                ],
            }
        )

        for history_row in (
            result.get("history")
            or []
        ):
            histories.append(
                {
                    "condition": args.condition,
                    "test_subject": int(
                        subject
                    ),
                    **history_row,
                }
            )

    for subject in subjects:
        if subject in cached_results:
            append_result(
                cached_results[subject],
                subject,
            )

    # ============================================================
    # RUN ONLY MISSING FOLDS
    #
    # IMPORTANT:
    # Seed is based on the ORIGINAL fold position,
    # not the resumed position.
    #
    # Example:
    # S01..S16 cached, S17 missing
    # S17 must still use cfg.seed + 17.
    # ============================================================

    for fold, subject in enumerate(
        subjects,
        start=1,
    ):

        if subject in cached_results:
            print(
                f"resume {fold}/{len(subjects)} "
                f"S{subject}: cached",
                flush=True,
            )
            continue

        print(
            f"start {fold}/{len(subjects)} "
            f"S{subject}: running",
            flush=True,
        )

        result = fit_predict_fold(
            X,
            y,
            groups,
            int(subject),
            args.condition,
            cfg,
            seed=cfg.seed + fold,
        )

        save_json(
            result,
            output
            / f"fold_S{int(subject):02d}.json",
        )

        cached_results[subject] = result

        append_result(
            result,
            subject,
        )

        metrics = result["metrics"]

        print(
            f"fold {fold}/{len(subjects)} "
            f"S{subject}: "
            f"acc={metrics['accuracy']:.4f}, "
            f"macro-F1={metrics['macro_f1']:.4f}, "
            f"fit={result['fit_seconds']:.1f}s, "
            f"fold={result['fold_elapsed_seconds']:.1f}s",
            flush=True,
        )

    # ============================================================
    # VERIFY COMPLETENESS
    # ============================================================

    completed_subjects = sorted(
        cached_results.keys()
    )

    missing_subjects = [
        subject
        for subject in subjects
        if subject not in cached_results
    ]

    if missing_subjects:
        print(
            "LOSO incomplete; summary will NOT be finalized.",
            flush=True,
        )

        print(
            f"Missing subjects: {missing_subjects}",
            flush=True,
        )

        return

    # ============================================================
    # REBUILD COMPLETE FOLD TABLE
    #
    # Sort by actual subject ID rather than execution order.
    # ============================================================


    # append_result above was already called for cached folds
    # and new folds. Rebuild cleanly to avoid duplicates.

    rows = []
    histories = []

    for subject in subjects:
        append_result(
            cached_results[subject],
            subject,
        )

    frame = pd.DataFrame(
        rows
    )

    frame = frame.sort_values(
        "test_subject"
    ).reset_index(
        drop=True
    )

    frame.to_csv(
        output / "fold_results.csv",
        index=False,
    )

    # ============================================================
    # SUMMARY STATISTICS
    # ============================================================

    metric_names = [
        "accuracy",
        "macro_f1",
        "rest_recall",
        "active_only_accuracy",
        "active_only_macro_f1",
        "inflation_pp",
    ]

    metric_summary = {}

    for metric in metric_names:
        values = pd.to_numeric(
            frame[metric],
            errors="coerce",
        )

        valid = values.dropna()

        metric_summary[metric] = {
            "mean": float(
                valid.mean()
            )
            if len(valid)
            else float("nan"),

            "sd": float(
                valid.std(
                    ddof=1
                )
            )
            if len(valid) > 1
            else 0.0,
        }

    summary = {
        "config_hash": config_hash(
            cfg
        ),

        "feature_schema": manifest[
            "feature_schema"
        ],

        "db": args.db,

        "condition": args.condition,

        "n_subjects": int(
            frame[
                "test_subject"
            ].nunique()
        ),

        "requested_subjects": [
            int(subject)
            for subject in subjects
        ],

        "completed_subjects": [
            int(subject)
            for subject in completed_subjects
        ],

        "metrics": metric_summary,

        "environment": env_manifest(),
    }

    save_json(
        summary,
        output / "summary.json",
    )

    # ============================================================
    # LAMBDA HISTORY
    # ============================================================

    if histories:
        history_frame = pd.DataFrame(
            histories
        )

        history_frame.to_csv(
            output / "history.csv",
            index=False,
        )

        plot_lambda(
            history_frame,
            output / "lambda_schedule.png",
        )

    print(
        f"LOSO COMPLETE: "
        f"{args.db} / {args.condition} "
        f"({len(subjects)} subjects)",
        flush=True,
    )
def cmd_ablation(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)

    conditions = [
        "litedan",
        "litedan_fixed_0p1",
        "litedan_fixed_0p5",
        "litedan_fixed_1p0",
        "litedan_no_grl",
    ]

    root = (
        cfg.output_root
        / args.db
        / "ablation"
    )

    root.mkdir(
        parents=True,
        exist_ok=True,
    )

    expected_subjects = None
    frames = {}

    # ------------------------------------------------------------
    # Load already-computed LOSO results
    # ------------------------------------------------------------

    for condition in conditions:

        source_file = (
            cfg.output_root
            / args.db
            / condition
            / "fold_results.csv"
        )

        if not source_file.exists():
            print(
                f"ABLATION WAIT: "
                f"{args.db}/{condition} "
                f"has no fold_results.csv yet."
            )
            print(
                "No models will be retrained."
            )
            return

        frame = pd.read_csv(
            source_file
        )

        if "test_subject" not in frame.columns:
            print(
                f"ABLATION WAIT: "
                f"{source_file} has no test_subject column."
            )
            return

        subjects = sorted(
            set(
                pd.to_numeric(
                    frame["test_subject"],
                    errors="coerce",
                )
                .dropna()
                .astype(int)
                .tolist()
            )
        )

        if expected_subjects is None:
            expected_subjects = subjects
        else:
            if subjects != expected_subjects:
                print(
                    f"ABLATION WAIT: incomplete/mismatched subjects "
                    f"for {condition}."
                )

                print(
                    f"Expected subjects: {expected_subjects}"
                )

                print(
                    f"Found subjects   : {subjects}"
                )

                print(
                    "The ablation analysis will not run "
                    "until all conditions contain the same "
                    "held-out subjects."
                )

                return

        required_columns = {
            "test_subject",
            "accuracy",
            "macro_f1",
            "active_only_accuracy",
            "active_only_macro_f1",
            "rest_recall",
            "inflation_pp",
        }

        missing = (
            required_columns
            - set(frame.columns)
        )

        if missing:
            print(
                f"ABLATION WAIT: "
                f"{condition} is missing columns: "
                f"{sorted(missing)}"
            )
            return

        frames[condition] = frame

    # ------------------------------------------------------------
    # Verify equal paired subjects
    # ------------------------------------------------------------

    if expected_subjects is None:
        print(
            f"No completed ablation results found for {args.db}."
        )
        return

    if len(expected_subjects) < 2:
        print(
            f"ABLATION WAIT: only "
            f"{len(expected_subjects)} subject(s) available."
        )
        return

    # ------------------------------------------------------------
    # Build combined paired table
    # ------------------------------------------------------------

    rows = []

    for condition in conditions:

        frame = frames[condition]

        for _, row in frame.iterrows():

            rows.append(
                {
                    "condition": condition,
                    "test_subject": int(
                        row["test_subject"]
                    ),
                    "accuracy": float(
                        row["accuracy"]
                    ),
                    "macro_f1": float(
                        row["macro_f1"]
                    ),
                    "active_only_accuracy": float(
                        row[
                            "active_only_accuracy"
                        ]
                    ),
                    "active_only_macro_f1": float(
                        row[
                            "active_only_macro_f1"
                        ]
                    ),
                    "rest_recall": float(
                        row["rest_recall"]
                    ),
                    "inflation_pp": float(
                        row["inflation_pp"]
                    ),
                }
            )

    combined = pd.DataFrame(
        rows
    )

    combined = combined.sort_values(
        [
            "test_subject",
            "condition",
        ]
    ).reset_index(
        drop=True
    )

    combined.to_csv(
        root / "ablation_results.csv",
        index=False,
    )

    # ------------------------------------------------------------
    # Paired accuracy statistics
    # ------------------------------------------------------------

    condition_values = {
        condition: (
            combined.loc[
                combined["condition"]
                == condition,
                "accuracy",
            ]
            .tolist()
        )
        for condition in conditions
    }

    stats = paired_condition_stats(
        condition_values
    )

    save_json(
        stats,
        root / "ablation_stats.json",
    )

    # ------------------------------------------------------------
    # Descriptive summaries for all metrics
    # ------------------------------------------------------------

    metrics = [
        "accuracy",
        "macro_f1",
        "active_only_accuracy",
        "active_only_macro_f1",
        "rest_recall",
        "inflation_pp",
    ]

    summary = {
        "db": args.db,
        "n_subjects": int(
            len(expected_subjects)
        ),
        "subjects": [
            int(x)
            for x in expected_subjects
        ],
        "conditions": conditions,
        "metrics": {},
    }

    for metric in metrics:

        metric_summary = {}

        for condition in conditions:

            values = pd.to_numeric(
                combined.loc[
                    combined["condition"]
                    == condition,
                    metric,
                ],
                errors="coerce",
            ).dropna()

            metric_summary[condition] = {
                "mean": float(
                    values.mean()
                ),
                "sd": float(
                    values.std(
                        ddof=1
                    )
                ) if len(values) > 1 else 0.0,
                "median": float(
                    values.median()
                ),
                "n": int(
                    len(values)
                ),
            }

        summary["metrics"][metric] = (
            metric_summary
        )

    save_json(
        summary,
        root / "ablation_summary.json",
    )

    print(
        f"ABLATION COMPLETE: {args.db}"
    )

    print(
        f"Subjects: {len(expected_subjects)}"
    )

    print(
        "Conditions:"
    )

    for condition in conditions:
        print(
            f"  {condition}: "
            f"{len(frames[condition])} folds"
        )

    print(
        f"Output: {root}"
    )
def cmd_aggregate(args: argparse.Namespace) -> None:
    root = Path(args.results_root) / args.db
    frames = []
    for path in root.glob("**/fold_results.csv"):
        frames.append(pd.read_csv(path))
    ablation = root / "ablation" / "ablation_results.csv"
    if ablation.exists():
        frames.append(pd.read_csv(ablation))
    if not frames:
        raise SystemExit(f"No result CSVs found under {root}")
    frame = pd.concat(frames, ignore_index=True)
    output = root / "aggregate"
    output.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output / "all_results.csv", index=False)
    summary = frame.groupby("condition")[[
        "accuracy", "macro_f1", "rest_recall", "active_only_accuracy",
        "active_only_macro_f1", "inflation_pp"
    ]].agg(["mean", "std"])
    summary.to_csv(output / "summary.csv")
    plot_subject_accuracy(frame[["condition", "test_subject", "accuracy"]], output / "loso_accuracy.png")
    plot_metric_summary(frame, "macro_f1", output / "macro_f1.png")
    plot_metric_summary(frame, "active_only_accuracy", output / "active_only_accuracy.png")
    print(summary)


def cmd_benchmark(args: argparse.Namespace) -> None:
    import psutil

    cfg = load_config(args.config)
    rng = np.random.default_rng(cfg.seed)
    X = rng.normal(size=(2048, cfg.protocol.feature_k)).astype(np.float32)
    y = np.arange(len(X)) % 41
    domains = np.arange(len(X)) % 20
    model = LiteDAN(
        n_features=cfg.protocol.feature_k,
        n_classes=41,
        n_domains=20,
        hidden_dim=cfg.model.hidden_dim,
        dropout=cfg.model.dropout,
        epochs=2,
        batch_size=cfg.model.batch_size,
        learning_rate=cfg.model.learning_rate,
        weight_decay=cfg.model.weight_decay,
        device="cpu",
        seed=cfg.seed,
        early_stopping_patience=None,
    )
    start = time.perf_counter()
    model.fit(X, y, domains)
    train_seconds = time.perf_counter() - start
    model.predict(X[:8])
    latencies = []
    for _ in range(100):
        start = time.perf_counter()
        model.predict(X[:1])
        latencies.append((time.perf_counter() - start) * 1000.0)
    result = {
        "processor": platform.processor(),
        "logical_cpus": psutil.cpu_count(),
        "physical_cpus": psutil.cpu_count(logical=False),
        "parameters": model.parameter_count(),
        "train_seconds_smoke": train_seconds,
        "latency_ms_p50": float(np.percentile(latencies, 50)),
        "latency_ms_p95": float(np.percentile(latencies, 95)),
        "environment": env_manifest(),
    }
    save_json(result, args.output)
    print(json.dumps(result, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Lite-DAN Paper 3 reproducible experiments"
        )
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    doctor = sub.add_parser(
        "doctor"
    )
    doctor.add_argument(
        "--device",
        default="cpu",
    )
    doctor.set_defaults(
        func=cmd_doctor
    )

    smoke = sub.add_parser(
        "smoke-test"
    )
    smoke.set_defaults(
        func=cmd_smoke
    )

    validate = sub.add_parser(
        "validate-data"
    )

    validate.add_argument(
        "--db",
        required=True,
    )

    validate.add_argument(
        "--exercise",
        type=int,
        action="append",
        dest="exercise",
    )

    validate.add_argument(
        "--data-root"
    )

    validate.add_argument(
        "--config",
        default="configs/main.yaml",
    )

    validate.set_defaults(
        func=cmd_validate_data
    )

    prepare = sub.add_parser(
        "prepare"
    )

    prepare.add_argument(
        "--db",
        required=True,
    )

    prepare.add_argument(
        "--exercise",
        type=int,
        action="append",
        dest="exercise",
    )

    prepare.add_argument(
        "--data-root"
    )

    prepare.add_argument(
        "--config",
        default="configs/main.yaml",
    )

    prepare.set_defaults(
        func=cmd_prepare
    )

    loso = sub.add_parser(
        "run-loso"
    )

    loso.add_argument(
        "--db",
        required=True,
    )

    loso.add_argument(
        "--condition",
        required=True,
        choices=CONDITIONS,
    )

    loso.add_argument(
        "--test-subject",
        type=int,
        default=None,
        help=(
            "Run only one held-out subject "
            "for benchmarking."
        ),
    )

    loso.add_argument(
        "--config",
        default="configs/main.yaml",
    )

    loso.set_defaults(
        func=cmd_loso
    )

    ablation = sub.add_parser(
        "run-ablation"
    )

    ablation.add_argument(
        "--db",
        required=True,
    )

    ablation.add_argument(
        "--config",
        default="configs/main.yaml",
    )

    ablation.set_defaults(
        func=cmd_ablation
    )

    aggregate = sub.add_parser(
        "aggregate"
    )

    aggregate.add_argument(
        "--db",
        required=True,
    )

    aggregate.add_argument(
        "--results-root",
        default="results",
    )

    aggregate.set_defaults(
        func=cmd_aggregate
    )

    bench = sub.add_parser(
        "benchmark-cpu"
    )

    bench.add_argument(
        "--output",
        default=(
            "results/cpu_benchmark.json"
        ),
    )

    bench.add_argument(
        "--config",
        default="configs/main.yaml",
    )

    bench.set_defaults(
        func=cmd_benchmark
    )

    return parser
def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()