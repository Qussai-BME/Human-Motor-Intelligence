# Final Release Verification — Human Motor Intelligence 1.1.0

**Release disposition:** READY FOR PUBLIC RELEASE

## P6 C1 scientific closure
- Protocol: `P6-C1-MI-R04-v1.0`
- Dataset condition: PhysioNet EEGMMIDB R04 unilateral motor imagery, S001–S020.
- Models: M1/M2/M3 with quality order frozen before downstream analysis.
- MyoSim fixture: 1/1 COMPLETE.
- Primary runs: 60; task success 0/60 for every model.
- Rerun runs: 60; task success 0/60 for every model.
- Rerun task artifacts: 60; run IDs and SHA-256 hashes distinct from primary.
- Decoder traces: deterministic and byte-identical between primary and rerun.
- Primary endpoint: non-discriminative; continuous endpoints remain exploratory.

## Release integrity
- Current-facing status documents are consistent with C1 completion.
- R03 is retained only as engineering/preflight baseline evidence.
- Raw R04 EDF files are not redistributed; source hashes remain recorded in the dataset manifest.
- No build/cache/bytecode artifacts are included in the public tree.
- The release manifest is self-excluded to avoid circular hashing.

## Automated verification
- Pytest result is recorded in the release build log.
- Public-release doctor: PASS.
- DOCX accessibility audit: 0 high / 0 medium / 0 low.
- DOCX render: 3 pages visually inspected.

## Scientific boundary
The release supports the registered R04 cohort/task result only. It does not establish clinical efficacy, prosthetic efficacy, online human BCI performance, or a general law relating offline decoder quality to control utility.
