# V2 Recovery R3 Test Execution Log

## Scope

This log records verification executed during R3 interim-release assembly. It does not change or recompute any research output.

| Test surface | Command outcome | Status | Interpretation |
|---|---|---|---|
| Main programme repository | `PYTHONPATH=src pytest -q` | **28 passed** in 0.86 s | PASS |
| MyoSim default configuration | `pytest -q -k 'not pybullet'` | Configuration blocked before collection by uninstalled `pytest-cov` addopts | Environment limitation, not a programme-test failure |
| MyoSim with coverage addopts removed | `pytest -q -o addopts='' -k 'not pybullet'` | PyBullet files fail collection because optional `pybullet` is absent | Environment limitation confirmed |
| MyoSim MuJoCo-oriented selection | PyBullet backend files ignored; `-k 'not pybullet'` | **62 passed**, but two collection-safe availability assertions still expect PyBullet and fail | 62 MuJoCo-capable tests passed; optional-backend expectations are not applicable |
| MyoSim explicit PyBullet dependency selection | PyBullet-dependent cases explicitly isolated | **62 passed, 2 deselected**, one additional parametrized PyBullet case identified as requiring the missing dependency | Confirms the third PyBullet-dependent case; no claim of full-suite execution |

## Environment Limitation

The local MyoSim checkout can exercise its MuJoCo-capable code path. It cannot collect or pass the optional PyBullet backend tests on this Python 3.12 environment because `pybullet` is unavailable; the repository’s default pytest configuration also expects `pytest-cov`, which is not installed. The relevant failing/inapplicable cases are:

| Case | Dependency reason |
|---|---|
| `tests/integration/test_cli_main.py::test_doctor_and_list_backends_report_runtime_schema` | Explicitly asserts PyBullet availability |
| `tests/unit/test_coverage_boundaries.py::test_backend_factory_reports_creates_and_rejects_unknown` | Explicitly asserts PyBullet availability |
| `tests/integration/test_cli_main.py::test_validate_model_reports_backend_schema[pybullet]` | Instantiates PyBullet backend |
| `tests/integration/test_pybullet_backend.py` | Imports PyBullet at collection |
| `tests/unit/test_coverage_backend_edges.py` | Imports PyBullet at collection |

No attempt was made to install or emulate PyBullet after the recorded environment limitation. The successful main test suite and the 62 passing MuJoCo-capable cases provide the applicable verification evidence for the R2 patch in this release; they do not certify unexecuted PyBullet functionality.

## Log Files

The shell logs are retained under `audit/test_logs/` as `main_repo_pytest_r3.txt` and `myosim_mujoco_capable_pytest_r3.txt`.
