# Input Inventory — Closure R1

**Owner:** Qussai Adlbi  
**Inventory date:** 2026-10-02  
**Authoritative candidate:** `Human_Motor_Intelligence_COMPLETE_PUBLIC_RELEASE_Qussai_Adlbi_P3_P6_R3_2026-10-02.zip`

## Candidate package

- SHA-256: `98769011098a00b8afa5e44cc2ae5d11ade4809135bf5ff8c714a9c6f873a41e`
- Size: 38639598 bytes
- ZIP integrity: passed `unzip -t`; 1,624 entries in the supplied candidate.
- Root: `human-motor-intelligence-v1_1/`
- No Git metadata was present in the candidate; no source commit or tag can be truthfully assigned.

## Critical sources and precedence

| Area | Current authoritative source | Evidence tier | Current disposition |
|---|---|---:|---|
| P1 | `[supplied-input]/Rest-Class_Metric_Inflation_in_Zero-Calibration_Cross-Subject_sEMG.docx` plus extracted audit text | 5 / source manuscript | Frozen source-grounded record; full raw-result package is not in candidate |
| P2 | `[supplied-input]/Paper2_MainManuscript_FINAL.docx` plus extracted audit text | 5 / source manuscript | Frozen source-grounded record; full raw-result package is not in candidate |
| P3 | Zenodo archive `10.5281/zenodo.22768799`, preserved at `external/p3_litedan_v1_0_0/`, plus supplied DOCX | 2–5 | Accepted external evidence: 27 summaries, 657 LOSO folds |
| P4 | `results/real/v2-recovery-r1*`, P4 manuscript, manifest, statistics, rerun | 2–5 | Current R3 evidence retained |
| P5 | `results/real/v2-recovery-r2*`, P5 manuscript, manifest, statistics, rerun | 2–5 | Current R3 evidence retained |
| P6 R2 | `results/real/v2-recovery-r2/p6_real_replay_initial_state_repeats_r2/` and audit records | 2–4 | Frozen systems/integration fixture study |
| P6 R3 | No accepted trace source; source audit in `papers/paper_6/TRACE_SOURCE_AUDIT.md` | — | BLOCKED before execution |
| MyoSim | `[supplied-input]/MyoSim_V1.1_Public_Release_0.1(1).zip` | 3 | Public runtime and fixture only; not a decoder source |
| MyoControl | `[supplied-input]/myocontrol-main.zip` | 3–5 | Code and result JSONs; no checkpoint or permitted source data present |
| MyoAdapt | `[supplied-input]/MyoAdapt_v2_0_HARDENED_PATCHED.zip` | 3 | Code/export surface; no compatible frozen checkpoint/source-data bundle |
| BioSignal-FM | `[supplied-input]/BioSignal-FM-V4-Prepublication-Release.zip` | 3 | Representation platform; no P6-compatible decoder trace source |

## Checksums

```text
candidate ZIP       98769011098a00b8afa5e44cc2ae5d11ade4809135bf5ff8c714a9c6f873a41e
P3 Zenodo archive   b382a40aa9a40556a6169ca805fc92c1d75a94e6d982b845ca489dd37c158f14
P1 manuscript       8388430d30d0ab965251f68f4e9e11e94d2cd425f5eb16efd05f22223fe5cb4b
P2 manuscript       c2d54049065b1e1554a875440e664ece93aebd517723842006e42ec2722bc378
P3 manuscript       1a84ccc9e6985f46947245f4815b618d1195067f832bbe8703bcb95350b5256f
MyoControl archive  505bdf6033f89937c64cd7bb102505d6525ace1781de194203f045471186f54b
MyoSim archive      26c66dc215f0c26f7b1978321d90b0bde45a5b5691f730076c60a71149f503d2
MyoAdapt archive    17c158fd137fbaf771877d18f1b25caa8bf27dca73f54da6bac65b525c20b12a
BioSignal-FM archive 9c78b2f1fa8ba607135900a04c2dd133c9788bbc9ad202ac52168c9e4f68c2c3
```

## Omitted dependencies

Raw NinaPro/NEMAR recordings, derived participant caches, MyoControl model weights, and an authenticated P6 decoder output stream are not present. Their absence is preserved as a dependency, not filled with synthetic substitutes.
