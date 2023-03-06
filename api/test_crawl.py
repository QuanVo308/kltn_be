import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



# Initialize the webdriver
driver = webdriver.Chrome(
        "D:\Downloads\chromedriver_win32\chromedriver.exe")
# driver.maximize_window()
# Navigate to the Lazada Vietnam website
driver.get("https://www.lazada.vn/dien-thoai-di-dong/?page=1")

# Wait for the search bar to be present and interactable
# search_bar = WebDriverWait(driver, 1).until(
#     EC.element_to_be_clickable((By.XPATH, '//input[@id="q"]'))
# )

next_page = driver.find_element("class", "ant-pagination-next")

search_term = "lazada"

# Enter a search term
# next_page.send_keys(search_term)
# next_page.submit()
next_page.click()
time.sleep(5)

# suggestion_list = driver.find_element(By.CLASS_NAME, 'suggest-list--3Tm8')

# suggestion_keywords = [item.text for item in suggestion_list.find_elements(By.CLASS_NAME, 'suggest-common--2KmE ')]

# with open("app/lazada/lazada_search_suggestions.json", "w") as file:
#     file.write(
#         json.dumps({"search_term": search_term, "suggestions": suggestion_keywords}, indent=4, ensure_ascii=False))

# Close the webdriver
driver.quit()