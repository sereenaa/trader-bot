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
                sells.append(row.Close) # sell if we have held the position longer than 10 days
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



# From ChatGPT
"""
This function takes a DataFrame df of stock prices with a Close column, and performs a simple backtest for long and short trades. 
The function calculates a 10-day simple moving average of the stock price, and generates a trading signal of 1 (long) when the price is above the moving average, and -1 (short) when the price is below the moving average. 
The function then calculates the daily returns based on the trading signal, and calculates the cumulative returns and drawdowns.

The function also creates a DataFrame trades of the trades made based on the trading signal.
"""
def backtest_long_short_trades(df):
    """
    Given a DataFrame of stock prices with a 'Close' column,
    performs a simple backtest for long and short trades.
    Returns a DataFrame of the trades and a summary of the backtest.
    """
    # Calculate the 10-day simple moving average
    # df['SMA10'] = df['Close'].rolling(window=10).mean()

    # Create a column for the trading signal (1 for long, -1 for short)
    # df['signal'] = 0
    # df.loc[df['Close'] > df['SMA10'], 'signal'] = 1
    # df.loc[df['Close'] < df['SMA10'], 'signal'] = -1

    # Calculate the daily returns based on the trading signal
    df['Returns'] = df['signal'] * df['Close'].pct_change()

    # Calculate the cumulative returns and drawdowns
    df['Cumulative Returns'] = (1 + df['Returns']).cumprod()
    df['Cumulative Max'] = df['Cumulative Returns'].cummax()
    df['Drawdown'] = df['Cumulative Max'] - df['Cumulative Returns']
    df['Drawdown %'] = df['Drawdown'] / df['Cumulative Max']

    # Create a DataFrame of the trades
    trades = pd.DataFrame(columns=['Entry Date', 'Entry Price', 'Exit Date', 'Exit Price', 'Returns'])
    is_in_position = False
    for i, row in df.iterrows():
        if row['signal'] == 1 and not is_in_position:
            entry_date = i
            entry_price = row['Close']
            is_in_position = True
        elif row['signal'] == -1 and is_in_position:
            exit_date = i
            exit_price = row['Close']
            returns = (exit_price - entry_price) / entry_price
            trades.loc[len(trades)] = [entry_date, entry_price, exit_date, exit_price, returns]
            is_in_position = False

    # Calculate the summary statistics
    total_trades = len(trades)
    total_returns = trades['Returns'].sum()
    winning_trades = len(trades[trades['Returns'] > 0])
    losing_trades = len(trades[trades['Returns'] < 0])
    win_rate = winning_trades / total_trades
    lose_rate = losing_trades / total_trades
    average_return = total_returns / total_trades
    max_drawdown = df['Drawdown %'].max()

    # Print the summary statistics
    print(f"Total trades: {total_trades}")
    print(f"Total returns: {total_returns:.2%}")
    print(f"Win rate: {win_rate:.2%}")
    print(f"Lose rate: {lose_rate:.2%}")
    print(f"Average return per trade: {average_return:.2%}")
    print(f"Max drawdown: {max_drawdown:.2%}")

    print(df)

    return trades


# My own backtest function 
def sez_backtest(df, stop_loss_perc=0.02, take_profit_perc=0.04):
    # Create a DataFrame of the trades
    trades = pd.DataFrame(columns=['Entry Date', 'Entry Price', 'Exit Date', 'Exit Price', 'Long or Short', 'Returns'])

    # Start not in a position
    position = 0 

    # Initialize stop loss and take profit
    stop_loss = 0
    take_profit = 0

    # Loop through the data 
    for i, row in df.iterrows(): 
        
        # If we're not in a trade
        if position == 0:

            # Check if we should enter a long 
            if row['signal'] == 1:
                # print('Entered a long position')

                # Enter a long 
                position = 1
                entry_date = row['Datetime']
                entry_price = row['Close']

                # Update the stop loss to stop_loss_perc% below the entry price 
                stop_loss = row['Close'] * (1-stop_loss_perc)

                # Update the take profit to take_profit_perc% above the entry price 
                take_profit = row['Close'] * (1+take_profit_perc)

            # Check if we should enter a short 
            elif row['signal'] == -1:
                # print('Entered a short position')

                # Enter a short 
                position = -1
                entry_date = row['Datetime']
                entry_price = row['Close']

                # Update the stop loss to stop_loss_perc% above the entry price 
                stop_loss = row['Close'] * (1+stop_loss_perc)

                # Update the take profit to take_profit_perc% below the entry price 
                take_profit = row['Close'] * (1-take_profit_perc)

            # Otherwise do nothing 
            else: 
                continue

        # If we're in a long position
        elif position == 1:

            # If stop loss has been hit 
            if df['Close'][i] <= stop_loss:

                # Close the trade 
                position = 0
                exit_date = row['Datetime']
                exit_price = row['Close']
                returns = (exit_price - entry_price) / entry_price
                long_or_short = 'long'
                trades.loc[len(trades)] = [entry_date, entry_price, exit_date, exit_price, long_or_short, returns]

            # If take profit has been hit 
            elif df['Close'][i] >= take_profit:

                # Close the trade 
                position = 0
                exit_date = row['Datetime']
                exit_price = row['Close']
                returns = (exit_price - entry_price) / entry_price
                long_or_short = 'long'
                trades.loc[len(trades)] = [entry_date, entry_price, exit_date, exit_price, long_or_short, returns]

            # If the price is 1/2 of the take profit, update the stop loss to break even 
            elif df['Close'][i] == (take_profit/2):
                stop_loss = df['Close'][i] 


        # If we're in a short position
        elif position == -1:
            # If stop loss has been hit 
            if df['Close'][i] >= stop_loss:
                # print('Stop loss target has been hit')

                # Close the trade 
                position = 0
                exit_date = row['Datetime']
                exit_price = row['Close']
                returns = (entry_price - exit_price) / entry_price
                long_or_short = 'short'
                trades.loc[len(trades)] = [entry_date, entry_price, exit_date, exit_price, long_or_short, returns]

            # If take profit has been hit 
            elif df['Close'][i] <= take_profit:
                # print('Take profit target has been hit')

                # Close the trade 
                position = 0
                exit_date = row['Datetime']
                exit_price = row['Close']
                returns = (entry_price - exit_price) / entry_price
                long_or_short = 'short'
                trades.loc[len(trades)] = [entry_date, entry_price, exit_date, exit_price, long_or_short, returns]
                
            # If the price is 1/2 of the take profit, update the stop loss to break even 
            elif df['Close'][i] == (take_profit/2):
                stop_loss = df['Close'][i] 

    print(trades)


    returns = sum(trades['Returns'])
    print('Returns: ' + str(returns))

    return trades