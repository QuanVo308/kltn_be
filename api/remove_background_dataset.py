import cv2
import numpy as np
from rembg import remove, new_session
import time
import PIL
import pathlib
from multiprocessing.pool import ThreadPool

base_dir = pathlib.Path("D:/Downloads/totally_looks_like_ds")
left = base_dir / "left/left"
right = base_dir / "right/right"

rbase_dir = pathlib.Path("D:/Downloads/totally_looks_like_ds2")
rleft = rbase_dir / "left/left"
rright = rbase_dir / "right/right"

def remove_background_thread(paths):
    session = new_session()
    quantity = len(paths)
    count = 0
    for path in paths:
        count+=1
        print(f'{count}/{quantity}')
        img = PIL.Image.open(path)
        output = remove(img, session=session)
        new_image = PIL.Image.new("RGB", output.size, "WHITE") 
        new_image.paste(output, mask = output.split()[3]) 
        if 'left' in str(path).split('\\'):
            new_image.save(rleft / path.name)
        else:
            new_image.save(rright / path.name)



count = 0
paths = []
paths.extend(list(left.glob("*")))
paths.extend(list(right.glob("*")))

print(len(paths))
thread_num = 2
with ThreadPool(processes=thread_num) as pool:
    results = pool.imap_unordered(remove_background_thread, np.array_split(paths, thread_num))
    for result in results:
        pass

# np.array_split(lst, 5)
