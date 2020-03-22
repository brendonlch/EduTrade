import requests
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import os

# Downloading today data from SGX using SGX API
today = datetime.now()
start_date = today-timedelta(1)
start_date = start_date.strftime('%Y%m%d')# Format must be in: '20190808'
end_date = today.strftime('%Y%m%d')
default_folder = './data'

# Start downloading data    
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
url = f'https://api.sgx.com/announcements/v1.0/?periodstart={start_date}_160000&periodend={end_date}_155959&pagestart=0&pagesize=20'
res = requests.get(url, headers)

# Store the downloaded data into dataframe (for easier access later)
json_data = res.json()['data']
df = pd.DataFrame(json_data)

# Assuming we are interested in the updates related to "LODHA DEVELOPERS INTERNATIONAL LIMITED"
stock_name = 'LODHA DEVELOPERS INTERNATIONAL LIMITED'

# Filtered out those unwanted company updates information
df = df[df['issuer_name']==stock_name]