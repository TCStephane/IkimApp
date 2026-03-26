"""import sqlite3
from config import DB_PATH

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db():
    with open("database/schema.sql", "r") as file:
        schema = file.read()

    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()


def execute_query(query, params=None):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def fetch_one(query, params=None):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

def fetch_all(query, params=None):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

def commit_changes():
    pass"""
