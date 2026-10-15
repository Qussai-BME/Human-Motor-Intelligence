# P6 R3 Protocol and Deviation Record

**Status:** Historical protocol record reconciled after audit; not a confirmatory motor-imagery protocol.  
**Dataset/run actually used:** PhysioNet EEGMMIDB v1.0.0, R03. The official dataset documentation identifies R03 as motor execution, not imagery.  
**Design:** 20 subjects × 3 decoder configurations; source-only quality ranking; offline MyoSim replay.

## Frozen analysis choices
- Source-only mean 3-fold balanced accuracy used to rank M1/M2/M3 before task analysis.
- Primary endpoint: `COMPLETE` task status.
- Secondary continuous endpoints: final error, path length, command corrections, grasp stability, and transition-derived release events.
- Paired omnibus tests: Friedman with subject as block; Kendall's W reported.
- No row-level Spearman correlation because the quality predictor is model-level with only three distinct values.

## Material limitations/deviations discovered in closure audit
1. R03 is motor-execution EEG, not motor imagery.
2. T1/T2 were mapped to generic OPEN/CLOSE commands for software integration; this mapping is abstract and not physiologically validated.
3. All 60 tasks failed to reach `COMPLETE`, making the primary endpoint non-discriminating.
4. The original per-run release counter did not reflect explicit release transitions. A reconciled metric was derived from transition logs; original values were preserved.
5. The independent rerun aggregate matches the primary aggregate, but individual rerun JSON artifacts are absent; full independent rerun execution cannot be independently audited from this archive.

## Disposition
These records support exploratory systems feasibility only. They do not support a confirmatory motor-imagery decoder-quality-to-task-success claim.
