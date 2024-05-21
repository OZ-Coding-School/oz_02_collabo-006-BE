from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os, time, platform, configparser, ssl, certifi

ssl._create_default_https_context = ssl._create_unverified_context

CONF = configparser.ConfigParser()
CONF.read("/Users/joowhi/oz_02_collabo-006-BE/config.ini")

chrome_driver_path = '/usr/local/bin/chromedriver'
# 리눅스용 ChromeOptions 설정
user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # GUI 없이 실행
chrome_options.add_argument("--no-sandbox")  # Sandbox 프로세스 사용 안 함
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 안 함
chrome_options.add_argument("incognito")  # 시크릿 모드
chrome_options.add_argument(f"user-agent={user_agent}")

# Chrome WebDriver 설정
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

# 사용자 입력
username = CONF["crawling"]["INSTA_ID"]
password = CONF["crawling"]["INSTA_PASS"]

# 크롤링할 계정들
instaIdList = [
    "somi_art_official",
    # "ucm.nail",
    # "change_it_mk",
    # "riyu_nail",
    # "muyo_nail",
    # "clareo_nail",
    # "nail_jj5h",
    # "o.nnail",
    # "h_nail_shop",
]

# 인스타그램 로그인
def login_insta(username, password):
    # 로그인 URL
    login_url = "https://www.instagram.com/accounts/login/"
    driver.get(login_url)
    time.sleep(3)  # 페이지가 완전히 로드될 때까지 대기

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    time.sleep(5) # 로그인이 완료될 때까지 대기

    # 현재 페이지 URL을 확인하여 로그인이 성공했는지 확인
    current_url = driver.current_url
    if current_url == login_url:
        print("로그인에 실패했습니다.")
        return False
    else:
        print("로그인에 성공했습니다.")
        return True

# 인스타그램 프로필에서 이미지 URL 및 해시태그 가져오기
def get_image_urls(insta_id):
    baseUrl = "https://www.instagram.com/"
    profile_url = baseUrl + insta_id

    driver.get(profile_url)
    time.sleep(5)

    # 무한 스크롤을 통해 모든 이미지 로드
    scroll_pause_time = 5
    # image_urls = set()  # 중복된 이미지를 피하기 위해 집합 사용

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 현재 페이지의 이미지 파싱
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        insta_images = soup.find_all("img", {"class": "x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3"})
        for img in insta_images:
            try:
                image_name = img['alt']
                image_url = img['src']
                image_urls.add({"image_name":image_name,"image_url":image_url})
                print(image_urls.add({"image_name":image_name,"image_url":image_url}), "!!!!!!!!!!!!!")
            except Exception as e:
                print(f"이미지 URL 추출 중 오류 발생: {e}")
        
        # 무한 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print(list(image_urls))
    return list(image_urls)

    # 게시글 div 선택
    posts = soup.find_all("div", class_="v1Nh3")

    # 해당하는 해시태그가 포함된 게시글의 이미지 URL 리스트 생성
    hashtag_image_urls = []
    for post in posts:
        img = post.find("img")
        if img:
            image_url = img.get("src")
            # 게시글 내용에서 해시태그 확인
            caption = post.find("div", class_="C4VMK").text
            if hashtag in caption:
                hashtag_image_urls.append(image_url)

    return hashtag_image_urls

# 이미지 저장
def save_images(image_urls, insta_id):
    # 이미지 저장 경로 설정
    save_dir = "images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 이미지 다운로드 및 저장
    for i, url in enumerate(image_urls):
        name = url["iamge_name"]
        print(name, "네임!!!!")
        url = url["image_url"]
        print(url, "주소!!!!")
        try:
            image_data = urlopen(url).read()
            # file_path = os.path.join(save_dir, f"{insta_id}_image_{i+1}.jpg")
            file_path = os.path.join(save_dir, f"{name}.jpg")
            with open(file_path, "wb") as f:
                f.write(image_data)
            print(f"{file_path} 저장 완료")
        except Exception as e:
            print(f"{insta_id} 계정 이미지 다운로드 실패: {url}, 에러: {e}")

# 인스타그램에 로그인 후 크롤링
if login_insta(username, password):
    for insta_id in instaIdList:
        print(f"{insta_id} 계정 크롤링 중...")
        image_urls = get_image_urls(insta_id)
        save_images(image_urls, insta_id)

# WebDriver 종료
driver.quit()
