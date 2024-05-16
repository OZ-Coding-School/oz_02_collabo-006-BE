from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time

#https://www.instagram.com/explore/tags/nail/?hl=en

baseUrl = "https://www.instagram.com/explore/tags/"
plusUrl = input("검색할 태그를 입력하세요 : ")
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html)

insta = soup.select("._aagw")

for i in insta:
    print(i.a['href'])

driver.close()
