#!/bin/bash

python manage.py makemigrations

# 데이터베이스 마이그레이션
python manage.py migrate

# 정적 파일 수집
python manage.py collectstatic --noinput

# python manage.py create_my_superuser

# 서버 시작
exec "$@"
