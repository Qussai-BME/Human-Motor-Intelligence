# CPU-First Q1 Upgrade Release Notes

## Release identity

This is a versioned prospective extension release for Human Motor Intelligence V2 Recovery R3. It preserves the frozen R1/R2 evidence namespaces and adds only new CPU-first extension artefacts.

## Included evidence

The release includes the preregistered upgrade matrix, two protocol amendments, deterministic CPU runners and analyzers, P4 log-Euclidean LOSO output with exact independent rerun, P5 confidence-weighted fusion output with exact independent rerun, and P5 feature-group corruption/missing-modality output with exact independent rerun.

## Explicit non-inclusions

No raw BDF/EDF/GDF/SET/FIF files or external derived caches are bundled. No P4 aligned result is included because the fold-local implementation did not complete within the available CPU execution window. No calibration result, cross-dataset result, raw-channel robustness result, Paper 2 result, P3 result, or P6 R3 decoder-quality result is inferred or fabricated.

## Scientific status

The extension supports narrow method-level conclusions only. P4 log-Euclidean representation is executable under LOSO but is not a superiority claim. P5 confidence weighting did not establish benefit over EEG-only. P5 feature-group perturbation and fallback results are not raw hardware robustness or clinical evidence.

## Reproducibility

Use the runners under `scripts/`, the protocol amendments under `audit/`, and the result directories under `results/extensions/`. External derived caches and the licensed source datasets must be supplied separately. All primary/rerun subject-level and trial-level outputs included in this release are byte-identical at the checksums recorded in `audit/CPU_Q1_UPGRADE_VERIFICATION_R3.md`.

P3 and P6 R3 remain external evidence gates and are not changed by this release.
