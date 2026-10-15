# Research and Release Roadmap
## V2 Recovery R3 Current-State Plan

## Position

The programme has completed a substantial evidence and infrastructure layer: source-bound P4/P5 external validations, P6 simulator-state methodology with a trace-provenance hard stop, Q1 integration records, and a local reproducibility framework. The next steps are gated by evidence availability rather than convenience.

## Evidence-Gated Roadmap

| Gate | Prerequisite | Authorized work after gate | Completion evidence |
|---|---|---|---|
| G1 — P3 intake | Original Paper 3 export/manifests, protocol context, usage permission | By-reference manifest import and eligibility audit; no protocol reconstruction | P3 provenance/eligibility report and correctly scoped integration update |
| G2 — P6 trace intake | Three frozen authentic replay traces plus authoritative manifest/checksums/model/source identity | Register R2_004 or new R3 namespace; validate/parser-check traces; execute locked state protocol | Condition-level records, D1–D5-style input checks, independent rerun, justified comparison |
| G3 — Direct EEG expansion | Registered legal BCI IV-2a source access and protocol | Source-specific LOSO study separate from P4 | Manifest, gates, subject-level outcomes, rerun, source-bound manuscript update |
| G4 — Multimodal robustness | Paired, source-defined EEG–EMG cohort and registered missing-modality policy | EEG-only, EMG-only, fusion, EEG-missing, EMG-missing comparisons | Complete matched-condition result and validity audit |
| G5 — Additional modalities | Registered/authorized ECG or ECoG/iEEG source and task-specific protocol | Separate modality-specific benchmark | Source-compatible validation/reproducibility package |
| G6 — Translational research | Safety, ethics, hardware, and clinical-study design | Hardware/clinical assessment, if independently approved | Separate evidence package; no inference from current offline/simulation studies |

## Near-Term Release Maintenance

Before external submission or collaborator handoff, maintain the interim release label, verify the ZIP checksum, retain raw-data exclusion, and ensure all public summaries link to `SCIENTIFIC_LIMITATIONS.md` and the P6 R3 hard-stop record. The Word versions of P4/P5/P6 are publication-formatted copies of the frozen-current manuscripts; their claim boundaries are identical to the Markdown sources.

## Decision Rule

No gate may be bypassed by synthetic trace editing, authorless condition labels, retrospective model mapping, source pooling, or post-hoc tuning. A blocked study is a legitimate outcome and should remain visible in all release revisions until its stated prerequisite is fulfilled.

## References

[1]: audit/SPECIFICATION_COMPLETION_MATRIX_ALL_SPECS_R3.md "All-Specification Completion Matrix"
[2]: papers/RESEARCH_GATE_PREPARATION_RECOVERY_R3.md "P6 R3 Research Gate"
[3]: SCIENTIFIC_LIMITATIONS.md "Scientific Limitations"

The roadmap follows the documented completion status and evidence-gating rules.[1] [2] [3]
