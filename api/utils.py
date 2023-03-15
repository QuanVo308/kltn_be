import numpy as np
from rest_framework import exceptions
from tensorflow import keras
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import PIL
from threading import Thread
import pathlib
import math
from .models import *
from urllib.parse import unquote
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from unidecode import unidecode
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime
from django.utils import timezone
import json
import re
import time
from dotenv import load_dotenv
load_dotenv()

# TRAINNED_MODEL = keras.models.load_model('D:\QuanVo\KLTN\models\output_kaggle tllds 245x200 out128 float ac66/checkpoint')
THREAD_NUMBER_IMAGE = 2
THREAD_NUMBER_LINK_SOURCE = math.ceil(os.cpu_count()/2.0)
MODEL_OUTPUT_LENGTH = 130
EXPIRE_INFO_DAYS = 3


otps = webdriver.ChromeOptions()
# otps.add_argument('--headless')
otps.add_argument("--disable-extensions")
otps.add_argument("--disable-logging")
otps.add_argument("--log-level=3")


otps2 = webdriver.ChromeOptions()
otps2.add_argument('--headless')
otps2.add_argument("--disable-extensions")
otps2.add_argument("--disable-logging")
otps2.add_argument("--log-level=3")

# webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=otps).quit()


class PropagatingThread(Thread):
    def run(self):
        self.exc = None
        try:
            if hasattr(self, '_Thread__target'):
                # Thread uses name mangling prior to Python 3.
                self.ret = self._Thread__target(
                    *self._Thread__args, **self._Thread__kwargs)
            else:
                self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e


def products_have_no_image():
    ps = []
    for p in Product.objects.all():
        # t = timezone.now() - p.updated_at
        if len(p.images.all()) == 0:
            ps.append(p)
    return ps


def check_update_expire(instance):
    try:
        period = timezone.now() - instance.updated_at
        if period.days > EXPIRE_INFO_DAYS:
            return True
        return False
    except Exception as e:
        return True

def delete_all_product_multithread():
    products = Product.objects.all()
    quantity = len(products)
    total_thread = os.cpu_count() * 8
    threads = []
    for thread_num in range(total_thread):
        threads.append(PropagatingThread(target=delete_product, args=(products[
            int(quantity/total_thread * thread_num): 
            int(quantity/total_thread * (thread_num + 1))
            ],)))
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def delete_product(products):
    for idx, product in enumerate(products):
        # print(product.id, f'{idx}/{len(products)}')
        product.delete()


def load_models():
    # return TRAINNED_MODEL
    return keras.models.load_model('C:/Users/Quan/Documents/Temp/models/resnet18 64x64 output 150 margin1 acc74/checkpoint')


def crawl_lazada_categories():
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps)
    driver.get("https://www.lazada.vn/")

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    for a in soup.find_all('li', attrs={"class": "lzd-site-menu-sub-item"}):
        category_link = a.find('a', href=True)
        description = unidecode(category_link.find('span').text)

    for a in soup.find_all('a', href=True, attrs={"class": "UPUwyq"}):
        a.text
        a['href']

    SourceData.objects.filter(platform='Lazada').delete()

    for a in soup.find_all('li', attrs={"class": "lzd-site-menu-sub-item"}):
        category_link = a.find('a', href=True)
        description = "Lazada " + category_link.find('span').text
        source = SourceData()
        source.platform = "Lazada"
        source.link = f"https:{category_link['href']}"
        source.description = description
        source.save()

    driver.quit()


def crawl_shopee_categories():
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps2)
    driver.get("https://shopee.vn/all_categories")

    try:
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")

        for a in soup.find_all('a', href=True, attrs={"class": "a-sub-category--display-name"}):
            a['href']
            a.text

        SourceData.objects.filter(platform='Shopee').delete()

        for a in soup.find_all('a', href=True, attrs={"class": "a-sub-category--display-name"}):
            category_link = "https://shopee.vn" + a['href']
            description = "Shopee " + a.text

            source = SourceData()
            source.platform = "Shopee"
            source.link = f"{category_link}"
            source.description = unidecode(description)
            source.save()

        driver.quit()
    
    except Exception as e:
        print(e)
        driver.quit()


def crawl_shopee_categories_from_home():
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps)
    driver.get("https://shopee.vn/")

    try:
        close = driver.execute_script(
            'return document.querySelector("#main shopee-banner-popup-stateful").shadowRoot.querySelector("div.home-popup__close-area div.shopee-popup__close-btn")')
        close.click()
    except Exception as e:
        print("cannot close ad shopee", e)

    try:
        next = driver.execute_script(
            'return document.querySelector("div.LYxxi- div.carousel-arrow--next")')
        next.click()
        time.sleep(2)
        image_menu = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.K34m1x")))
    except Exception as e:
        print(f"cannot load other categories shopee {e}")

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    for a in soup.find_all('a', href=True, attrs={"class": "home-category-list__category-grid"}):
        link = "https://shopee.vn" + a['href']
        a.find('div', attrs={"class": "K34m1x"}).text

    SourceData.objects.filter(platform='Shopee').delete()

    for a in soup.find_all('a', href=True, attrs={"class": "home-category-list__category-grid"}):
        category_link = "https://shopee.vn" + a['href']
        description = "Shopee " + a.find('div', attrs={"class": "K34m1x"}).text

        source = SourceData()
        source.platform = "Shopee"
        source.link = f"{category_link}"
        source.description = unidecode(description)
        source.save()

    driver.quit()


