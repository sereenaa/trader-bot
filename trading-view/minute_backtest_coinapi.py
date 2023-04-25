import requests
import json
import os

api_endpoint = "https://rest.coinapi.io/v1/ohlcv/BINANCE_SPOT_ETH_USD/history"
api_key = os.getenv('XCOINAPIKEY')
headers = {"X-CoinAPI-Key": api_key}

query_params = {
    "period_id": "1MIN",
    "time_start": "2022-04-23T00:00:00",
    "time_end": "2023-04-23T00:00:00",
    "limit": 100000,
    "symbol_id": "BINANCE_SPOT_ETH_USD"
}

response = requests.get(api_endpoint, headers=headers, params=query_params)
data = response.json()

print(data)

with open("data_coinapi.json", "w") as json_file:
    # Write the JSON data to the file
    json.dump(data, json_file)

# import pandas as pd

# df = pd.DataFrame(data)
# df["time_period_start"] = pd.to_datetime(df["time_period_start"])
# df.set_index("time_period_start", inplace=True)


# print(df)