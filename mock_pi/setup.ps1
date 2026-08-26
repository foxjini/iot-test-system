Set-Location -Path $PSScriptRoot

python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}

Write-Host ""
Write-Host "Done. Open mock_pi\.env and set DEVICE_ID and API_KEY" -ForegroundColor Yellow
Write-Host "(issued when you register a device in the dashboard)."
