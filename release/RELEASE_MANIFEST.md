# Public Release Manifest — Human Motor Intelligence 1.1.0

**Scientific status:** P6 C1 is scientifically complete under the registered R04 motor-imagery protocol. R03 is retained only as an engineering/preflight baseline.

The release manifest is self-excluded from its own SHA-256 file list to avoid circular hashing.

## P6 C1 closure

- PhysioNet EEGMMIDB R04, S001–S020, strict LOSO.
- M1/M2/M3 quality order frozen before downstream task analysis.
- Model-independent MyoSim fixture: 1/1 `COMPLETE`.
- Primary: 60 runs; 0/60 task success for all models.
- Rerun: 60 runs; 0/60 task success for all models.
- 60 rerun task JSON artifacts have distinct run IDs and SHA-256 hashes from primary.
- Decoder traces are byte-identical across primary/rerun because the frozen decoder stage is deterministic.
- Raw R04 EDF files are not redistributed; their provenance and SHA-256 hashes are recorded in the dataset manifest.

## Scope boundary

The results support a negative/non-discriminative finding for the registered cohort, task, controller, and MyoSim configuration. They do not support clinical, prosthetic, online-human, or general decoder-quality-to-control-utility claims.

## File inventory

**Files covered by SHA-256 manifest:** see `RELEASE_MANIFEST.json` (`file_count`)
