from urllib.parse import urlsplit
from urllib.request import urlretrieve

url = 'https://yuklio.com/f/RbQz6-img015.jpg'

split = urlsplit(url)

filename = "/tmp/" + split.path.split("/")[-1]

urlretrieve(url, filename)

print(url, filename)
