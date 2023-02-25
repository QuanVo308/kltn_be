import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
# from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import PIL
from matplotlib import image as mpimg
import matplotlib as mpl
import tensorflow_datasets as tfds
import pathlib
import os
import math
import random
import gc

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

print('importing model')
m = keras.models.load_model('D:\QuanVo\KLTN\models\output_kaggle tllds 245x200 out128 float ac66/checkpoint')

print('get image')
po = 1121
ne = 3333

# img = PIL.Image.open(list(pathlib.Path("D:/Downloads/totally_looks_like_ds/left/left/").glob(f'{po:05d}.jpg'))[0])
# img_p = PIL.Image.open(list(pathlib.Path("D:/Downloads/totally_looks_like_ds/right/right/").glob(f'{po:05d}.jpg'))[0])
# img_n = PIL.Image.open(list(pathlib.Path("D:/Downloads/totally_looks_like_ds/left/left/").glob(f'{ne:05d}.jpg'))[0])

img = PIL.Image.open(pathlib.Path("D:\Picture\ThaoNguyenHoa\IMG_2211.JPG"))
img_p = PIL.Image.open(pathlib.Path("D:\Picture\ThaoNguyenHoa\IMG_2214.JPG"))
img_n = PIL.Image.open(pathlib.Path("D:\Picture\ThaoNguyenHoa\IMG_2219.JPG"))

img = img.resize(size = (200,245))
img_p = img_p.resize(size = (200,245))
img_n = img_n.resize(size = (200,245))

# plt.imshow(img)
# print(img)

img_arr = np.asarray(img)/255.
img_p_arr = np.asarray(img_p)/255.
img_n_arr = np.asarray(img_n)/255.

print('predicting')
anchor = m.predict(np.stack([img_arr]), verbose=0)
positive = m.predict(np.stack([img_p_arr]), verbose=0)
negative = m.predict(np.stack([img_n_arr]), verbose=0)
print(anchor.shape)
print(positive.shape)
print(negative.shape)

ap_distance = tf.math.reduce_euclidean_norm(anchor - positive, axis=1)
an_distance = tf.math.reduce_euclidean_norm(anchor - negative, axis=1)

if ap_distance < an_distance:
    result = "PASS"
    # p+=1
else:
    result = "FAIL"

anchor_norm = normalize(anchor, axis=1)
positive_norm = normalize(positive, axis=1)
negative_norm = normalize(negative, axis=1)

ap_cosine_distance = cosine_similarity(anchor_norm , positive_norm)
an_cosine_distance = cosine_similarity(anchor_norm , negative_norm)

if ap_cosine_distance > an_cosine_distance:
    result_c = "PASS"
    # p_c+=1
else:
    result_c = "FAIL"

print(f"pos:{po} neg:{ne}")
print(f"{result}  ap_distance:{ap_distance.numpy()} an_distance:{an_distance.numpy()}")
print(f"{result_c}  ap_cosine_distance:{ap_cosine_distance} an_cosine_distance:{an_cosine_distance}")
# print(f"{p/i*100:.3f}% {p}/{i}")
# print(f"{p_c/i*100:.3f}% {p_c}/{i} cosine")
print("\n")


# print('test dataset')
# i = 0.0
# p = 0
# p_c = 0
# while True:
#     i+=1
#     po = random.randint(0, 6016)
#     ne = random.randint(0, 6016)
#     img = PIL.Image.open(list(pathlib.Path("D:/Downloads/totally_looks_like_ds/left/left/").glob(f'{po:05d}.jpg'))[0])
#     img_p = PIL.Image.open(list(pathlib.Path("D:/Downloads/totally_looks_like_ds/right/right/").glob(f'{po:05d}.jpg'))[0])
#     img_n = PIL.Image.open(list(pathlib.Path("D:/Downloads/totally_looks_like_ds/left/left/").glob(f'{ne:05d}.jpg'))[0])
#     # img = img_norm(img)
#     img = img.resize(size = (200,245))
#     img_p = img_p.resize(size = (200,245))
#     img_n = img_n.resize(size = (200,245))
    
#     img_arr = np.asarray(img)/255.
#     img_p_arr = np.asarray(img_p)/255.
#     img_n_arr = np.asarray(img_n)/255.
    
#     anchor = m.predict(np.stack([img_arr]), verbose=0)
#     positive = m.predict(np.stack([img_p_arr]), verbose=0)
#     negative = m.predict(np.stack([img_n_arr]), verbose=0)
    
#     ap_distance = tf.math.reduce_euclidean_norm(anchor - positive, axis=1)
#     an_distance = tf.math.reduce_euclidean_norm(anchor - negative, axis=1)
    
#     if ap_distance < an_distance:
#         result = "PASS"
#         p+=1
#     else:
#         result = "FAIL"
    
#     anchor_norm = normalize(anchor, axis=1)
#     positive_norm = normalize(positive, axis=1)
#     negative_norm = normalize(negative, axis=1)
    
#     ap_cosine_distance = cosine_similarity(anchor_norm , positive_norm)
#     an_cosine_distance = cosine_similarity(anchor_norm , negative_norm)
    
#     if ap_cosine_distance > an_cosine_distance:
#         result_c = "PASS"
#         p_c+=1
#     else:
#         result_c = "FAIL"
    
#     print(f"pos:{po} neg:{ne}")
#     print(f"{result}  ap_distance:{ap_distance.numpy()} an_distance:{an_distance.numpy()}")
#     print(f"{result_c}  ap_cosine_distance:{ap_cosine_distance} an_cosine_distance:{an_cosine_distance}")
#     print(f"{p/i*100:.3f}% {p}/{i}")
#     print(f"{p_c/i*100:.3f}% {p_c}/{i} cosine")
    # print("\n")

print('check')
