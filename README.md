# Item Catalog
## A web application for restaurants Items


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

you will find a file called _requirements.txt_
run this command in the terminal while being the the same directory

        pip3 install -r requirements.txt --user

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

You will not be able to change anything in the Database,
Unless you sign in.