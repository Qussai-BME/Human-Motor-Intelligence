# Master End-to-End Package Assembly Audit
## V2 Recovery R3 Current-State Addendum

## Package Intent

The master end-to-end package is a **comprehensive interim current-state release**. It must allow an external reviewer to inspect the umbrella architecture, contracts, registry, protocols, benchmark/reporting surfaces, P4/P5 evidence, P6 R2 systems evidence, P6 R3 trace-provenance hard stop, P3 pending status, manuscripts, Word deliverables, tests, and reproducibility records without receiving raw participant data or an invented computation.

## Inclusion Criteria

| Required package content | Acceptance rationale |
|---|---|
| Source, tests, `pyproject.toml`, CLI, registry, contracts, adapters, benchmark/reporting/provenance code | Enables inspection and local Research-OS verification |
| All governing specifications including the 2026-08-26 master end-to-end copy | Makes the release self-contained and auditable |
| Master-spec compliance audit, implementation status, release note, and workflow test logs | Shows what was executed against the new specification |
| Frozen P4/P5 primary and rerun artefacts, protocols, validations, figures, papers, appendices, reviews, and DOCX | Retains complete available external-validation evidence |
| P6 R2 patch, guide, baseline/state artefacts, rerun, manuscript, appendix, review, and identity hard stop | Preserves systems evidence and governance correction together |
| Public-review README, disclosure, citation, license, notice, limitations, release/checklist documents | Prevents a reviewer from misreading the package as final or clinical |
| Verified artifact manifest and release validators | Provides byte-level evidence identity and structural checks |

## Exclusion Criteria

| Excluded content | Reason |
|---|---|
| Raw BDF/EDF/GDF/SET/FIF data | Participant/source-data governance; data must be acquired independently |
| Derived NPZ cache | Derived participant data and cache are outside the release policy |
| Credentials, `.env`, secret/key material | Security and local-first governance |
| `.git`, runtime cache, compiled Python files | Non-essential, potentially environment-specific material |
| P6 R2_004 amendment, R3 execution namespace, synthetic replacement traces, decoder-quality statistics | These do not exist and must never be fabricated |
| Vendored MyoSim/MyoAdapt/MyoControl/BioSignal-FM source trees | Child projects remain independent and separately licensed |

## Required Interpretation

The package is publishable for expert review when called **V2 Recovery R3 Master End-to-End Interim Current-State**. It must not be labelled final-authoritative, P6-complete, clinical, product-ready, or a real-decoder functional benchmark. The P6 R3 hard stop and P3 pending state are release acceptance requirements: if either disclosure is absent, the package fails this audit.[1] [2]

## References

[1]: MASTER_END_TO_END_SPEC_COMPLIANCE_AUDIT_R3.md "Master End-to-End Specification Compliance Audit"
[2]: V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Replay Identity Hard Stop"
[3]: ../RELEASE_NOTES_MASTER_END_TO_END_R3.md "Master End-to-End Release Notes"

The inclusion, exclusion, and interpretation rules follow the master-spec audit, P6 hard-stop, and release notes.[1] [2] [3]
