#!/bin/bash
cd /opt/django-community-board

# 가상환경 활성화 (필수)
source .venv/bin/activate

# 기존에 8000번 쓰고 있는 프로세스 있으면 죽임 (안전장치)
fuser -k 8000/tcp

# 서버 실행 (nohup으로 백그라운드 실행해야 끊기지 않음)
# 로그는 /dev/null로 버리거나 별도 파일로 저장
nohup python3 manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &
