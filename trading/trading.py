import pika
import uuid
import json
from datetime import datetime, time, timedelta
import time
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/transaction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors = CORS(app, support_credentials=True, resources={r'/*': {"origins": "*"}})
###  This microservice contain Transaction class 
""" 
List of Functions for User
    @app.route("/purchase", methods=['POST'])
    - purchase()            -> communicate with user management to purchase stock 
    @app.route("/sell", methods=['POST'])
    - sell()                -> communicate with user management to sell stock
    @app.route("/transactionhistory, methods=['GET'])
    - view(username)        -> Get user transaction history based on username

Other Functions
    send_order(data):                         
        --> setup the AMQP service 
        --> create uuid and add correlation row into database
        --> sends a message to user_service

    get_all_correlation()                     
        --> return all the rows from TransactionCorrelation table (used in trading_reply)

    update_correlation_status(corrid,status)  
        --> update the status in TransactionCorrelation table (used in trading_reply)
    
"""
#FOR DEBUGGING - eprint()
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


"""

    Databases 

"""

class Transaction(db.Model):
    __tablename__ = 'trading'
    transactionid = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    symbol = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    qty = db.Column(db.Integer(), nullable=False)
    transactiontype = db.Column(db.String(64), nullable=False)
    transactiontime = db.Column(db.String(64), nullable=False)

    def __init__(self, transactionid, username, symbol, price, qty, transactiontype, transactiontime): #Initialise the objects
        self.transactionid = transactionid
        self.username = username
        self.symbol = symbol
        self.price =price
        self.qty = qty
        self.transactiontype = transactiontype
        self.transactiontime = transactiontime

    def json(self): 
        return {"transactionid": self.transactionid, "username": self.username, "symbol": self.symbol, "price": self.price, "qty": self.qty
            , "transactiontype": self.transactiontype, "transactiontime": self.transactiontime}

class TransactionCorrelation(db.Model):
    """
        This class is used to store the correlation id used for retrieving data from the stock microservice.
        * Functions
            - __init__(self, corrid, status)
            - json(self)
    """
    __tablename__ = 'correlation'
    correlation_id = db.Column(db.String(64), primary_key=True)
    status = db.Column(db.String(64), nullable=False)

    def __init__(self, correlation_id, status): #Initialise the objects
        self.correlation_id = correlation_id
        self.status = status

    def json(self): 
        return {"correlation_id": self.correlation_id, "status": self.status}


###########################################################################


@app.route("/purchase", methods=['POST'])
@cross_origin(supports_credentials=True)
def purchase():
    data = request.get_json()

    # Automating Transaction ID and Transaction Time
    transactions = [transaction.json() for transaction in Transaction.query.all()]
    data['transactionid'] = 1 if len(transactions) == 0 else max(transactions, key = lambda x:x['transactionid'])['transactionid'] + 1
    data['transactiontime'] = (datetime.now()- timedelta(hours = 4)).strftime("%Y/%m/%d %H:%M:%S")

    order = Transaction(**data)
    #Communicate with user management
    corrid = send_order(data)

    correlation = TransactionCorrelation.query.filter_by(correlation_id=corrid).first()
    status = correlation.status

    i = 0
    while(status == ''):
        db.session.commit()
        correlation = TransactionCorrelation.query.filter_by(correlation_id=corrid).first()
        status = correlation.status
        time.sleep(5)
        print(i)
        i += 5

    try:
        db.session.add(order)
        db.session.commit()
    except:
        return jsonify({"message":"An error occured creating purchase order"}), 500
    return jsonify(order.json()), 200

@app.route("/sell", methods=['POST'])
def sell():
    data = request.get_json()

    # Automating Transaction ID and Transaction Time
    transactions = [transaction.json() for transaction in Transaction.query.all()]
    data['transactionid'] = 1 if len(transactions) == 0 else max(transactions, key = lambda x:x['transactionid'])['transactionid'] + 1
    data['transactiontime'] = (datetime.now()- timedelta(hours = 4)).strftime("%Y/%m/%d %H:%M:%S")
    
    #####################################
    purchasedtime = data['purchasedtime']
    data.pop('purchasedtime')
    #####################################
    
    order = Transaction(**data)
    #Communicate with user management - Call function below
    
    ########################################
    data['purchasedtime'] = purchasedtime
    ########################################
    
    
    corrid = send_order(data)

    correlation = TransactionCorrelation.query.filter_by(correlation_id=corrid).first()
    status = correlation.status

    i = 0
    print("Loading", end = "")
    while(status == ''):
        db.session.commit()
        correlation = TransactionCorrelation.query.filter_by(correlation_id=corrid).first()
        status = correlation.status
        time.sleep(2)
        print(".", end = "")
    print()
    if (status == "success"):
        try:
            db.session.add(order)
            db.session.commit()
            return jsonify(order.json()), 200
        except:
            return jsonify({"message":"An error occured creating sell order"}), 500
    return jsonify({"message":"An error occured creating sell order"}), 500

@app.route("/transactionhistory", methods=['GET'])
def view():
    username = request.arg.get("username")
    transaction = Transaction.query.filter_by(username=username).first() #Book.query.filter.by(isbn13=isbn13) = select * from book WHERE isbn13 = isbn13, .first() to limit by first item
    if transaction:
        return jsonify(transaction.json()), 200
    return jsonify({"message": "No transaction found"}), 404

def send_order(data):
    # hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    # port = 5672 # default messaging port.
    # # connect to the broker and set up a communication channel in the connection
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    #     # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    #     # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls

    hostname = "host.docker.internal" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
        # connect to the broker and set up a communication channel in the 
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, virtual_host="/", credentials=credentials))
    channel = connection.channel()
    # set up the exchange if the exchange doesn't exist
    exchangename="edutrade"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # extract the data out for the message
    
    # prepare the message body content
    message = json.dumps(data, default=str) # convert a JSON object to a string

    # Prepare the correlation id and reply_to queue and do some record keeping
    corrid = str(uuid.uuid4())
    row = {"correlation_id": corrid, "status":""}
    correlation = TransactionCorrelation(**row)
    # add correlation row into database
    try:
        db.session.add(correlation) 
        db.session.commit()  
    except:
        return jsonify({"message": "An error occurred creating a request."}), 500
    replyqueuename = "trading.reply"
    # prepare the channel and send a message to Stock
    channel.queue_declare(queue='trading', durable=True) # make sure the queue used by Shipping exist and durable
    channel.queue_bind(exchange=exchangename, queue='trading', routing_key='trading.info') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="trading.info", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
            reply_to=replyqueuename, # set the reply queue which will be used as the routing key for reply messages
            correlation_id=corrid # set the correlation id for easier matching of replies
        )
    )
    print(f"{data['symbol']} request sent to user management microservice.")
    # close the connection to the broker
    connection.close()
    return corrid

def get_all_correlation():
    db.session.commit()
    return [correlation.json() for correlation in TransactionCorrelation.query.all()]

def update_correlation_status(corrid,status):
    correlation = TransactionCorrelation.query.filter_by(correlation_id=corrid).first()
    correlation.status = status
    db.session.commit()



if __name__ == '__main__': #So that it can run with this file instead of another file importing this file
    app.run(host = '0.0.0.0', port=5020, debug=True)