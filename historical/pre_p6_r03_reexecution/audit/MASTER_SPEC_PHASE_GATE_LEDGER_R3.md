# Master Specification Phase-Gate Ledger
## Human Motor Intelligence — V2 Recovery R3 Current-State Execution

## Governance Rule

This ledger is the operational control record for the end-to-end master specification. A phase is marked **COMPLETE** only when its acceptance evidence is present and independently checkable. A phase marked **BLOCKED** has an external input dependency and is not substituted with inferred, synthetic, or relabelled material. A phase marked **DEFERRED** is intentionally outside the evidence-first V1 scope.

> **Frozen-evidence rule:** No entry in this ledger authorizes modification, recomputation, relabelling, or replacement of V1/V1.1, P4 R1, P5 R2, or P6 R2 retained artifacts. New governance records may only reference them.

## Phase Control Table

| Master phase | Acceptance gate | Baseline state | Required evidence/control record | Current disposition |
|---|---|---|---|---|
| 0 — Architectural freeze | Child projects remain independent; integration boundaries are explicit | Architecture, adapters, registry, contracts, and public-review boundary exist | `audit/test_logs/phase0_architecture_freeze_r3.txt`; architecture/gap/risk audit | COMPLETE — source scan found no copied child-project source tree; the sole `artifacts/integrated_demo/myosim` match is a code-free demonstrator output |
| 1 — Contract hardening | Existing integrations pass | Versioned records and validations exist | `audit/test_logs/phase1_contract_adapter_compatibility_r3.txt` — 11 contract/adapter tests passed; versioned records and boundary modules inspected | COMPLETE — metadata/provenance-only contracts and independent-project adapters remain compatible |
| 2 — Registry hardening | Synthetic metadata experiment can be registered and replayed | Hash-guarded local registry/event log and seeded catalog exist | `phase2_registry_workflow_r3.json`: 22 catalog entries, idempotent experiment/run hashes and event log, raw-data-loaded=false, benchmark-eligible=false; 9 registry/catalog/CLI tests passed | COMPLETE — synthetic metadata only; no scientific or benchmark claim created |
| 3 — Benchmark engine | One real EMG benchmark end-to-end | Engine/report assets plus externally archived P3 evidence package | `audit/P3_EXTERNAL_EVIDENCE_ACCEPTANCE_R3.md`; P3 registry, 657 fold records, summaries, and provenance notes | INFRASTRUCTURE COMPLETE; P3 evidence accepted as external package, not rerun by umbrella |
| 4 — EMG research validation | Existing validated EMG protocols run through orchestration and reproduced results labelled | P3 original package now externally archived and accepted | `audit/P3_EXTERNAL_EVIDENCE_ACCEPTANCE_R3.md`; full P3 package included under `external/p3_litedan_v1_0_0/` | COMPLETE AS EXTERNAL EVIDENCE ACCEPTANCE — umbrella re-execution remains a separate future validation |
| 5 — EEG validation | At least one reproducible real EEG experiment | P4/P5 primary/rerun, D1–D5, statistics, manuscripts exist | `phase5_eeg_eegemg_validation_r3.txt`: 5 EEG/fusion tests passed; P4/P5 CSV reruns byte-identical with retained SHA-256; both validation files record five pass states | COMPLETE — P4 remains harmonized external validation; P5 remains amended Jeong external validation, not pooled/direct replication |
| 6 — Multimodal preparation | Fusion/missing-modality contracts; synthetic fusion path passes | P5 fusion protocol/contract and transparent real-data evaluation exist | `phase6_multimodal_preparation_r3.txt` — 3 fusion tests passed; P5 declares EEG-only, EMG-only, early/late transparent fusion and explicitly excludes deep/missing-modality analysis | COMPLETE AS PREPARATION — empirical missing-modality and deep-fusion research remain separately unexecuted |
| 7 — MyoSim integration | Deterministic reproducible replay | Adapter, integration fixture, patch/test, R2 rerun records exist | `phase7_myosim_integration_r3.txt`: 3 MyoSim source-path integration tests plus 3 umbrella adapter tests passed; R2 run records byte-identical; patch SHA retained | COMPLETE AS SYSTEMS INTEGRATION — replay input is `synthetic-demo`/`example-decoder-v1`, not an authenticated decoder-quality condition |
| 8 — Functional benchmark | At least one complete real/replay decoder control benchmark | R2 systems fixture exists; authentic decoder traces missing | `MASTER_SPEC_PHASE8_P6_FUNCTIONAL_GATE_R3.md` and `phase8_p6_functional_gate_r3.txt`: fixture SHA/metadata verified; trace manifest inventory empty; R2_004 and R3 execution paths absent as required | BLOCKED EXTERNALLY — authenticated three-condition trace package and prospective registration required |
| 9 — Research showcase | Reviewer can navigate architecture/evidence/reproduction rapidly | README, disclosure, papers, Word outputs, reports, public-review audit exist | `docs/RESEARCH_SHOWCASE_QUICKSTART_R3.md`, deterministic Mermaid source/PNG, and `phase9_research_showcase_r3.txt`; all-spec validator passed | COMPLETE — ten-minute review route exposes architecture, evidence, demonstrator boundary, reproduction commands, and P3/P6 gates |
| 10 — Product discovery | External users demonstrate repeated value | No external-user evidence; no product operations enabled | `MASTER_SPEC_PHASE10_PRODUCT_DISCOVERY_GATE_R3.md` defines local-first researcher-readiness and future consented-pilot requirements | DEFERRED BY DESIGN — no billing/cloud/telemetry/traction claim before external evidence |
| Release discipline | Semantic status, provenance, limitations, licence, reproducibility and no overwrite | Versioned current-state release records and validators exist | Final full suite: 29 passed; `doctor` passed; R3/all-spec validators passed; verified manifest regenerated; phase-complete ZIP extracted and passed 29 tests | COMPLETE FOR CURRENT STATE — publish only as interim current-state, never final-authoritative while P3/P6 remain external gates |

