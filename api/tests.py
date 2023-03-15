
from unidecode import unidecode
from urllib.parse import unquote

text = 'https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567'

a = {'a':0, 'b':1}
b = {'a':2, 'b':6}
c = {'a':3, 'b':7}
d = {'a':4, 'b':8}
l = [a,b,c,d]

print(l)

i = [i for i in l if i['a'] == 3]
print(i)
