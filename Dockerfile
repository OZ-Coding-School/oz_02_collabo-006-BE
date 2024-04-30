# 기본 이미지로 Python 3.11을 선택합니다.
### 우분투 초기 설정 ###
# ubuntu 이미지 18.04 버전을 베이스 이미지로 한다
FROM ubuntu:18.04

FROM python:3.12



# # 우분투에서 다운로드 속도가 느리기 때문에 다운로드 서버를 바꿔주었다
RUN sed -i 's@archive.ubuntu.com@mirror.kakao.com@g' /etc/apt/sources.list

# apt 업그레이트 및 업데이트
RUN apt-get -y update && apt-get -y dist-upgrade

# apt-utils dialog : 우분투 초기 설정 / libpq-dev : PostgreSQL 의존성
RUN apt-get install -y apt-utils dialog libpq-dev


RUN apt-get install -y python3-pip python3-dev




# 환경 변수 설정으로 Python이 stdout에 출력하도록 합니다.
ENV PYTHONUNBUFFERED=0
ENV PYTHONIOENCODING=utf-8

# pip setuptools 업그레이드
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

RUN pip install --upgrade pip \
  && pip install poetry


# 작업 디렉터리 설정
WORKDIR /src

# pyproject.toml 파일과 poetry.lock 파일(있는 경우) 복사
COPY pyproject.toml poetry.lock* ./

# 종속성 설치
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi
