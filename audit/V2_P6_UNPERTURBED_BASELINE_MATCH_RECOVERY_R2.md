# V2 P6 Unperturbed Baseline Match — Recovery R2

**Status:** Pass; perturbation design may proceed under a new explicit amendment.  
**Purpose:** Verify that the currently installed MyoSim V1.1 task/replay path reproduces the preserved benchmark endpoints before any initial-state variation is introduced.

## Inputs

The baseline used the pick-and-place CSV replay and control/task values matching the benchmark configuration: seed `20260822`, MuJoCo timestep `0.002 s`, fixed controller thresholds, fixed pick-place geometry, and no perturbation configuration. It wrote only to the new R2 namespace:

```text
results/real/v2-recovery-r2/p6_unperturbed_baseline_runs/14ceb24a45a74cec92666e832eeb2d3d/
```

The preserved MyoSim benchmark summary is `dependencies/myosim_v1_1/artifacts/benchmarks/05837f1e4266452f8e4a3351f8c0594b/summary.json`.

## Endpoint Comparison

| Endpoint | Preserved benchmark | R2 unperturbed baseline | Match |
|---|---:|---:|---|
| Task success | true | true | Exact |
| Final state | `COMPLETE` | `COMPLETE` | Exact |
| Completion time (s) | 3.22 | 3.22 | Exact |
| Final error (m) | 0.04985601966004137 | 0.04985601966004137 | Exact |
| Path length (m) | 0.9678159612131996 | 0.9678159612131996 | Exact |
| Grasp stability steps | 14 | 14 | Exact |
| Command corrections | 3 | 3 | Exact |
| Invalid state | false | false | Exact |
| Event count | 33 | 33 | Exact |
| Mean confirmation latency (s) | 0.30 | 0.30 | Exact |
| State-transition count | 5 | 5 | Exact |

The observed endpoints match exactly; the effective numerical tolerance is therefore zero for the recorded values. The old provenance package version and path differ from the current recovered runtime packaging, but the simulation/task/control outputs required for the R2 baseline gate are identical. This record does not rerun, overwrite, or reclassify frozen V1.1 evidence.

> The baseline pass demonstrates equivalence of the unperturbed task path. It does not create an independent sample or estimate outcome variability.

## Authorization Boundary

A new P6 R2 factor may now be implemented only as a separately declared, bounded, seed-linked **initial joint-state perturbation**. The replay trace, decoder/mapping, controller policy, task geometry, success rule, and synthetic-corruption boundary remain fixed. Every perturbed run must record its actual seed, configured range, realized offsets, and observed initial state.
