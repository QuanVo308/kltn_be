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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

otps = webdriver.ChromeOptions()
# otps.add_argument('--headless')
# otps.add_argument("--disable-extensions")
# otps.add_argument("--disable-logging")
# otps.add_argument("--log-level=3")
# random_proxy = "117.5.106.105:4001"
# PROXY = "61.28.238.4:3128"
# otps.add_argument('--proxy-server=%s' % PROXY)
def shopee_login(driver):
    user_name = driver.find_element(
        By.XPATH, '//input[@placeholder="Email/Số điện thoại/Tên đăng nhập"]')
    password = driver.find_element(
        By.XPATH, '//input[@placeholder="Mật khẩu"]')

    user_name.send_keys("0963940029")
    password.send_keys("Quanvobakhong8")
    password.send_keys(Keys.ENTER)
# Initialize the webdriver
driver = webdriver.Chrome(service=Service(
                    ChromeDriverManager().install()), options=otps)

driver.get("https://shopee.vn/máy-xay-osaka-nhật-nắp-đồng-xay-được-cả-thế-giới-i.112945489.19849668258")

try_times = 0
crawled = True
len_old = 0
# try again if cannot find element to click to open image menu
# while try_times < 5:
#     try:
#         user_name = driver.find_element(By.XPATH,
#                                                    '//input[@placeholder="Email/Số điện thoại/Tên đăng nhập"]')
#         password = driver.find_element(By.XPATH, '//input[@placeholder="Mật khẩu"]')

#         user_name.send_keys("0963940029")
#         password.send_keys("Quanvobakhong8")
#         password.send_keys(Keys.ENTER)
#         break
#     except Exception as e:
#             # print("check", e)
#             time.sleep(1)
#             try_times += 1
# time.sleep(30)

while try_times < 3:
    try:
        # try:
        """close 18+ alert"""
        alert_close = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.shopee-alert-popup__btn.btn-solid-primary")))
        alert_close.click()
        break
        # except:
        #     pass
        """open image menu (removed)"""
        # image_menu = WebDriverWait(driver, 2).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.MZ9yDd:nth-of-type({2 if try_times < 7 else 1})")))
        # image_menu.click()
        # break
    except Exception as e:
        # print("check", e)
        # time.sleep(1)
        try_times += 1

try_times = 0
while try_times < 10:

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MZ9yDd div")))
    except Exception as e:
        # print(e)
        try_times += 1
    try:
        shopee_login(driver)
    except:
        pass
    try_times += 1
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    all_soup = soup.find_all('div', attrs={"class": "MZ9yDd"})
    len_new = len(all_soup)
    if len_new == 0 or len_new != len_old:
        len_old = len_new
        time.sleep(1)
    else:
        try:
            for a in all_soup:
                image_link = a.find(
                    'div', attrs={"class": "A4dsoy uno8xj"})['style']
                image_link = re.findall("url\(\"(.+)\"\)", image_link)[0]
            soup.select(".dR8kXc a.akCPfg:last-of-type")[0].text
            break
        except:
            time.sleep(1)
            pass
    
    next_button = True
    new_image = False
    while next_button:
        content = driver.page_source
        next_button = False
        for _ in range(2):
            soup = BeautifulSoup(content, "html.parser")
            try:
                fail = 0
                for a in soup.find_all('div', attrs={"class": "MZ9yDd"}):
                    try:
                        image_link = a.find(
                            'div', attrs={"class": "A4dsoy"})['style']
                        image_link = re.findall(
                            "url\(\"(.+)\"\)", image_link)[0]
                        
                        print(image_link)

                        
                    except Exception as e:
                        print("craw image shopee product error", e)

                        fail += 1
                        pass
                # if fail != 0:
                    # raise exceptions.ValidationError('shopee load image error')
                break
            except Exception as e:
                print('shopee not load image after click next', e)
                time.sleep(1)

        for i in range(2):
            try:
                image_menu = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"button.shopee-icon-button.JaQdda.Xr3frH")))
                for _ in range(5):
                    image_menu.click()

                time.sleep(1)
                break
            except Exception as e:
                if i == 1:
                    next_button = False
                time.sleep(1)
                print(f"shopee click next error {i}")

                pass