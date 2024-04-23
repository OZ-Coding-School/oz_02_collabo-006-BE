
---  

`mysql`, `django`, `poetry`

# 프로젝트 가이드  

### 프로젝트 처음시작 설정  

- poetry 설치하기  
  - 설치완료 후 `poetry --version` 으로 설치 확인하기.  

  - mac  
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

  - windows  
  ```bash
  curl -sSL https://install.python-poetry.org | python -
  ```

<br>

- poetry 가상환경에 패키지 설치  
   
  ```bash
  poetry update
  ```

<br>

- 장고 마이그레이트  

  ```bash
  python manage.py makemigrations
  ```

  ```bash
  python manage.py migrate
  ```

<br>

- 장고 슈퍼유저 생성  

  ```bash
  python manage.py createsuperuser
  ```

<br>


---  

# APIs  

### users

- 사용자 생성
  - `/api/v1/user/`

- 사용자 수정
  - `/api/v1/user/<int:user_id>/`