def crawl_lazada_all():
    sources = SourceData.objects.filter(platform='Lazada')

    threads = []
    for thread_num in range(0, THREAD_NUMBER_LINK_SOURCE):
        threads.append(PropagatingThread(
            target=crawl_lazada_page_multithread, args=(sources, thread_num,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


# def crawl_lazada_multi_page(source):
#     driver = webdriver.Chrome(
#         "D:\Downloads\chromedriver_win32\chromedriver.exe", options=otp)
#     # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=otp)
#     if source.multi_page == True:
#         for page in range(source.min_page, source.max_page+1):
#             print(f"{source.link}{page}")
#             crawl_lazada_page(f"{source.link}{page}",
#                              driver, source.key_words)
#     else:
#         crawl_lazada_page(source.link, driver, source.key_words)

#     driver.quit()


def crawl_lazada_page_multithread(sources, thread_num):
    source_quantity = len(sources)
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps)
    for i in range(source_quantity):
        if i % THREAD_NUMBER_LINK_SOURCE == thread_num:
            crawl_lazada_page(sources[i], driver, thread_num)
    driver.quit()


def crawl_lazada_page(source, driver, thread_num):
    link = source.link

    # webdriver.Chrome("D:\Downloads\chromedriver_win32\chromedriver.exe", options=otp)
    try:
        product_list = []
        driver.get(link)
        same = 0
    except Exception as e:
        print("crawl lazada page 0 error", e)
    while same <= 5:
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        print(f"crawling page {thread_num} {driver.current_url}")
        product_list = []
        same += 1

        for a in soup.find_all('div', attrs={"class": "qmXQo"}):
            try:
                product_info = a.find('div', attrs={"class": "RfADt"}).find(
                    'a', attrs={'age': '0'},  href=True)
                price = a.find('span', attrs={"class": "ooOxS"})
                product_info.getText()  # name
                product_info['href']  # product link
                price.text  # price

                products = Product.objects.filter(
                    link=f"https:{product_info['href']}")

                p = Product() if len(products) == 0 else products[0]

                if check_update_expire(p):
                    p.link = f"https:{product_info['href']}"
                    p.name = unidecode(product_info.getText())
                    p.price = unidecode(price.text)
                    p.source_description = unidecode(source.description)
                    p.save()
                    same = 0
                    product_list.append(p)

            except Exception as e:
                print("crawl page error", e)
                pass

        # crawl_lazada_image_multithread(product_list)

        try:
            next_page = WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "li[title = \"Next Page\"] button.ant-pagination-item-link:not([disabled])")))
            next_page.click()
        except:
            print(f'lazada change page error {link}', e)
            pass
    # driver.quit()


def crawl_lazada_image_multithread(product_list):
    try:
        threads = []
        l = len(product_list)
        if l == 0:
            return
        for thread_num in range(0, THREAD_NUMBER_IMAGE):
            threads.append(PropagatingThread(
                target=crawl_lazada_image_thread, args=(product_list, thread_num,)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    except Exception as e:
        print("crawl image error", e)
        pass


def crawl_lazada_image_thread(product_list, thread_num):
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps)

    l = len(product_list)
    for i in range(l):
        if i % THREAD_NUMBER_IMAGE == thread_num:
            crawl_lazada_image(product_list[i], driver)

    driver.quit()


def crawl_lazada_image(product, driver):
    driver.get(product.link)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    for a in soup.find_all('img', attrs={"class": "pdp-mod-common-image item-gallery__thumbnail-image"}):
        try:
            a['src']
            images = Image.objects.filter(link=f"{a['src']}")

            i = Image() if len(images) == 0 else images[0]

            if check_update_expire(i):
                i.link = f"{a['src']}"
                i.product = product
                i.save()

        except Exception as e:
            print("craw image product error", e)
            pass


def crawl_shopee_all():
    try_time = 3
    while try_time >= 0:
        try:
            try_time -= 1

            sources = SourceData.objects.filter(platform='Shopee', crawled__in=[False])
            threads = []
            for thread_num in range(0, THREAD_NUMBER_LINK_SOURCE):
                threads.append(PropagatingThread(
                    target=crawl_shopee_page_multithread, args=(sources, thread_num,)))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            sources = SourceData.objects.filter(platform='Shopee', crawled__in=[False])
            if len(sources) == 0:
                return
        except Exception as e:
            print("crawl shopee all error ", e)




def crawl_shopee_page_multithread(sources, thread_num):
    # sources = sources[:2]
    try:
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=otps)
        source_quantity = len(sources)
        for i in range(source_quantity):
            if i % THREAD_NUMBER_LINK_SOURCE == thread_num:
                crawl_shopee_page(sources[i], driver)
        driver.quit()
    except Exception as err_374:
        driver.quit()
        print('shopee multithread crawl page error', err_374)


