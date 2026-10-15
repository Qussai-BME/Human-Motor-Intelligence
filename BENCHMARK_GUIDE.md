# Benchmark, Provenance, and Reporting Guide

## Benchmark Principle

A benchmark is a **protocol-identified comparison of eligible measured runs**, not a collection of similarly named metrics. The benchmark engine will aggregate only completed, real-data-eligible `ExperimentRecord` entries that share one protocol and one dataset. It accepts a single metric at a time and requires one subject-level observation for each model–subject combination.

> **A model accuracy computed on individual windows is not automatically a subject-level statistical observation.** The registered protocol determines the appropriate aggregation before the value reaches the benchmark engine.

## Preconditions for Aggregation

| Required condition | Engine behavior if absent | Reason |
|---|---|---|
| Completed real-data eligible run | Rejects the input | Synthetic/incomplete runs must not enter scientific benchmark summaries. |
| Single `protocol_id` | Rejects the input | Metric names alone do not make studies comparable. |
| Single `dataset_id` | Rejects the input | Dataset mixture requires an explicitly registered meta-analysis design. |
| Observations linked to registered runs | Rejects the input | Prevents unprovenanced metric insertion. |
| One metric per model/subject | Rejects duplicate entries | Forces upstream protocol-aware window/trial aggregation. |
| Matching model identity | Rejects mismatch | Preserves run-to-observation provenance. |

The first seed catalog contains no eligible benchmark observations. This is intentional: it is infrastructure, not a claim that any model has been rerun under the umbrella protocol.

## Statistics Policy

The engine produces descriptive mean, standard deviation, subject count, and coverage notes. It may calculate a Friedman test only when at least three model conditions have **identical paired subject coverage** and the optional statistical dependency is present. It does not automatically select a different test when those conditions fail. Wilcoxon, Holm correction, effect sizes, confidence intervals, and post-hoc analyses must be invoked only when their appropriateness is determined by the registered study protocol.

| Situation | Output |
|---|---|
| One model condition | Descriptive summary; no inter-model inference. |
| Two models | Descriptive summary; no automatic alternate test. |
| Three or more models but mismatched participants | Descriptive summary; explicit note that paired inference was not run. |
| Three or more matched model conditions with SciPy available | Friedman output labeled as descriptive/protocol-review required. |
| Synthetic fixture / incomplete run / protocol mixture | Hard failure; no result. |

## Paper Asset Generation

A valid `BenchmarkResult` can generate the following assets without inventing narrative interpretation.

| Asset | Contents |
|---|---|
| JSON | Full benchmark result, notes, and any statistical status. |
| CSV | Model-level subject-count/mean/standard-deviation table. |
| Markdown | Factual benchmark table, notes, and machine-readable statistic status. |
| LaTeX | Booktable-compatible summary table with a factual caption. |
| SVG | Vector bar figure of subject-level mean values and visible `n`. |
| Caption text | A factual caption that does not claim superiority or significance. |

The generator refuses to treat a visual bar difference as a result statement. Any manuscript interpretation must be written/reviewed by the research team with reference to the registered protocol and the complete measured artifacts.

## Reproducibility Manifest

`ReproducibilityManifest` records configuration, a SHA-256 configuration hash, environment fingerprint/hash, best-effort Git evidence, seed, producing project, protocol, dataset, and artifact content hashes. It can verify both its own configuration/environment hash integrity and each referenced artifact later.

```python
from research_core.provenance import ReproducibilityManifest

manifest = ReproducibilityManifest.create(
    name="registered-action",
    project_id="myoadapt-v2",
    protocol_id="emg-loso-v1",
    dataset_id="ninapro-db7",
    configuration={"external_manifest": "path/to/manifest.json"},
    seed=42,
    repo_root=".",
).with_artifact("path/to/output.csv", "metrics")
manifest.write("artifacts/registered-action/manifest.json")

verification = ReproducibilityManifest.verify("artifacts/registered-action/manifest.json")
```

The manifest is an umbrella-level provenance companion. It does not replace the richer existing MyoAdapt, BioSignal-FM, or MyoSim manifests; an integration action should retain the child-project manifest as a separately hashed `ArtifactRecord`.

## Test Evidence

The implementation test suite verifies benchmark protocol/dataset guards, duplicate-subject rejection, subject-level report output, deterministic report assets, manifest artifact hashing, and tamper detection. Test fixtures are explicitly non-deliverable engineering fixtures and are not included in the registry or in any benchmark report.
