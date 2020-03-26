#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
import json
import sys
import os
import csv
from alerting import get_all_alerts, getEmailRequest
# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
# Use a reply-to queue and correlation_id to get a corresponding reply
import pika
# If see errors like "ModuleNotFoundError: No module named 'pika'", need to
# make sure the 'pip' version used to install 'pika' matches the python version used.


##########################################################################
# Once receive stock order, process and send reply callback to stock #
##########################################################################

def receive_alert():
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

    replyqueuename="stock.info"
    channel.queue_declare(queue=replyqueuename, durable=True) # make sure the queue used for "reply_to" is durable for reply messages
    channel.queue_bind(exchange=exchangename, queue=replyqueuename, routing_key="stock.info") # make sure the reply_to queue is bound to the exchange
    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=replyqueuename, on_message_callback=callback, # set up the function called by the broker to process a received message
    ) # prepare the reply_to receiver
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("Received an order by " + __file__)
    print(body)
    processStock(json.loads(body))
    # print processing result; not really needed
    # json.dump(result, sys.stdout, default=str) # convert the JSON object to a string and print out on screen
    print() # print a new line feed to the previous json dump
    print() # print another new line as a separator
    channel.basic_ack(delivery_tag=method.delivery_tag)

def processStock(stock):
    all_alerts = get_all_alerts(stock['symbol'])
    for alert in all_alerts:
        alert['stockPrice'] = stock['price']
        if alert['alerttype'] == '>' and stock['price'] > alert['price']:
            getEmailRequest(alert)
            #send email function(username, symbol, alerttype, alert price, stock price) -> to retrieve and send email
        elif alert['alerttype'] == '<' and stock['price'] < alert['price']:
            #send email function(username, symbol, alerttype, alert price, stock price) -> to retrieve and send email
            getEmailRequest(alert)





# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is " + os.path.basename(__file__) + ": listening for a stock update from stock...")
    receive_alert()
