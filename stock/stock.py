import pika
import requests
import json
import operator
import sys
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
###  This microservices contains Stock and Stockdata class 
"""
List of Functions for Stock
    @app.route("/stock/loadstock")
    - get_all_stock()             -> calls the AlphaVantage API to load latest stock into database
    @app.route("/stock/past/<string:symbol>")
    - get_all_data(symbol)        -> retrieve all stockdata in database for the symbol
    @app.route("/stock/getpastprices/<string:username>)
    - get_all_past_prices(symbol) -> calls the AlphaVantage API to load past prices of symbol into database
    @app.route("/stock/<string:symbol>")
    - get_stock_data(symbol)      -> retrieve current latest stockdata in database
    @app.route("/stock/all")
    - get_all_stock_price()       -> to get all stock latest prices 
    @app.route("/stock/allstockdata")
    - get_all_stock_data()        -> to get all stock latest data
    @app.route("/stock/symbol")
    - get_all_symbol()            -> to get all symbols in database

Other Functions
    - get_all_symbol()           -> returns all symbol in database
    - get_stock(symbol)          -> returns the object of that symbol in stockdata 
    - send_message(update_stock) -> sends the latest stock object through amqp fire and forget to alerting 

Port Number
    - 6010
"""
#FOR DEBUGGING - eprint()
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Stock(db.Model):
    """
        This class is used to store the stocks.
    """

    __tablename__ = 'stock'

    symbol = db.Column(db.String(64), primary_key=True)
    stockname = db.Column(db.String(64), nullable=False)
    apikey = db.Column(db.String(64), nullable=False)
    apicount = db.Column(db.Integer(), nullable=False)
    

    def __init__(self, symbol, stockname, apikey, apicount): #Initialise the objects
        self.symbol = symbol
        self.stockname = stockname
        self.apikey = apikey
        self.apicount = apicount


    def json(self): 
        return {"symbol": self.symbol, "stockname": self.stockname, "apikey": self.apikey, "apicount": self.apicount}

class Stockdata(db.Model):
    """
        This class is used to store the stocks.
    """

    __tablename__ = 'stockdata'

    symbol = db.Column(db.String(64), primary_key=True)
    stockname = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    volume = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.String(64), nullable=False, primary_key=True)

    def __init__(self, symbol, stockname, price, volume, time): #Initialise the objects
        self.symbol = symbol
        self.stockname = stockname
        self.price = price
        self.volume = volume
        self.time = time


    def json(self): 
        return {"symbol": self.symbol, 
        "stockname": self.stockname,
        "price": self.price,
        "volume": self.volume,
        "time": self.time}

#Load data in stockdata table - Call this to continuosly load API
@app.route("/stock/loadstock") 
def get_all_stock():
    stock = Stock.query.all()
    list_of_stock = {}
    # Getting all stock symbol and stock name in list_of_stock
    eprint("Getting all stock symbol and stock name in list_of_stock...")
    for stocks in stock:
        stock_symbol = stocks.symbol
        stock_name = stocks.stockname
        api_key = stocks.apikey
        list_of_stock[stock_symbol] = [stock_name, api_key]
    key_list = list(list_of_stock.keys())

    while 1:
        us_time = datetime.now() - timedelta(hours = 4)
        eprint(f'Current US Timezone (GMT-4): {us_time}')

        # To get the timing to retrieve the next set of data
        rounded_time = us_time + (datetime.min - us_time) % timedelta(minutes = 5)  # round up to nearest 5 minutes
        countdown = int(rounded_time.timestamp() - us_time.timestamp()) + 2         # how long before the next API call (in seconds) (added 2 sec just to be safe)

        for key in key_list:
            #Get data from API
            eprint(f"Getting data for {key} from API...")
            added = False
            while not added:
                try:
                    api_key = list_of_stock[key][1]
                    url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={key}&interval=5min&apikey={api_key}")
                    data = requests.get(url).json()
                    all_stocks = data.get("Time Series (5min)")

                    #Counting each apicount to keep track
                    current_stock = Stock.query.filter_by(symbol=key).first()
                    current_stock.apicount = current_stock.apicount +1
                    db.session.commit()
                    
                    #Scrap data from API
                    if (all_stocks != None):
                        eprint("Scraping data from API...")
                        all_time = sorted(list(all_stocks.keys()))
                        stock_name = list_of_stock[key][0]
                        latest_time = all_time[-1]
                        stock_price = float(all_stocks[latest_time]["4. close"])
                        volume = int(all_stocks[   latest_time]["5. volume"])
                        the_stock = Stockdata(key,stock_name,stock_price,volume,latest_time)
                        # return jsonify(the_stock.json())
                        # Adding into database
                        eprint("Adding into database...")
                        db.session.add(the_stock)
                        db.session.commit()
                        added = True

                        # Sends message to alerting 
                        send_message(the_stock.json())
                except:
                    break
        for i in range(countdown):
            eprint(f"Standby...  {countdown - i} seconds remaining till next retrival [{rounded_time}]", end = '\r')
            time.sleep(1)
        eprint()
    return "System stopped"

