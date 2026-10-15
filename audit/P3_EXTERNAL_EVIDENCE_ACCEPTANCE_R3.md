# P3 External Evidence Acceptance — R3

**Responsible author:** Qussai Adlbi  
**Disposition:** ACCEPTED AS EXTERNALLY ARCHIVED EVIDENCE; NOT RERUN IN THE UMBRELLA ENVIRONMENT

## Accepted source

The supplied P3 manuscript was cross-checked against the public Lite-DAN repository and its Zenodo archive:

- Repository: https://github.com/Qussai-BME/LiteDAN-cross-subject-sEMG
- Archive: https://doi.org/10.5281/zenodo.22768799
- Archive version: v1.0.0
- Downloaded archive SHA-256: `b382a40aa9a40556a6169ca805fc92c1d75a94e6d982b845ca489dd37c158f14`
- Supplied manuscript SHA-256: `1a84ccc9e6985f46947245f4815b618d1195067f832bbe8703bcb95350b5256f`

## Evidence inventory

The archived package contains the protocol configuration, source package, registry, provenance notes, aggregate summaries, and 657 subject-level fold records across 27 planned experiments (9 conditions × DB2/DB3/DB7). Raw NinaPro recordings and derived feature caches are correctly excluded from the public archive.

A structural audit confirmed 360 fold records for DB2, 99 for DB3, and 198 for DB7, totalling 657. The package's provenance note reports that the 27 aggregate values were cross-checked against the manuscript Table 2. The supplied manuscript reports the same cohort sizes and headline results.

## Programme integration decision

P3 is now represented in the programme as **complete external evidence**, not as an independently rerun umbrella benchmark. Its code and results are preserved under `external/p3_litedan_v1_0_0/`, and the supplied Word manuscript is preserved under `deliverables/`.

This acceptance closes the P3 evidence dependency for programme-level documentation. It does not create a new umbrella orchestration run, and it does not change the locked results of P4, P5, or P6 R2.

## P6 boundary

P3 does **not** satisfy the P6 R3 decoder-quality gate. Its fold outputs are classification/evaluation records, not three immutable MyoSim intent streams mapped to worst/mid/best decoder conditions with model identity, source subject/session, serialization semantics, and checksums. P6 R3 therefore remains blocked before execution.

## Provenance and disclosure

The upstream P3 archive's provenance and citation metadata are retained. No raw data, authorship statement, or provenance disclosure was removed or rewritten to imply a different experimental origin. Programme-level author metadata is normalized to **Qussai Adlbi** where controlled by this umbrella release.
