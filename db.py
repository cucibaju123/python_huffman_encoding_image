import sqlite3
from sqlite3.dbapi2 import Connection, Cursor


def connect():
    try:
        conn = sqlite3.connect("database.db")
        return conn

    except Exception as e:
        print(e)


def create_table(conn: sqlite3.Connection):
    try:
        cursor = conn.cursor()

        cursor.execute(
            "CREATE TABLE nodes(id integer PRIMARY KEY, symbol text, prob integer)"
        )
        conn.commit()

    except Exception as e:
        print(e)


def insert(conn: sqlite3.Connection, list_of_nodes):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "create table if not exists nodes(id integer primary key, symbol text, prob integer)"
        )
        cursor.executemany(
            "insert into nodes(symbol, prob) values(?, ?)", list_of_nodes
        )
        conn.commit()
    except Exception as e:
        print(e)


def delete(conn: sqlite3.Connection):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "create table if not exists nodes(id integer primary key, symbol text, prob integer)"
        )
        cursor.execute("delete from nodes")
        conn.commit()
    except Exception as e:
        print(e)


def fetch(conn: sqlite3.Connection):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "create table if not exists nodes(id integer primary key, symbol text, prob integer)"
        )
        cursor.execute("select * from nodes")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(e)


def close(conn: sqlite3.Connection):
    try:
        conn.close()
    except Exception as e:
        print(e)
