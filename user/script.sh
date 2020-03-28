#!/bin/bash
# Start the first process
python user.py &
# Start the second process
python user_trading_service.py &
# Start the last process
python user_alert_service.py
