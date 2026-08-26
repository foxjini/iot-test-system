Set-Location -Path $PSScriptRoot

npm install

if (-not (Test-Path .env.local)) {
    Copy-Item .env.local.example .env.local
}

Write-Host ""
Write-Host "Done. frontend\.env.local was created - the default NEXT_PUBLIC_API_BASE_URL" -ForegroundColor Yellow
Write-Host "works as-is when everything runs on this same PC."
