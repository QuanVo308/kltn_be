import numpy as np
from rest_framework import exceptions
from tensorflow import keras
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import PIL
from threading import Thread
import pathlib
from .models import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from unidecode import unidecode
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os

# TRAINNED_MODEL = keras.models.load_model('D:\QuanVo\KLTN\models\output_kaggle tllds 245x200 out128 float ac66/checkpoint')
THREAD_NUMBER = os.cpu_count() -1
MODEL_OUTPUT_LENGTH = 130


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


def load_models():
    return keras.models.load_model('D:/QuanVo/KLTN/models/resnet18 64x64 output 150 margin1 acc74/checkpoint')


def craw_lazada_all():
    sources = SourceData.objects.filter(platform='Lazada')
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver = webdriver.Chrome(
        "D:\Downloads\chromedriver_win32\chromedriver.exe")
    
    for source in sources:
        if source.multi_page == True:
            for page in range(source.min_page, source.max_page+1):
                print(f"{source.link}{page}")
                craw_lazada_page(f"{source.link}{page}", driver)
        else:
            craw_lazada_page(source.link)
    driver.quit()

def craw_lazada_page_thread(source, thread_num):
    for page in range(source.min_page, source.max_page+1):
        if page % THREAD_NUMBER == thread_num:
            print(page, thread_num)
            craw_lazada_page(f"{source.link}{page}")


def craw_lazada_page(link, driver):
    
    product_list = []
    driver.get(link)
    content = driver.page_source
    
    soup = BeautifulSoup(content, "html.parser")

    for a in soup.find_all('div', attrs={"class": "qmXQo"}):
        product_info = a.find('div', attrs={"class": "RfADt"}).find(
            'a', attrs={'age': '0'},  href=True)
        price = a.find('span', attrs={"class": "ooOxS"})

        try:
            product_info.getText()  # name
            product_info['href']  # product link
            price.text  # price

            products = Product.objects.filter(
                link=f"https:{product_info['href']}")
            p = Product() if len(products) == 0 else products[0]
            p.link = f"https:{product_info['href']}"
            p.name = unidecode(product_info.getText())
            p.price = unidecode(price.text)
            p.save()
            product_list.append(p)

        except Exception as e:
            print(e)
            pass

    craw_lazada_image_multithread(product_list)


def craw_lazada_image_multithread(product_list):
    try:
        threads = []
        l = len(product_list)
        if l == 0:
            return
        for thread_num in range(0, THREAD_NUMBER):
            threads.append(PropagatingThread(
                target=craw_lazada_image_thread, args=(product_list, thread_num,)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    except Exception as e:
        print("crawl image error", e)
        pass


def craw_lazada_image_thread(product_list, thread_num):
    driver = webdriver.Chrome(
        "D:\Downloads\chromedriver_win32\chromedriver.exe")
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    l = len(product_list)
    for i in range(l):
        if i % THREAD_NUMBER == thread_num:
            craw_lazada_image(product_list[i], driver)

    driver.quit()


def craw_lazada_image(product, driver):
    driver.get(product.link)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    for a in soup.find_all('img', attrs={"class": "pdp-mod-common-image item-gallery__thumbnail-image"}):
        try:
            a['src']
            images = Image.objects.filter(link=f"{a['src']}")
            i = Image if len(images) == 0 else images[0]
            i = Image()
            i.link = f"{a['src']}"
            i.product = product
            i.save()

        except Exception as e:
            print(e)
            pass


def craw_lazada_image_empty():
    product_list = []

    for p in Product.objects.all():
        if len(p.images.all()) == 0:
            product_list.append(p)

    craw_lazada_image_multithread(product_list)
