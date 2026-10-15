# All-Specification Release Test Execution Log
## V2 Recovery R3 Current-State

| Test surface | Command / evidence | Result | Status |
|---|---|---|---|
| Main programme suite after all-specification additions | `PYTHONPATH=src pytest -q` from project root | **28 passed** in 4.30 s | PASS |
| Existing P4/P5/P6 R3 document/evidence validator | `scripts/validate_r3_interim_release.py` recorded earlier | Required R3 documents, exact rerun checks, exclusions, image targets, and terminology audit passed | PASS |
| All-specification release validator | `scripts/validate_all_specs_release_r3.py` | Required reports/Word files, local links, rerun hashes, raw/cache exclusion, Word content, p-value tables, and P6 hard-stop checks passed | PASS |
| MyoSim MuJoCo-capable selection | Retained `audit/V2_R3_TEST_EXECUTION_LOG.md` and shell log | 62 applicable tests passed in the documented selection | PASS within exercised scope |
| MyoSim PyBullet backend | Retained execution record | Not certified: optional `pybullet` unavailable under current Python 3.12; default configuration also requests absent `pytest-cov` | Explicit limitation |

The documentation and Word-generation utilities do not alter the research-core test surface. The main suite was nevertheless rerun after these additions to document release readiness.

## References

[1]: V2_R3_TEST_EXECUTION_LOG.md "R3 MyoSim and Main-Test Record"
[2]: ALL_SPECS_RELEASE_VALIDATION_R3.md "All-Specification Release Validation"
[3]: WORD_RENDER_QA_NOTES_R3.md "Word Render QA Notes"

The test record is interpreted together with the retained R3 environment and release-validation records.[1] [2] [3]
