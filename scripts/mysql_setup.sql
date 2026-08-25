-- IoT 테스트 시스템용 DB 생성 스크립트 (MySQL / MariaDB 공용).
-- root 계정을 그대로 사용한다 (팀별로 독립 설치되는 테스트 도구이므로 별도 앱 계정을 만들지 않는다).
--
-- Windows: MySQL(MySQL Command Line Client) 또는 MariaDB(HeidiSQL, mysql CLI 등)에서
--   mysql -u root -p < scripts/mysql_setup.sql
-- 로 실행한다.

CREATE DATABASE IF NOT EXISTS iot_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 위 명령은 실행됐는데 백엔드 기동 시 "Access denied for user 'root'@'127.0.0.1'" 오류가
-- 나면, root 계정이 'localhost' 전용으로만 등록되어 있고 127.0.0.1(TCP) 접속용 계정이
-- 따로 없는 경우다. 아래 두 줄의 주석을 풀고 YOUR_ROOT_PASSWORD를 실제 root 비밀번호로
-- 바꿔서 다시 실행하면 해결된다.
-- CREATE USER IF NOT EXISTS 'root'@'127.0.0.1' IDENTIFIED BY 'YOUR_ROOT_PASSWORD';
-- GRANT ALL PRIVILEGES ON *.* TO 'root'@'127.0.0.1';
-- FLUSH PRIVILEGES;
