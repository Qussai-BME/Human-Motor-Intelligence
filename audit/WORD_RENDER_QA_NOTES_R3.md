# Word Render QA Notes — V2 Recovery R3

## P4 DOCX Visual Check

**File reviewed:** `deliverables/P4_STRICT_ZERO_CALIBRATION_EEG_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.docx`  
**Pages reviewed:** 1–4 of 13

| Aspect | Observation | Status |
|---|---|---|
| Cover page | Professional title page rendered correctly with title, subtitle, author/version/evidence table, header, and centered page numbering | PASS |
| Typography | Title/heading hierarchy and body text are legible and visually consistent | PASS |
| Evidence disclaimer | Cover clearly states that quantitative statements are reproduced from retained artefacts and that DOCX does not supersede the versioned Markdown record | PASS |
| Manuscript structure | Front matter, Abstract, Introduction, Related Work, Data and Methods, and Results sections appear in correct order | PASS |
| Table rendering | The first visible results table on page 4 renders cleanly with shaded header and readable grid layout | PASS |
| Figure / appendix status | Not yet checked in this pass because only pages 1–4 were reviewed | PENDING |

## Next QA Steps

Remaining tasks are to inspect later pages of P4 for figure/appendix layout, and then apply the same visual QA procedure to the generated P5 and P6 DOCX files before final packaging.

## P4 DOCX Visual Check — Remaining Pages Reviewed

**Additional pages reviewed:** 5–9 of 13

| Aspect | Observation | Status |
|---|---|---|
| Figure rendering | The subject-level macro-F1 figure renders cleanly on page 5 with readable axes, caption, and discussion flow beneath it | PASS |
| End-of-manuscript sections | Discussion, Limitations, Conclusion, Data and Code Availability, and References appear in the expected order and remain legible | PASS |
| Appendix transition | Supplementary Appendix begins clearly on a new section with a visible framing note about retained evidence boundaries | PASS |
| Appendix table styling | Validation/reproducibility tables render correctly with repeated shaded headers and readable grid lines | PASS |
| Wide record tables | The long subject-level appendix tables render in landscape orientation and remain visually accessible on pages 8–9 | PASS |
| Remaining appendix pages | Pages 10–13 were not included in this visual extraction batch and still require a final spot check if full-document visual QA is desired | PARTIAL / ACCEPTABLE FOR NOW |

### Interim P4 Word QA Conclusion

The P4 DOCX is professionally formatted and suitable to keep as the template baseline for the corresponding P5 and P6 Word outputs. No rendering defect requiring regeneration was observed in the reviewed pages.

## P5 DOCX Visual Check

**File reviewed:** `deliverables/P5_TRANSPARENT_EEG_EMG_FUSION_EXTERNAL_VALIDATION_V2_RECOVERY_R3_Q1.docx`  
**Pages reviewed:** 1–5 of 10

| Aspect | Observation | Status |
|---|---|---|
| Cover page | Professional title page rendered correctly with amended external-validation evidence boundary and matching visual style to P4 | PASS |
| Manuscript flow | Abstract, Introduction, Related Work, Data and Methods, Results, and Discussion appear in correct order | PASS |
| Core numerical presentation | Primary macro-F1 values, SHA-256 statement, and amended-cohort description are visible and legible | PASS |
| Table rendering | Cohort/property table and primary-outcome summary table render cleanly with readable headers | PASS |
| Figure rendering | Subject-level macro-F1 figure renders correctly and is integrated into the Results/Discussion transition | PASS |
| Remaining pages | Pages 6–10, including the later sections and appendix portion, still require spot-check review | PENDING |

### Interim P5 Word QA Conclusion

The reviewed portion of the P5 DOCX is visually consistent with the intended professional template and shows no rendering defect that would require regeneration at this stage.

## P6 DOCX Visual Check

**File reviewed:** `deliverables/P6_INITIAL_STATE_ROBUSTNESS_AND_DECODER_QUALITY_STATUS_V2_RECOVERY_R3_Q1.docx`  
**Pages reviewed:** 1–5 of 9

