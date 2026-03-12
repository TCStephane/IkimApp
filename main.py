from services.auth import login
from models.cycle import Cycle, cycle_menu
from services.transaction_history import transaction_menu
from models.member import manage_members_menu

def start_app():
    login()
    main_menu()

def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Manage Members")
        print("2. Record Contribution")
        print("3. View Cycle Status")
        print("4. Generate Report")
        print("5. Transaction History")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            print("Manage Members - Feature not implemented yet.")
        elif choice == "2":
            print("Record Contribution - Feature not implemented yet.")
        elif choice == "3":
            # This now calls the function in models/cycle.py
            cycle_menu() 
        elif choice == "4":
            # This now calls the function in models/cycle.py
            pass
        elif choice == "5":
            # This now calls the function in services/transaction_history.py
            transaction_menu()

        elif choice == "6":
            print("Exiting IkimApp. Goodbye!")
            break
        else:
            print("Feature not implemented yet or invalid choice.")

if __name__ == "__main__":
    start_app()