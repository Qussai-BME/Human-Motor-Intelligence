# P3 Final Audit — Closure R1

**Disposition:** COMPLETE FOR PROGRAMME INTEGRATION AS EXTERNALLY ARCHIVED EVIDENCE.  
**Independent umbrella rerun:** not performed; no claim of rerun is made.

## Evidence audited

- Zenodo archive: `10.5281/zenodo.22768799`
- Archive SHA-256: `b382a40aa9a40556a6169ca805fc92c1d75a94e6d982b845ca489dd37c158f14`
- Supplied manuscript SHA-256: `1a84ccc9e6985f46947245f4815b618d1195067f832bbe8703bcb95350b5256f`
- Repository package: `external/p3_litedan_v1_0_0/`
- Protocol: `configs/protocol_v1_1.yaml`
- Registry: `registry_v1_1/`
- Provenance: `docs/DATA_PROVENANCE.md`

## Structural checks

| Check | Result |
|---|---:|
| DB2 fold files | 360 |
| DB3 fold files | 99 |
| DB7 fold files | 198 |
| Total LOSO fold files | 657 |
| Planned condition/cohort summaries | 27 |
| Aggregate summaries present | PASS |
| Raw NinaPro recordings/cache redistribution | Correctly absent |
| Source code and tests present | PASS |

## Scientific checks

The package reports classical baselines, CORAL, Lite-DAN variants, active-only metrics, rest recall, and subject-level LOSO outputs. The README and provenance file explicitly describe strict zero-calibration evaluation, cohort differences, and missing-label handling. The package does not justify a universal learned-adaptation winner: its headline findings include cases where classical models exceed Lite-DAN and cases where adversarial alignment does not improve the result.

## Limitations retained

1. The umbrella did not acquire or rerun the raw NinaPro data.
2. The external package does not contain a MyoSim-compatible intent event stream.
3. Its upstream citation/provenance metadata remain part of the preserved source record.
4. Supervisor review and publication status are external statuses and remain unasserted.

**Conclusion:** P3 is integrated as qualified external evidence. It closes the P3 package dependency for programme documentation but does not open P6 R3.
