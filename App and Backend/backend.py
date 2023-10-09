from flask import Flask, jsonify
from flask import request
from flask import Response
from flask_cors import CORS
from pprint import pprint
import json
import os
import threading
import time
import sqlite3
from sqlite3 import Error
import subprocess


app = Flask(__name__)
CORS(app)


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


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


def task(uid, label):
    proc = subprocess.Popen(
        ["python", "worker.py", str(uid), str(label)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(proc.communicate()[0])


database = "./user.db"


@app.route("/", methods=["GET"])
def printstuff():
    return jsonify(
        greeting=["hello", "world"],
    )


@app.route("/id/<id>", methods=["GET"])
def validateId(id):
    conn = create_connection(database)
    results = querry(conn, f"select * from user where id='{id}'")
    if len(results) > 0:
        results = results[0]
        if id == results[0]:
            print("ok")
            return json.dumps({"id": results[0], "class": results[2]}), 200
    return json.dumps({"id": -1, "class": "-1"}), 200


@app.route("/audio", methods=["POST"])
def process_audio():
    data = request.get_data()
    data_length = request.content_length
    if data_length > 1024 * 1024 * 10:
        return "File too large!", 400
    jsonData = json.loads(request.headers["New"])
    print(jsonData)
    if jsonData["tno"] == 0:
        if not os.path.exists(jsonData["uid"]):
            os.makedirs(jsonData["uid"])
        filename = str(jsonData["uid"]) + "/"
        if jsonData["p"] == "ios":
            with open(filename + "cmd.wav", "wb") as binary_file:
                binary_file.write(data)
        if jsonData["p"] == "android":
            with open(filename + "cmd.mp3", "wb") as binary_file:
                binary_file.write(data)
        from checker import identification

        res, op = identification(jsonData["uid"], 1)
        if res == True:
            return (
                json.dumps({"text": "Authenticated", "col": "green", "output": op}),
                200,
            )
        else:
            return (
                json.dumps({"text": "Not Authenticated", "col": "red", "output": op}),
                200,
            )
    else:
        if jsonData["tno"] == 1:
            os.mkdir(jsonData["uid"])

        # process data here:
        filename = str(jsonData["uid"]) + "/" + str(jsonData["tno"])
        if jsonData["p"] == "ios":
            with open(filename + ".wav", "wb") as binary_file:
                binary_file.write(data)
        if jsonData["p"] == "android":
            with open(filename + ".mp3", "wb") as binary_file:
                binary_file.write(data)
        if jsonData["tno"] == 10:
            threading.Thread(
                target=task, args=(jsonData["uid"], 1), daemon=True, name="Monitor"
            ).start()
            return (
                json.dumps({"text": "Learning started please wait before testing"}),
                200,
            )
    return json.dumps({"text": "Audio successfully processed!"}), 200
