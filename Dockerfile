# Python 3.12 베이스 이미지 사용
FROM python:3.12

# apt-get 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get -y dist-upgrade \
    && apt-get install -y libpq-dev

# 환경 변수 설정
ENV PYTHONUNBUFFERED=0
ENV PYTHONIOENCODING=utf-8

# pip 및 setuptools 업그레이드
RUN pip install --upgrade pip setuptools

# poetry 설치
RUN pip install poetry

# 작업 디렉터리 설정 및 파일 복사
WORKDIR /src
COPY . .

# pyproject.toml과 poetry.lock 파일 복사 및 종속성 설치
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
