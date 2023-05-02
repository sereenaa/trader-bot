from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os


url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical'
parameters = {
    'count':'10000',
    'convert':'USD', 
    'symbol':'ETH', 
    'time_period':'daily'
}

os.environ['COINMARKETCAPAPIKEY'] = ''
api_key = os.getenv('COINMARKETCAPAPIKEY')
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data)

    with open("data_cmc.json", "w") as json_file:
        # Write the JSON data to the file
        json.dump(data, json_file)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)