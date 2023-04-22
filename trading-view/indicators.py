import pandas as pd 
import numpy as np
import ta

# Moving Average
# n is short term window eg. 50
# m is long term window eg. 100
# Appends the short term moving average and long term moving average to the dataframe
def sma(df, n, m): 
    df['sma_1'] = df.Close.rolling(n).mean()
    df['sma_2'] = df.Close.rolling(m).mean()


# RSI 
def rsi(df, n): 
    df['rsi_{}'.format(n)] = ta.momentum.rsi(df.Close, window=n)


# Exponential Moving Average
# Appends the chosen EMA to the dataframe
# https://www.youtube.com/watch?v=VhOAHQKb4mM&list=PLFZ0Tjtnb1cE7rgFyf7cBojjRXz9oSdKt&index=10&t=368s
def ema(df, column_name, length): 
    # src is the column of the pandas dataframe you want to calculate EMA on
    # it is converted to a numpy array
    src = df[column_name].to_numpy()

    ind = np.empty(shape=src.shape, dtype=float)
    alpha = 2 / (length + 1)

    for i in range(len(src)): 
        if i==0 or np.isnan(src[i]) or (i>0 and np.isnan(ind[i-1])): 
            ind[i] = src[i]
            continue

        ind[i] = (alpha * src[i]) + (1 - alpha) * ind[i-1]

    ind[:length - 1] = np.nan

    df['ema_{}'.format(length)] = ind

    return ind


# Generate the long/short signal
def get_long_short_signal(df): 
    # 0 = not in position, 1 = long, -1 = short

    df.loc[df['Close'] > df['sma_1'], 'signal'] = 1
    df.loc[df['Close'] < df['sma_1'], 'signal'] = -1