| Aspect | Observation | Status |
|---|---|---|
| Cover page | Professional cover rendered correctly with distinct amber accent and explicit evidence-boundary statement that R3 decoder-quality execution is blocked | PASS |
| Hard-stop visibility | The front matter and abstract pages clearly state that authentic condition traces are absent and that R3 was not executed | PASS |
| Manuscript flow | Abstract, Introduction, Related Work, Data and Methods, Results, Discussion, Limitations, and Conclusion appear in the correct order across the reviewed pages | PASS |
| Table/figure rendering | The R2 endpoint table, descriptive scatter figure, and R3 execution-status table all render legibly | PASS |
| Claim safety after conversion | The DOCX preserves the distinction between a reproducible R2 fixture study and an unexecuted decoder-quality comparison | PASS |
| Remaining pages | Pages 6–9, including the appendix portion, still require later spot-check review | PENDING |

### Interim P6 Word QA Conclusion

The reviewed portion of the P6 DOCX successfully preserves the programme’s most critical evidence-governance message: R2 is a systems-fixture result, whereas R3 decoder-quality inference remains blocked pending authentic trace provenance.

## P5 DOCX Visual Check — Remaining Pages Reviewed

**Additional pages reviewed:** 6–10 of 10

| Aspect | Observation | Status |
|---|---|---|
| End-of-manuscript sections | Limitations, Conclusion, Data and Code Availability, and References render clearly and remain professionally spaced | PASS |
| Appendix transition | Supplementary Appendix begins clearly on a separate section with an evidence-boundary framing note | PASS |
| Validation and reproducibility tables | D1–D5 and artefact/reproducibility tables render cleanly with readable repeated headers | PASS |
| Full subject-level appendix table | The long 24×4 record table is preserved in landscape orientation and remains legible across pages 8–9 | PASS |
| Statistical appendix | The descriptive/pairwise table renders correctly; however, the `Raw p` column displays `nan`, which reflects the current appendix-generation output rather than a Word rendering fault | CONTENT ISSUE TO FIX |
| Figure and no-confusion-matrix note | The appendix figure and retained no-post-hoc-confusion-matrix statement render correctly on page 10 | PASS |

### Interim P5 Word QA Conclusion

The P5 DOCX layout is strong and suitable for delivery, but the appendix source should be corrected so that the `Raw p` column shows retained numerical values instead of `nan` before final packaging.

## P5 DOCX Corrective QA

**Page re-reviewed:** Page 9 after appendix regeneration

The `Raw p` column now displays retained numerical p values (`0.68398643`, `0.00200093`, `0.35962629`, `0.00020516`, `0.96644723`, `0.00012708`) rather than `nan`. The correction uses the existing locked `p_value_raw` field from the P5 statistics artefact and introduces no new analysis. The landscape table remains legible.

**Corrective status: PASS.**

## P6 DOCX Visual Check — Remaining Pages Reviewed

**Additional pages reviewed:** 6–9 of 9

| Aspect | Observation | Status |
|---|---|---|
| End-of-manuscript sections | Data and Code Availability and References render clearly, with the hard-stop source path still visible | PASS |
| Appendix transition | Supplementary Appendix starts cleanly on a new section with an evidence-boundary statement | PASS |
| Protocol/reproducibility table | Appendix protocol and interpretation table is readable and preserves the integration-fixture classification | PASS |
| Full per-record table | The 20-seed table renders in landscape orientation and remains legible across pages 7–8 | PASS |
| Endpoint table | Wilson interval and bootstrap summary rows remain readable and numerically intact | PASS |
| Figure and interpretation note | The appendix figure renders correctly on page 9 and is followed by the no-confusion-matrix / no-valid-R3-condition statement | PASS |

### Final P6 Word QA Conclusion

The P6 DOCX preserves both scientific readability and the programme’s critical governance boundary. No layout or wording defect requiring regeneration was observed in the reviewed pages.

## P4 DOCX Visual Check — Final Pages Reviewed

**Additional pages reviewed:** 10–13 of 13

| Aspect | Observation | Status |
|---|---|---|
| Long appendix table continuity | The remaining subject-level rows continue cleanly across pages 10–11 with stable landscape layout and readable grid structure | PASS |
| Pairwise statistics table | The page-12 pairwise statistical table renders correctly and now shows retained raw p values rather than placeholder `nan` output | PASS |
| Figure and closing note | The appendix figure on page 13 renders clearly and the no-post-hoc-confusion-matrix statement remains visible and readable | PASS |
| Full-document completeness | Cover, manuscript body, figure, appendix, long tables, pairwise statistics, and figure-availability note are all present through the end of the document | PASS |

### Final P4 Word QA Conclusion

The P4 DOCX has now been spot-checked across its full page range and is suitable for final delivery as a standalone file and as part of the revised interim ZIP.
