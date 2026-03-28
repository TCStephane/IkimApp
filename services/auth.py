#import modules from other member contrubutions
from getpass import getpass
from database.db_connection import DB_CONNECTION, DB_CURSOR
import hashlib
import time


# Global variable to track which user is currently logged into the system
CURRENT_USER = None

def set_current_user(username):
    """Updates the global session variable with the logged-in username."""
    global CURRENT_USER
    CURRENT_USER = username

def get_current_user():
    """Retrieves the username of the person currently using the system."""
    return CURRENT_USER


# --- Authentication Logic ---
def check_user_credentials(username, password):
    """
    Validates a username and password against the database.
    Note: Uses MD5 hashing for comparison.
    """
    if not username or not password:
        return False
    
    # Hash the input password to compare it with the stored hash
    md5_password = hashlib.md5(password.encode()).hexdigest()
    
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    DB_CURSOR.execute(query, (username, md5_password))
    user = DB_CURSOR.fetchone()
    
    return True if user else False

def login():
    """
    Handles the interactive login loop.
    Includes a cooling-off period after 3 failed attempts to prevent brute-forcing.
    """
    attempts = 0
    while True:
        print("\n--- User Login ---")
        username = input("Enter username: ").strip()
        password = getpass("Enter password: ").strip() # Masks password input
        
        if check_user_credentials(username, password):
            print("Login successful!")
            set_current_user(username)
            break
        else:
            print("Invalid username or password.")
            attempts += 1
            
        # Security: Rate limiting after multiple failures
        if attempts >= 3:
            print("\nToo many failed attempts. Please wait...")
            for i in range(5, 0, -1):
                print(f"Try again in {i} seconds...")
                time.sleep(1)
            attempts = 0 # Reset attempts after wait period

def change_password():
    """
    Allows the logged-in user to update their password.
    Requires verification of the old password before allowing a change.
    """
    current_user = get_current_user()
    if not current_user:
        print("No user is currently logged in.")
        return False

    print(f"\n--- Change Password for {current_user} ---")
    
    # Verify identity by asking for current password first
    current_password = getpass("Enter current password: ").strip()
    md5_current = hashlib.md5(current_password.encode()).hexdigest()

    try:
        # Use a local cursor for this specific transaction
        cursor = DB_CONNECTION.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (current_user, md5_current))
        user = cursor.fetchone()
        
        if not user:
            print("Current password is incorrect.")
            cursor.close()
            return False

        # Get and validate new password
        new_password = getpass("Enter new password: ").strip()
        confirm_password = getpass("Confirm new password: ").strip()
        
        if new_password != confirm_password:
            print("Passwords do not match.")
            cursor.close()
            return False

        # Hash the new password and update the database
        md5_new = hashlib.md5(new_password.encode()).hexdigest()
        update_query = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(update_query, (md5_new, current_user))
        
        DB_CONNECTION.commit()
        cursor.close()

        print(f"Password changed successfully for {current_user}")
        return True
    except Exception as e:
        print(f"Error changing password: {e}")
        return False