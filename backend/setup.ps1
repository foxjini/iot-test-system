Set-Location -Path $PSScriptRoot

python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}

Write-Host ""
Write-Host "Done. Open backend\.env and set your MySQL root password in DATABASE_URL." -ForegroundColor Yellow
Write-Host "If the iot_test database does not exist yet, run ..\scripts\mysql_setup.sql first."
