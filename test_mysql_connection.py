#!/usr/bin/env python3
"""
MySQL 호스트 기반 인증 연결 테스트 스크립트
"""
import os
import sys
import django
from django.conf import settings

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_board_project.settings')
django.setup()

def test_mysql_connection():
    """MySQL 연결 및 호스트 정보 확인"""
    try:
        from django.db import connection
        
        print("=== MySQL 연결 테스트 ===")
        
        # 연결 생성
        with connection.cursor() as cursor:
            # 호스트 정보 조회
            cursor.execute("SELECT @@hostname, USER(), CONNECTION_ID(), @@version;")
            result = cursor.fetchone()
            
            print(f"MySQL 서버 호스트명: {result[0]}")
            print(f"연결된 사용자: {result[1]}")
            print(f"연결 ID: {result[2]}")
            print(f"MySQL 버전: {result[3]}")
            
            # 현재 클라이언트 호스트명 확인
            cursor.execute("SELECT @@hostname;")
            client_host = cursor.fetchone()[0]
            print(f"클라이언트 호스트명: {client_host}")
            
            # 데이터베이스 목록 확인
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()
            print(f"사용 가능한 데이터베이스: {[db[0] for db in databases]}")
            
        print("✅ MySQL 연결 성공!")
        return True
        
    except Exception as e:
        print(f"❌ MySQL 연결 실패: {e}")
        return False

def test_django_models():
    """Django 모델 테스트"""
    try:
        from django.db import connection
        
        print("\n=== Django 모델 테스트 ===")
        
        # 테이블 생성 테스트
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_host_auth (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hostname VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # 테스트 데이터 삽입
            import socket
            hostname = socket.gethostname()
            cursor.execute(
                "INSERT INTO test_host_auth (hostname) VALUES (%s);",
                [hostname]
            )
            
            # 데이터 조회
            cursor.execute("SELECT * FROM test_host_auth ORDER BY created_at DESC LIMIT 5;")
            results = cursor.fetchall()
            
            print("최근 테스트 데이터:")
            for row in results:
                print(f"  ID: {row[0]}, 호스트명: {row[1]}, 생성시간: {row[2]}")
            
            # 테스트 테이블 삭제
            cursor.execute("DROP TABLE test_host_auth;")
            
        print("✅ Django 모델 테스트 성공!")
        return True
        
    except Exception as e:
        print(f"❌ Django 모델 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    print("Django MySQL 호스트 기반 인증 테스트 시작...\n")
    
    # MySQL 연결 테스트
    mysql_ok = test_mysql_connection()
    
    if mysql_ok:
        # Django 모델 테스트
        django_ok = test_django_models()
        
        if django_ok:
            print("\n🎉 모든 테스트 통과! 호스트 기반 인증이 정상적으로 작동합니다.")
        else:
            print("\n⚠️ MySQL 연결은 성공했지만 Django 모델 테스트에서 문제가 발생했습니다.")
    else:
        print("\n❌ MySQL 연결에 실패했습니다. 설정을 확인해주세요.")
        sys.exit(1)

