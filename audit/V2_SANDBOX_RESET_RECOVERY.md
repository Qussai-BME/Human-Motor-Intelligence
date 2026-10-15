# V2 Sandbox Reset Recovery Record

**Recorded:** 2026-08-23 (GMT+3)  
**Status:** Recovery record; not scientific evidence  
**Scope:** Execution environment only

## Event

During the V2.0 external-validation acquisition stage, the sandbox reported that it had been reset and that most files from the previous session were cleared. The former V1.1/V2 worktree and all external derived caches were absent immediately after this event. This record distinguishes the operational loss from the programme's frozen scientific evidence: absence of a local copy is **not** evidence that a prior result did not exist, and no historical results may be silently reconstructed, overwritten, or relabelled.

## Verified Recovery Source

The baseline repository was restored only from the user-supplied archive below. The archive remains unmodified in `<LOCAL_WORKSPACE>/upload`.

| Field | Value |
|---|---|
| Source archive | `[supplied-input]/human-motor-intelligence-deliverable.zip` |
| SHA-256 | `a7c686187faf23ba1c859d036ff03bbe494a7691e1858229b2d161717b6c3cec` |
| Restored destination | `<LOCAL_WORKSPACE>/human_motor_workspace/work/human-motor-intelligence-v1_1` |
| Restored top-level project identity | `human-motor-intelligence` baseline archive |
| Recovery action | Extracted to a fresh worktree; the upload was not modified |

## Post-reset Inventory

At the time of the reset, the following **V2 execution-layer assets were not present** in the sandbox and therefore cannot be treated as locally available artefacts: the V2 external runner, V2 protocol/audit documents, P4 OpenBMI derived cache, P5 Jeong derived cache, and generated manifests/results. The source user uploads, including the V2 specification and supplied P1/P2 manuscripts, remain available separately.

| Evidence tier | Recovery treatment |
|---|---|
| Frozen V1 baseline | Restored from the user-supplied delivery archive; do not alter historical evidence claims. |
| Frozen V1.1 results | Not contained in the restored archive. They remain historically described in the inherited task record, but must not be regenerated into the old result paths or represented as newly rerun. |
| V2 P4/P5 caches/results | Lost from this execution environment before any P4/P5 scientific model result was accepted. P4 cache had previously completed D1, but that cache is no longer locally available and must be re-acquired under a new, documented V2 recovery run namespace. |
| V2 P6 | No repeated-real-replay experiment had begun; no result was lost. |

## Recovery Guardrails

All renewed V2 work must use a separate recovery namespace and preserve the original V1/V1.1 paths as read-only historical references. Any newly re-acquired external cache will carry fresh download receipts, checksums, manifests, protocol identifiers, and independent rerun evidence. No partial P5 cache, preflight-only cache, or values observed before the reset may enter analysis.

> The reset is an operational interruption, not a licence to relax the locked protocol, infer missing values, or backfill claims. All subsequent outputs must be independently reproducible from preserved user inputs and live authoritative sources.

## Next Recovery Steps

The recovery sequence is: (1) restore and test the applicable local research framework; (2) rebuild V2 code and locked protocol documents from the preserved specification and recorded decisions; (3) revalidate P4/P5 source metadata before re-acquisition; (4) acquire/cache/validate datasets anew under a recovery namespace; and (5) run analyses only after D1–D5 pass and independent reruns are recorded.
