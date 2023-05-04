from multiprocessing.pool import ThreadPool
from rembg import remove, new_session
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
from .serializers import *
from urllib.parse import unquote
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from unidecode import unidecode
from selenium import webdriver
from bs4 import BeautifulSoup
from django.db.models import Count
import pandas as pd
import requests
import datetime
from django.utils import timezone
import json
import re
import time
from io import BytesIO
import shutil
import random
from django.db.models import Q
import gc
import cv2
import binascii
import pyunpack
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from dotenv import load_dotenv
import os
from selenium.webdriver.common.keys import Keys
load_dotenv()


TRAINNED_MODEL = "temp"
# TRAINNED_MODEL = keras.models.load_model(os.environ.get('TRAINNED_MODEL_PATH'))
THREAD_QUANTITY_CRAWL_PRODUCT = int(
    os.environ.get('THREAD_QUANTITY_CRAWL_PRODUCT'))
THREAD_NUMBER_LINK_SOURCE = int(
    os.environ.get('THREAD_QUANTITY_CRAWL_LINK_SOURCE'))
MODEL_OUTPUT_LENGTH = int(os.environ.get('MODEL_OUTPUT_LENGTH'))
EXPIRE_INFO_DAYS = int(os.environ.get('EXPIRE_INFO_DAYS'))
SHOPEE_USERNAME = os.environ.get('SHOPEE_USERNAME')
SHOPEE_PASSWORD = os.environ.get('SHOPEE_PASSWORD')
AUTO_UPDATE_NEW_TIMEOUT_H = 40
AUTO_UPDATE_OLD_TIMEOUT_H = 40


otps = webdriver.ChromeOptions()
# otps.add_argument('--headless')
otps.add_argument("--disable-extensions")
otps.add_argument("--disable-logging")
otps.add_argument("--log-level=3")


otps2 = webdriver.ChromeOptions()
# otps2.add_argument('--headless')
otps2.add_argument("--disable-extensions")
otps2.add_argument("--disable-logging")
otps2.add_argument("--log-level=3")

# webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=otps).quit()


# def load_models():
# return TRAINNED_MODEL
# return keras.models.load_model(os.environ.get('TRAINNED_MODEL_PATH'))

def cleanup_category():
    print('clean up category')
    categories = Category.objects.all()
    for category in categories:
        qs = Category.objects.filter(name=category.name)
        if len(qs) > 1:
            category.delete()


def cleanup_product():
    print('clean up product')
    products = Product.objects.all()
    for product in products:
        qs = Product.objects.filter(link=product.link)
        if len(qs) > 1:
            print(product.id)
            product.delete()


def cleanup_webdriver():
    base_dir = pathlib.Path(os.environ.get('TRASH_TEMP_WEBDRIVER_PATH'))
    count = 0

    for path in base_dir.glob("scoped_dir*"):
        count += 1
        print(count, str(path))
        shutil.rmtree(str(path))
    print(count)


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


# def update_exact_image_multithread():
#     images = Image.objects.filter(embedding_vector=[])
#     print(len(images))
#     quantity = len(images)
#     total_thread = os.cpu_count()
#     threads = []
#     images = np.array_split(images, total_thread)
#     for thread_num in range(total_thread):
#         threads.append(PropagatingThread(
#             target=exact_image_thread, args=(images[thread_num],)))

#     for thread in threads:
#         thread.start()
#     for thread in threads:
#         thread.join()

#     # del model
#     # gc.collect()


# def exact_image_thread(images):
#     for idx, image in enumerate(images):
#         # print(image.id, f'{idx}/{len(images)}')
#         try:
#             image.embedding_vector = exact_embedding_from_link(image.link)
#             image.save()
#         except:
#             image.delete()


def delete_all_product_multithread():
    products = Product.objects.all()
    quantity = len(products)
    total_thread = os.cpu_count() * 8
    threads = []
    products = np.array_split(products, total_thread)
    for thread_num in range(total_thread):
        threads.append(PropagatingThread(
            target=delete_product, args=(products[thread_num],)))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def delete_product(products):
    for idx, product in enumerate(products):
        # print(product.id, f'{idx}/{len(products)}')
        product.delete()


