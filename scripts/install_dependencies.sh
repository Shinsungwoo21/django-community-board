#!/bin/bash
# 에러가 나면 스크립트 중단 (안전장치)
set -e

# 프로젝트 폴더로 이동
cd /opt/django-community-board

echo ">>> 1. OS 필수 패키지 설치 (빌드스펙에서 가져옴)"
# MariaDB 연동이나 Python 컴파일에 필요한 도구들 설치
# (-y 옵션 필수: 중간에 Y/N 물어보지 않게)
dnf install -y python3.11 python3.11-pip python3.11-devel mariadb105-devel gcc gcc-c++ make

echo ">>> 2. 가상환경 설정"
# 가상환경이 없으면 생성
if [ ! -d ".venv" ]; then
    python3.11 -m venv .venv
    echo "가상환경 생성 완료"
fi

# 가상환경 활성화
source .venv/bin/activate

echo ">>> 3. Python 의존성 패키지 설치"
# requirements.txt에 있는 내용 설치
pip install --upgrade pip
pip install -r requirements.txt

echo ">>> 4. DB 마이그레이션 (필요 시)"
# 데이터베이스 최신화
python3 manage.py migrate

echo ">>> 설치 완료"
