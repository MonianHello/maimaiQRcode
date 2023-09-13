import sqlite3

conn = sqlite3.connect('user_system.sqlite')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  data TEXT,
                  token TEXT,
                  expiration_time INTEGER
               )''')

conn.commit()
conn.close()
