import requests
import json
import operator
import sys
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

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
    time = db.Column(db.String(64), nullable=False)

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
                        volume = int(all_stocks[latest_time]["5. volume"])
                        the_stock = Stockdata(key,stock_name,stock_price,volume,latest_time)
                        # return jsonify(the_stock.json())
                        # Adding into database
                        eprint("Adding into database...")
                        db.session.add(the_stock)
                        db.session.commit()
                        added = True
                except:
                    time.sleep(20)
        eprint("Standby...")
        time.sleep(300)
    return "System stopped"


@app.route("/stock/<string:stockname>") #
def get_stock_price(stockname):
    stock = Stock.query.filter_by(stockname=stockname).first()
    symbol = stock.symbol
    latest_stock = Stockdata.query.filter_by(symbol=symbol).first()
    stock_price = latest_stock.price
    return jsonify({"price":stock_price})

@app.route("/stock/all") #
def get_all_stock_price():
    key_list = get_all_symbol()
    list_of_prices = {}
    for key in key_list:
        stockdata = Stockdata.query.filter_by(symbol=key).first()
        list_of_prices[key] = stockdata.price
    return jsonify(list_of_prices)


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

# @app.route("/")
# def get_stock():
#     return all_stocks

app.run(port=6004, debug=True)

       