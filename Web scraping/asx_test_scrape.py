import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

URL = 'https://au.finance.yahoo.com/quote/%5EAXJO/history?p=%5EAXJO'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')


# for row in soup.find_all('tr', class_ = 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'): 
#     for column in soup.find_all('td', class_ = 'Py(10px)'): 
#         text = column.text
#         print(text)

date = []
open = []
high = []
low_close = []
adj_close = []
volume = [] 


for row in soup.find_all('td', class_ = 'Py(10px)'): 
    text = row.text
    print(row)
