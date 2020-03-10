#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
import json
import sys
import os
import csv
from user import UserCorrelation, User, Holdings, minus_credit, add_holding
# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
# Use a reply-to queue and correlation_id to get a corresponding reply
import pika
# If see errors like "ModuleNotFoundError: No module named 'pika'", need to
# make sure the 'pip' version used to install 'pika' matches the python version used.


##########################################################################
# Once receive trading order, process and send reply callback to trading #
##########################################################################

def receive_trade_request():
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

    replyqueuename="trading"
    channel.queue_declare(queue=replyqueuename, durable=True) # make sure the queue used for "reply_to" is durable for reply messages
    channel.queue_bind(exchange=exchangename, queue=replyqueuename, routing_key="trading.info") # make sure the reply_to queue is bound to the exchange
    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=replyqueuename, on_message_callback=callback, # set up the function called by the broker to process a received message
    ) # prepare the reply_to receiver
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("Received an order by " + __file__)
    result = processOrder(json.loads(body))
    # print processing result; not really needed
    json.dump(result, sys.stdout, default=str) # convert the JSON object to a string and print out on screen
    print() # print a new line feed to the previous json dump
    print() # print another new line as a separator
    exchangename = "edutrade"
    # prepare the reply message and send it out
    replymessage = json.dumps(result, default=str) # convert the JSON object to a string
    replyqueuename="trading.reply"
    # A general note about AMQP queues: If a queue or an exchange doesn't exist before a message is sent,
    # - the broker by default silently drops the message;
    # - So, if really need a 'durable' message that can survive broker restarts, need to
    #  + declare the exchange before sending a message, and
    #  + declare the 'durable' queue and bind it to .infothe exchange before sending a message, and
    #  + send the message with a persistent mode (delivery_mode=2).
    channel.queue_declare(queue=replyqueuename, durable=True) # make sure the queue used for "reply_to" is durable for reply messages
    channel.queue_bind(exchange=exchangename, queue=replyqueuename, routing_key=replyqueuename) # make sure the reply_to queue is bound to the exchange
    channel.basic_publish(exchange=exchangename,
            routing_key=properties.reply_to, # use the reply queue set in the request message as the routing key for reply messages
            body=replymessage, 
            properties=pika.BasicProperties(delivery_mode = 2, # make message persistent (stored to disk, not just memory) within the matching queues; default is 1 (only store in memory)
                correlation_id = properties.correlation_id, # use the correlation id set in the request message
            )
    )
    channel.basic_ack(delivery_tag=method.delivery_tag) # acknowledge to the broker that the processing of the request message is completed

def processOrder(order):
    print("Processing an order:")
    print(order)
    resultstatus = "failure" # simulate success/failure with a random True or False
    print("Minusing credits...") #Do try except
    if(minus_credit(order)):
        print("Successfully minus credits...")
        resultstatus = "success"
    print("Adding into personal holdings...")
    if(add_holding(order)):
        print("Successfully placed into holdings...")
        resultstatus = "success"
    # Can do anything here. E.g., publish a message to the error handler when processing fails.
    result = {'status': resultstatus, 'order': order}
    print("Successful purchase.")
    return result



# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is " + os.path.basename(__file__) + ": listening for a trade info from trading...")
    receive_trade_request()
