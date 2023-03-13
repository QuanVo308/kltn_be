import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
from unidecode import unidecode

# Initialize the webdriver
driver = webdriver.Chrome(
    "D:\Downloads\chromedriver_win32\chromedriver.exe")
# driver.maximize_window()
# Navigate to the Lazada Vietnam website
driver.get("https://shopee.vn/all_categories")


# close = driver.execute_script(
#         'return document.querySelector("#main shopee-banner-popup-stateful").shadowRoot.querySelector("div.home-popup__close-area div.shopee-popup__close-btn")')
# close.click()

# next = driver.execute_script(
#         'return document.querySelector("div.LYxxi- div.carousel-arrow--next")')
# next.click()
# time.sleep(2)
# image_menu = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.K34m1x")))

# height = driver.execute_script("return document.body.scrollHeight")
# scroll_length = 0
# scroll_step = 500

# while scroll_length < height:
#     driver.execute_script(
#         f"window.scrollTo({scroll_length}, {scroll_length + scroll_step})")
#     scroll_length += scroll_step
#     # time.sleep(0.5)
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-sqe=\"link\"]")))
#     height = driver.execute_script("return document.body.scrollHeight")

content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

# with open("example2.txt", "w", encoding="utf-8") as f:
#     f.write(f"{str(soup)}")
count = 0

for a in soup.find_all('a', href = True, attrs={"class": "a-sub-category--display-name"}):
    count += 1
    print(count)
    # print(a.find('a', attrs={"data-sqe": "link"}))
    product_link = a['href']
    print(f"https://shopee.vn{product_link}")
    print(a.text)
    print('\n')

print(count, driver.current_url)


# content = driver.page_source
# soup = BeautifulSoup(content, "html.parser")



driver.quit()
