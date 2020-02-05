import sqlite3
print('Setting Up Database...')
conn = sqlite3.connect('restaurant.db')
c = conn.cursor()

print('Making Tables...')

c.execute("""CREATE TABLE "restaurant" (
"name"	VARCHAR(80) NOT NULL,
"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
"user_token"	TEXT
);""")

c.execute("""CREATE TABLE "menu_item" (
"name"	VARCHAR(80) NOT NULL,
"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
"course"	VARCHAR(250),
"description"	VARCHAR(250),
"price"	VARCHAR(8),
"restaurant_id"	INTEGER,
FOREIGN KEY("restaurant_id") REFERENCES "restaurant"("id")
);""")


print('Database is now ready!')
conn.commit()
