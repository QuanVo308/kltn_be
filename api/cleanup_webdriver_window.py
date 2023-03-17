
import pathlib
import shutil


base_dir = pathlib.Path("C:\Program Files (x86)")
count = 0

for path in base_dir.glob("scoped_dir*"):
    count+=1
    print(count ,str(path))
    shutil.rmtree(str(path))
print(count)