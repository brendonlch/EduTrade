import pika
import uuid
import json
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
###  This microservice contain User, Holdings, and Correlation class
"""
List of Functions for User
    @app.route("/user")
    - get_all_users()           -> return all the users in the 'user' database
    @app.route("/user/<string:username>")
    - get_user_by_id(username)  -> return info from 'user' database with username as input
    @app.route("/userauthenticate")
    - user_authenticate()       -> password validation
    @app.route("/user/<string:username>", methods=['POST'])
    - add_user(username)        -> insert user info into 'user' database using POST method
    @app.route("/user/delete/<string:username>", methods=['POST'])
    - delete_user(username)          -> delete user details
    @app.route("/user/update/<string:username>", methods=['POST'])
    - update_user(username)          -> update user details

List of Functions for Holdings
    @app.route("/holdings/<string:username>")
    - get_all_holdings(username):    -> returns all holdings from user

Other Functions
    - minus_credit(order)                      -> to minus any credits made by purchase order
    - add_credit(order)                        -> to add any credits made by sell order
    - add_holding(order)                       -> to add successful purchase order into holdings
    - remove_holding(order)                    -> to remove any sell order from holdings
    - get_all_correlation()                    -> to commit any correlation id getting added
    - update_correlation_status(corrid,status) -> to update status for the message in correlation table
    - get_user_by_id(username)                 -> return user object if there are any in database 

Port Number
    - 5010
"""

"""

    Databases

"""
#FOR DEBUGGING - eprint()
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


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

    def __init__(self, username, password, name, age, email, institution, credit = 100): #Initialise the objects
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

class UserCorrelation(db.Model):
    """
        This class is used to store the correlation id used for retrieving data from the stock microservice.
        * Functions
            - __init__(self, corrid, status)
            - json(self)
    """
    __tablename__ = 'correlation'
    corrid = db.Column(db.String(64), primary_key=True)
    status = db.Column(db.String(64), nullable=False)

    def __init__(self, corrid, status): #Initialise the objects
        self.corrid = corrid
        self.status = status

    def json(self):
        return {"corrid": self.corrid, "status": self.status}


###########################################################################


@app.route("/user")
def get_all_users():
    return jsonify({"users": [user.json() for user in User.query.all()]})

@app.route("/user/<string:username>")
def get_user_by_id(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(user.json()), 200
    return jsonify({"message": "User not found"}), 404

@app.route("/userauthenticate", methods=['POST'])
def user_authenticate():
    data = request.get_json()
    username = data['username']
    user = User.query.filter_by(username=username).first()
    if user:
        if user.password == data["password"]:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "fail", "message": "Incorrect Password!"}), 401
    return jsonify({"status": "fail", "message": "User not found"}), 404

@app.route("/user/<string:username>", methods=['POST'])
def add_user(username):
    if (User.query.filter_by(username=username).first()):
        return jsonify({"message": "A user with username '{}' already exists.".format(email)}), 400
    data = request.get_json()
    eprint(data)
    user = User(username, **data) # **data represents the rest of the data
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the user."}), 500
    return jsonify(user.json()), 201

@app.route("/user/delete/<string:username>", methods=['POST'])
def delete_user(username):
    current_user = User.query.filter_by(username=username).first()
    if (current_user):
        try:
            db.session.delete(current_user)
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred deleting the user."}), 500
    return 201

@app.route("/user/update/<string:username>", methods=['POST'])
def update_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        data = request.get_json()
        user.name = data["name"]
        user.age = data["age"]
        user.email = data["email"]
        user.institution = data["institution"]
        user.password = data["password"]
    try:
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the user."}), 500
    return jsonify(user.json()), 201

@app.route("/holdings/<string:username>") #To find bought stock
def get_all_holdings(username):
    # Stockname
    # Current price

    return jsonify({"holdings": [user.json() for user in Holdings.query.filter_by(username=username)]})


def minus_credit(order):
    user = User.query.filter_by(username=order['username']).first()
    if user.credit >= (order['qty']*order['price']):
        user.credit = user.credit - (order['qty']*order['price'])
        try:
            db.session.commit()
        except:
            return False
        return True
    else:
        return False

def add_credit(order):
    user = User.query.filter_by(username=order['username']).first()
    user.credit = user.credit + (order['qty']*order['price'])
    try:
        db.session.commit()
    except:
        return False
    return True

def add_holding(order):
    user = User.query.filter_by(username=order['username']).first()
    holding = Holdings(order['username'],order['symbol'],order['qty'],order['price'],0,order['transactiontime'])
    try:
        db.session.add(holding)
        db.session.commit()
    except:
        return False
    return True

def remove_holding(order):
    holding = Holdings.query.filter_by(username=order['username'], symbol=order['symbol'], datepurchased=order['purchasedtime']).first()
    if(order['qty'] == holding.qty):
        try:
            db.session.delete(holding)
            db.session.commit()
        except:
            return False
        return True
    else:
        holding.qty = holding.qty - order['qty']
        try:
            db.session.commit()
        except:
            return False
        return True

def get_all_correlation():
    db.session.commit()
    return [correlation.json() for correlation in UserCorrelation.query.all()]

def update_correlation_status(corrid,status):
    correlation = UserCorrelation.query.filter_by(correlation_id=corrid).first()
    correlation.status = status
    db.session.commit()

def get_user_by_id(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.json()
    return False

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5010, debug=True)
