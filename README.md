---  

# 사용한 서비스  
- NCP(Cloud Outbound Mailer)
  - 메일링 서비스에 이용

- NCP(Simple & Easy Notification Service)
  - 문자메세지 서비스에 이용

- NCP(Server)
  - aws ec2 비슷함

- NCP(Object Storage)
  - aws s3 비슷함


---  

`mysql`, `django`, `poetry`

# 프로젝트 가이드  

### 프로젝트 처음시작 설정  

- poetry 설치하기  
  - 설치완료 후 `poetry --version` 으로 설치 확인하기.  

  - mac  
    - brew 로 설치하기(파이썬 우선 설치하기)  
    ```bash
    brew install poetry
    ```

    - crul로 설치하기

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    # poetry --version 으로 버전확인이 안되면 설치 후 나타나는 path 추가 명령어 실행해야함. 
    ```

  - windows  
    - pip 으로 설치(파이썬 우선 설치하기)  
    ```bash
    pip install poetry
    ```

    - curl 로 설치하기
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

![alt text](images/markdown-image-1.png)  

![alt text](images/markdown-image-2.png)

<br>

<br>

---  
---  
---  

<br>

# 주휘 add
- 포스트에 미디어 추가하는 방법 논의해보기
  - 미디어와 포스트 다대다 관계인지 일대일인지.. ??? (확인하기)



