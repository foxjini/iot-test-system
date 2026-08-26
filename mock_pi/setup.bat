@echo off
chcp 65001 >nul
cd /d %~dp0
python -m venv .venv
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo Done. Open mock_pi\.env and set DEVICE_ID and API_KEY
echo (issued when you register a device in the dashboard).
pause
