# importing some standard modules
import sqlite3
import requests
import json
from flask import Flask, render_template
from flask import request, redirect, url_for, flash, jsonify
app = Flask(__name__)


# this Function will get the sign in token
# info by using google API

def getTokenInfo(Token):
    res = requests.get(
        'https://oauth2.googleapis.com/tokeninfo?id_token=' +
        Token)
    return res.json()

# Here we know if the restaurant is owened by some user


def isOwnedBy(restaurant, token_id):
    owner = getTokenInfo(restaurant[2])
    claimer = getTokenInfo(token_id)
    if 'email' in owner.keys() and 'email' in claimer.keys():
        if owner['email'] == claimer['email']:
            return True

    return False


"""
Restaurants table by row number:
        0 > Name
        1 > id
        2 > user_token
items table by row number:
        0 > name
        1 > id
        2 > category
        3 > description
        4 > price
        5 > restaurant_id
"""
'MAIN PAGE'
'READ'

# The main page
# an overview for all restaurants


@app.route('/')
@app.route('/restaurants')
def restaurants():

    conn = sqlite3.connect('./restaurant.db')
    c = conn.cursor()
    c.execute('select * from restaurant ')
    renstaurants = c.fetchall()
    c.execute('select * from menu_item ')
    items = c.fetchall()
    return render_template('overview.html',
                           restaurants=renstaurants,
                           items=items)
# CRUD system


'Create'


@app.route('/new', methods=['GET', 'POST'])
def newRestaurant():
    # we need first to check if
    # user is logged in
    if 'idtoken' in request.cookies.keys() and \
            request.cookies['idtoken'] != 'none':

        if request.method == 'GET':
            return render_template('newRestaurant.html')
        elif request.method == 'POST':
            newRest = request.form['name']
            conn = sqlite3.connect('./restaurant.db')
            c = conn.cursor()
            # Assign the token to the restaurant
            # for later Authentication
            c.execute('INSERT INTO restaurant(name,user_token) \
                VALUES (?,?);', [newRest, request.cookies['idtoken']])
            conn.commit()
            return redirect(
                url_for('getRestaurant', restaurant_id=c.lastrowid)
            )
    else:
        flash('You can not edit the Database. Please Sign in')
        return redirect(url_for('restaurants'))


'UPDATE'


