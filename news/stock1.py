import requests
import json
import operator
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

url = ('https://www.alphavantage.co/query?'
       'function=TIME_SERIES_INTRADAY&'
       'symbol=MSFT&'
       'interval=5min&'
       'apikey=3PEN1QC6AGKBYT1J')
stock = requests.get(url) 
stock_json = stock.json()
all_stocks = stock_json.get("Time Series (5min)")
keys = list(all_stocks.keys())
data = all_stocks.get(keys[0], "")


@app.route("/")
def getstock():
    return all_stocks
    
app.run(port=6004, debug=True)

       
