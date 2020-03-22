import pika
import uuid
import json
import datetime, time
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/alert'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
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
    percentage = db.Column(db.Float(precision=2), nullable=False)
    alerttype = db.Column(db.String(64), nullable=False)

    def __init__(self, alertid, username, symbol, price, percentage, alerttype): #Initialise the objects
        self.alertid = alertid
        self.username = username
        self.symbol = symbol
        self.price = price
        self.percentage = percentage
        self.alerttype = alerttype

    def json(self): 
        return {"alertid": self.alertid, "username": self.username, "symbol": self.symbol, "price": self.price, "percentage": self.percentage
            , "alerttype": self.alerttype}

###########################################################################

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
    
    alert.percentage = data["percentage"]
    
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


if __name__ == '__main__': #So that it can run with this file instead of another file importing this file
    app.run(port=7001, debug=True)
