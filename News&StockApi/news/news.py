import requests
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

url = ('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=4ee93aecade8498289feb167a5b8aa69')
news = requests.get(url) 
news_finance = news.json()

@app.route("/")
def get_news():
       return news_finance

app.run(port=6002, debug=True)
