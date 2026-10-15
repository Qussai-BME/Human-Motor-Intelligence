# Human Motor Intelligence — Six-Paper Research Synthesis (V2 Recovery R1)

> **P2 note (2026-10-06):** statements about Paper 2 in this document describe its first version and are superseded; see `P2_SUPERSESSION_NOTICE.md` in `papers/`.


## Programme Thesis

The programme investigates how motor intent can be decoded across individuals without subject-specific calibration. Its evidence does not form a single pooled benchmark. Rather, it follows linked but distinct questions about metric validity, cross-subject representation transfer, EEG generalisation, transparent multimodal fusion, and downstream replay/control evaluation.

## Paper Sequence

| Paper | Central question | Current evidence status | Main contribution / limit |
|---|---|---|---|
| P1 | Can rest-class prevalence inflate apparent cross-subject sEMG performance? | Author-supplied source grounded | Shows a source-specific divergence between aggregate accuracy and macro/active performance; not a universal prevalence law. |
| P2 | Why can adaptation fail for a MiniROCKET sEMG representation under LOSO? | Author-supplied source grounded | Identifies a representation-specific PPV conditioning mechanism; not a verdict on all adaptation. |
| P3 | Companion EMG extension | **`[VALUE NOT PROVIDED — PENDING PAPER 3 EVIDENCE]`** | No content, number, or conclusion is available for synthesis. |
| P4 | Does strict zero-calibration subject-level EEG MI evaluation extend to an independent dataset? | V2 external validation completed | OpenBMI Recovery R1 passed D1–D5 and exact rerun; interpretation remains external/harmonized, not direct replication. |
| P5 | Does transparent EEG–EMG fusion benefit cross-subject MI decoding externally? | V2 source gate blocked | No valid Jeong result; no external fusion conclusion. Frozen Cho2017 result remains primary. |
| P6 | Do decoder-quality/replay conditions predict system outcome across independent repeats? | V2 capability gate blocked | No valid repeat distribution because current MyoSim seed does not vary state/task/replay conditions. |

## P1–P2 Evidence Alignment

P1 and P2 share a cross-subject sEMG domain but have different target/metric policies. P1’s rest-inclusive reporting identifies a potential rest-class interpretation problem. P2 excludes rest from reported accuracy and focuses on MiniROCKET representation conditioning under adaptation. These papers should be read together as a warning that both **what is evaluated** and **what is represented** can change the apparent cross-subject conclusion. They must not be combined into a common accuracy table without harmonizing their target definitions.

## P4 V2 External Validation

P4 Recovery R1 tested five fixed conditions under zero-calibration, subject-level LOSO on 54 OpenBMI subjects. Mean macro-F1 ranged from 0.5962 (linear) to 0.6364 (compact CNN). The omnibus Friedman test was significant (χ²=16.16, *p*=0.00281), but no predeclared pairwise comparison survived Holm adjustment. An independent 54-fold rerun reproduced the complete 270-row subject-level result file byte-for-byte.

This supports a modest, auditably reproducible statement: a strict subject-independent binary MI evaluation can be executed on an external large EEG cohort with performance distributions that remain heterogeneous across subjects. It does not directly reproduce BCI IV-2a, settle a universal performance question, or establish a definitive winning model within the tested family.

## P5 and P6: Why the Stops Matter

P5 and P6 illustrate the programme’s governance threshold. The Jeong derivative looked scientifically relevant, but the locked all-11-class, 25-subject MI cohort was unavailable because one subject lacks the third imagery run and two classes. Continuing with an unannounced 24-subject or nine-class subset would turn data availability into an outcome-adjacent selection. The programme stopped instead.

Likewise, MyoSim exposes a seed field, but its inspected reset path seeds NumPy then resets MuJoCo deterministically without sampling state/task/replay variation. Re-running this identical condition would create repeat labels, not independent repeats. The programme therefore has no V2 P6 distribution, confidence interval, or system robustness claim. These stops are substantive findings about evidence readiness rather than holes to conceal.

## Integrated Claim Boundary

> The programme supports protocol-specific, auditable investigation of cross-subject motor-intent decoding. It does not yet support a universal model ranking, a causal account of EMG dominance during imagery, a general fusion verdict, a clinical benefit claim, or a repeat-based control robustness estimate.

## Traceability

Programme-level readers should consult `Q1_EVIDENCE_EXPANSION_MASTER_AUDIT.md` for all evidence tiers and `SIX_PAPER_CLAIM_COUNTERCLAIM_AUDIT.md` for claim status. P4 quantitative values are traceable to the immutable Recovery R1 result and rerun directories. P1/P2 are traceable to supplied DOCX source extracts. P3 uses only the explicit pending placeholder. P5/P6 use hard-stop audits rather than fabricated result artefacts.
