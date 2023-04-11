import pandas as pd 


# n is short term window eg. 50
# m is long term window eg. 100
def ma_calc(df, n, m): 
    df['sma_1'] = df.Close.rolling(n).mean()
    df['sma_2'] = df.Close.rolling(m).mean()


# simple backtest function using sma_1 and sma_2
# this assumes the df already has the sma columns
def backtest(df): 
    in_position = False
    profits = []

    for index, row in df.iterrows(): 
        if not in_position:
            if row.sma_1 > row.sma_2:
                buyprice = row.Close
                in_position = True
        if in_position: 
            if row.sma_1 < row.sma_2: 
                profit = (row.Close - buyprice)/buyprice # this is in percentage decimals
                profits.append(profit)
                in_position=False
    
    print(profits)

    # formula for the returns
    # gain = (pd.Series(profits) + 1).prod()

    gain = sum(profits)
    return gain 



# # https://tvdb.brianthe.dev/ 
# import tradingview_ta as ta # pip install tradingview-ta

# # Define the parameters for the MACD indicator
# symbol = "AAPL"    # The symbol for the stock you want to get data for
# interval = "1m"    # The time interval for the data (1 minute in this case)
# fast_period = 12   # The fast period for the MACD indicator
# slow_period = 26   # The slow period for the MACD indicator
# signal_period = 9  # The signal period for the MACD indicator

# # Fetch the MACD data using the TradingView API
# macd_data = ta.macd(symbol=symbol, interval=interval, fast_period=fast_period, slow_period=slow_period, signal_period=signal_period)

# # Print the MACD data
# print(macd_data)


# {'Recommend.Other': 0, 'Recommend.All': 0.26666667, 'Recommend.MA': 0.53333333, 'RSI': 60.28037412, 'RSI[1]': 58.58364778, 'Stoch.K': 73.80404453, 'Stoch.D': 79.64297643, 'Stoch.K[1]': 78.88160227, 'Stoch.D[1]': 85.97647064, 'CCI20': 46.58442886, 'CCI20[1]': 34.57058796, 'ADX': 35.78754863, 'ADX+DI': 23.16948389, 'ADX-DI': 13.82449817, 'ADX+DI[1]': 24.15991909, 'ADX-DI[1]': 13.87125505, 'AO': 6675.72158824, 'AO[1]': 7283.92420588, 'Mom': 1532.6, 'Mom[1]': 108.29, 'MACD.macd': 2444.73734978, 'MACD.signal': 2606.00138275, 'Rec.Stoch.RSI': 0, 'Stoch.RSI.K': 18.53740187, 'Rec.WR': 0, 'W.R': -26.05634845, 'Rec.BBPower': 0, 'BBPower': 295.52055898, 'Rec.UO': 0, 'UO': 55.68311917, 'close': 45326.97, 'EMA5': 45600.06414333, 'SMA5': 45995.592, 'EMA10': 45223.22433151, 'SMA10': 45952.635, 'EMA20': 43451.52018338, 'SMA20': 43609.214, 'EMA30': 41908.5944052, 'SMA30': 40880.391, 'EMA50': 40352.10222373, 'SMA50': 37819.3566, 'EMA100': 40356.09177879, 'SMA100': 38009.7808, 'EMA200': 39466.50411569, 'SMA200': 45551.36135, 'Rec.Ichimoku': 0, 'Ichimoku.BLine': 40772.57, 'Rec.VWMA': 1, 'VWMA': 43471.81729377, 'Rec.HullMA9': -1, 'HullMA9': 45470.37107407, 'Pivot.M.Classic.S3': 11389.27666667, 'Pivot.M.Classic.S2': 24559.27666667, 'Pivot.M.Classic.S1': 33010.55333333, 'Pivot.M.Classic.Middle': 37729.27666667, 'Pivot.M.Classic.R1': 46180.55333333, 'Pivot.M.Classic.R2': 50899.27666667, 'Pivot.M.Classic.R3': 64069.27666667, 'Pivot.M.Fibonacci.S3': 24559.27666667, 'Pivot.M.Fibonacci.S2': 29590.21666667, 'Pivot.M.Fibonacci.S1': 32698.33666667, 'Pivot.M.Fibonacci.Middle': 37729.27666667, 'Pivot.M.Fibonacci.R1': 42760.21666667, 'Pivot.M.Fibonacci.R2': 45868.33666667, 'Pivot.M.Fibonacci.R3': 50899.27666667, 'Pivot.M.Camarilla.S3': 37840.08, 'Pivot.M.Camarilla.S2': 39047.33, 'Pivot.M.Camarilla.S1': 40254.58, 'Pivot.M.Camarilla.Middle': 37729.27666667, 'Pivot.M.Camarilla.R1': 42669.08, 'Pivot.M.Camarilla.R2': 43876.33, 'Pivot.M.Camarilla.R3': 45083.58, 'Pivot.M.Woodie.S3': 21706.84, 'Pivot.M.Woodie.S2': 25492.42, 'Pivot.M.Woodie.S1': 34876.84, 'Pivot.M.Woodie.Middle': 38662.42, 'Pivot.M.Woodie.R1': 48046.84, 'Pivot.M.Woodie.R2': 51832.42, 'Pivot.M.Woodie.R3': 61216.84, 'Pivot.M.Demark.S1': 35369.915, 'Pivot.M.Demark.Middle': 38908.9575, 'Pivot.M.Demark.R1': 48539.915, 'open': 44695.95, 'P.SAR': 48068.64, 'BB.lower': 37961.23510877, 'BB.upper': 49257.19289123, 'AO[2]': 7524.31223529, 'volume': 32744.424503, 'change': 1.44612354, 'low': 44203.28, 'high': 45560}




# from tradingview_ta import TA_Handler, Interval, Exchange
# tesla = TA_Handler(
#     symbol="TSLA",
#     screener="america",
#     exchange="NASDAQ",
#     interval=Interval.INTERVAL_1_DAY
#     #proxies={'http': 'http://0.0.0.0:8080', 'https': 'https://0.0.0.0:443'}
# )
# print(tesla.get_analysis().summary)


# eth = TA_Handler(
#     symbol="ETHUSDT",
#     screener="Crypto",
#     exchange="BINANCE",
#     interval=Interval.INTERVAL_1_MINUTE
#     #proxies={'http': 'http://0.0.0.0:8080', 'https': 'https://0.0.0.0:443'}
# )

# print(eth.get_analysis().summary)
# print(eth.get_analysis().indicators)


