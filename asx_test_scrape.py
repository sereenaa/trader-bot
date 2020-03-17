import requests
from bs4 import BeautifulSoup

URL = 'https://au.finance.yahoo.com/quote/%5EAXJO/history?p=%5EAXJO'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

for row in soup.find_all('td', class_ = 'Py(10px)'): 
    text = row.text
    print(text)


