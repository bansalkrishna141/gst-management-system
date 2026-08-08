import os
import mysql.connector
from mysql.connector import Error

def get_connection():
    password = os.getenv("GST_DB_PASSWORD", "")

    return mysql.connector.connect(
        host=os.getenv("GST_DB_HOST", "localhost"),
        user=os.getenv("GST_DB_USER", "root"),
        password=password,
        database=os.getenv("GST_DB_NAME", "gst_management")
    )

def test_connection():
    try:
        connection = get_connection()
        connection.close()
        return True, "Connected to MySQL successfully."
    except Error as exc:
        return False, str(exc)