def exact_embedding_from_link(link):
    try:
        response = requests.get(link, timeout=3)
        image = PIL.Image.open(BytesIO(response.content))

        if np.asarray(image).shape[2] != 3:
            new_image = PIL.Image.new("RGB", image.size, "WHITE")
            new_image.paste(image, mask=image.split()[3])
            image = new_image

        image = image.resize(size=(200, 245))
        image_arr = np.asarray(image)/255.

        with tf.device('/device:CPU:0'):
            embedding_vector = TRAINNED_MODEL.predict(
                np.stack([image_arr]), verbose=0).tolist()
        gc.collect()
        tf.keras.backend.clear_session()
        return embedding_vector
    except Exception as e:
        gc.collect()
        tf.keras.backend.clear_session()
        # print('exacting image from link error', e)
        raise exceptions.ValidationError(f'exacting image from link error {e}')
        return []


def update_exact_image_multithread_temp(products):
    try:
        products = np.array_split(products, THREAD_QUANTITY_CRAWL_PRODUCT)
        print('loading done', len(products))
        threads = []
        for thread_num in range(THREAD_QUANTITY_CRAWL_PRODUCT):
            threads.append(PropagatingThread(
                target=exact_embedding_images_temp, args=(products[thread_num], )))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    except Exception as e:
        print('exact rembg multi thread error', e)


def exact_embedding_images_temp(products):

    for product in products:
        print(product.id)
        fail = 0
        for image in product.images.all():
            image_fail = True
            if image.embedding_vector_temp != [] or image.embedding_vector_temp is not None:
                continue
            for _ in range(2):
                try:
                    fail += 1
                    image.embedding_vector_temp = exact_embedding_from_link(
                        image.link)
                    image.save()
                    image_fail = False
                    fail -= 1
                    break
                except Exception as e:
                    print(
                        f'product {product.id} image {image.id} new exact error', e)
            # if image_fail:
            #     image.delete()
        if fail == 0:
            # product.rembg = True
            product.save()


def update_exact_image_multithread_rembg(products):
    session = new_session()
    try:
        products = np.array_split(products, THREAD_QUANTITY_CRAWL_PRODUCT)
        print('loading done', len(products))
        threads = []
        for thread_num in range(THREAD_QUANTITY_CRAWL_PRODUCT):
            threads.append(PropagatingThread(
                target=exact_embedding_images_rembg, args=(products[thread_num], session, )))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    except Exception as e:
        print('exact rembg multi thread error', e)


def exact_embedding_images_rembg(products, session):

    for product in products:
        print(product.id)
        fail = 0
        for image in product.images.all():
            image_fail = True

            for _ in range(2):
                try:
                    fail += 1
                    image.embedding_vector_temp = exact_embedding_from_link(
                        image.link)
                    image.embedding_vector = exact_embedding_from_link_rembg(
                        image.link, session)
                    image.save()
                    image_fail = False
                    fail -= 1
                    break
                except Exception as e:
                    print(
                        f'product {product.id} image {image.id} new exact error', e)
            if image_fail:
                image.delete()
        if fail == 0:
            product.rembg = True
            product.save()


def exact_embedding_from_link_rembg(link, session):
    try:
        response = requests.get(link, timeout=3)
        image = PIL.Image.open(BytesIO(response.content))
        image = image.resize(size=(200, 245))

        image_rmbg = remove(image, session=session)
        # Create a white rgb background
        new_image = PIL.Image.new("RGB", image_rmbg.size, "WHITE")
        new_image.paste(image_rmbg, mask=image_rmbg.split()[3])

        image_arr = np.asarray(new_image)/255.

        with tf.device('/device:CPU:0'):
            embedding_vector = TRAINNED_MODEL.predict(
                np.stack([image_arr]), verbose=0).tolist()
        gc.collect()
        tf.keras.backend.clear_session()
        return embedding_vector
    except Exception as e:
        gc.collect()
        tf.keras.backend.clear_session()
        # print('exacting image from link error', e)
        raise exceptions.ValidationError(
            f'exacting image rembg from link error {e}')
        return []


def get_not_crawl_products(product_list):
    ps = [product for product in product_list if product.crawled == False]
    return ps


