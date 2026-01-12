import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",          # put your MySQL password if you have one
        database="login_db",
        port=3306
    )
