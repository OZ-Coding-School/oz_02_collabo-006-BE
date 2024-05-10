
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


- simeple jwt 토큰받기

```python
  import requests

  url = 'http://127.0.0.1:8000/login/sjwt/'
  headers = {'Content-Type': 'application/json'}
  data = {"username": "example", "password": "1234"}

  response = requests.post(url, headers=headers, json=data)
  print(response.json())
```
- 요청을 하면 아래와같이 리프래쉬 토큰과 어새스 토큰을 받는다.

```bash

# http response
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNDEyMzU5MywiaWF0IjoxNzE0MDM3MTkzLCJqdGkiOiI1MmQ4N2IwOGM0NTU0YTU4YThkNTA4Nzg5ODBjM2IzMSIsInVzZXJfaWQiOjF9.XInfEFNPpafiY1h6kzqJixhyeg3oyABjvS6ZL2TvKOw",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0MDM3NDkzLCJpYXQiOjE3MTQwMzcxOTMsImp0aSI6IjRmZWU3ODc4ZmJiOTRmMTc5MmQxNzBiOGYxOWJhNDNhIiwidXNlcl9pZCI6MX0.hADxc7ys6uGAnVyNFs_oFBHIZhkbZiyJpKbl93Kt-g0"
}

```


![alt text](images/markdown-image.png)  

<br>

<br>

<br>

`/api/v1/user/login/sjwt/`

```json

  {
      "username": "efedf", 
      "password": "1Rlddawns@", 
      "phone": "1233345"
  }

```

# swagger
```bash
http://127.0.0.1:8000/swagger
```

![alt text](images/markdown-image-2.png)



<br>

<br>

<br>

---  
---  
---  

<br>

# 범준
- 프론트엔드에서 테스트를 하기위한 도커 파일 만드는중..  
  -  python manage.py create_my_superuser
  -  app폴더내에 다음경로를 만들어서 파일을 만들면 별도로 명령어 생성가능. management/commnads/[somefilename.py]
     -  도커 생성할때 어드민 유저자동생성 `id` admin `비번` 1234
-  





```bash
poetry add psycopg2
```

```bash
poetry add psycopg
```

![alt text](images/markdown-image-1.png)

- 전체 정상적으로 도커 실행됐는데 웹페이지 로딩안될때 로그 보면서 해결하기  
```bash
sudo docker logs [컨테이너명]
```


```bash
sudo docker-compose up --build -d
```


---




# 주휘 add
- 포스트에 미디어 추가하는 방법 논의해보기
  - 미디어와 포스트 다대다 관계인지 일대일인지.. ??? (확인하기)



