#! /bin/bash

# Start the first process
python alerting.py &
# Start the second process
python alerting_stock_service.py &
# Start the third process
python alerting_user_reply.py