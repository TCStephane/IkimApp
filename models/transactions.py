from datetime import datetime
from database.db_connection import DB_CONNECTION, DB_CURSOR

class Contribution:
    def __init__(self, member_id, amount, payment_date, payment_type):
        self.member_id = member_id
        #self.cycle_id = cycle_id
        self.amount = amount
        self.payment_date = payment_date
        self.payment_type = payment_type

    def save(self):
        query = """
        insert into transactions (member_id, amount, tx_datetime, transaction_type)
        values (%s, %s, %s, %s)
        """
        params = (self.member_id, self.amount, self.payment_date, self.payment_type)
        try:
            DB_CURSOR.execute(query, params)
            DB_CONNECTION.commit()
            return True
        except Exception as e:
            print(f"Error saving contribution: {e}")
            return False

    @staticmethod
    def get_by_member(member_id):
        query = "SELECT * FROM contributions WHERE member_id = %s"
        try:
            DB_CURSOR.execute(query, (member_id,))
            return DB_CURSOR.fetchone()
        except Exception as e:
            print(f"Error fetching contribution: {e}")
            return None

    @staticmethod
    def get_all():
        query = "SELECT * FROM transactions"
        try:
            DB_CURSOR.execute(query)
            return DB_CURSOR.fetchall()
        except Exception as e:
            print(f"Error fetching contributions: {e}")
            return []

def log_payment():
    print("\n--- Log Member Payment ---")

    try:
        member_id = int(input("Enter Member ID: "))
    except ValueError:
        print("Please enter a valid member ID.")
        return
    
    try:
        DB_CURSOR.execute("SELECT * FROM members WHERE member_id = %s", (member_id,))
        member = DB_CURSOR.fetchone()
    except Exception as e:
        print(f"Error fetching member: {e}")
        return

    if not member:
        print("Member not found.")
        return
    
    try:
        amount = float(input("Enter payment amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid amount.")
        return
    

    print("Payment Type:")
    print("1. Savings")
    print("2. Loan Repayment")
    print("3. Interest")

    choice = input("Select option: ")

    if choice == "1":
        payment_type = "Savings"
    elif choice == "2":
        payment_type = "Loan_repayment"
    elif choice == "3":
        payment_type = "Interest"
    else:
        print("Invalid option")
        return

    contribution = Contribution(
        member_id=member_id,
        amount=amount,
        payment_date=str(datetime.now()),
        payment_type=payment_type
    )

    success = contribution.save()

    if success:
        print("Payment recorded successfully.")
    else:
        print("Failed to record payment.")

    #payments.append(payment)

    #print("Payment recorded successfully.")
