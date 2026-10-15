# CPU Q1 Upgrade Package Assembly Audit R3

## Package

`human-motor-intelligence-v2-recovery-r3-cpu-first-q1-upgrade-current-state.zip`

## Included

The archive contains the CPU extension runners and analyzers, preregistered matrices and amendments, P4/P5 primary and independent-rerun extension outputs, trial predictions, statistics, release notes, and verification logs.

## Excluded

Raw recordings and external derived caches are excluded. P4 aligned output is absent because no valid result was released. Calibration, cross-dataset, Paper 2, P3, and P6 R3 decoder-quality outputs are absent because they were not executed or remain externally blocked.

## Acceptance checks

| Check | Result |
|---|---|
| ZIP integrity | PASS after final rebuild; checksum manifest excludes itself by design |
| Required extension result artefacts | PASS |
| Primary/rerun exact comparisons | PASS |
| Project tests after extension | 29 passed |
| Raw recordings in archive | 0 |
| NPZ derived caches in archive | 0 |
| P3/P6 R3 fabricated outputs | 0 |
| Claim-safe pending conditions | Explicitly documented |

The archive is a **CPU-first extension current-state release**, not a replacement for the comprehensive programme archive and not a final-authoritative all-programme release.
