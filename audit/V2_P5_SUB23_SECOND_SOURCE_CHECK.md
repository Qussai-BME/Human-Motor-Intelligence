# V2 P5 Sub-23 Second-Source Verification

**Timestamp:** 2026-08-23 (GMT+3)  
**Purpose:** Mandatory independent check before any P5 exclusion decision.  
**Decision basis:** Source availability only; no P5 model was fitted and no P5 result was computed before this record.

## Question

The NEMAR BIDS derivative `nm000311` did not expose `sub-23/ses-0` run-2, which is the wrist-twist MI task under the programme mapping. This audit tested whether the missing recording was available through the original GigaDB deposit or an author-attributed mirror, independently of the NEMAR derivative.

## Sources and Responses

| Source | Exact URL checked | Observed response | Finding |
|---|---|---|---|
| Original GigaDB record | https://gigadb.org/dataset/100788 | Dataset page/API HTTP 200 on 2026-08-23 | The original DOI record lists 25 samples including `sub23`, provides a `RawData.tar.gz` bundle, and states the original experiment has three sessions. Its public Files API exposes one aggregate raw archive, not an individually addressable `sub23` recording. |
| Original raw aggregate, headers only | https://s3.ap-northeast-1.wasabisys.com/gigadb-datasets/live/pub/10.5524/100001_101000/100788/RawData.tar.gz | HTTP 200; `Accept-Ranges: bytes`; `Content-Length: 227518962464`; ETag `d021909552172434a60d00121632f0f3-9863` | The original delivery is a single 227.5 GB compressed aggregate. Its unindexed format provides no individual-file URL/API that can confirm or retrieve only `session1_sub23_twist_MI` without streaming the entire archive. No raw-archive download was started because this would be an uncontrolled 227 GB acquisition and exceeds the programme’s bounded-storage/targeted-access policy. |
| Original supporting publication | https://academic.oup.com/gigascience/article/9/10/giaa098/5918864 | HTTP 200 text extraction | The availability statement directs users to GigaDB. The data-description section names `Raw data`/`Converted data` folders and BrainVision participant files. It names no separate author-maintained mirror or corrigendum. |
| Author-attributed independent mirror (Zenodo/MOABB) | https://zenodo.org/records/19021437 | HTTP 200 on 2026-08-23 | Record lists the eight paper authors as creators, states it is a repackage of GigaDB DOI `10.5524/100788`, and contains `sub23.zip` (8,906,851,045 bytes; declared MD5 `0c884a93a75ee9af2093c3a671871e46`). |
| Exact mirror file | https://zenodo.org/records/19021437/files/sub23.zip?download=1 | HTTP download completed; local MD5 pass | Full archive was acquired temporarily outside the repository and verified `sub23.zip: OK`. `zipinfo` contains `session1_sub23_reaching_MI.{eeg,vhdr,vmrk}` and `session1_sub23_multigrasp_MI.{eeg,vhdr,vmrk}` but **no** `session1_sub23_twist_MI.{eeg,vhdr,vmrk}` entry. |

## Interpretation

The original paper directs data access only to GigaDB; no corrigendum or alternative author data URL was identified in its availability statement. The original GigaDB file catalogue does not expose a selective `sub-23` task file endpoint and delivers the raw material only through a 227.5 GB compressed aggregate. The independently accessible author-attributed repackage, which explicitly derives from the original GigaDB DOI, was fully checksum-verified and confirms that the relevant `session1_sub23_twist_MI` BrainVision recording is absent while the other two session-1 MI tasks are present.

> The programme therefore treats the third MI task for `sub-23` as unavailable through the authoritative, individually retrievable sources checked. This is a source-availability finding, not an outcome-based exclusion.

This check cannot prove a negative statement about every byte in the opaque original 227.5 GB aggregate without an unbounded full-stream operation. It does establish that no selective original-deposit file endpoint exists and that the author-attributed derived archive lacks the required files. Under the R2 specification’s source-availability rule, this is sufficient to consider the predeclared 24-subject amendment.

## Evidence Boundary

No derived cache was written from this archive and no model was fit. The temporary `sub23.zip` is retained only until the cohort-amendment path and exact raw-boundary decision are finalized, then must be deleted because no analysis should mix BDF-derived participants with a differently resampled BrainVision repackage for one subject. The frozen V1, V1.1, and V2 Recovery R1 P4 evidence remains untouched.

## References

[1] [GigaDB original deposit 100788](https://doi.org/10.5524/100788)  
[2] [Jeong et al. (2020), *GigaScience*](https://doi.org/10.1093/gigascience/giaa098)  
[3] [Zenodo author-attributed repackage, record 19021437](https://doi.org/10.5281/zenodo.19021437)
