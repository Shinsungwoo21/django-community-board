#!/bin/bash
cd /opt/django-community-board

# 1. 기존 프로세스 정리 (안전장치. 없으면 말고 식으로 처리)
fuser -k 8000/tcp || true

# 2. 가상환경 활성화 (필수)
source .venv/bin/activate

# 3. 서버 실행 (로그는 /opt/django_app.log 에 남김. 백그라운드 & 필수)
# /dev/null 대신 로그 파일 지정
nohup python manage.py runserver 0.0.0.0:8000 >> /opt/django_app.log 2>&1 &

echo "Django server started in background."
