from getpass import getpass
from config import ADMIN_PASSWORD
import time

def login():
    count = 0
    while True:
        if getpass("Enter Admin password: ") == ADMIN_PASSWORD:
            print("Logged in successfully")
            break
        else:
            if count <= 5:
                print("Incorrect password. Try again.")
                count +=1
            else:
                for i in range(10, 0, -1):
                    print(f"Too many incorrect passwords try again in {i} seconds")
                    time.sleep(1)
                count = 0
            