import sqlite3
from sqlite3 import Error
import json


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn


def create_user(conn, user):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = """ INSERT INTO user(id,label,class)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()

    return cur.lastrowid


def select_all_users(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def querry(conn, qur):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(qur)

    rows = cur.fetchall()

    return rows


def truncate(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("Delete from user")


database = "./user.db"
conn = create_connection(database)
# with conn:
#     values=('9j1ase',1,123)
#     print(create_user(conn,values))
select_all_users(conn)
# id='65d8'
# result=querry(conn,f"select * from user where id='{id}'")
# print(result)
# truncate(conn)
# select_all_users(conn)
