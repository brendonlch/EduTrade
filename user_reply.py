#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import sys
import os
import csv
from user import Correlation, User, Holdings
# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
# Use a reply-to queue and correlation_id to get a corresponding reply
import pika
# If see errors like "ModuleNotFoundError: No module named 'pika'", need to
# make sure the 'pip' version used to install 'pika' matches the python version used.

###########################
# Waiting for stock reply #
###########################

def receive_stock_request():
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

    replyqueuename="stock.info"
    channel.queue_declare(queue=replyqueuename, durable=True) # make sure the queue used for "reply_to" is durable for reply messages
    channel.queue_bind(exchange=exchangename, queue=replyqueuename, routing_key=replyqueuename) # make sure the reply_to queue is bound to the exchange
    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=replyqueuename,
            on_message_callback=reply_callback, # set up the function called by the broker to process a received message
    ) # prepare the reply_to receiver
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def reply_callback(channel, method, properties, body): # required signature for a callback; no return
    """processing function called by the broker when a message is received"""
    # Load correlations for existing created orders from a file.
    # - In practice, using DB (as part of the order DB) is a better choice than using a file.
    rows = [correlation.json() for correlation in UserCorrelation.query.all()]
    # Check if the reply message contains a valid correlation id recorded in the file.
    # - Assume each line in the file is in this CSV format: <order_id>, <correlation_id>, <status>, ...
    matched = False
    for row in rows:
        if not 'correlation_id' in row:
            print('Warning for Correlation Database: no "correlation_id" for a request:', row)
            continue
        corrid = row['correlation_id']
        if corrid == properties.correlation_id: # check if the reply message matches one request message based on the correlation id
            print("--Matched reply message with a correlation ID: " + corrid)
            # Can do anything needed for the scenario here, e.g., may update the 'status', or inform UI or other applications/services.
            print(body) # Here, simply print the reply message directly
            print()
            matched = True
            break
    if not matched:
        print("--Wrong reply correlation ID: No match of reply correlation ID: No match of " + properties.correlation_id)
        print()
    # acknowledge to the broker that the processing of the message is completed
    channel.basic_ack(delivery_tag=method.delivery_tag)


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is " + os.path.basename(__file__) + ": listening for a stock info reply from stock...")
    receive_stock_request()
