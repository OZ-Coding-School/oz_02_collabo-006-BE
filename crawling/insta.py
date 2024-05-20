from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

import configparser
CONF = configparser.ConfigParser()
CONF.read("../config.ini")

# ChromeDriver 경로 설정 (실제 경로로 수정)
chrome_driver_path = r"chromedriver.exe"  # ChromeDriver 경로 설정
service = Service(chrome_driver_path)


instaIdList = [
    "somi_art_official",
    "ucm.nail",
    "change_it_mk",
    "riyu_nail",
    "muyo_nail",
    "clareo_nail",
    "nail_jj5h",
    "o.nnail",
    "h_nail_shop",
]

# 사용자 입력
username = CONF["crawling"]["INSTA_ID"]
password = CONF["crawling"]["INSTA_PASS"]

# 인스타그램 로그인 페이지 URL
login_url = "https://www.instagram.com/accounts/login/"

# WebDriver 설정
driver = webdriver.Chrome(service=service)

# 인스타그램 로그인 페이지로 이동
driver.get(login_url)

# 로그인 정보 입력 및 제출
time.sleep(3)  # 페이지가 완전히 로드될 때까지 대기
username_field = driver.find_element(By.NAME, "username")
password_field = driver.find_element(By.NAME, "password")

username_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

# 로그인이 완료될 때까지 대기
time.sleep(5)

# 현재 페이지 URL을 확인하여 로그인이 성공했는지 확인할 수 있습니다.
current_url = driver.current_url
if current_url == login_url:
    print("로그인에 실패했습니다.")
else:
    print("로그인에 성공했습니다.")


# 사용자 입력
username = "somi_art_official"
baseUrl = "https://www.instagram.com/"
profile_url = baseUrl + username

# ChromeDriver 경로 설정 (실제 경로로 수정)
# chrome_driver_path = r"C:\Users\COM\Desktop\2024 django project\oz_02_collabo-006-BE\crawling\chromedriver.exe"  # ChromeDriver 경로 설정
service = Service(chrome_driver_path)

from selenium.webdriver.chrome.options import Options

options = Options()

user = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"


options.add_argument(f"User-Agent={user}")
options.add_experimental_option("detach", True)
# 주소줄 바로 밑에 자동 실행중 나오는거 없애는거.
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# options.add_argument("--start-maximized")
# options.add_argument("--start-fullscreen")
# options.add_argument("window-size=500, 500")

# 브라우저 화면이 나오지 않은 상태에서 크롤링
# options.add_argument("--headLess")

# 오디오 음소거
# options.add_argument("--mute-audio")
# 시크릿 모드
options.add_argument("incognito")

# WebDriver 설정 및 페이지 열기
driver = webdriver.Chrome(service=service, options=options)
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
soup = BeautifulSoup(html, "html.parser")

# 이미지 선택자
insta_images = soup.select("img")

# 이미지 URL 리스트 생성
image_urls = []
for img in insta_images:
    if "src" in img.attrs:
        image_urls.append(img["src"])

# 드라이버 종료
driver.quit()

# 이미지 저장 경로 설정
save_dir = "images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 이미지 다운로드 및 저장
for i, url in enumerate(image_urls):
    try:
        image_data = urlopen(url).read()
        file_path = os.path.join(save_dir, f"image_{i+1}.jpg")
        with open(file_path, "wb") as f:
            f.write(image_data)
        print(f"{file_path} 저장 완료")
    except Exception as e:
        print(f"이미지 다운로드 실패: {url}, 에러: {e}")
