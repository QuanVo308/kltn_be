import numpy as np
# import matplotlib.pyplot as plt
# import tensorflow as tf
from tensorflow import keras
from pymongo import MongoClient
# from sklearn.model_selection import train_test_split
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.preprocessing import normalize
import PIL
# from matplotlib import image as mpimg
# import matplotlib as mpl
# import tensorflow_datasets as tfds
import pathlib
# import os
# import math
# import random
# import gc

# trained_model = keras.models.load_model('D:\QuanVo\KLTN\models\output_kaggle tllds 245x200 out128 float ac66/checkpoint')

def get_db_handle(db_name, host, port, username, password):

 client = MongoClient(host=host,
                      port=int(port),
                      username=username,
                      password=password
                     )
 db_handle = client['db_name']
 return db_handle, client