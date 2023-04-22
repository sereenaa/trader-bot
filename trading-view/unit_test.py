import pandas as pd

from indicators import sma, rsi, ema, get_long_short_signal
from helper_functions import buy_sell_condition, sez_backtest

data = {'Datetime': ['2023-04-04 22:34:00.000000', '2023-04-04 22:35:00.000000', '2023-04-04 22:36:00.000000', '2023-04-04 22:37:00.000000', '2023-04-04 22:38:00.000000'],
        'Open': [1800, 1810, 1790, 1820, 1800],
        'High': [1805, 1815, 1800, 1825, 1810],
        'Low': [1795, 1805, 1785, 1815, 1800], 
        'Close': [1800, 1810, 1790, 1820, 1800], 
        'signal': [0, -1, 0, 0, 0]
}

df = pd.DataFrame(data)

sma(df, 10, 50)
rsi(df, 10)
ema(df, 'Open', 200)
buy_sell_condition(df)
# get_long_short_signal(df)

print(df)

sez_backtest(df)