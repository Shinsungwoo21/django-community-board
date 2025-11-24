"""
MySQL 호스트 기반 인증을 위한 커스텀 데이터베이스 백엔드
"""
import socket
from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.db.backends.mysql.creation import DatabaseCreation
from django.db.backends.mysql.introspection import DatabaseIntrospection
from django.db.backends.mysql.operations import DatabaseOperations
from django.db.backends.mysql.schema import DatabaseSchemaEditor


class DatabaseWrapper(MySQLDatabaseWrapper):
    """
    MySQL 연결 시 클라이언트 호스트명을 명시적으로 지정하는 커스텀 백엔드
    """
    
    def get_new_connection(self, conn_params):
        """
        새로운 데이터베이스 연결을 생성할 때 호스트명을 명시적으로 지정
        """
        # 현재 호스트명 가져오기
        hostname = socket.gethostname()
        
        # 연결 파라미터에 호스트명 추가
        if 'init_command' not in conn_params:
            conn_params['init_command'] = ""
        
        # MySQL에 클라이언트 호스트명 설정
        init_command = conn_params['init_command']
        if init_command:
            init_command += "; "
        init_command += f"SET @client_hostname = '{hostname}';"
        conn_params['init_command'] = init_command
        
        # 부모 클래스의 연결 생성 메서드 호출
        connection = super().get_new_connection(conn_params)
        
        # 연결 후 호스트명 확인 쿼리 실행
        with connection.cursor() as cursor:
            cursor.execute("SELECT @@hostname, USER(), CONNECTION_ID();")
            result = cursor.fetchone()
            print(f"MySQL 연결 정보: Host={result[0]}, User={result[1]}, Connection ID={result[2]}")
        
        return connection


# Django가 인식할 수 있도록 클래스들을 노출
DatabaseCreation = DatabaseCreation
DatabaseIntrospection = DatabaseIntrospection
DatabaseOperations = DatabaseOperations
DatabaseSchemaEditor = DatabaseSchemaEditor

