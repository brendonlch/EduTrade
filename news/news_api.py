from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

###  This microservice contain User and Holdings class 
""" 
List of Functions for News
    @app.route("/user/<string:ticker>")
    - get_news_by_ticker(ticker)  -> return news with ticker as input
    @app.route("/user/<string:username>", methods=['POST'])
    - add_news(ticker)        -> insert related ticker news using POST method
"""

class Ticker_news(db.Model):
    """
        This class is used to store the registered users in the database.
        * Functions
            - __init__(self, username, password, name, age, email, institution, credit)
            - json(self)
    """
    __tablename__ = 'ticker_news'

    author = db.Column(db.String(100), primary_key=True)
    desc = db.Column(db.String(2048), nullable=False)
    publish_date = db.Column(db.Datetime, nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(2048), nullable=False)
    url_article = db.Column(db.String(2048), nullable=False)
    
    def __init__(self, username, password, name, age, email, institution, credit): #Initialise the objects
        self.username = username
        self.password = password
        self.name = name
        self.age = age
        self.email = email
        self.institution = institution
        self.credit = credit

    def json(self): 
        return {"username": self.username, "password": self.password, "name": self.name, "age": self.age
            , "email": self.email, "institution": self.institution, "credit": self.credit}

class Holdings(db.Model):
    """
        This class is used to store the stock holdings that the user has.
    """

    __tablename__ = 'holdings'

    username = db.Column(db.String(64), primary_key=True)
    symbol = db.Column(db.String(64), nullable=False)
    qty = db.Column(db.String(64), nullable=False)
    buyprice = db.Column(db.Float(precision=2), nullable=False)
    limit = db.Column(db.Float(precision=2), nullable=False)
    datepurchased = db.Column(db.DateTime, primary_key=True)

    def __init__(self, username, symbol, qty, buyprice, limit, datepurchased): #Initialise the objects
        self.username = username
        self.symbol = symbol
        self.qty = qty
        self.buyprice = buyprice
        self.limit = limit
        self.datepurchased = datepurchased

    def json(self): 
        return {"username": self.username, "symbol": self.symbol, "qty": self.qty, "buyprice": self.buyprice
            , "limit": self.limit, "datepurchased": self.datepurchased}

@app.route("/user")
def get_all_users():
    return jsonify({"users": [user.json() for user in User.query.all()]}) 

if __name__ == '__main__': #So that it can run with this file instead of another file importing this file
    app.run(port=5000, debug=True)