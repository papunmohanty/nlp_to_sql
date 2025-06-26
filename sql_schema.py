# SQLite Database Schema

import sqlite3

# Connection
connection = sqlite3.connect('example.db')

# Cursor
cursor = connection.cursor()

# Create Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    role TEXT NOT NULL
)
''')

# Commit and close
connection.commit()
connection.close()
