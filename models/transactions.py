#import modules from other member contrubutions
from datetime import datetime
from database.db_connection import DB_CONNECTION, DB_CURSOR
from models.member import view_members
from services.auth import check_user_credentials, get_current_user
from getpass import getpass

class Contribution:
    """
    Represents a member's financial contribution or payment.
    Handles the data structure and database persistence for transactions.
    """

    def __init__(self, member_id, amount, payment_date, payment_type):
        """Initializes a contribution instance with required transaction details."""
        self.member_id = member_id
        self.amount = amount
        self.payment_date = payment_date
        self.payment_type = payment_type

    def save(self):
        """
        Persists the contribution record to the 'transactions' table.
        Returns:
            bool: True if save is successful, False otherwise.
        """
        query = """
        INSERT INTO transactions (member_id, amount, tx_datetime, transaction_type)
        VALUES (%s, %s, %s, %s)
        """
        params = (self.member_id, self.amount, self.payment_date, self.payment_type)
        try:
            DB_CURSOR.execute(query, params)
            DB_CONNECTION.commit()  # Ensure data is written to the DB
            return True
        except Exception as e:
            # Log the specific error to console for debugging
            print(f"Error saving contribution: {e}")
            return False

def log_payment():
    """
    Orchestrates the UI flow for logging a payment:
    1. Displays members
    2. Validates input
    3. Authenticates the staff member
    4. Saves the record
    """
    print("\n--- Log Member Payment ---")

    # Display list of members to help the user find the correct ID
    view_members()

    # --- Step 1: Member Validation ---
    try:
        member_id = int(input("Enter Member ID to log payment: "))
    except ValueError:
        print("Please enter a valid member ID.")
        return

    # Verify if the member actually exists in the database
    DB_CURSOR.execute("SELECT * FROM members WHERE member_id = %s", (member_id,))
    member = DB_CURSOR.fetchone()
    if not member:
        print("Member not found.")
        return

    # --- Step 2: Amount & Type Validation ---
    try:
        amount = float(input("Enter payment amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid amount.")
        return

    # Map user selection to database-friendly strings
    print("Payment Type:\n1. Savings\n2. Loan Repayment\n3. Interest")
    choice = input("Select option: ")
    payment_mapping = {"1": "Savings", "2": "Loan_repayment", "3": "Interest"}
    payment_type = payment_mapping.get(choice)
    
    if not payment_type:
        print("Invalid option")
        return

    # --- Step 3: Confirmation ---
    print(f"\nConfirm: Save {amount} for {member['member_name']} towards {payment_type}?")
    confirm = input("Enter Y to confirm, N to cancel: ").strip().lower()
    if confirm != "y":
        print("Payment cancelled.")
        return

    # --- Step 4: Security (Password Verification) ---
    # Requires the current logged-in user to re-authenticate before sensitive DB writes
    MAX_ATTEMPTS = 3
    attempts = 0
    current_user = get_current_user()
    
    while attempts < MAX_ATTEMPTS:
        password = getpass(f"Enter password for {current_user} to proceed: ").strip()
        if check_user_credentials(current_user, password):
            break
        else:
            attempts += 1
            print(f"Password incorrect. Attempts left: {MAX_ATTEMPTS - attempts}")

    if attempts == MAX_ATTEMPTS:
        print("Too many failed attempts. Payment not saved.")
        return

    # --- Step 5: Final Execution ---
    contribution = Contribution(
        member_id=member_id,
        amount=amount,
        payment_date=str(datetime.now()),
        payment_type=payment_type
    )
    
    if contribution.save():
        print("Payment recorded successfully.")
    else:
        print("Failed to record payment.")