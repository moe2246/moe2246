import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            password = user_password,
            database = db_name
        )
        print("Connection to MYSQL Successful")
    except Error as e:
        print(f' The error {e} has occured')
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f' The error {e} has occured')

def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f' The error {e} has occured')

def execute_read_row_query(connection, query, params=None):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query, params)
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f' The error {e} has occured')
    finally: cursor.close()
    return result