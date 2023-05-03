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

# Initialize the webdriver
driver = webdriver.Chrome(service=Service(
                    ChromeDriverManager().install()), options=otps)

driver.get("https://shopee.vn/buyer/login")

try_times = 0
crawled = True
len_old = 0
# try again if cannot find element to click to open image menu
while try_times < 5:
    try:
        user_name = driver.find_element(By.XPATH,
                                                   '//input[@placeholder="Email/Số điện thoại/Tên đăng nhập"]')
        password = driver.find_element(By.XPATH, '//input[@placeholder="Mật khẩu"]')

        user_name.send_keys("0963940029")
        password.send_keys("Quanvobakhong8")
        password.send_keys(Keys.ENTER)
        break
    except Exception as e:
            # print("check", e)
            time.sleep(1)
            try_times += 1
time.sleep(30)

# try_times = 0
# while try_times < 10:
    
#     try:
#         WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".rNteT0 div")))
#     except Exception as e:
#         # print(e)
#         try_times += 1

#     try_times += 1
#     content = driver.page_source
#     soup = BeautifulSoup(content, "html.parser")
#     all_soup = soup.find_all('div', attrs={"class": "y4F+fJ rNteT0"})
#     len_new = len(all_soup)
#     if len_new == 0 or len_new != len_old:
#         len_old = len_new
#         time.sleep(1)
#     else:
#         try:
#             for a in all_soup:
#                 image_link = a.find(
#                 'div', attrs={"class": "A4dsoy uno8xj"})['style']
#                 image_link = re.findall("url\(\"(.+)\"\)", image_link)[0]
#             break
#         except:
#             # print(try_times)
#             time.sleep(1)
#             pass
# print('done 1')
# content = driver.page_source
# soup = BeautifulSoup(content, "html.parser")

# for a in soup.find_all('div', attrs={"class": "y4F+fJ rNteT0"}):
#     try:
#         image_link = a.find(
#             'div', attrs={"class": "A4dsoy uno8xj"})['style']
#         image_link = re.findall("url\(\"(.+)\"\)", image_link)[0]
#         category = soup.select(".dR8kXc a.akCPfg:last-of-type")
#         print(unidecode(category[0].text).lower())
#         # images = Image.objects.filter(link=f"{image_link}")

#         # i = Image() if len(images) == 0 else images[0]
#         # if check_update_expire(i):
#         #     i.link = f"{image_link}"
#         #     i.product = product
#         #     i.save()

#         print(image_link)

#     except Exception as e:
#         print("craw image shopee product error", e)
#         pass

# try_times = 0
# while try_times < 10:
    
#     try:
#         WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".MZ9yDd div")))
#     except Exception as e:
#         # print(e)
#         try_times += 1

#     try_times += 1
#     content = driver.page_source
#     soup = BeautifulSoup(content, "html.parser")
#     all_soup = soup.find_all('div', attrs={"class": "MZ9yDd"})
#     len_new = len(all_soup)
#     if len_new == 0 or len_new != len_old:
#         len_old = len_new
#         time.sleep(1)
#     else:
#         try:
#             for a in all_soup:
#                 image_link = a.find(
#                 'div', attrs={"class": "A4dsoy uno8xj"})['style']
#                 image_link = re.findall("url\(\"(.+)\"\)", image_link)[0]
#             break
#         except:
#             # print(try_times)
#             time.sleep(1)
#             pass
# print('done 1')
# content = driver.page_source
# soup = BeautifulSoup(content, "html.parser")

# im_links = []

# next_button = True
# while next_button:
#     content = driver.page_source
    
#     for _ in range(2):
#         soup = BeautifulSoup(content, "html.parser")
#         next_button = False
#         try:
#             for a in soup.find_all('div', attrs={"class": "MZ9yDd"}):
#                 # print(a, '\n')
#                 image_link = a.find(
#                 'div', attrs={"class": "A4dsoy uno8xj"})['style']
#                 image_link = re.findall("url\(\"(.+)\"\)", image_link)[0]
#                 print(image_link)
#                 if image_link not in im_links:
#                     im_links.append(image_link)
#                     next_button = True
#             break
#         except Exception as e:
#             print('check1', e)
#             time.sleep(1)
        

#     try:
#         image_menu = WebDriverWait(driver, 2).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, f"button.shopee-icon-button.JaQdda.Xr3frH")))
#         for _ in range(5):
#             image_menu.click()

#         time.sleep(1)
#     except Exception as e:
#         next_button = False
#         print("click next error", e)
#         pass

# print(im_links)
# print(len(im_links))

