Set-Location -Path $PSScriptRoot
& .\.venv\Scripts\Activate.ps1
python run.py
Read-Host "Press Enter to close"
