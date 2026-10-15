# Upload Guide — Human Motor Intelligence v1.2.0

## 1. Final local checks
```bash
pip install -e ".[dev,p6]"                  # Python >= 3.11
python scripts/public_release_doctor.py     # must print "status": "PASS"
pytest -q                                   # 44 passed, 2 skipped (46 passed with MyoSim installed)
```
If any file changes after this point, run `python scripts/build_release_manifest.py` and then the doctor again, otherwise the manifest check fails.

## 2. Size and layout
The tree is about 330 MB (no single file above 50 MB; no raw EEG). The 146k per-episode C2 files live in four compressed archives under `p6/c2_episode/raw_archives/` with SHA-256 sums.

## 3. Publish to an existing GitHub repository
Do not run `git init` or force-push: the repository already has history (v1.0.0). Clone it and replace its contents:
```bash
git clone https://github.com/Qussai-BME/Human-Motor-Intelligence.git repo
cd repo
git config core.autocrlf false
# remove all tracked files except .git, copy the contents of this package in, then:
git add -A
git status --short          # review deletions and additions
git commit -m "Human Motor Intelligence v1.2.0: P6 C1 audit and C2 episode-level study"
git push origin main
git tag -a v1.2.0 -m "v1.2.0" && git push origin v1.2.0
```

## 4. Zenodo
Open the existing Zenodo record, choose "New version", replace the file with this package's ZIP, set the version to `v1.2.0`, review the metadata and publish. Publication is permanent. If the GitHub–Zenodo integration is enabled for the repository, a GitHub release creates the Zenodo version automatically; do not do both.

## 5. Before you announce
- Confirm that PhysioNet EEGMMIDB and MyoSim/MuJoCo licence terms are still current (see `DATA_AND_LICENSES.md`).
- Do not describe P6 as clinical validation or as a general law relating decoder quality to control utility (`SCIENTIFIC_LIMITATIONS.md`).
- Manuscript texts are not part of this archive (see `README.md`).
