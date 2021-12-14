import sqlite3
from sqlite3 import Error
from datetime import datetime

testset = set()
testset.add("hallo")
testset.add("this")
testset.add("is")
testset.add("a")
testset.add("test")

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

set = testset
for code in set:
    row = insert(code)
    print(row)
inquiry()
conn.close()
