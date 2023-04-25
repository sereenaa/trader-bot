import pandas as pd
import numpy as np


from indicators import sma, rsi, ema, get_long_short_signal
from helper_functions import buy_sell_condition, sez_backtest

df = pd.read_csv('ethusd_investingdotcom.csv')
df.rename(columns={'Date': 'Datetime', 'Price': 'Close'}, inplace=True)
df['Close']=df['Close'].str.replace(',','')
df['Close']=df['Close'].astype('float')

# apply indicators
sma(df, 10, 50)
rsi(df, 10)
ema(df, 'Close', 200)
buy_sell_condition(df)
get_long_short_signal(df)

print('### NEW RESULTS ###')
print(df)

print('### BEGIN BACKTEST ###')
sez_backtest(df, stop_loss_perc=0.0001, take_profit_perc=0.03)