@app.route('/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if 'idtoken' in request.cookies.keys():
        conn = sqlite3.connect('./restaurant.db')
        c = conn.cursor()
        c.execute('SELECT * from restaurant\
                    where id=?', [restaurant_id])
        restaurant = c.fetchone()
        if isOwnedBy(restaurant, request.cookies['idtoken']):
            # if it is a GET, we need to show an HTML
            if request.method == 'GET':
                return render_template(
                    'editRestaurant.html', restaurant=restaurant
                )
            # or else we update the DB
            elif request.method == 'POST':
                restaurantName = request.form['name']
                c.execute('UPDATE restaurant \
                    SET name = ?\
                    WHERE id = ?', [restaurantName, restaurant_id])
                conn.commit()
                return redirect(url_for('restaurants'))
        else:
            flash('You can only edit data you created!')
            return redirect(url_for('restaurants'))
    else:
        flash('You can not edit the Database. Please Sign in')
        return redirect(url_for('restaurants'))


'DELETE'


@app.route('/<int:restaurant_id>/del', methods=['POST', 'GET'])
def delRestaurant(restaurant_id):
    if 'idtoken' in request.cookies.keys():
        conn = sqlite3.connect('./restaurant.db')
        c = conn.cursor()
        c.execute('SELECT * from restaurant\
                where id=?', [restaurant_id])
        restaurant = c.fetchone()
        if isOwnedBy(restaurant, request.cookies['idtoken']):
            if request.method == 'GET':

                return render_template('delRestaurant.html',
                                       restaurant=restaurant)
            elif request.method == 'POST':
                c.execute('DELETE from restaurant\
                    where id=?', [restaurant_id])
                c.execute('DELETE from menu_item\
                    where restaurant_id=?', [restaurant_id])
                conn.commit()
                return redirect(url_for('restaurants'))
        else:
            flash('You can only delete data you created!')
            return redirect(url_for('restaurants'))
    else:
        flash('You can not edit the Database. Please Sign in')
        return redirect(url_for('restaurants'))


'RESTAURANT PAGE'
# this will show the restaurant
# and all its items


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/<int:restaurant_id>')
def getRestaurant(restaurant_id):
    if 'idtoken' in request.cookies.keys():
        conn = sqlite3.connect('./restaurant.db')
        c = conn.cursor()
        c.execute('select * from restaurant where id = ?', [restaurant_id])
        restaurantDB = c.fetchall()
        c.execute('select * from menu_item where restaurant_id=?',
                  [restaurant_id])
        items = c.fetchall()
        if len(restaurantDB) == 1:
            restaurant = restaurantDB[0]
            return render_template(
                'menu.html', restaurant=restaurant, items=items
            )
        else:
            return '<h1>404</h1>'
    else:
        flash('You can not edit the Database. Please Sign in')
        return redirect(url_for('restaurants'))


'CREATING NEW ITEM PAGE'


@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET', 'POST'])
@app.route('/<int:restaurant_id>/new',  methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if 'idtoken' in request.cookies.keys() and \
            request.cookies['idtoken'] != 'none':
        conn = sqlite3.connect('./restaurant.db')
        c = conn.cursor()
        c.execute('SELECT * from restaurant\
                    where id=?', [restaurant_id])
        restaurant = c.fetchone()
        if isOwnedBy(restaurant, request.cookies['idtoken']):
            if request.method == 'POST':

                newItem = [
                    restaurant_id,
                    request.form['name'],
                    request.form['price'],
                    request.form['description']
                ]

                c.execute('INSERT INTO menu_item\
                    (restaurant_id,name,price,description)\
                    VALUES (?,?,?,?);', newItem)
                conn.commit()

                flash("item was created Successfully!")

                return redirect(
                    url_for(
                        'getRestaurant', restaurant_id=restaurant_id
                    )
                )
            elif request.method == 'GET':
                return render_template(
                    'newItem.html', restaurant_id=restaurant_id
                )
        else:
            flash('You can only edit data you created!')
            return redirect(url_for('restaurants'))

    else:
        flash('You can not edit the Database. Please Sign in')
        return redirect(url_for('restaurants'))


'EDITING AN ITEM PAGE'

# Editing an item


@app.route(
    '/restaurant/<int:restaurant_id>/<int:item_id>/edititem',
    methods=['POST', 'GET']
)
@app.route(
    '/<int:restaurant_id>/<int:item_id>/editmenu',
    methods=['POST', 'GET']
)
def editMenuItem(restaurant_id, item_id):
    if 'idtoken' in request.cookies.keys():
        conn = sqlite3.connect('./restaurant.db')
        c = conn.cursor()
        c.execute('SELECT * from restaurant\
                    where id=?', [restaurant_id])
        restaurant = c.fetchone()
        if isOwnedBy(restaurant, request.cookies['idtoken']):

            if request.method == 'GET':
                c.execute('SELECT * FROM menu_item\
                    WHERE id=?', [item_id])
                item = c.fetchone()
                return render_template(
                    'editItem.html',
                    restaurant_id=restaurant_id, MenuItem=item)
            elif request.method == 'POST':
                item = [request.form['name'],
                        request.form['price'],
                        request.form['description'],
                        item_id]

                c.execute('UPDATE menu_item \
                    SET name = ?, price=?,\
                    description =?   \
                    WHERE id = ?', item)
                conn.commit()
                flash("item was edited Successfully!")

                return redirect(
                    url_for('getRestaurant', restaurant_id=restaurant_id))
        else:
            flash('You can only edit data you created!')
            return redirect(url_for('restaurants'))
    else:
        flash('You can not edit the Database. Please Sign in')
        return redirect(url_for('restaurants'))


'DELETING AN ITEM PAGE'


@app.route(
    '/restaurant/<int:restaurant_id>/<int:item_id>/delitem',
    methods=['POST', 'GET']
)
@app.route(
    '/<int:restaurant_id>/<int:item_id>/delitem',
    methods=['POST', 'GET']
)
def deleteMenuItem(restaurant_id, item_id):
    if 'idtoken' in request.cookies.keys():
        conn = sqlite3.connect('./restaurant.db')
        c = conn.cursor()
        c.execute('SELECT * from restaurant\
                    where id=?', [restaurant_id])
        restaurant = c.fetchone()
        if isOwnedBy(restaurant, request.cookies['idtoken']):
            if request.method == 'GET':
                c.execute('select * from menu_item \
                    where id=?', [item_id])
                item = c.fetchone()
                return render_template(
                    'delmenuitem.html', item=item, restaurant_id=restaurant_id)
            elif request.method == 'POST':
                c.execute('DELETE FROM menu_item \
                    where id =?', [item_id])
                conn.commit()
                flash("item was deleted Successfully!")
                return redirect(
                    url_for('getRestaurant', restaurant_id=restaurant_id))
        else:
            flash('You can only delete data you created!')
            return redirect(url_for('restaurants'))
    else:
        flash('You can not edit the Database. Please Sign in')
        return redirect(url_for('restaurants'))


'login handling'


@app.route('/signin', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return redirect(url_for('restaurants'))
    elif request.method == 'POST':
        idinfo = getTokenInfo(request.cookies['idtoken'])
        try:
            if 'error' in idinfo.keys():
                raise ValueError('Invalid token')

            elif idinfo['iss'] not in \
                    ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            # I will leave it like this in case i want to
            # add more client IDs
            elif idinfo['azp'] not in \
                    [('660832907745-97560tbqo9knj00pd16n64e4lvnk3rm8' +
                      '.apps.googleusercontent.com')]:
                raise ValueError('Wrong Client ID.')
            # ID token is valid.
            # Get the user's Google Account ID from the decoded token.

            else:
                return idinfo['name']
        except ValueError:
            pass


'logout handling'


@app.route('/signout')
def signout():
    return "You are now not logged in"


'JSON format'


@app.route('/restaurants/JSON')
def JSONoverview():
    conn = sqlite3.connect('./restaurant.db')
    c = conn.cursor()
    restaurants = []

    """
    getting All restaurants and putting
    them into an array of objects
    """
    c.execute('SELECT * FROM restaurant')
    counter = 0
    for rest in c.fetchall():
        restaurants.append(
            {
                'id': rest[1],
                'name': rest[0],
                'items': []
            }
        )
        counter += 1
    """
    Now we get all items and go through
    all of them to see which item is in which
    restaurant
    """
    counter = 0
    c.execute('SELECT * FROM menu_item')
    items = c.fetchall()
    for rest in restaurants:
        for item in items:
            if item[5] == restaurants[counter]['id']:
                restaurants[counter]["items"].append(
                    {
                        'id': item[1],
                        'name': item[0],
                        'category': item[2],
                        'description': item[3],
                        'price': item[4]
                    }
                )
        counter += 1

    return jsonify(restaurants)


@app.route('/<int:restaurant_id>/JSON')
def JSONmenu(restaurant_id):
    conn = sqlite3.connect('./restaurant.db')
    c = conn.cursor()
    c.execute('SELECT * from restaurant\
        where id=?', [restaurant_id])
    restaurant = {
        'name': c.fetchone()[0],
        'items': []
    }
    c.execute('SELECT * from menu_item\
        where restaurant_id=?',
              [restaurant_id])
    itemsDB = c.fetchall()
    for item in itemsDB:
        restaurant['items'].append(
            {
                'name': item[0],
                'description': item[3],
                'category': item[2],
                'price': item[4]
            }
        )
    return jsonify(restaurant)


@app.route('/<int:restaurant_id>/<int:item_id>/JSON')
def JSONitem(restaurant_id, item_id):
    conn = sqlite3.connect('./restaurant.db')
    c = conn.cursor()
    c.execute('SELECT * from menu_item\
        where id=?', [item_id])
    itemDB = c.fetchone()
    item = {
        'name': itemDB[0],
        'description': itemDB[3],
        'category': itemDB[2],
        'price': itemDB[4],
    }
    return jsonify(item)


if __name__ == "__main__":
    app.secret_key = 'S3Cr3T_pAsS'
    app.debug = True
    app.run('0.0.0.0', port=2005)
