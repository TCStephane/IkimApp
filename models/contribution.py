from datetime import date
"""class Contribution:
    def __init__(self, member_id, cycle_id, amount, date):
        self.member_id = member_id
        self.cycle_id = cycle_id
        self.amount = amount
        self.date = date

    def save(self):
        pass

    @staticmethod
    def get_by_member(member_id):
        pass

    @staticmethod
    def get_all():
        pass"""

def log_payment():
    print("\n--- Log Member Payment ---")

    member_id = input("Enter Member ID: ")
    amount = float(input("Enter Amount: "))
    payments = []

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

    payment = {
        "member_id": member_id,
        "amount": amount,
        "payment_type": payment_type,
        "date": str(date.today())
    }

    payments.append(payment)

    print("Payment recorded successfully.")

log_payment()