@app.route("/stock/past/<string:symbol>") # StockData
def get_all_data(symbol):
    return jsonify({"stock": [stocksData.json() for stocksData in Stockdata.query.filter_by(symbol=symbol)]})

@app.route("/stock/getpastprices/<string:symbol>")
def get_all_past_prices(symbol):
    current_stock = Stock.query.filter_by(symbol=symbol).first()
    stock_symbol = current_stock.symbol
    eprint(stock_symbol)
    stock_name = current_stock.stockname
    api_key = current_stock.apikey
    url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}")
    eprint(url)
    data = requests.get(url).json()
    # return data
    all_stocks = data.get("Time Series (5min)")
    for time in all_stocks:
        stock_price = float(all_stocks[time]['4. close'])
        volume = int(all_stocks[time]['5. volume'])
        stock = Stockdata(stock_symbol, stock_name, stock_price, volume, time)
        db.session.add(stock)
    db.session.commit()
    return jsonify({"message":"Successfully Added"})


@app.route("/stock/<string:symbol>") # StockData
def get_stock_data(symbol):
    latest_stock = Stockdata.query.filter_by(symbol=symbol).order_by(Stockdata.time.desc()).first()
    #stock_price = latest_stock.price
    return jsonify(latest_stock.json())



@app.route("/stock/all")  # Symbol : Price
def get_all_stock_price():
    key_list = get_all_symbol()
    list_of_prices = {}
    for key in key_list:
        stockdata = Stockdata.query.filter_by(symbol=key).first()
        list_of_prices[key] = stockdata.price
    return jsonify(list_of_prices)

@app.route("/stock/allstockdata")
def get_all_stock_data():
    all_symbol = get_all_symbol()
    stockdata_dict = {"stocksdata": []}
    for symbol in all_symbol:
        latest_stock = Stockdata.query.filter_by(symbol=symbol).order_by(Stockdata.time.desc()).first()
        stockdata_dict["stocksdata"].append(latest_stock.json())
    return jsonify(stockdata_dict)

@app.route("/stock/symbol")
def get_all_symbol():
    stock = Stock.query.all()
    list_of_stock = {}
    # Getting all stock symbol and stock name in list_of_stock
    for stocks in stock:
        stock_symbol = stocks.symbol
        stock_name = stocks.stockname
        api_key = stocks.apikey
        list_of_stock[stock_symbol] = [stock_name, api_key]
    key_list = list(list_of_stock.keys())
    return jsonify(key_list)

def get_all_symbol():
    stock = Stock.query.all()
    list_of_stock = {}
    # Getting all stock symbol and stock name in list_of_stock
    for stocks in stock:
        stock_symbol = stocks.symbol
        stock_name = stocks.stockname
        api_key = stocks.apikey
        list_of_stock[stock_symbol] = [stock_name, api_key]
    key_list = list(list_of_stock.keys())
    return key_list


def get_stock(symbol):
    stock = Stockdata.query.filter_by(symbol=symbol).first()
    return stock

def send_message(update_stock):
    eprint(update_stock)
    # hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    # port = 5672 # default messaging port.
    # # connect to the broker and set up a communication channel in the connection
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    hostname = "host.docker.internal" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
        # connect to the broker and set up a communication channel in the 
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, virtual_host="/", credentials=credentials))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="edutrade"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')
    # prepare the message body content
    message = json.dumps(update_stock, default=str) # convert a JSON object to a string
    # send the message
    # always inform Monitoring for logging no matter if successful or not
    channel.basic_publish(exchange=exchangename, routing_key="stock.info", body=message)

if __name__ == '__main__': 
    app.run(host='0.0.0.0',port=6010, debug=True)

       
