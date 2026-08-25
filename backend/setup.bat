@echo off
cd /d %~dp0
python -m venv .venv
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo 완료. backend\.env 파일에서 DATABASE_URL, CORS_ORIGINS를 확인하세요.
echo MySQL에 iot_test DB/계정이 없다면 먼저 ..\scripts\mysql_setup.sql 을 실행하세요.
pause
