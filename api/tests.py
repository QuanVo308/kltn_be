
# from threading import Thread
# class PropagatingThread(Thread):
#     def run(self):
#         self.exc = None
#         try:
#             if hasattr(self, '_Thread__target'):
#                 # Thread uses name mangling prior to Python 3.
#                 self.ret = self._Thread__target(
#                     *self._Thread__args, **self._Thread__kwargs)
#             else:
#                 self.ret = self._target(*self._args, **self._kwargs)
#         except BaseException as e:
#             self.exc = e

# def test(num, list_num):
#     # print(num)
#     for i in range(num):
#         list_num.append({'test':i})

# all_list = {}

# threads = []
# for i in range(4):
#     temp_list = []
#     all_list[f'{i}'] = temp_list
#     threads.append(PropagatingThread(
#                     target=test, args=(i, temp_list,)))

# for thread in threads:
#     thread.start()
# for thread in threads:
#     thread.join()

# all_l = []
# for key in all_list:
#     print(key)
#     all_l.extend(all_list[key])

# all_l = sorted(all_l, key=lambda d: d['test'], reverse=True)
# print(all_list)
# print(all_l)
"""test2"""
# import cv2
# import numpy as np
# from rembg import remove
# import time
# import PIL


# # img = cv2.imread("D:\Downloads\custom_test_dataset\\0201.jfif")
# img = PIL.Image.open("D:\Downloads\custom_test_dataset\\0111.JPG")
# print(np.asarray(img).shape)
# print(type(img))

# output = remove(img)
# print(np.asarray(output).shape)
# output.save('person_transp_bckgrnd.png')

# new_image = PIL.Image.new("RGB", output.size, "WHITE") 
# new_image.paste(output, mask = output.split()[3])              
# # new_image.convert('RGB') 

# # background = PIL.Image.new("RGB", new_image.size, (255, 255, 255))
# # background.paste(new_image, mask = new_image.split()[3])
# # background.save("sample_2.jpg", "JPEG", quality=100)

# print(np.asarray(new_image).shape)
# # print(np.asarray(background).shape)
# new_image.save('person_transp_bckgrnd.png')


# cv2.imwrite('person_transp_bckgrnd.png', output)

# time.sleep(10)

"""test3"""
# from multiprocessing.pool import ThreadPool
# from time import sleep

# def task(num = 1, num2 = 2):
#     # report a message
#     print(f'Task executing {num}')
#     # block for a moment
#     # sleep(1)
#     # report a message
#     print(f'Task done {num}')

# inputs = [(i, i+1) for i in range(1000)]
# # print(inputs)
# pool = ThreadPool(processes=20)
# # issue tasks to the thread pool
# results = pool.imap_unordered(task, inputs)

# for result in results:
#     print('print result', result)
# # close the thread pool
# pool.close()

import numpy as np

lst = range(21)
np.array_split(lst, 5)
print(type(np.array_split(lst, 5)))