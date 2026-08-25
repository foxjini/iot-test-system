@echo off
cd /d %~dp0
python -m venv .venv
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo 완료. backend\.env 파일에서 DATABASE_URL의 root 비밀번호를 실제 값으로 바꾸세요.
echo iot_test DB가 없다면 먼저 ..\scripts\mysql_setup.sql 을 실행하세요 (MySQL/MariaDB 공용).
pause
