@echo off
chcp 65001 >nul
cd /d %~dp0
python -m venv .venv
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo Done. Open backend\.env and set your MySQL root password in DATABASE_URL.
echo If the iot_test database does not exist yet, run ..\scripts\mysql_setup.sql first.
pause
