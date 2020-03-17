import requests
from bs4 import BeautifulSoup

URL = 'https://au.finance.yahoo.com/quote/%5EAXJO/history?p=%5EAXJO'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
