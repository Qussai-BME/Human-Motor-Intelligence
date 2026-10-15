# Child Project Validation Matrix
## V2 Recovery R3 Current-State Addendum

## Validation Principle

The umbrella project is a thin integration layer. Child repositories remain separate implementation baselines. This matrix records the public integration boundary, exercised validation, and explicit environment limits; it does not claim modification, vendoring, or complete independent certification of an unavailable dependency path.

| Child system | Umbrella integration boundary | Source modification | Current validation evidence | Limitation / next valid step |
|---|---|---|---|---|
| MyoControl | Serialized prediction fields mapped to `IntentRecord` | None | Adapter contract tests in the main 28-test suite; synthetic demonstrator boundary retained | A real decoder export/manifest is needed before scientific P6 replay use |
| MyoAdapt | Run-manifest/artifact references mapped to `ExperimentRecord`/`ArtifactRecord` | None | Manifest-import adapter and main-suite tests | Original Paper 3 manifest/results are pending; do not reconstruct its locked study |
| BioSignal-FM V4 | Public canonical signal/representation metadata mapping | None | Adapter contract tests and architecture audit | No source model import or foundation-model claim; a valid external export is required for future evidence |
| MyoSim V1.1 | Public intent event / CSV replay integration and local R2 patch record | R2 initial-state patch held outside the programme repository as a versioned patch | Baseline/capability checks, P6 records/rerun, main-suite MyoSim adapter tests, 62 applicable MuJoCo-capable local tests | PyBullet remains unverified in Python 3.12; P6 R3 needs authentic frozen traces |

## Test and Environment Record

| Surface | Result | Status |
|---|---|---|
| Main umbrella suite | 31 passed | PASS |
| MyoSim strict MuJoCo path / R2 systems evidence | Exercised through retained compatibility and state records | PASS within declared scope |
| MyoSim optional PyBullet tests | Collection/execution limited by absent `pybullet`; default configuration also requests absent `pytest-cov` | NOT CERTIFIED |
| Generic isolated MyoControl suite (historical audit) | Environment dependency issue previously documented | NOT RE-RUN as child source remains untouched |
| Generic isolated MyoAdapt suite (historical audit) | Package import/setup issue previously documented | NOT RE-RUN as child source remains untouched |
| Generic isolated BioSignal-FM suite (historical audit) | Environment dependency issue previously documented | NOT RE-RUN as child source remains untouched |

## Boundary Controls

All connectors are mapping-only. The umbrella registry stores hashes/references rather than raw datasets. P6’s local initial-state extension is delivered as a separately identified patch against user-provided MyoSim V1.1 and is not a claim that the upstream child source was rewritten. The patch’s purpose is to make an initial-state factor real and recorded; it does not authenticate the replay input as a decoder output.[1]

## References

[1]: patches/README_MYOSIM_INITIAL_STATE_RECOVERY_R2.md "MyoSim Initial-State Patch Guide"
[2]: audit/V2_R3_TEST_EXECUTION_LOG.md "R3 Test Execution Log"
[3]: FINAL_PROJECT_REPORT.md "Legacy Master-Stack Project Report"
[4]: audit/V2_R3_P6_REPLAY_IDENTITY_HARD_STOP.md "P6 R3 Replay Identity Hard Stop"

The child-system treatment and current environmental limits follow the retained integration and test records.[1] [2] [3] [4]
