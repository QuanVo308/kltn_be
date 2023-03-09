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


# Initialize the webdriver
driver = webdriver.Chrome(
    "D:\Downloads\chromedriver_win32\chromedriver.exe")
# driver.maximize_window()
# Navigate to the Lazada Vietnam website
driver.get("https://shopee.vn/Tai-Nghe-Ch%E1%BB%A5p-Tai-Kh%C3%B4ng-M6-K%E1%BA%BFt-Bluetooth-%C3%82m-Si%C3%AAu-Tr%E1%BA%A7m-C%C3%B3-G%E1%BA%ADp-L%E1%BA%A1i-i.824146607.18050567425?sp_atk=ce479673-81e8-4507-a238-99fdb6267d04&xptdk=ce479673-81e8-4507-a238-99fdb6267d04")



# next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".shopee-icon-button.shopee-icon-button--right")))
# # next_page.click()



# def shopee_scroll_to_end(driver):
#     height = driver.execute_script("return document.body.scrollHeight")
#     scroll_length = 0
#     scroll_step = 500

#     while scroll_length < height:
#         driver.execute_script(f"window.scrollTo({scroll_length}, {scroll_length + scroll_step})")
#         scroll_length += scroll_step
#         # time.sleep(0.5)
#         WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._8MceUQ")))
#         print(height)
#         height = driver.execute_script("return document.body.scrollHeight")

# shopee_scroll_to_end(driver)
# height = driver.execute_script("return document.body.scrollHeight")
# scroll_length = 0
# scroll_step = 500

# while scroll_length < height:
#     driver.execute_script(f"window.scrollTo({scroll_length}, {scroll_length + scroll_step})")
#     scroll_length += scroll_step
#     # time.sleep(0.5)
#     WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._8MceUQ")))
#     print(height)
#     height = driver.execute_script("return document.body.scrollHeight")

# next_page = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ol-xs-2-4 .shopee-search-item-result__item")))

# next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".shopee-icon-button.shopee-icon-button--right")))
# next_page.click()
# next_page = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._8MceUQ")))

image_menu = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".MZ9yDd div")))
image_menu.click()

try_times = 0
while try_times < 5:
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".rNteT0 div")))
        try_times = 10
        print("find it")
    except Exception as e:
        print(e)

try_times = 0
while try_times < 10:
    try:
        WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".rNteT0 div")))
        try_times = 10
        print("find it")
    except Exception as e:
        print(e)
        try_times += 1

content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

# with open("example2.txt", "w", encoding="utf-8") as f:
#     f.write(f"{str(soup)}")
i = 0
for a in soup.find_all('div', attrs={"class": "y4F+fJ rNteT0"}):
    try:
        image_link = a.find('div', attrs={"class": "A4dsoy uno8xj"})['style']
        print(re.findall("url\(\"(.+)\"\)", image_link)[0])
        # images = Image.objects.filter(link=f"{a['src']}")

        # i = Image() if len(images) == 0 else images[0]

        # if check_update_expire(i):
        #     i.link = f"{a['src']}"
        #     i.product = product
        #     i.save()

    except Exception as e:
        print("craw image product error", e)
        pass

# slider = driver.find_element(By.className("nc_iconfont btn_slide"))

# search_term = "lazada"
# actions.move_to_element(slider).click_and_hold().drag_and_drop_by_offset(200, 0).release().perform()
# Enter a search term
# next_page.send_keys(search_term)
# next_page.submit()
# next_page.click()
# time.sleep(10)


driver.quit()
