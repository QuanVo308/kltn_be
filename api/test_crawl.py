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
driver.get("https://shopee.vn/-Balo-HOT-Balo-adidas-ph%E1%BA%A3n-quang-Balo-%C4%91i-h%E1%BB%8Dc-%C4%91i-ch%C6%A1i-xu-th%E1%BA%BF-2021-i.76158273.2490794473")

try_times = 0
crawled = True
len_old = 0
# try again if cannot find element to click to open image menu
while try_times < 10:
    try:
        image_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.MZ9yDd ")))
        image_menu.click()
        break
    except Exception as e:
        # print("check", e)
        time.sleep(1)
        try_times += 1

try_times = 0
while try_times < 10:
    
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".rNteT0 div")))
    except Exception as e:
        # print(e)
        try_times += 1

    try_times += 1
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    all_soup = soup.find_all('div', attrs={"class": "y4F+fJ rNteT0"})
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

for a in soup.find_all('div', attrs={"class": "y4F+fJ rNteT0"}):
    try:
        image_link = a.find(
            'div', attrs={"class": "A4dsoy uno8xj"})['style']
        image_link = re.findall("url\(\"(.+)\"\)", image_link)[0]
        # images = Image.objects.filter(link=f"{image_link}")

        # i = Image() if len(images) == 0 else images[0]
        # if check_update_expire(i):
        #     i.link = f"{image_link}"
        #     i.product = product
        #     i.save()

        print(image_link)

    except Exception as e:
        print("craw image shopee product error", e)
        pass

# with open("example2.txt", "w", encoding="utf-8") as f:
#     f.write(f"{str(soup)}")
count = 0

# for a in soup.find_all('div', attrs={"class": "y4F+fJ rNteT0"}):
#     count += 1
#     print(count)
#     image_link = a.find('div', attrs={"class": "A4dsoy uno8xj"})['style']
#     image_link = re.findall("url\(\"(.+)\"\)", image_link)[0]
#     print(image_link)
#     print('\n')

print(count, driver.current_url)


# content = driver.page_source
# soup = BeautifulSoup(content, "html.parser")



driver.quit()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import chromedriver_autoinstaller # pip install chromedriver-autoinstaller

# chromedriver_autoinstaller.install() # To update your chromedriver automatically
# driver = webdriver.Chrome()

# # Get free proxies for rotating
# def get_free_proxies(driver):
#     driver.get('https://sslproxies.org')

#     table = driver.find_element(By.TAG_NAME, 'table')
#     thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
#     tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

#     headers = []
#     for th in thead:
#         headers.append(th.text.strip())

#     proxies = []
#     for tr in tbody:
#         proxy_data = {}
#         tds = tr.find_elements(By.TAG_NAME, 'td')
#         for i in range(len(headers)):
#             proxy_data[headers[i]] = tds[i].text.strip()
#         if proxy_data['Country'] == 'Vietnam':
#             proxies.append(proxy_data)
    
#     return proxies


# free_proxies = get_free_proxies(driver)

# print(free_proxies)
