#!/bin/bash
set -e

# Wait for PostgreSQL to become available
until psql -h "$DB_HOST" -U "$DB_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

python manage.py makemigrations

# 데이터베이스 마이그레이션 실행
python manage.py migrate

# 정적 파일 수집
python manage.py collectstatic --no-input --settings=config.settings

# python manage.py create_my_superuser

# 커맨드 라인에서 전달된 명령 실행 (CMD에서 정의된 명령)
exec "$@"
