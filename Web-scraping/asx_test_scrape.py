import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

URL = 'https://au.finance.yahoo.com/quote/%5EAXJO/history?p=%5EAXJO'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')


date = []
open = []
high = []
low = []
close = []
adj_close = []
volume = [] 

for row in soup.find_all('tr'):
    i=0
    for item in row: 
        if i==0:
            date.append(item.text)
        if i==1: 
            open.append(item.text)
        if i==2: 
            high.append(item.text)
        if i==3: 
            low.append(item.text)
        if i==4: 
            close.append(item.text)
        if i==5: 
            adj_close.append(item.text)
        if i==6: 
            volume.append(item.text)
        i+=1

df = pd.DataFrame(list(zip(date, open, high, low, close, adj_close, volume)))