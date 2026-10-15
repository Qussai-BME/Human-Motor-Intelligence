# V2 Protocol Amendment Recovery R2 001

**Protocol ID:** `nemar-nm000311-jeong-p5-external-loso-24subject-r2`  
**Registered:** 2026-08-23 (GMT+3)  
**Applies to:** New V2 Recovery R2 P5 external validation only.  
**Does not modify:** V1, V1.1, V2 Recovery R1 P4, frozen Cho2017 P5 primary evidence, or any historic result path.

## Amendment Trigger

The prior locked 25-subject Jeong `ses-0` all-11-class external-validation plan stopped because NEMAR `nm000311` did not provide `sub-23` run-2. The mandatory independent source check is complete in `audit/V2_P5_SUB23_SECOND_SOURCE_CHECK.md`. The original GigaDB record exposes data only through a 227.5 GB aggregate raw archive, with no selective per-file endpoint; the author-attributed Zenodo repackage `10.5281/zenodo.19021437` was checksum-verified and lacks all `session1_sub23_twist_MI` BrainVision files while retaining the reach and multigrasp MI files.

The exclusion is therefore **objective, source-availability-based, and not outcome-related**. It was determined before any Recovery R2 P5 cache, feature set, model fit, score, statistical result, or rerun.

## Cohort

The amended fixed cohort is: `sub-1`, `sub-2`, `sub-3`, `sub-4`, `sub-5`, `sub-6`, `sub-7`, `sub-8`, `sub-9`, `sub-10`, `sub-11`, `sub-12`, `sub-13`, `sub-14`, `sub-15`, `sub-16`, `sub-17`, `sub-18`, `sub-19`, `sub-20`, `sub-21`, `sub-22`, `sub-24`, and `sub-25`.

`sub-23` is explicitly excluded. No other inclusion/exclusion criterion is introduced. The task boundary remains `ses-0`, MI-only, all three available task runs, and all eleven labels for every retained subject. Motor execution data remain excluded.

## Descriptive Balance Check

The official GigaDB sample API supplied age and sex metadata for all 25 participants. The full cohort has age mean 27.80 years (SD 2.47; range 24–32) and 10 female/15 male participants. The retained cohort has age mean 27.79 years (SD 2.52; range 24–32) and 9 female/15 male participants. `sub-23` is a 28-year-old female. The retention changes age mean by −0.008 years and reduces female count by one; it does not induce an observable age-range shift. This is descriptive only; an inferential comparison against a single excluded participant would not be meaningful.

Evidence: `audit/v2_p5_jeong_24subject_demographic_balance.json`.

## Locked R2 Analysis

| Element | Locked decision |
|---|---|
| Source | NEMAR `nm000311` v1.0.2, CC0-1.0; `ses-0` BDF/TSV records only |
| Cohort | 24 named subjects above; `sub-23` excluded before model fitting |
| Task | Motor imagery only; 11 classes (6 reach, 3 grasp, 2 twist); all three runs |
| Modalities | Exact channel-name selection: 60 EEG, 7 EMG; 4 EOG excluded |
| Conditions | EEG-only LDA, EMG-only LDA, early feature-concatenation LDA, late mean-probability LDA |
| Calibration | Strict LOSO; held-out subject contributes no fitted scaler, feature normalizer, classifier, tuning, or adaptation information |
| Primary endpoint | Subject-level macro-F1 across all 11 labels |
| Secondary endpoints | Accuracy and balanced accuracy, labelled secondary |
| Statistics | Subject unit; descriptive mean/SD; 10,000-resample percentile bootstrap mean CI; Friedman across four conditions; all six paired two-sided Wilcoxon tests; Holm adjustment; paired effect sizes |
| Missing-modality stress | Not included in the primary R2 external validation. The four fixed conditions already test unimodal and transparent-fusion mechanisms. Artificial modality deletion would create a distinct synthetic stress design and is rejected here to prevent scope drift. |
| Reproducibility | D1–D5, protocol/validation/manifest/environment files, subject outputs, exact independent rerun CSV/checksum agreement before manuscript integration |

## Stop Conditions

Stop before model fitting if source version/license/provenance changes, any retained subject does not contain 550 MI trials and all eleven labels, channel identity cannot be verified, D1–D5 fail, target-fold isolation cannot be demonstrated, or raw temporary storage cannot be cleaned after cache creation. Do not replace a missing retained file from the Zenodo mirror, because that would mix a differently processed source path into the primary cohort.

## Claim Boundary

This is an amended **external validation** cohort, not a direct replication of frozen Cho2017. Its statistics will not be pooled or averaged with Cho2017. It may be described as qualitatively consistent or divergent only after a completed R2 result with all gates and independent rerun.
