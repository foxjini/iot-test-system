@echo off
cd /d %~dp0
call npm install
if not exist .env.local copy .env.local.example .env.local
echo.
echo 완료. frontend\.env.local 파일에서 NEXT_PUBLIC_API_BASE_URL을 확인하세요.
pause
