import pika
import uuid
import json
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user'
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
    @app.route("/user/<string:username>", methods=['POST'])
    - add_user(username)        -> insert user info into 'user' database using POST method

List of Functions for Holdings 
    @app.route("/holdings/<string:username>")
    - get_all_holdings(username)     -> return all holdings that the user has with username as input 
    @app.route("/holdings/<string:username>", methods=['POST'])
    - add_stock_to_user(username)    -> insert a stock transaction to 'holdings' database using POST method
    @app.route("/holdings/remove",  methods=['POST'])
    - remove_stock_from_user():      -> remove stock from user with POST method

Other Functions
    - send_stock_request(symbol)        -> retrieve stock information from Stock microservice with symbol as input
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

@app.route("/holdings/<string:username>") #To find bought stock
def get_all_holdings(username):
    return jsonify({"holdings": [user.json() for user in Holdings.query.filter_by(username=username)]}) 


def send_stock_request(symbol):
    hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="edutrade"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare the message body content
    message = symbol # convert a JSON object to a string

    # Prepare the correlation id and reply_to queue and do some record keeping
    corrid = str(uuid.uuid4())
    row = {"correlation_id": corrid, "status":""}
    correlation = UserCorrelation(row)
    # add correlation row into database
    try:
        db.session.add(correlation) 
        db.session.commit()  
    except:
        return jsonify({"message": "An error occurred creating a request."}), 500
    replyqueuename = "stock.reply"
    # prepare the channel and send a message to Stock
    channel.queue_declare(queue='stock', durable=True) # make sure the queue used by Shipping exist and durable
    channel.queue_bind(exchange=exchangename, queue='stock', routing_key='stock.info') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="stock.info", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
            reply_to=replyqueuename, # set the reply queue which will be used as the routing key for reply messages
            correlation_id=corrid # set the correlation id for easier matching of replies
        )
    )
    print(f"{symbol} request sent to Stock microservice.")
    # close the connection to the broker
    connection.close()
    return corrid

def minus_credit(order):
    user = User.query.filter_by(username=order['username']).first()
    user.credit = user.credit - (order['qty']*order['price'])
    try:
        db.session.commit()
    except:
        return False
    return True

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


if __name__ == '__main__': 
    app.run(port=5000, debug=True)