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

otps = webdriver.ChromeOptions()
# otps.add_argument('--headless')
# otps.add_argument("--disable-extensions")
# otps.add_argument("--disable-logging")
# otps.add_argument("--log-level=3")
# random_proxy = "117.5.106.105:4001"
# PROXY = "61.28.238.4:3128"
# otps.add_argument('--proxy-server=%s' % PROXY)

# Initialize the webdriver
driver = webdriver.Chrome(
    "D:\Downloads\chromedriver_win32\chromedriver.exe", options=otps)
# driver.maximize_window()
# Navigate to the Lazada Vietnam website
driver.get("https://shopee.vn/T%E1%BA%A5m-l%C3%B3t-ch%E1%BB%91ng-th%E1%BA%A5m-cho-b%C3%A9-v%E1%BA%A3i-s%E1%BB%A3i-tre-4-l%E1%BB%9Bp-Wooji-kt-50x70cm-i.325798615.14072215681?sp_atk=7e808a4d-30af-4886-8d24-7bca31571e88&xptdk=7e808a4d-30af-4886-8d24-7bca31571e88")

try_times = 0
crawled = True
len_old = 0
# try again if cannot find element to click to open image menu
while try_times < 5:
    try:
        try:
            alert_close = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.shopee-alert-popup__btn.btn-solid-primary")))
            alert_close.click()
            break
        except:
            pass
        # image_menu = WebDriverWait(driver, 2).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.MZ9yDd:nth-of-type({2 if try_times < 7 else 1})")))
        # image_menu.click()
        break
    except Exception as e:
            # print("check", e)
            time.sleep(1)
            try_times += 1

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

try_times = 0
while try_times < 10:
    
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MZ9yDd div")))
    except Exception as e:
        # print(e)
        try_times += 1

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
            break
        except:
            # print(try_times)
            time.sleep(1)
            pass
print('done 1')
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

im_links = []

next_button = True
while next_button:
    content = driver.page_source
    
    for _ in range(2):
        soup = BeautifulSoup(content, "html.parser")
        next_button = False
        try:
            for a in soup.find_all('div', attrs={"class": "MZ9yDd"}):
                # print(a, '\n')
                image_link = a.find(
                'div', attrs={"class": "A4dsoy uno8xj"})['style']
                image_link = re.findall("url\(\"(.+)\"\)", image_link)[0]
                print(image_link)
                if image_link not in im_links:
                    im_links.append(image_link)
                    next_button = True
            break
        except Exception as e:
            print('check1', e)
            time.sleep(1)
        

    try:
        image_menu = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"button.shopee-icon-button.JaQdda.Xr3frH")))
        for _ in range(5):
            image_menu.click()

        time.sleep(1)
    except Exception as e:
        next_button = False
        print("click next error", e)
        pass

print(im_links)
print(len(im_links))