def crawl_shopee_image(product, driver):
    driver.get(product.link)
    try_times = 0
    clicked = False
    while try_times < 10:
        try:
            image_menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.MZ9yDd ")))
            image_menu.click()
            clicked = True
        except Exception as e:
            print("check", e)
            time.sleep(1)
            try_times += 1

    try_times = 0
    while try_times < 10:
        
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".rNteT0 div")))
            # try_times = 10
            # print("find it")
        except Exception as e:
            # print(e)
            try_times += 1

        try_times += 1
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        if len(soup.find_all('div', attrs={"class": "y4F+fJ rNteT0"})) == 0:
            time.sleep(1)
        else:
            break
 
    

    if len(soup.find_all('div', attrs={"class": "y4F+fJ rNteT0"})) == 0:
        raise exceptions.ValidationError(f"shopee cannot find image {product.name} {clicked}")
    
    for a in soup.find_all('div', attrs={"class": "y4F+fJ rNteT0"}):
        try:
            image_link = a.find(
                'div', attrs={"class": "A4dsoy uno8xj"})['style']
            image_link = re.findall("url\(\"(.+)\"\)", image_link)[0]
            images = Image.objects.filter(link=f"{image_link}")

            i = Image() if len(images) == 0 else images[0]
            if check_update_expire(i):
                i.link = f"{image_link}"
                i.product = product
                i.save()

        except Exception as e:
            print("craw image shopee product error", e)
            pass

    product.crawled = True
    product.save()

def get_not_crawl_products(product_list):
    ps = [product for product in product_list if product.crawled == False]
    return ps
    
def crawl_shopee_image_multithread(product_list):
    try_time = 3
    while try_time >= 0:
        products_not_crawled = get_not_crawl_products(product_list)
        if len(products_not_crawled) == 0:
            return
        
        try_time-=1

        try:
            threads = []
            l = len(products_not_crawled)
            if l == 0:
                return
            for thread_num in range(0, THREAD_NUMBER_IMAGE):
                threads.append(PropagatingThread(
                    target=crawl_shopee_image_thread, args=(products_not_crawled, thread_num,)))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

        except Exception as e:
            print("shopee crawl image error", e)
            pass


def crawl_shopee_image_thread(product_list, thread_num):
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps)
    try:

        l = len(product_list)
        for i in range(l):
            if i % THREAD_NUMBER_IMAGE == thread_num:
                try:
                    crawl_shopee_image(product_list[i], driver)
                except Exception as err:
                    print('shopee crawl image error', err)
    except Exception as e:
        driver.quit()
        print('shopee multithread crawl image error', e)
    driver.quit()


def shopee_scroll_to_end(driver):
    height = driver.execute_script("return document.body.scrollHeight")
    scroll_length = 0
    scroll_step = 500
    while scroll_length < height:
        # print(scroll_length, height)
        driver.execute_script(
            f"window.scrollTo({scroll_length}, {scroll_length + scroll_step})")
        scroll_length += scroll_step
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-sqe=\"link\"]")))
        height = driver.execute_script("return document.body.scrollHeight")


def crawl_shopee_page(source, driver):
    link = source.link
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=otp)
    same = 0
    product_list = []
    try:
        driver.get(link)

    except Exception as e_481:
        print("crawl shopee page 0 error", e_481)

    while same <= 5:

        try:
            shopee_scroll_to_end(driver)

            content = driver.page_source
            print(driver.current_url)
            soup = BeautifulSoup(content, "html.parser")
            product_list = []
            same += 1
            for a in soup.find_all('div', attrs={"class": "col-xs-2-4 shopee-search-item-result__item"}):
                try:
                    product_price = a.find(
                        'span', attrs={"class": "du3pq0"}).getText()
                    product_name = a.find(
                        'div', attrs={"class": "_1yN94N WoKSjC _2KkMCe"}).getText()  # name
                    product_link = a.find(
                        'a', attrs={"data-sqe": "link"})['href'].split('?')[0]  # product link

                    products = Product.objects.filter(
                        name=f"{unidecode(product_name)}")

                    p = Product() if len(products) == 0 else products[0]

                    # new_key_words = [kw for kw in key_words if kw not in p.key_words]

                    # if check_update_expire(p) or len(new_key_words) != 0:
                    if check_update_expire(p):
                        p.link = f"https://shopee.vn{product_link}"
                        p.name = unidecode(product_name)
                        p.price = unidecode(product_price)
                        p.source_description = source.description
                        # p.key_words.extend(new_key_words)
                        p.save()
                        same = 0
                        product_list.append(p)
                except Exception as e1:
                    print("shopee crawl page find element", e1)

        except Exception as err:
            print(f'shopee crawl page error {link}', err)
            pass

        crawl_shopee_image_multithread(product_list)

        try:
            next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".shopee-icon-button.shopee-icon-button--right")))
            next_page.click()
        except Exception as e_533:
            print(f'shopee change page error {link}', e_533)
            pass
    source.crawled = True
    source.save()
    # driver.quit()
