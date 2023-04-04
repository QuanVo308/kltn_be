

import time

def test(a, t):
    for i in range(20):
        print(t, i)
        time.sleep(0.5)

tasks = []
for i in range(10):
    test(i, i)


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

