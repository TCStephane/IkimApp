from datetime import date
from database.db import fetch_one, fetch_all, execute_query

class Contribution:
    def __init__(self, member_id, amount, payment_date, payment_type):
        self.member_id = member_id
        #self.cycle_id = cycle_id
        self.amount = amount
        self.payment_date = payment_date
        self.payment_type = payment_type

    def save(self):
        query = """
        insert into contributions (member_id, amount, payment_date, payment_type)
        values (?, ?, ?, ?)
        """
        params = (self.member_id, self.amount, self.payment_date, self.payment_type)
        execute_query(query, params)

    @staticmethod
    def get_by_member(member_id):
        query = "SELECT * FROM contributions WHERE member_id = ?"
        return fetch_one(query, (member_id,))

    @staticmethod
    def get_all():
        query = "SELECT * FROM contributions"
        return fetch_all(query)

def log_payment():
    print("\n--- Log Member Payment ---")

    try:
        member_id = int(input("Enter Member ID: "))
    except ValueError:
        print("Please enter a valid member ID.")
        return
    
    member = fetch_one("SELECT * FROM members WHERE member_id = ?", (member_id,))
    if not member:
        print("Member not found.")
        return

    try:
        amount = float(input("Enter Payment Amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid Amount")
        return
    #payments = []

    

    print("Payment Type:")
    print("1. Savings")
    print("2. Loan Repayment")
    print("3. Fine")

    choice = input("Select option: ")

    if choice == "1":
        payment_type = "Savings"
    elif choice == "2":
        payment_type = "Loan Repayment"
    elif choice == "3":
        payment_type = "Fine"
    else:
        print("Invalid option")
        return

    contribution = Contribution(
        member_id=member_id,
        amount=amount,
        payment_date=str(date.today()),
        payment_type=payment_type
    )

    success = contribution.save()

    if success:
        print("Payment recorded successfully.")
    else:
        print("Failed to record payment.")

    #payments.append(payment)

    #print("Payment recorded successfully.")
