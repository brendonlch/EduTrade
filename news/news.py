import requests
import json
import operator
import sys
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/news'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
###  This microservices contains News class 
"""
List of Functions for News
    @app.route("/news/<string:usename>")
    - get_news_by_tickers(symbol) -> calls the API to retrieve latest news
    @app.route("/news/getnews/<string:ticker>")
    - get_news_db_ticker(ticker)  -> retrieve news based on stock symbol/ ticker

Other Functions
    -

Port Number
    - 6020
"""
#FOR DEBUGGING - eprint()
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
#hardcoded data suppose to be for testing

class News(db.Model):
    __tablename__ = 'news'

    author = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(2048), nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False)
    ticker = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(2048), nullable=False)
    url = db.Column(db.String(500), primary_key=True)

    def __init__(self, author, description, publish_date, ticker, title, url): #Initialise the objects
        self.author = author
        self.description = description
        self.publish_date = publish_date
        self.ticker = ticker
        self.title = title
        self.url = url

    def json(self): 
        return {"author": self.author, 
        "description": self.description, 
        "publish_date": self.publish_date, 
        "ticker": self.ticker,
        "title": self.title, 
        "url": self.url}


# def get_all_symbol():
#   data = requests.get("http://localhost:6004/stock/symbol")
#   all_symbol = data.json()
#   return all_symbol

@app.route("/news/<string:symbol>", methods =['GET'])
def get_news_by_tickers(symbol):
  url = (f'https://stocknewsapi.com/api/v1?tickers={symbol}&items=10&token=yiuzo44nggvo8trouq4lkmtsdq4bclz7omhvqkmq')
  response = requests.get(url)
  metadata = response.json()
  for news in metadata["data"]:
    for symbol in news["tickers"]:
      url = news["news_url"]
      title = news["title"]
      publish_date = datetime.strptime(news["date"],"%a, %d %b %Y %H:%M:%S %z")
      description = news["text"]
      author = news["source_name"]

      latest_news = News(author, description, publish_date, symbol, title, url)
      # return jsonify(latest_news.json())
      try:
        db.session.add(latest_news)
        db.session.commit()
      except:
        continue
    
  return jsonify({"Status": "Successfully added"}) ,201

@app.route("/news/getnews/<string:ticker>", methods=['GET'])
def get_news_db_ticker(ticker):
  return jsonify({"news": [news.json() for news in News.query.filter_by(ticker=ticker)]})


if __name__ == '__main__':
  app.run(host='0.0.0.0',port=6020, debug=True)
