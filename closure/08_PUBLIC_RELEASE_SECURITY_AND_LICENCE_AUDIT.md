# Public Release Security and Licence Audit — Closure R1

## Checks performed

- Scanned candidate paths for common credential filenames and private-key markers.
- Confirmed raw biomedical recordings and derived large participant caches are not included in the candidate.
- Confirmed P3 retains its own MIT/CITATION/provenance files.
- Confirmed component archives are referenced by checksum but not silently vendored into the umbrella release.
- Identified `__pycache__`, `.pytest_cache`, temporary verification directories, and other generated runtime artefacts as excluded from the new candidate.

## Licence boundaries

Programme-owned material remains governed by the umbrella `LICENSE`/`NOTICE`. P3 retains its upstream MIT licence and citation metadata. MyoSim, MyoAdapt, BioSignal-FM, and MyoControl remain separate archives with their own terms. NinaPro/NEMAR data access and redistribution conditions remain external; raw data are not redistributed.

## Security disposition

No credential or token was found in the audited candidate paths. No secret values are reproduced in this report. A live public upload was not performed and is not claimed.
