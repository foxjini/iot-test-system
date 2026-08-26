@echo off
chcp 65001 >nul
cd /d %~dp0
call npm install
if not exist .env.local copy .env.local.example .env.local
echo.
echo Done. frontend\.env.local was created - the default NEXT_PUBLIC_API_BASE_URL
echo works as-is when everything runs on this same PC.
pause
