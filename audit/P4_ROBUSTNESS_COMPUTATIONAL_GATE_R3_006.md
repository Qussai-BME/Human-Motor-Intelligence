# P4 Robustness Computational Gate — R3-006

## Decision

The registered clean-train/corrupted-test P4 robustness runner was started using the temporal representation selected by the representation ablation. After more than 15 minutes of sustained CPU execution, no result directory or partial result artifact had been written. The process was stopped to protect the sandbox and prevent an incomplete result from entering the evidence namespace.

## Scientific status

No robustness number, figure, or claim was released from the interrupted process. The P4 robustness experiment remains **PENDING COMPUTATIONAL GATE**. The failed execution does not invalidate P4 R1, P4 log-Euclidean R3-001, or P4 representation ablation R3-004. A future implementation may use a compiled/vectorized temporal transform or a lighter prevalidated classifier, but it must receive a new protocol/run record and independent rerun.

## Boundary

This gate is not a negative robustness result. It is an execution non-result. No claim about channel dropout, noise, jitter, or deployment robustness may cite R3-006.
