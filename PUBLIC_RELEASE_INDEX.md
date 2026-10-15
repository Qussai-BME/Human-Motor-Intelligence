# Public Release Index

P6 is reported in three stages. **C1** (R04 motor imagery, strict LOSO, frozen decoder quality, validated fixture, 60 + 60 run-level artifacts) returned 0/60 task successes. A **post-hoc audit** (`p6/c1_audit`) showed that endpoint was unreachable by design (oracle also 0/20). The **C2 registered follow-up** (`p6/c2_episode`) restored a valid endpoint (oracle 100/100) and showed that control success in the confidence-gated controller follows gate passage, not decoder accuracy.

Entry points: `README.md`, `P6_FINAL_STATUS.md`, `papers/paper_6/` (manuscript v2, results summary, claim–evidence matrix), `p6/c2_episode/README.md`, `release/RELEASE_MANIFEST.json`.

The earlier R03 experiment remains available as an engineering/preflight motor-execution baseline only and is not reclassified as motor imagery.
