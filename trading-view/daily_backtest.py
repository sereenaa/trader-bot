import pandas as pd
import numpy as np


from indicators import sma, rsi, ema, get_long_short_signal
from helper_functions import buy_sell_condition, sez_backtest
import helper_functions as hf
import datetime
import time

df = pd.read_csv('eth_1min.csv')    #'ethusd_investingdotcom.csv')
df.info()
df.rename(columns={'Start_time': 'Datetime'}, inplace=True)

print("apply indicators")
print("sma(df, 10, 50)\nrsi(df, 10)\nema(df, 'Close', 200)\nbuy_sell_condition(df)\nget_long_short_signal(df)")
sma(df, 10, 50)
rsi(df, 10)
ema(df, 'Close', 200)
buy_sell_condition(df)
get_long_short_signal(df)
sez_backtest(df[600001:700000], stop_loss_perc=0.0001, take_profit_perc=0.03, fee_pct=0.02*0.8/100)

# Put signal back to SQL table
# import sqlite3
# conn=sqlite3.connect("hhx_test.db")
# df.to_sql('eth_prepared',conn, if_exists='replace')
# conn.close()

print('### BEGIN BACKTEST ###')
df.info()
len(df)
df10=df[:100]

df.query("signal==-1").count()
df.query("short==1").count()

start_time=time.time()
df["Close"]*2
# df.query('Close<131.8').head(1)
# df.query('Close<131.8').tail(1)
print((time.time()-start_time)*10000)



df10.rolling(window=len(df10)).apply(lambda x:x[1==1].idxmin())



# t=df[-14400:]
# hf.backtest_long_short_trades(t)
# sez_backtest(t, stop_loss_perc=0.0001, take_profit_perc=0.03)

# ###### multithtask/asyncio ################
# print("Try multitask")
# import asyncio
# async def async_test(task_id, t, stop_loss_perc, take_profit_perc):
#     print(f"Task {task_id} started")
#     sez_backtest(t, stop_loss_perc=0.0001, take_profit_perc=0.03)
#     print(f"Task {task_id} completed")
# async def main():
#     # Create and gather tasks
#     tasks = [async_test(1, df[:100000],stop_loss_perc=0.0001, take_profit_perc=0.03), async_test(2, df[100001:200000],stop_loss_perc=0.0001, take_profit_perc=0.03)]
#     await asyncio.gather(*tasks)
# asyncio.run(main())

###### multithreading ################
# print("Try multithreading")
# import threading
# def threading_test(task_id, t, stop_loss_perc, take_profit_perc):
#     print(f"Task {task_id} started")
#     sez_backtest(t, stop_loss_perc=0.0001, take_profit_perc=0.03)
#     print(f"Task {task_id} completed")
# thread1 = threading.Thread(target=threading_test(1, df[:100000],stop_loss_perc=0.0001, take_profit_perc=0.03))
# thread2 = threading.Thread(target=threading_test(2, df[100001:200000],stop_loss_perc=0.0001, take_profit_perc=0.03))
# thread1.start()
# thread2.start()

# # Wait for both threads to finish
# thread1.join()
# thread2.join()
# print("Done")

########## multiprocessing ############
# print("Try multiprocessing")
# import multiprocessing
# if __name__ == '__main__':
#     # Utilise all CPUs
#     numbers = [i for i in range(1,multiprocessing.cpu_count()+1)]
#     # Create a multiprocessing pool with the number of available CPUs
#     pool = multiprocessing.Pool()

#     # Map the "square" function to the numbers using the multiprocessing pool
#     results = pool.map(sez_backtest(df[:100000],stop_loss_perc=0.0001, take_profit_perc=0.03), numbers)

#     # Close the pool to free up resources
#     pool.close()


import unittest
import concurrent.futures

# Define your test cases
class MyTestCase(unittest.TestCase):
    def test_case1(self):
        sez_backtest(df[:100000],stop_loss_perc=0.0001, take_profit_perc=0.03)

    def test_case2(self):
        sez_backtest(df[100001:200000],stop_loss_perc=0.0001, take_profit_perc=0.03)

    def test_case3(self):
        sez_backtest(df[200001:300000],stop_loss_perc=0.0001, take_profit_perc=0.03)

    def test_case4(self):
        sez_backtest(df[300001:400000],stop_loss_perc=0.0001, take_profit_perc=0.03)

    def test_case5(self):
        sez_backtest(df[500001:600000],stop_loss_perc=0.0001, take_profit_perc=0.03)

    def test_case6(self):
        sez_backtest(df[600001:700000],stop_loss_perc=0.0001, take_profit_perc=0.03)

# From 2020-05-18 20:21:00 to 2020-07-27 06:59:00, Returns: 6853.403651320905
# From 2020-01-01 00:00:00 to 2020-03-10 10:39:00, Returns: 14009.309681216591
# From 2020-07-27 07:01:00 to 2020-10-04 18:39:00, Returns: 22581.633793422832
# From 2020-03-10 10:41:00 to 2020-05-18 20:19:00, Returns: 17680.58063646557
# From 2021-02-20 16:01:00 to 2021-05-01 01:39:00, Returns: 209467.1081605477
# From 2020-12-13 05:21:00 to 2021-02-20 15:59:00, Returns: 192046.70263408808


if __name__ == '__main__':
    # Get all the test methods from the test case class
    test_methods = unittest.TestLoader().getTestCaseNames(MyTestCase)

    # Create a TestSuite with the test case and methods
    suite = unittest.TestSuite()
    for method_name in test_methods:
        suite.addTest(MyTestCase(method_name))

    # Define the function to execute a test case
    def run_test(test):
        result = unittest.TestResult()
        test.run(result)
        return result

    # Create a ThreadPoolExecutor with a maximum of 5 worker threads
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    # Submit the test execution tasks to the executor
    results = executor.map(run_test, suite)

    # Iterate over the results to get the outcome of each test case
    for test, result in zip(suite, results):
        print(f"Test: {test.id()} - Outcome: {result.wasSuccessful()}")

    # Cleanup the executor
    executor.shutdown()



# My own backtest function 
def sez_backtest(df, stop_loss_perc=0.01, take_profit_perc=0.03):
    df=df[60001:70000]
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

    # import sqlite3
    # conn=sqlite3.connect("hhx_test.db")
    # trades.to_sql('trades',conn, if_exists='replace')
    # conn.close()
    # print(trades)
    
    returns = sum(trades['Returns'])
    print(f'From {datetime.datetime.fromtimestamp(df["Datetime"].iloc[0]).strftime("%Y-%m-%d %H:%M:%S")} to {datetime.datetime.fromtimestamp(df["Datetime"].iloc[len(df)-1]).strftime("%Y-%m-%d %H:%M:%S")}, Returns: ' + str(returns))

    type(df["Datetime"].iloc[0])
    return trades

