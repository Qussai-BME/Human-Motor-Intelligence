> **Current P6 state (2026-10-06): P6 C1 (PhysioNet EEGMMIDB R04 motor imagery, S001–S020, strict LOSO) was executed under the frozen protocol. The MyoSim control fixture passed 1/1; decoder-conditioned task success was 0/60 for every model in both the primary run and the rerun, so the primary task-success endpoint is non-discriminative. R03 is retained as an engineering baseline only. See `P6_FINAL_STATUS.md`.**

# Derived-Cache Release Boundary — Human Motor Intelligence 1.2.0

This note defines what derived participant-data caches are and are not distributed by the current public release.

## Current rule

Raw and participant-level derived biosignal caches are external inputs. The repository distributes reproducibility metadata, aggregate results, selected trace artefacts, manifests, and code where licensing and provenance permit.

## P6

P6 does not redistribute the source EEG EDF recordings. Released decoder artefacts are: the C1 traces (`p6/c_mi_r04_primary`, `p6/c_mi_r04_rerun`, hashes in their `TRACE_MANIFEST.json`), the retained R03 baseline traces (`p6/exploratory_r03_*`), and for C2 the decoder feature/prediction caches (`.npz`) packaged in `p6/c2_episode/raw_archives/P6_C2_wp5_decoder_caches.tar.gz` (SHA-256 in `SHA256SUMS.txt`) together with per-episode replay files and run records in the other archives. Source-file hashes are in `p6/c2_episode/registry/EEGMMIDB_MANIFEST.csv` (relative paths).

R03 is motor execution, not motor imagery. No derived-cache file is used to relabel R03 as imagery. Derived caches are not a substitute for the source data.

## Reuse

Researchers reproducing P6 must obtain the source data from PhysioNet and supply the external MyoSim runtime independently. The runner scripts use explicit arguments or environment variables (`MYOSIM_DIR`, `EEGMMIDB_DIR`, `C2_OUT`, `C2_RAW`) rather than workstation-specific paths.
