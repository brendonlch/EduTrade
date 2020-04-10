EduTrade
EduTrade is a virtual financial stock market platform, designed to train teenagers from ages 13 to 18 in the fundamentals of trading US stocks, which covers how to start trading and proper trading practices that they can apply in the future.
 
Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
Input all the files in the www directory in a folder for localhost access
Make sure your WAMP/MAMP server is running
Load/Import in all the SQL files in the sql-files folder into PHPMyAdmin localhost database
Run docker.compose.yml
* To get all the latest images and run all images to their respective containers
Run localhost:1337 in browser to access Kong through Konga
* Create an admin account (username: admin, password: adminadmin)
* Input (name: default, Kong Admin URL: http://kong:8001)
* Under the ‘Snapshots’ section, import the snapshot_config_final.json file
* Click ‘restore’, tick all the boxes and confirm. 
* If you face any errors, click ‘restore’ again. The configurations should have no errors now.

Running the tests  
Loading of data from API
Run Compose up on docker.compose.yml
Run localhost:8000/stock/stock/loadstock in browser
* To get all the latest stock into the database
* Keep this browser running to load the latest stock into the database 
* NOTE : Market opens at 9:30pm Singapore Time (UTC+8)


Testing of application
* Run localhost:8000/EduTrade/templates/login.html
* Start trading by creating an account

Built With
* Docker - To contain all our image and public repository
* Kong - To allow API Gateway to control the API calls from the browser
* RabbitMQ - To allow AMQP messaging 
* External APIs

Authors
G8T5
* Earnest Ng
* Brendon Lim
* Ng Wen Jie
* Rohit Bhojwani 
* Brydon Seah 

Acknowledgements
* StockNewsAPI - https://stocknewsapi.com/ - Maximum of 500 API calls until 10th May 2020
* AlphaVantage API - https://www.alphavantage.co/ - Maximum of 500 API calls per day - 5 calls per 5 minutes