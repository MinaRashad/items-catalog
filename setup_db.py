import sqlite3
print('Setting Up Database...')
conn = sqlite3.connect('restaurant.db')
c = conn.cursor()

print('Making Tables...')

c.execute("""CREATE TABLE "restaurant" (
	"name"	VARCHAR(80) NOT NULL,
	"id"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);""")

c.execute("""CREATE TABLE "menu_item" (
	"name"	VARCHAR(80) NOT NULL,
	"id"	INTEGER NOT NULL,
	"course"	VARCHAR(250),
	"description"	VARCHAR(250),
	"price"	VARCHAR(8),
	"restaurant_id"	INTEGER,
	FOREIGN KEY("restaurant_id") REFERENCES "restaurant"("id"),
	PRIMARY KEY("id")
);""")


print('Inserting an Element into the table...')
c.execute('INSERT INTO restaurant(name) VALUES("Seven o\' Diamonds")')
conn.commit()
rest_id = c.lastrowid
c.execute(
    """INSERT INTO menu_item(name,price,restaurant_id) 
    VALUES("Ultra Cheese Burger", "25$",?)""",[rest_id]
    )
conn.commit()