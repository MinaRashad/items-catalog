# Item Catalog
## A web application for restaurants Items

a web application that uses sqlite3 and python3 to 
view items and categorize them according to the restaurant

### Initialization

*pre-requirements*:
    1.Python3

install python3 with

        sudo apt install python3

*requirements*:
    1.sqlite3
    2.requests
    3.json
    4.flask


run this command in the terminal while being the the same directory

        pip3 install -r requirements.txt

or in case it did not work try:

	    pip3 install -r requirements.txt --user

### Initializing Database

to create the database you need to run setup_db.py:

	python3 setup_db.py

### Running the server

run the following command to start the server:

        python3 main.py

and open this link in the browser: http://localhost:2005

*If you open anything else (e.g. 0.0.0.0:2005) ,The login won't work
because google does not accept IPs as origins


### About

On the main page you can see:
    Restaurants and their Items
    a button to sign in with google
    a button to add another restaurant
    buttons to change restaurants names
    buttons to delete restaurants

## Available APIs

1.to get all Database in JSON format enter the following URL:

_http://localhost:2005/restaurants/JSON_

2.to get data about a specific restaurant

_http://localhost:2005/restaurant-id/JSON_

3.to get data about a specific item

_http://localhost:2005/restaurant-id/item-id/JSON_

