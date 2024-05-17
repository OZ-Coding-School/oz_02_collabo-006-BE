from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os

# 사용자 입력
username = input("검색할 아이디를 입력하세요 : ")
baseUrl = "https://www.instagram.com/"
profile_url = baseUrl + username

# ChromeDriver 경로 설정 (실제 경로로 수정)
chrome_driver_path = r'C:\Users\COM\Desktop\2024 django project\oz_02_collabo-006-BE\crawling\chromedriver.exe'  # ChromeDriver 경로 설정
service = Service(chrome_driver_path)

# WebDriver 설정 및 페이지 열기
driver = webdriver.Chrome(service=service)
driver.get(profile_url)

# 페이지 로드 대기
time.sleep(5)

# 무한 스크롤을 통해 모든 이미지 로드
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 페이지 소스 가져오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 이미지 선택자
insta_images = soup.select("img")

# 이미지 URL 리스트 생성
image_urls = []
for img in insta_images:
    if 'src' in img.attrs:
        image_urls.append(img['src'])

# 드라이버 종료
driver.quit()

# 이미지 저장 경로 설정
save_dir = 'images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 이미지 다운로드 및 저장
for i, url in enumerate(image_urls):
    try:
        image_data = urlopen(url).read()
        file_path = os.path.join(save_dir, f'image_{i+1}.jpg')
        with open(file_path, 'wb') as f:
            f.write(image_data)
        print(f'{file_path} 저장 완료')
    except Exception as e:
        print(f'이미지 다운로드 실패: {url}, 에러: {e}')
