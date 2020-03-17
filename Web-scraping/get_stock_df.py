import re
from io import StringIO
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

class getStockHistory: 
    URL = 'https://au.finance.yahoo.com/quote/{0}/history?p={0}'

    print(URL)