## Non-Negotiable External Gates

| Gate | Exact missing input | Prohibited shortcut | Reopening condition |
|---|---|---|---|
| P3 EMG evidence | Original paper package, source/provenance, protocol and result material | Reconstructing a paper from summary values, importing an unverified claim, or treating scaffolding as an execution | Author-supplied provenance-complete package is validated and registered |
| P6 R3 decoder quality | Three frozen authentic traces with condition mapping, SHA-256, source/subject, model/checkpoint/version, serialization semantics, and use permission | Calling the `synthetic-demo` example a decoder trace, renaming it as a worst model, generating confidence/trace variants, or computing a three-condition statistic | Prospective amendment and separately namespaced run after trace acceptance |

## Evidence References

[1]: MASTER_END_TO_END_SPEC_COMPLIANCE_AUDIT_R3.md "Master End-to-End Specification Compliance Audit"
[2]: V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Replay Identity Hard Stop"
[3]: ../papers/RESEARCH_GATE_PREPARATION_RECOVERY_R3.md "P6 R3 Research-Gate Preparation"
[4]: ../REAL_DATA_VALIDATION_REPORT.md "Real Data Validation Report"
[5]: ../REPRODUCIBILITY_REPORT.md "Reproducibility Report"

This ledger operationalizes the master-spec audit, P6 hard-stop, research gate, data-validation, and reproducibility records.[1] [2] [3] [4] [5]


## R3 CPU-First Upgrade Addendum

| Extension | Acceptance evidence | Disposition |
|---|---|---|
| P5 R3-005 calibration | `results/extensions/v2-cpu-q1-upgrade-r3-005/p5_clean_loso_calibration/`; analysis statistics; independent rerun namespace; byte-identical trial probability SHA-256 | COMPLETE — confidence-aware fusion did not improve calibration or accuracy over the strongest alternatives; negative result retained |
| P4 R3-006 robustness | `audit/P4_ROBUSTNESS_COMPUTATIONAL_GATE_R3_006.md` | PENDING COMPUTATIONAL GATE — execution stopped after sustained CPU use without producing evidence; no scientific result released |

The P5 calibration completion does not alter the accepted P3 evidence boundary or the P6 R3 authenticated decoder-trace gate. The P4 computational gate is distinct from both external gates and may be reopened only with an optimized, separately registered implementation.
