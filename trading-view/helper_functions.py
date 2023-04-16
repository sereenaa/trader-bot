
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

    # formula for the returns
    # gain = (pd.Series(profits) + 1).prod()

    gain = sum(profits)
    print("Strategy gain: " + str(gain))
    return gain 

def hodl_gain(df=None, start_date=None):
    start_price = df.loc[df['Datetime'] == start_date, 'Close'].values[0]
    end_price = df.iloc[-1]['Close']
    gain = (end_price-start_price)/start_price
    print("HODL gain: " + str(gain))
    return gain

