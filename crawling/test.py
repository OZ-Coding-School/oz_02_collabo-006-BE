import requests
# API 엔드포인트 URL

def login():
    url = "http://127.0.0.1:8000/api/v1/user/login/"

    # 헤더
    headers = {
        "Content-Type": "application/json",
    }

    # 요청 데이터 (JSON 형식)
    data = {
        "username": "test1",
        "password": "1Rlaqjawns@"
    }

    # POST 요청 보내기
    response = requests.post(url, headers=headers, json=data)

    # 응답 확인
    if response.status_code == 200:
        print("요청 성공:", response.json())
        return response.json()["accessToken"]
        # return response.json()
    else:
        print("요청 실패:", response.status_code, response.text)




# API 엔드포인트 URL
url = "http://127.0.0.1:8000/api/v1/post/create/"

# 헤더
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {login()}"
}

# 요청 데이터 (JSON 형식)
data = {
"media": list(download_image_as_base64(url)),
"content": "202405211911",
"visible":"true",
"comment_ck":"true"
}

# POST 요청 보내기
response = requests.post(url, headers=headers, json=data)

# 응답 확인
if response.status_code == 200:
    print("요청 성공:", response.json())
else:
    print("요청 실패:", response.status_code, response.text)

