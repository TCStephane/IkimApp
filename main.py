# main.py IkimApp 
# Entry point for IkimApp
# Handles login, main menu, and calls features from other modules
# Import methods from other modules / group members
from services.auth import login, change_password
from models.cycle import cycle_menu
from services.transaction_history import transaction_menu
from models.member import manage_members_menu
from models.transactions import log_payment
from services.reports import reports_menu

def start_app():
    """ 
    Starts the application.
    1. Prompts the user to login.
    2. Shows the main menu only after successful login.
    """
    login() # Handle user login and stores current logged in user's username to be used across the app
    main_menu() # Show main menu after login passes

def main_menu():
    """
    Displays the main menu and shows respective menu for the user's choice 
    """
    while True:
        # Print main menu options
        print("\n--- Main Menu ---")
        print("1. Manage Members")
        print("2. Record Contribution")
        print("3. Cycle Management")
        print("4. View Report")
        print("5. Transaction History")
        print("6. Change Login Password")
        print("7. Exit")

        # Get user choice
        choice = input("Enter your choice: ").strip()

        # Route user choice to appropriate function
        if choice == "1":
            # Manage members (Add, View, Remove)
            manage_members_menu()  # Function in models/member.py
        elif choice == "2":
            # Log a member contribution/payment
            log_payment()           # Function in models/transactions.py
        elif choice == "3":
            # View or manage cycle status
            cycle_menu()            # Function in models/cycle.py
        elif choice == "4":
            # Placeholder: Generate report (feature to implement)
            reports_menu()
        elif choice == "5":
            # View transaction history
            transaction_menu()      # Function in services/transaction_history.py
        elif choice == "6":
            # Change the password of the currently logged-in user
            change_password()       # Function in services/auth.py
        elif choice == "7":
            # Exit the application gracefully
            print("Exiting IkimApp. Goodbye!")
            break
        else:
            # Invalid option entered
            print("Invalid choice.")

# Run the app if this file is executed directly
if __name__ == "__main__":
    start_app()