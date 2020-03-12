import requests
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/news'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
#FOR DEBUGGING - eprint()
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
#hardcoded data suppose to be for testing

class NewsObj(db.Model):
      __tablename__ = 'news'

      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(248), nullable=False)
      author = db.Column(db.String(248), nullable=False)
      description = db.Column(db.String(2048), nullable=False)
      published = db.Column(db.String(1000), nullable=False)
      ticker = db.Column(db.String(100), nullable=False)
      url = db.Column(db.String(2048), nullable=False)

      def __init__(self, id, title, author, description, published, ticker, url): #Initialise the objects
       self.id = id
       self.title = title
       self.author = author
       self.description = description
       self.published = published
       self.ticker = ticker
       self.url = url

      def json(self): 
        return {"id": self.id, "title": self.title, "author": self.author, "description": self.description, "published": self.published, "ticker": self.ticker,"url": self.url}


@app.route("/")
def get_news_by_tickers():
  new_data = data['result_data']
  count = 0
  new_dict = {}
  news_objects = {}
  obj_of_news = {}

  for data1 in new_data['GOOGL']:
    count += 1
    new_dict[count] = data1
    for i in range (1 , len(new_dict) + 1):
        y = NewsObj(i, new_dict[i]['title'], new_dict[i]['author'], new_dict[i]['description'], new_dict[i]['published'], new_dict[i]['ticker'], new_dict[i]['url'])
        news_objects[i] = y.json()
  try:
    for i in range (1, len(news_objects) + 1):
      #return news_objects
      # return(news_objects)
      individual_news = news_objects[i]
      obj_news = NewsObj(**individual_news)   
      db.session.add(obj_news)
      db.session.commit()
  except:
    return jsonify({"message": "An error occurred adding news"}), 500
  return jsonify({"message": "Successfully added"}), 201
  
app.run(port=6002, debug=True)
