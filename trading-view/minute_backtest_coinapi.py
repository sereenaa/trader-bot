# The API request is limited. It worked, but I could only get a few rows of data 

import requests
import json
import os

# api_endpoint = "https://rest.coinapi.io/v1/ohlcv/BINANCE_SPOT_ETH_USD/history"
os.environ["XCOINAPIKEY"] = ''
api_key = os.getenv('XCOINAPIKEY')
# headers = {"X-CoinAPI-Key": api_key}

# query_params = {
#     "period_id": "1MIN",
#     "time_start": "2022-04-23T00:00:00",
#     "time_end": "2023-04-23T00:00:00",
#     "limit": 100000,
#     "symbol_id": "BINANCE_SPOT_ETH_USD"
# }

# response = requests.get(api_endpoint, headers=headers, params=query_params)
# data = response.json()

# print(data)


url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_ETH_USD/history?period_id=1MIN&time_start=2020-01-01T00:00:00'
headers = {'X-CoinAPI-Key' : api_key}
response = requests.get(url, headers=headers)

my_json = response._content.decode('utf8').replace("'", '"')
data = json.loads(my_json)
s = json.dumps(data, indent=4, sort_keys=True)



with open("data_coinapi.json", "w") as json_file:
    # Write the JSON data to the file
    json.dump(s, json_file)

# import pandas as pd

# df = pd.DataFrame(data)
# df["time_period_start"] = pd.to_datetime(df["time_period_start"])
# df.set_index("time_period_start", inplace=True)


# print(df)