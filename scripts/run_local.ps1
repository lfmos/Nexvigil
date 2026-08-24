$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "NexVigil v0.1 dependencies installed."
Write-Host "Start the API with:"
Write-Host "python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
