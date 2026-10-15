# Benchmark Report
## V2 Recovery R3 Current-State Addendum

## Benchmark Governance

The benchmark engine accepts comparisons only when dataset, protocol, task, label space, calibration policy, outcome definitions, and subject-level inference are compatible. This report applies that rule to the currently retained evidence. A statistic that is valid within an experiment is not automatically a benchmark-wide ranking.[1]

## Benchmark-Eligible Study-Level Results

| Study | Eligibility decision | Internal comparison family | Primary outcome | Result boundary |
|---|---|---|---|---|
| P4 R1 OpenBMI | Eligible for its declared OpenBMI binary-MI LOSO comparison | Five predeclared model conditions, 54 subject-level outcomes each | Macro-F1 | Internal OpenBMI-only comparison; not BCI IV-2a ranking |
| P5 R2 Jeong | Eligible for its declared amended Jeong all-11-class MI LOSO comparison | Four predeclared LDA conditions, 24 subject-level outcomes each | Macro-F1 | Internal Jeong-only comparison; not pooled with Cho2017 or P4 |
| P6 R2 | Not a biosignal benchmark | One simulation fixture across 20 initial states | Task completion/error/state | Systems evidence only; not a decoder-quality benchmark |
| P6 R3 | Not executed | None | None | No valid condition traces; no benchmark entry |

## P4 Internal Benchmark Summary

| Model | Mean macro-F1 | SD | Pairwise status after Holm |
|---|---:|---:|---|
| Linear | 0.5962 | Retained in statistics artefact | No supported superiority claim |
| LDA | 0.5980 | Retained in statistics artefact | No supported superiority claim |
| Linear SVM | 0.6123 | Retained in statistics artefact | No supported superiority claim |
| Spectral | 0.6130 | Retained in statistics artefact | No supported superiority claim |
| Compact CNN | 0.6364 | Retained in statistics artefact | Highest descriptive mean; no Holm-surviving pairwise contrast |

The P4 Friedman test is χ²=16.16, p=0.0028118. Its post-hoc family contains ten comparisons; minimum Holm-adjusted p=0.104209. The appropriate result is a non-null overall model effect with unresolved pairwise superiority after multiplicity correction.[2]

## P5 Internal Benchmark Summary

| Condition | Mean macro-F1 | SD | Interpretation |
|---|---:|---:|---|
| EEG-only LDA | 0.0812699 | 0.0251763 | Reference condition |
| EMG-only LDA | 0.0484373 | 0.0257410 | Lower than three specified conditions in selected within-source contrasts |
| Early-fusion LDA | 0.0754068 | 0.0341115 | No Holm-supported gain over EEG-only |
| Late-fusion LDA | 0.0805164 | 0.0315438 | No Holm-supported gain over EEG-only |

The P5 Friedman test is χ²=16.25, p=0.0010077. The EEG-only/early/late versus EMG-only contrasts meet the declared Holm-adjusted threshold in specific directions, but none of the fusion-versus-EEG-only contrasts do. This does not establish a general property of multimodal fusion or an EMG mechanism.[3]

## Non-Comparable Evidence

P4 and P5 must not be placed on a shared numeric leaderboard because they differ in source, subject set, class structure, modality set, model family, and scientific question. The historical Cho2017 evidence remains frozen as a distinct source. P6 task outcomes are not classifier macro-F1 and must not be converted into an upstream decoder benchmark.

## Future Benchmark Admission Requirements

A new real-data entry must provide an immutable data/source manifest, D1–D5 validation, a registered protocol, subject-level outcomes, a reproducibility rerun, and a compatibility decision against the existing benchmark family. P6 can enter a decoder-quality control benchmark only after three authentic immutable decoder traces and their authoritative condition manifest pass the R3 research gate.[4]

## References

[1]: BENCHMARK_GUIDE.md "Benchmark Governance"
[2]: results/real/v2-recovery-r1/nemar-nm000338-openbmi-p4-external-loso-recovery-r1/statistics_macro_f1.json "P4 Statistics"
[3]: results/real/v2-recovery-r2/nemar-nm000311-jeong-p5-external-loso-24subject-r2/statistics_macro_f1.json "P5 Statistics"
[4]: papers/RESEARCH_GATE_PREPARATION_RECOVERY_R3.md "R3 Research Gate"

The benchmark classifications follow the programme’s compatibility and claim-boundary controls.[1] [2] [3] [4]
