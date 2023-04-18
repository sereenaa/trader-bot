
import yfinance as yf
import pandas as pd 
from datetime import timedelta
from sqlalchemy import create_engine #pip install sqlalchemy==1.4.16

from indicators import ma, rsi, ema
from helper_functions import backtest, hodl_gain, buy_sell_condition, backtest_v2, backtest_v3

# create sqlite engine
engine = create_engine('sqlite:///sez_test.db')

# download ETH data from Yahoo Finance
# Only 7 days worth of 1m granularity data are allowed to be fetched per request.
df = yf.download('ETH-USD', start=pd.to_datetime('today') - timedelta(7), interval='1m')
# df.to_sql('ETHUSD_1m', engine)
# print(df)

# read from existing database
result = pd.read_sql('SELECT * FROM ETHUSD_1m', engine)
print(result)

# get the max datetime from existing database
max_date = pd.read_sql('SELECT MAX(Datetime) FROM ETHUSD_1m', engine).values[0][0]
print(max_date)

# append new rows to existing database
new_rows = df[df.index > max_date]
new_rows.to_sql('ETHUSD_1m', engine, if_exists='append')


# read from database again
new_result = pd.read_sql('SELECT * FROM ETHUSD_1m', engine)

# apply indicators
ma(new_result, 50, 100)
rsi(new_result, 10)
ema(new_result, 'Open', 200)
buy_sell_condition(new_result)
print(new_result)


# Test the strategies

gain = backtest(new_result)


hodl_gain = hodl_gain(new_result, '2023-04-04 22:34:00.000000')


pnl = backtest_v2(new_result)
print(pnl)


backtest_v3(new_result)