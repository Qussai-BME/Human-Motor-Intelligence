.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src"
$env:OPENBLAS_NUM_THREADS = "1"
$env:OMP_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
$env:NUMEXPR_NUM_THREADS = "1"
Write-Host "Environment ready: PYTHONPATH=src, single-threaded BLAS." -ForegroundColor Green
