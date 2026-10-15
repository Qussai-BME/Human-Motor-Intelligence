# P6 C1 Claim–Evidence Matrix

**Status: SCIENTIFICALLY COMPLETE WITH A NON-DISCRIMINATIVE PRIMARY ENDPOINT.**

| Claim | Evidence | Disposition |
|---|---|---|
| R04 provides the registered motor-imagery condition | `audit/DATASET_MANIFEST.json` | SUPPORTED
| Quality order is frozen before task analysis | `results/QUALITY_MAPPING.json` | SUPPORTED: M2 low, M3 mid, M1 high
| MyoSim task fixture is capable | Fixture reaches `COMPLETE` | SUPPORTED: 1/1
| Full primary replay exists | 60 traces + 60 task JSONs | SUPPORTED
| Full rerun replay exists | 60 traces + 60 task JSONs | SUPPORTED
| Rerun artifacts are independently identified | Distinct run IDs and artifact SHA-256 hashes | SUPPORTED
| Task success discriminates M1/M2/M3 | 0/60 for each model | NOT SUPPORTED; endpoint degenerate
| Offline decoder quality generally determines downstream control utility | Not identifiable from this endpoint | NOT SUPPORTED
| Clinical/prosthetic efficacy | Outside protocol | NOT SUPPORTED
