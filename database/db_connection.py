#Import DB Configuration from config.py settings file
from config import CONN_USER, CONN_DB_NAME, CONN_HOST, CONN_PASS, CONN_PORT, CONN_SSL_DISABLED

#Import connection driver library
import mysql.connector

#Create a re-usable database connection
DB_CONNECTION = mysql.connector.connect(
        host = CONN_HOST,
        port =CONN_PORT,
        user=CONN_USER,
        password = CONN_PASS,
        database = CONN_DB_NAME,
        ssl_disabled =CONN_SSL_DISABLED
    )

#create a database cursor
DB_CURSOR = DB_CONNECTION.cursor(dictionary=True)