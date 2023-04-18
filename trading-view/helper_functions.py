import pandas as pd

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


# Add columns that have a buy or sell flag
def buy_sell_condition(df):
    df['buy'] = (df.Close > df.sma_1) & (df.rsi_10 < 30)
    df['sell'] = df.rsi_10 > 40


# Strategy from ChatGPT
def backtest_v2(data):
    # Initialize PnL list
    pnl = []

    # Initialize variables for tracking trades
    position = 0  # 0 = flat, 1 = long, -1 = short
    stop_loss = 0  # Initial stop loss level
    take_profit = 0  # Initial take profit level

    # Loop over the historical data, starting from the second row
    for i in range(1, len(data)):
        # Check if we're already in a trade
        if position != 0:
            # Check if the stop loss level has been hit
            if position == 1 and data['Low'][i] < stop_loss:
                # Close the long position and update the stop loss and take profit levels
                position = 0
                stop_loss = 0
                take_profit = 0
                # Store the results
                close_price = data['Low'][i]
                pnl.append((close_price - open_price) / open_price)
            elif position == -1 and data['High'][i] > stop_loss:
                # Close the short position and update the stop loss and take profit levels
                position = 0
                stop_loss = 0
                take_profit = 0
                # Store the results
                close_price = data['Low'][i]
                pnl.append((open_price - close_price) / open_price)
            else:
                # Update the stop loss and take profit levels
                if position == 1:
                    stop_loss = max(stop_loss, data['Close'][i] * 0.95)  # 5% stop loss
                    take_profit = max(take_profit, data['Close'][i] * 1.05)  # 5% take profit
                elif position == -1:
                    stop_loss = min(stop_loss, data['Close'][i] * 1.05)  # 5% stop loss
                    take_profit = min(take_profit, data['Close'][i] * 0.95)  # 5% take profit

        # Check if we should enter a new trade
        if data['rsi_10'][i] < 30 and data['Close'][i] < data['ema_200'][i]:
            # Enter a long position with a stop loss at 2% below the entry price and a take profit at 2% above the entry price
            position = 1
            stop_loss = data['Close'][i] * 0.98
            take_profit = data['Close'][i] * 1.02
            # Store the open price
            open_price = data['Close'][i]
        elif data['rsi_10'][i] > 70 and data['Close'][i] > data['ema_200'][i]:
            # Enter a short position with a stop loss at 2% above the entry price and a take profit at 2% below the entry price
            position = -1
            stop_loss = data['Close'][i] * 1.02
            take_profit = data['Close'][i] * 0.98
            # Store the open price
            open_price = data['Close'][i]

    # Return the final position and the historical data
    return pnl



# From YouTube 
# https://www.youtube.com/watch?v=5KKildyGBeo&list=PLFZ0Tjtnb1cE7rgFyf7cBojjRXz9oSdKt&index=14
def backtest_v3(df):
    in_position = False 
    buys, sells = [], []

    for index, row in df.iterrows():
        if not in_position:
            if row.buy: 
                buys.append(row.Close)
                in_position = True 
                r_count = 0 # counter for the number of days that has passed
        if in_position:
            r_count += 1 # increase the counter for each day that has passed while we are in a position
            if row.sell: 
                sells.append(row.Close)
                in_position = False
                print('Sold because of indicator')
            elif r_count >= 10: 
                sells.append(row.price) # sell if we have held the position longer than 10 days
                in_position = False
                print('Sold after 10 days')

    trades = pd.DataFrame([buys, sells], index=['Buys', 'Sells'])
    trades = trades.T 
    trades['PnL'] = trades.Sells - trades.Buys
    trades['PnL%'] = (trades.Sells - trades.Buys)/trades.Buys
    print(trades)

    gain = sum(trades['PnL%'])
    print(gain)

    return gain