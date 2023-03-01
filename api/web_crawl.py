from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome("D:\Downloads\chromedriver_win32\chromedriver.exe")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

products=[] #List to store name of the product
prices=[] #List to store price of the product
images=[] #List to store rating of the product
# driver.get("https://www.flipkart.com/laptops/~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;uniq")

driver.get("https://www.flipkart.com/mobiles/mi~brand/pr?sid=tyy,4io&otracker=nmenu_sub_Electronics_0_Mi")

content = driver.page_source
soup = BeautifulSoup(content)
t = ""
# print(soup.findAll('div',attrs={"class":"_1AtVbE col-12-12"}))
for a in soup.findAll('div', attrs={"class":"_1AtVbE col-12-12"}):
    # print('check')
    name=a.find('div', attrs={'class':'_4rR01T'})
    price=a.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
    image=a.find('img', attrs={'class':'_396cs4'})
    try:
        image['src']
        name.text
        price.text
        products.append(name.text)
        prices.append(price.text)
        images.append(image['src']) 
    except:
        pass

df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':images}) 
df.to_csv('products.csv', index=False, encoding='utf-8')

