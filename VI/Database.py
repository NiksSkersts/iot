import pytz as pytz
import sqlite3
import time
from datetime import datetime, timedelta, tzinfo, timezone
from sqlite3 import Error


# Inserts into database. Converts Human readable date to EPOCH.
def insert(code):
    conn = sqlite3.connect("data.db")
    insert_query = ''' INSERT INTO barcode(code,date) VALUES (?,?)'''
    cur = conn.cursor()
    try:
        current = datetime.now(pytz.timezone("Europe/Riga"))
        # time.mktime converts human-readable datetime to EPOCH.
        ti = time.mktime(current.timetuple())
        cur.execute(insert_query, (code, ti))
        conn.commit()
    except Error as e:
        return -1
    return cur.lastrowid


# Counts the entries in database
def count():
    conn = sqlite3.connect("data.db")
    data_copy = conn.execute("SELECT max(rowid) from barcode")
    values = data_copy.fetchone()[0]
    return values


# selects the rows from database, that gets parsed and used in listing the data.
def inquiry():
    conn = sqlite3.connect("data.db")
    codes_in_database = set(())
    cur = conn.cursor()
    cur.execute("SELECT code, date FROM barcode")
    rows = cur.fetchall()
    for row in rows:
        codes_in_database.add(row)
    return codes_in_database
