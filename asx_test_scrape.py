import requests

URL = 'https://au.finance.yahoo.com/quote/%5EAXJO/history?p=%5EAXJO'
page = requests.get(URL)