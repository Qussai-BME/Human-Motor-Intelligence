# V2 P5 Sub-23 Second-Source Research Log

**Purpose:** Preserve live source findings while the mandatory independent source verification is in progress. This is not yet the final exclusion decision.

## Sources Opened

| Timestamp | Source distinct from NEMAR | URL | Observed response / finding |
|---|---|---|---|
| 2026-08-23 GMT+3 | Original GigaDB deposit | https://gigadb.org/dataset/100788 | HTTP page retrieval succeeded through webpage extraction and browser view. The page identifies DOI `10.5524/100788`, 25 healthy subjects, 60 EEG/7 EMG/4 EOG, three-day sessions, and a public contact submitter link. Its sample table includes `sub23`. |
| 2026-08-23 GMT+3 | Original peer-reviewed descriptor | https://academic.oup.com/gigascience/article/9/10/giaa098/5918864 | Direct page extraction succeeded. The article states that raw and converted participant data are available through GigaDB in “Raw data” and “Converted data” folders, containing `.eeg`, `.vmrk`, `.vhdr`, and `.mat` files. It directs readers to contact authors for code information and does not name a separate author-maintained data mirror or corrigendum in the extracted availability statement. |

## Facts Relevant to the Cohort Amendment

The original GigaDB sample metadata show `sub23` is female, aged 28, with three listed collection dates (2019-07-12, 2019-07-19, 2019-07-26). The original paper describes 25 right-handed healthy naive BCI users aged 24–32 years (15 men, 10 women) and three recording sessions. These facts can support a basic pre-model descriptive check if the second-source file inventory ultimately confirms that run-2 is not retrievable.

## Current Status

The original deposit contains a visible Files tab, but its detailed file table/download links have not yet been extracted in this log. The next action is to parse the browser-saved original-deposit HTML/API interactions and test exact original-deposit URLs for `sub23` session/run data. No exclusion amendment, data acquisition, or model fitting has occurred under V2 Recovery R2.

## References

[1] [GigaDB original deposit 100788](https://doi.org/10.5524/100788)  
[2] [Jeong et al. (2020), GigaScience](https://doi.org/10.1093/gigascience/giaa098)
