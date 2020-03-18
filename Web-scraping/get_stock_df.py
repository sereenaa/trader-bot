import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# USAGE: df = getStockHistory('ANZ.AX').get_df() 

class StockHistory: 
    df_link = 'https://au.finance.yahoo.com/quote/{ticker}/history?p={ticker}' 
    
    def __init__(self, symbol):
        self.symbol = symbol
    
    def get_df(self):
        URL = self.df_link.format(ticker=self.symbol)
        print(URL)
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
        return(df)