# def exact_embedding_vector_product(product_list):
#     try:
#         print('loading model')
#         # model = load_models()
#         print('exacting embedding vector')
#         threads = []
#         for thread_num in range(0, (THREAD_QUANTITY_CRAWL_PRODUCT * 2)):
#             threads.append(PropagatingThread(
#                 target=exact_embedding_vector_thread, args=(product_list, thread_num,)))
#         for thread in threads:
#             thread.start()
#         for thread in threads:
#             thread.join()
#         # del model
#         # gc.collect()

#     except Exception as e:
#         print("shopee exact_embedding_vector error", e)
#         pass


# def exact_embedding_vector_thread(product_list, thread_num):
#     for i in range(len(product_list)):
#         if i % (THREAD_QUANTITY_CRAWL_PRODUCT * 2) == thread_num:
#             product = product_list[i]
#             for image in product.images.all():
#                 if image.embedding_vector == []:
#                     try:
#                         image.embedding_vector = exact_embedding_from_link(
#                             image.link)
#                         # print('image calculated')
#                         image.save()
#                     except:
#                         # print("image deleted")
#                         image.delete()


def find_categories(category_ids=['']):
    categories = []
    for id in category_ids:
        try:
            categories.append(Category.objects.filter(id=id)[0])
        except Exception as e:
            print(f"get category error {e}")
    return categories


def find_product(name='', category_ids=['']):
    categories = find_categories(category_ids)

    search = unidecode(name).lower()
    search_words = search.split()
    name_queries = Q()
    for word in search_words:
        name_queries &= Q(name__icontains=word)

    category_queries = Q()
    for category in categories:
        category_queries |= Q(category=category)

    products = Product.objects.filter(category_queries).filter(name_queries)

    print(len(products))
    max_len = min(600, len(products))

    return products[:max_len]


def get_product_from_category_ids(category_ids):
    categories = find_categories(category_ids)
    category_queries = Q()
    for category in categories:
        category_queries |= Q(category=category)
    products = Product.objects.filter(category_queries)
    return products


def exact_image_embedding_from_zip(file):
    session = new_session()
    file_path = f'temp/{binascii.hexlify(os.urandom(10)).decode("utf8")}_{file.name}'
    folder_path = file_path.split('.')[0]

    path = default_storage.save(file_path, ContentFile(file.read()))

    if not os.path.exists("temp/"):
        os.makedirs("temp")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    pyunpack.Archive(file_path).extractall(folder_path)

    base_dir = pathlib.Path(folder_path)
    image_paths = []
    anchor_images = []
    for path in base_dir.glob("*"):
        image_paths.append(str(path))
        image = PIL.Image.open(pathlib.Path(path))
        image = image.resize(size=(200, 245))
        image = remove(image, session=session)

        if np.asarray(image).shape[2] != 3:
            new_image = PIL.Image.new("RGB", image.size, "WHITE")
            new_image.paste(image, mask=image.split()[3])
            image = new_image

        image_arr = np.asarray(image)/255.

        with tf.device('/device:CPU:0'):
            embedding_vector = TRAINNED_MODEL.predict(
                np.stack([image_arr]), verbose=0)

        anchor_images.append({
            'image_path': str(path),
            'embedding_vector':  embedding_vector})
    return anchor_images


def get_need_update_product():
    result = {}

    products = Product.objects.filter(
        source_description__startswith="Shopee", crawled__in=[True])

    total_thread = 4
    threads = []

    products = np.array_split(products, total_thread)
    print(len(products))
    for thread_num in range(total_thread):
        temp_list = []
        result[f'{thread_num}'] = temp_list
        threads.append(PropagatingThread(
            target=get_need_update_product_thread, args=(products[thread_num], temp_list,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    all_result = []
    for key in result:
        print(key)
        all_result.extend(result[key])

    return all_result


def get_need_update_product_thread(products, temp_list):
    print(len(products))
    for product in products:
        # print(product.id, len(product.images.all()))
        if len(product.images.all()) == 0 or check_update_expire(product):
            # print(product.id, len(product.images.all()))
            temp_list.append(product)
    print(len(temp_list))
    return temp_list
