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
        ssl_disabled =CONN_SSL_DISABLED,
        autocommit=True # create mnew connection each time
    )


#connection manager
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=CONN_HOST,
            port=CONN_PORT,
            user=CONN_USER,
            password=CONN_PASS,
            database=CONN_DB_NAME,
            ssl_disabled=CONN_SSL_DISABLED
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None
    

#execute query
def execute_query(query, params=None):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False
    
#fetch one
def fetch_one(query, params=None):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None
    

#fetch all
def fetch_all(query, params=None):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return []
#dictionary=True allows for us to access fields by their column names and not indexes. 
# e.g cycles['start_date'] is easier to read than cycles[0]
DB_CURSOR = DB_CONNECTION.cursor(dictionary=True)