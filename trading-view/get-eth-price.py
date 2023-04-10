
import yfinance as yf
import pandas as pd 
from datetime import timedelta
from sqlalchemy import create_engine #pip install sqlalchemy==1.4.16

# create sqlite engine
engine = create_engine('sqlite:///sez_test.db')

# download ETH data from Yahoo Finance
df = yf.download('ETH-USD', start=pd.to_datetime('today') - timedelta(7), interval='1m')
# df.to_sql('ETHUSD_1m', engine)
# print(df)

# read from existing database
result = pd.read_sql('SELECT * FROM ETHUSD_1m', engine)
# print(result)

# get the max datetime from existing database
max_date = pd.read_sql('SELECT MAX(Datetime) FROM ETHUSD_1m', engine).values[0][0]
# print(max_date)

# append new rows to existing database
new_rows = df[df.index > max_date]
new_rows.to_sql('ETHUSD_1m', engine, if_exists='append')


