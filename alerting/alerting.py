import pika
import uuid
import json
import time
from datetime import datetime, timedelta
import sys
from flask import Flask, request, jsonify
from flask_mail import Message, Mail
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/alert'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'esmg5t1@gmail.com',
	MAIL_PASSWORD = 'BrydonMeme'
	)
db = SQLAlchemy(app)
mail = Mail(app)
CORS(app)
###  This microservices contains Alterting class 

#FOR DEBUGGING - eprint()
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


"""

    Databases 

"""

class Alert(db.Model):
    __tablename__ = 'alert'
    alertid = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    symbol = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    alerttype = db.Column(db.String(64), nullable=False)

    def __init__(self, alertid, username, symbol, price, alerttype): #Initialise the objects
        self.alertid = alertid
        self.username = username
        self.symbol = symbol
        self.price = price
        self.alerttype = alerttype

    def json(self): 
        return {"alertid": self.alertid, "username": self.username, "symbol": self.symbol, "price": self.price, "alerttype": self.alerttype}


class AlertCorrelation(db.Model):
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

@app.route("/alert/<string:username>")
def get_alert_by_id(username):
    alert = Alert.query.filter_by(username=username).all()
    if alert:
        return jsonify({"alerts": [each.json() for each in alert]}), 200
    return jsonify({"message": "Alert not found"}), 404

# function to create/add an alert
@app.route("/alert/add", methods=["POST"])
def add_alert():
    data = request.get_json()
    # Automating Alert ID
    alerts = [alert.json() for alert in Alert.query.all()]
    data['alertid'] = 1 if len(alerts) == 0 else max(alerts, key = lambda x:x['alertid'])['alertid'] + 1
    alert = Alert(**data) #data represents the rest of the data 
    try:
        db.session.add(alert)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the alert."}), 500

    return jsonify(alert.json()), 201 # adds the alert into alert database

# function to update an alert
@app.route("/alert/update", methods=["POST"])
def update_alert():
    data = request.get_json()
    alert = Alert.query.filter_by(username=data["username"], symbol=data["symbol"], alerttype=data["alerttype"]).first() # gets data by username, symbol and alerttype
    
    if alert:
        alert.price = data['price']
        alert.alerttype = data['alerttype']
    
    try:
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the alert."}), 500

    return jsonify(alert.json()), 201 # updates the alert in alert database

# function to delete an alert
@app.route("/alert/delete", methods=["POST"])
def delete_alert():
    data = request.get_json()
    alert = Alert.query.filter_by(username=data["username"], symbol=data["symbol"], alerttype=data["alerttype"]).first() # gets data by username, symbol and alerttype
    if (alert):
        try:
            db.session.delete(alert)
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred deleting the alert."}), 500

    return "Alert successfully deleted", 201 # deletes the alert from alert database

def get_all_correlation():
    db.session.commit()
    return [correlation.json() for correlation in AlertCorrelation.query.all()]

def update_correlation_status(corrid,status):
    correlation = AlertCorrelation.query.filter_by(correlation_id=corrid).first()
    correlation.status = status
    db.session.commit()


def get_all_alerts(symbol):
    db.session.commit()
    return [alert.json() for alert in Alert.query.filter_by(symbol=symbol)]

def delete_alert(data):
    alert = Alert.query.filter_by(username=data["username"], symbol=data["symbol"], alerttype=data["alerttype"]).first() # gets data by username, symbol and alerttype
    if (alert):
        try:
            db.session.delete(alert)
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred deleting the alert."}), 500

    return "Alert successfully deleted", 201 # deletes the alert from alert database

def sendEmail(data):
    email = data['email']
    symbol = data['symbol']
    alertType = data['alerttype']
    alertPrice = data['price']
    stockPrice = data['stockPrice']
    msg = Message("Hello",
                  sender="esmg5t1@gmail.com", 
                  recipients=[email])
    text = ""
    timenow = (datetime.now() - timedelta(hours = 4)).strftime("%Y/%m/%d %H:%M:%S")
    if alertType == "<":
        text = f"Your selected stock {symbol} has fallen below your alert price: {alertPrice}\nCurrent Stock Price in US (as of {timenow}): {stockPrice})"
    elif alertType == ">":
        text = f"Your selected stock {symbol} has reached above your alert price: {alertPrice}\nCurrent Stock Price in US (as of {timenow}): {stockPrice})"
    msg.body = text
    with app.app_context():
        mail.send(msg)
    eprint('email sent!!')
    return 'Success'

def getEmailRequest(data):
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

    # extract the data out for the message
    
    # prepare the message body content
    message = json.dumps(data, default=str) # convert a JSON object to a string

    # Prepare the correlation id and reply_to queue and do some record keeping
    corrid = str(uuid.uuid4())
    row = {"correlation_id": corrid, "status":""}
    correlation = AlertCorrelation(**row)
    # add correlation row into database
    try:
        db.session.add(correlation) 
        db.session.commit()  
    except:
        return jsonify({"message": "An error occurred creating a request."}), 500
    replyqueuename = "alerting.reply"
    # prepare the channel and send a message to Stock
    channel.queue_declare(queue='alerting', durable=True) # make sure the queue used by Shipping exist and durable
    channel.queue_bind(exchange=exchangename, queue='alerting', routing_key='alerting.info') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="alerting.info", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
            reply_to=replyqueuename, # set the reply queue which will be used as the routing key for reply messages
            correlation_id=corrid # set the correlation id for easier matching of replies
        )
    )
    print(f"{data['username']} request sent to user management microservice.")
    # close the connection to the broker
    connection.close()
    return corrid


    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5030, debug=True)

