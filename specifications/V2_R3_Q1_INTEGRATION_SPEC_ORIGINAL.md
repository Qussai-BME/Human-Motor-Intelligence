V2 RECOVERY R3 — P6 DECODER-QUALITY × INITIAL-STATE COMPLETION AMENDMENT

Scope: extend the already-built, already-verified P6 Recovery R2 initial-state
perturbation capability (uniform_forearm_xy_v1, seeds 20260901-20260920) to
the two remaining real decoder-quality conditions from the frozen P6 single-
replay result (the mid-tier and best-performing decoder traces; tiny_cnn/
worst was already run in R2 — confirm which one R2 actually used and treat
the other two as the extension).

Do not change the perturbation distribution, seed set, task, controller, or
any other locked parameter from V2_PROTOCOL_AMENDMENT_RECOVERY_R2_003_P6.md.
This is purely a repetition of the identical protocol across two additional
fixed replay inputs.

Register a new protocol amendment (R2_004) stating explicitly: which decoder
trace R2 already used, and that this amendment adds the other two under
byte-identical perturbation methodology, before running anything.

Execute both decoder conditions x 20 seeds, full D1-D5, independent
reproducibility rerun (exact match required) for each, exactly as done for
the first condition.

Required analysis: report per-decoder-condition success/failure proportions
with Wilson CIs side by side (3 conditions x 20 runs = 60 total), and a
predeclared statistical comparison (e.g. Cochran's Q or Fisher's exact across
the three conditions) testing whether success proportion differs by decoder
quality. State plainly whether this now supports, contradicts, or remains
inconclusive about a decoder-quality-to-robustness relationship. If all three
still fail 0/20 identically, that is a complete, valid, and notably strong
result: task fragility to initial-state perturbation is independent of the
decoder-quality range tested. Report it exactly that way — do not search for
a way to manufacture a difference.

Update P6_REAL_REPLAY_INITIAL_STATE_ROBUSTNESS_V2_RECOVERY_R2.md into a
versioned R3 file with the complete three-condition result, superseding the
single-condition interpretation without deleting the R2 artifacts.

Same reproducibility, checksum, and hard-stop discipline as all prior phases
applies unchanged.
FINAL INTEGRATION AND PACKAGING — POST-R3

## PART D — MANUSCRIPT INTEGRATION TO FULL Q1 STANDARD (mandatory before packaging)

The current P4/P5/P6 evidence-status files are strong evidence reports but are
NOT yet complete Q1-standard manuscripts. Before final packaging, merge each
into the full required structure:

Title, Abstract, Keywords, Introduction, Related Work, Data and Methods,
Results, Discussion, Limitations, Conclusion, Data and Code Availability,
References.

Specifically:
1. Add a Keywords line to each of P4, P5, P6.
2. Add a proper Related Work section to P4 and P5, built from
   papers/LITERATURE_RESEARCH_LOG.md plus any additional live research needed
   to reach the same depth as the earlier six-paper program delivery
   (target: comparable citation density to that prior version, not fewer
   sources than were previously assembled).
3. Add an explicit Limitations section to P4 (currently missing as a
   standalone section).
4. For P6, integrate the R3 three-condition result (once complete) into the
   same full structure.
5. Produce a proper APPENDIX.md for each paper: full per-subject/per-record
   result tables, full pairwise statistical tables, reproducibility record,
   validation gate summary, confusion matrices/figures — matching the depth
   of the appendices already produced in the earlier six-paper program
   package (paper_4/paper_5/paper_6 APPENDIX.md files), updated with the new
   R1/R2/R3 evidence.
6. Produce Q1_REVIEW.md and EVIDENCE_GAP_AUDIT.md for each of P4, P5, P6,
   reflecting the final GREEN/YELLOW/RED disposition given all Recovery R1–R3
   evidence now available.
7. Run a final CROSS_REFERENCE_AUDIT and SIX_PAPER_RESEARCH_SYNTHESIS update
   incorporating all final results.

Every number carried into these manuscripts must trace to an already-produced
result artifact from R1/R2/R3 — no new computation is authorized in this
integration step, only writing/organizing/citing.

## PART E — FINAL PACKAGE

Once Part D is complete for all three papers:

1. Consolidate the entire project — all frozen V1/V1.1 evidence, all V2
   Recovery R1/R2/R3 evidence, all finalized Q1-standard manuscripts and
   appendices, all audits, all reproducibility records, the EMG series
   master evidence record, the MyoSim patch, and all program-level synthesis
   files — into a single directory representing the final, current state of
   the entire six-paper program.
2. Do not delete any historical/frozen evidence file; supersede only where
   explicitly versioned (R1 → R2 → R3) per the existing convention.
3. Produce a top-level `FINAL_PROGRAM_RELEASE_NOTES.md` summarizing: what
   exists, what evidence tier each paper's headline claim rests on, current
   Q1 disposition (evidence/literature/reviewer-resilience) for P4, P5, P6,
   and explicit outstanding items (if any) for author decision before
   submission.
4. Package the entire consolidated directory into a single final ZIP file.
5. Confirm the ZIP's contents against `papers/CROSS_REFERENCE_AUDIT.md` and
   the final reproducibility matrix before delivery — no orphaned or
   inconsistent file should remain.

Deliver exactly one final ZIP file representing the complete, current,
authoritative state of the Human Motor Intelligence six-paper program.