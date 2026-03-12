from getpass import getpass
from config import ADMIN_PASSWORD

def login():
    while True:
        if getpass("Enter Admin password: ") == ADMIN_PASSWORD:
            print("Logged in successfully")
            break
        else:
            print("Incorrect password. Try again.")