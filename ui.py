import pika
import uuid
import json
from datetime import datetime, time, timedelta
import time
import sys
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from os import environ

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors = CORS(app, support_credentials=True, resources={r'/*': {"origins": "*"}})

@app.route("/")
@cross_origin(supports_credentials=True)
def home():
    return render_template('login.html')


if __name__ == '__main__': #So that it can run with this file instead of another file importing this file
    app.run(host = '0.0.0.0', port=8888, debug=True)