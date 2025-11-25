#!/bin/bash
# 8000번 포트 사용하는 프로세스 찾아서 강제 종료
# fuser 명령어가 없으면 lsof 사용, 둘 다 없으면 에러 날 수 있으니 간단하게 처리

# 8000번 포트 사용 중인 PID 찾기
PID=$(lsof -t -i:8000)

# PID가 있으면 종료
if [ -n "$PID" ]; then
  kill -9 $PID
fi

# (중요) 종료할 게 없어도 성공으로 간주 (exit 0)
exit 0
