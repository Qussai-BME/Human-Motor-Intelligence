> **HISTORICAL / SUPERSEDED RECORD:** This document records an earlier pre-reopening state. It is retained for provenance only. Current P6 disposition is documented in `P6_FINAL_STATUS.md` and `closure/10_FINAL_CLOSURE_REPORT.md`.

# Human Motor Intelligence — Derived Cache Release
## V2 Recovery R3 Current-State

This is a **separate derived-cache release** for the available experiments. It is intended to complement, not replace, the source/evidence programme archive.

## Included scope

| Experiment | Included derived material | Count | Status |
|---|---|---:|---|
| P4 OpenBMI external LOSO | Subject NPZ caches plus one provenance JSON per subject | 54 NPZ + 54 provenance JSON | Verified |
| P5 amended Jeong external validation | Subject NPZ caches plus one provenance JSON per retained subject | 24 NPZ + 24 provenance JSON | Verified |
| P6 R2 initial-state systems integration | Protocol, environment, run records, and rerun metadata; no NPZ cache | Metadata/records only | Verified as systems fixture evidence |
| P6 R3 decoder-quality comparison | No cache | 0 | Not executed; blocked pending authentic trace provenance |

The P4 and P5 NPZ files are **derived intermediate arrays**, not raw BDF/EDF/GDF/SET/FIF recordings. Their paired provenance files are retained so that each cache can be mapped back to its declared subject, source, protocol, and environment. No raw recordings are included.

## Verification status

The release was checked with `scripts/validate_derived_cache_release_r3.py`. Each included NPZ was opened with `allow_pickle=False`, its array keys/shapes/dtypes were recorded, and each cache had a matching provenance JSON. The release manifest records SHA-256 for every file.

The cache release does not create, infer, or rename any P6 decoder condition. The available P6 replay remains the `synthetic-demo` / `example-decoder-v1` integration fixture described in the main programme archive. It is not a tiny-CNN/worst, mid-tier, or best authenticated decoder trace.

## Use with the main repository

1. Extract this archive outside the source repository, for example under `/data/human_motor_intelligence/derived_cache_r3/`.
2. Create a local copy of the relevant experiment configuration; do not edit frozen result configurations in place.
3. Set the local `derived_cache_root` to the extracted P4 or P5 directory.
4. Obtain the permitted raw source data independently from the official source record and follow its terms of access and attribution. Raw source data is intentionally not redistributed here.
5. Re-run only under a newly registered local experiment/protocol identity if recomputation is desired. The frozen P4/P5 result directories remain historical evidence and must not be overwritten.

## Important limitations

This archive is not a raw-data archive and is not sufficient by itself to reconstruct every preprocessing step without the source data, source access terms, and exact environment. It is a reproducibility aid containing the derived cache layer and its provenance, not a substitute for the official data source.

The package is an **interim current-state release**. P3 is integrated as qualified external archived evidence; it was not independently rerun in this umbrella. P6 R3 remains blocked and has no decoder-quality cache or statistics.

## References

[1]: papers/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md "P4 Q1 manuscript"
[2]: papers/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.md "P5 Q1 manuscript"
[3]: audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 replay identity hard stop"
[4]: audit/V2_P6_REAL_REPLAY_INITIAL_STATE_REPEAT_AUDIT_RECOVERY_R2.md "P6 R2 systems audit"
