import sqlite3

conn = sqlite3.connect('dating_bot.db')
cursor = conn.cursor()

# Создаем таблицу пользователей
cursor.execute('''  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tgid TEXT NOT NULL UNIQUE,
    name TEXT,
    location TEXT,
    gender TEXT,
    age INTEGER,
    about TEXT,
    photo TEXT
);''')
cursor.execute('''  CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tgid TEXT NOT NULL,
    gender TEXT,
    age_min INTEGER,
    age_max INTEGER
    
);''')
# cursor.execute(''' DROP TABLE matches''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tgid1 INTEGER NOT NULL,
    type1 TEXT,
    tgid2 INTEGER NOT NULL,
    type2 TEXT
);
''')
conn.commit()

