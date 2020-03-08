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
List of Functions for User
    @app.route("/user")
    - get_all_users()        -> return all the users in the 'user' database
    @app.route("/user/<string:username>")
    - get_user_by_id(username)  -> return info from 'user' database with username as input
    @app.route("/user/<string:username>", methods=['POST'])
    - add_user(username)        -> insert user info into 'user' database using POST method

List of Functions for Holdings 
    @app.route("/holdings/<string:username>")
    - get_all_holdings(username)     -> return all holdings that the user has with username as input 
    @app.route("/holdings/<string:username>", methods=['POST'])
    - add_stock_to_user(username)    -> insert a stock transaction to 'holdings' database using POST method
    @app.route("/holdings/remove",  methods=['POST'])
    - remove_stock_from_user():      -> remove stock from user with POST method

"""

class User(db.Model):
    """
        This class is used to store the registered users in the database.
        * Functions
            - __init__(self, username, password, name, age, email, institution, credit)
            - json(self)
    """
    __tablename__ = 'userinfo'

    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    institution = db.Column(db.String(64), nullable=False)
    credit = db.Column(db.Float(precision=2), nullable=False)

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

@app.route("/user/<string:username>")
def get_user_by_id(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(user.json())
    return jsonify({"message": "User not found"}), 404

@app.route("/user/<string:username>", methods=['POST'])
def add_user(username):
    if (User.query.filter_by(username=username).first()):
        return jsonify({"message": "A user with username '{}' already exists.".format(email)}), 400
    data = request.get_json()
    user = User(username, **data) # **data represents the rest of the data
    try:
        db.session.add(user) #db.session.add(book) = insert into book (isbn13,...) values (isbn13,...)
        db.session.commit()  #to commit
    except:
        return jsonify({"message": "An error occurred creating the user."}), 500
    return jsonify(user.json()), 201

@app.route("/holdings/<string:username>") #To find bought stock
def get_all_holdings(username):
    return jsonify({"holdings": [user.json() for user in Holdings.query.filter_by(username=username)]}) 

@app.route("/holdings/<string:username>", methods=['POST'])
def add_stock_to_user(username):
    data = request.get_json()
    holding = Holdings(username, **data) # **data represents the rest of the data
    try:
        db.session.add(holding)  
        db.session.commit() 
    except:
        return jsonify({"message": "An error occurred adding the stock."}), 500
    return jsonify(holding.json()), 201

@app.route("/holdings/remove",  methods=['POST'])
def remove_stock_from_user():
    data = request.get_json()
    holding = Holdings.query.filter_by(username=data['username'],symbol=data['symbol']).first()
    holding.qty = float(holding.qty)
    data['qty'] = float(data['qty'])
    if data['qty'] < holding.qty:
        try:
            holding.qty = holding.qty - data['qty']
            db.session.commit() #to commit
        except:
            return jsonify({"message": "An error occurred updating the stock."}), 500
    else:
        try:
            db.session.delete(holding) #db.session.add(book) = insert into book (isbn13,...) values (isbn13,...)
            db.session.commit() #to commit
        except:
            return jsonify({"message": "An error occurred removing the stock."}), 500
    return jsonify(holding.json()), 202

if __name__ == '__main__': #So that it can run with this file instead of another file importing this file
    app.run(port=5000, debug=True)