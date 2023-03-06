from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from unidecode import unidecode

driver = webdriver.Chrome("D:\Downloads\chromedriver_win32\chromedriver.exe")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

products = []  # List to store name of the product
prices = []  # List to store price of the product
images = []  # List to store rating of the product
product_links = []


for page in range(1, 3):
    driver.get(f"https://www.lazada.vn/dien-thoai-di-dong/?page={page}")

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    t = ""
    # print(soup.findAll('div',attrs={"class":"_1AtVbE col-12-12"}))
    for a in soup.find_all('div', attrs={"class": "qmXQo"}):
        # print('check')
        # name=a.find('div', attrs={'class':'_4rR01T'})
        # price=a.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
        # image=a.find('img', attrs={'class':'_396cs4'})
        link = a.find('div', attrs={"class": "RfADt"}).find(
            'a', attrs={'age': '0'},  href=True)
        price = a.find('span', attrs={"class": "ooOxS"})
        try:
            print(link.getText())
            print(link['href'])
            print(price.text)
            print('\n')
            # driver.get(f"https:{link['href']}")
            # product_content = driver.page_source
            # product_soup = BeautifulSoup(product_content, "html.parser")
            # for a in soup.find_all('div', attrs={"class":"pdp-product-price"}):
            # image['src']
            # name.text
            # price.text
            prices.append(unidecode(price.text))
            products.append(unidecode(link.text))
            # images.append(image['src'])
            product_links.append(link['href'])
        except Exception as e:
            print(e)
            pass


df = pd.DataFrame({'Product Name': products, 'price': prices,
                  'product_links': product_links})
df.to_csv('products.csv', index=False)
