from getpass import getpass
from database.db_connection import DB_CURSOR
import hashlib   # Used to convert password to MD5
import time


def check_user_credentials(username, password):
    """
    Check if the username and password pair exists in the database.
    The password is converted to MD5 before checking.
    MD5 Helps obscure /encrpty the password so it is not plain 'english' text
    """

    # Ensure user entered both fields
    if not username or not password:
        return False

    # Convert the input password to MD5
    md5_password = hashlib.md5(password.encode()).hexdigest()

    # Query database for matching username and password
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    DB_CURSOR.execute(query, (username, md5_password))

    # Fetch one matching record
    user = DB_CURSOR.fetchone()

    # Return True if user exists, else False
    return True if user else False


def login():
    """
    Prompt user to login until correct credentials are entered.
    Adds delay after 3 failed attempts.
    """

    attempts = 0  # Track failed attempts

    while True:
        print("\n--- User Login ---")
        # Get user input
        username = input("Enter username: ")
        password = getpass("Enter password: ")

        # Check credentials
        if check_user_credentials(username, password):
            print("Login successful!")
            break
        else:
            print("Invalid username or password.")
            attempts += 1

        # If 3 failed attempts, add delay
        if attempts >= 3:
            print("\nToo many failed attempts. Please wait...")

            for i in range(5, 0, -1):
                print(f"Try again in {i} seconds...")
                time.sleep(1)

            # Reset attempts after delay
            attempts = 0