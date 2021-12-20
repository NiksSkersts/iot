import sqlite3
from sqlite3 import Error
from datetime import datetime

conn = sqlite3.connect("data.db")

def insert(code):
    insert_query = ''' INSERT INTO barcode(code,date) VALUES (?,?)'''
    cur = conn.cursor()
    try:
        cur.execute(insert_query, (code, str(datetime.now().time())))
        conn.commit()
    except Error as e:
        return 0
    return cur.lastrowid


def count():
    data_copy = conn.execute("SELECT max(rowid) from barcode")
    values = data_copy.fetchone()[0]
    return values

def inquiry():
    cur = conn.cursor()
    cur.execute("SELECT * FROM barcode")
    rows = cur.fetchall()
    for row in rows:
        print(row)