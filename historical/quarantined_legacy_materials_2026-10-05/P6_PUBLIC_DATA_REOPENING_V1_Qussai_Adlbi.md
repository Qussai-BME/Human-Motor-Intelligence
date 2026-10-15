# P6 R3 Public-Data Reopening: Real EEG Decoder Traces and Initial-State Robustness Readiness

**Responsible author:** Qussai Adlbi  
**Protocol:** `p6-r3-public-data-reopening-v1`  
**Evidence status:** Real public-data decoder validation completed; simulator replay contract validated separately; historical P6 R3 remains a distinct hard stop.

## Result

A CPU-first LOSO study was executed on 20 real subjects from PhysioNet EEGMMIDB v1.0.0, using run R03 unilateral fist motor imagery. Each held-out subject contributed 15 annotated trials. Three predeclared decoder families produced 60 raw traces and 60 quality-stratum aliases, covering 900 held-out prediction events.

Quality strata were assigned using source-only three-fold balanced accuracy before interpreting held-out outcomes. The mapping was `quality_worst = middle`, `quality_middle = best`, and `quality_best = worst`. Held-out mean balanced accuracy was 0.454 for quality_worst, 0.438 for quality_middle, and 0.497 for quality_best. The relationship was weak and non-monotonic; no monotonic decoder-quality claim is supported.

The paired comparisons are recorded in `results/PAIRED_STATISTICS.json`. All three comparisons are reported without claim inflation. The quality_worst versus quality_best mean difference was approximately -0.043 (worst minus best), with a bootstrap interval spanning zero and a non-significant paired test. The decoder conditions therefore provide authentic quality-contrast traces, but not evidence of a universal quality-to-task-success law.

## Trace provenance

The traces were generated directly from held-out EDF recordings. Each CSV records source subject, model version, window identifier, predicted label, confidence, ground truth, and correctness. All source files have SHA-256 digests in `audit/DATASET_MANIFEST.json`; all trace digests are in `results/TRACE_MANIFEST_QUALITY_STRATA.json`. The traces are not synthetic and are not derived from the historical `synthetic-demo` fixture.

OPEN/CLOSE are documented MyoSim V1 IntentLabel values. The trace CSVs therefore satisfy the replay input schema. They remain offline decoder replay inputs, not clinical validation and not proof that an EEG label is equivalent to a prosthetic user's real-time intent.

## Limitations

The cohort is one PhysioNet run and one modality. The source has two classes and 20 subjects in this execution, not the full public repository. The decoder is a transparent CPU baseline rather than a clinical model. MyoSim receives the authenticated prediction stream, not raw EEG. Any task result is conditional simulator systems evidence. The historical P6 R3 hard stop remains preserved and is not silently rewritten.

## References

[1]: https://www.physionet.org/content/eegmmidb/1.0.0/ "EEG Motor Movement/Imagery Dataset v1.0.0"
[2]: https://doi.org/10.13026/C28G6P "PhysioNet EEGMMIDB DOI"
[3]: https://www.bbci.de/competition/iv/desc_2a.pdf "BCI Competition IV Data Set 2a description"

## MyoSim replay validation

One held-out S001 trace from each quality stratum was passed through MyoSim V1.1 (`0.1.3`) with the MuJoCo backend. All three runs completed with `invalid_state_detected=false`. The controller consumed 15 events per trace. Released-command count was zero in all three runs because the alternating held-out predictions did not satisfy the fixed temporal confirmation rule. This is an authentic controller outcome, not a decoder-quality failure or a fabricated task success. Full run IDs, trace digests, transition counts, and simulator provenance are in `results/MYOSIM_REPLAY_VALIDATION.json`.
