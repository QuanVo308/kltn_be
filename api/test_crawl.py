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


# Initialize the webdriver
driver = webdriver.Chrome(
    "D:\Downloads\chromedriver_win32\chromedriver.exe")
# driver.maximize_window()
# Navigate to the Lazada Vietnam website
driver.get("https://www.lazada.vn/products/dien-thoai-xiaomi-qin-f21-pro-moi-100-nguyen-hop-cai-san-tieng-viet-ch-play-day-du-i2197306887-s10458996501.html")

actions = ActionChains(driver)
content = driver.page_source

soup = BeautifulSoup(content, "html.parser")
with open("example2.txt", "w", encoding="utf-8") as f:
    f.write(f"{str(soup)}")

for a in soup.find_all('img', attrs={"class": "pdp-mod-common-image item-gallery__thumbnail-image"}):
    try:
        a['src']
        print(a['src'])
    except Exception as e:
        print("craw image product error", e)
        pass
# slider = driver.find_element(By.CSS_SELECTOR, ".nc_iconfont.btn_slide")
# slider = driver.find_element(By.className("nc_iconfont btn_slide"))

# search_term = "lazada"
# actions.move_to_element(slider).click_and_hold().drag_and_drop_by_offset(200, 0).release().perform()
# Enter a search term
# next_page.send_keys(search_term)
# next_page.submit()
# next_page.click()
time.sleep(10)

# suggestion_list = driver.find_element(By.CLASS_NAME, 'suggest-list--3Tm8')

# suggestion_keywords = [item.text for item in suggestion_list.find_elements(By.CLASS_NAME, 'suggest-common--2KmE ')]

# with open("app/lazada/lazada_search_suggestions.json", "w") as file:
#     file.write(
#         json.dumps({"search_term": search_term, "suggestions": suggestion_keywords}, indent=4, ensure_ascii=False))

# Close the webdriver
driver.quit()
