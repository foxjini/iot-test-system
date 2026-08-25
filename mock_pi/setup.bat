@echo off
cd /d %~dp0
python -m venv .venv
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo 완료. mock_pi\.env 파일에 DEVICE_ID, API_KEY를 입력하세요.
echo (프론트엔드 대시보드에서 디바이스를 등록하면 발급됩니다.)
pause
