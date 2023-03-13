
from unidecode import unidecode
from urllib.parse import unquote

text = 'https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567'

print(unquote(text))