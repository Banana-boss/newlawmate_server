-- MySQL 초기화 스크립트

-- 테스트 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS test_fastapi_db;

-- 권한 부여
GRANT ALL PRIVILEGES ON fastapi_db.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON test_fastapi_db.* TO 'root'@'%';
FLUSH PRIVILEGES;
