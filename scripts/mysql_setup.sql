-- IoT 테스트 시스템용 MySQL DB/계정 생성 스크립트.
-- Windows: MySQL 8.x 설치 후 "MySQL Command Line Client" 또는
--   mysql -u root -p < scripts/mysql_setup.sql
-- 로 실행한다. (root 비밀번호 입력 필요)

CREATE DATABASE IF NOT EXISTS iot_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'iot_test'@'localhost' IDENTIFIED BY 'iot_test_pw';
CREATE USER IF NOT EXISTS 'iot_test'@'%' IDENTIFIED BY 'iot_test_pw';
GRANT ALL PRIVILEGES ON iot_test.* TO 'iot_test'@'localhost';
GRANT ALL PRIVILEGES ON iot_test.* TO 'iot_test'@'%';
FLUSH PRIVILEGES;
