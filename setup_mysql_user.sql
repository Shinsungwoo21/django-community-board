-- MySQL 호스트 기반 인증을 위한 사용자 생성 스크립트
-- 이 스크립트를 MySQL에서 실행하여 Django용 사용자를 생성하세요

-- 1. 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS community_board CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 특정 호스트에서만 접속 가능한 사용자 생성
-- 'your-hostname'을 실제 호스트명으로 변경하세요
CREATE USER 'django_user'@'your-hostname' IDENTIFIED BY 'secure_password_here';

-- 3. 또는 IP 주소로 제한 (더 안전)
-- '192.168.1.100'을 실제 IP 주소로 변경하세요
CREATE USER 'django_user'@'192.168.1.100' IDENTIFIED BY 'secure_password_here';

-- 4. 권한 부여
GRANT ALL PRIVILEGES ON community_board.* TO 'django_user'@'your-hostname';
GRANT ALL PRIVILEGES ON community_board.* TO 'django_user'@'192.168.1.100';

-- 5. 권한 새로고침
FLUSH PRIVILEGES;

-- 6. 사용자 확인
SELECT User, Host FROM mysql.user WHERE User = 'django_user';

-- 7. 연결 테스트 (Django에서 실행할 때 확인)
-- SELECT @@hostname, USER(), CONNECTION_ID();

