import datetime
from database.db_connection import DB_CONNECTION, DB_CURSOR  # Import MySQL connection

class Cycle:
    def __init__(self, cycle_id, start_date, end_date, recipient_id=None):
        self.cycle_id = cycle_id
        self.start_date = start_date
        self.end_date = end_date
        self.recipient_id = recipient_id

    def __str__(self):
        recipient_name = CycleManager.get_member_name(self.recipient_id) if self.recipient_id else "Not assigned"
        return (f"Cycle ID: {self.cycle_id} | Start: {self.start_date} | "
                f"End: {self.end_date} | Recipient: {recipient_name}")


class CycleManager:

    @staticmethod
    def get_member_name(member_id):
        """Fetch a member's name from the DB"""
        if not member_id:
            return "Not assigned"
        DB_CURSOR.execute("SELECT member_name FROM members WHERE member_id=%s", (member_id,))
        row = DB_CURSOR.fetchone()
        return row['member_name'] if row else "Unknown"

    @classmethod
    def start_new_cycle(cls):
        """Create a new cycle in the DB"""
        # Simple date logic: start today, end in 7 days
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=6)

        DB_CURSOR.execute(
            "INSERT INTO cycles (cycle_name, start_date, end_date) VALUES (%s, %s, %s)",
            (f"Cycle {start_date}", start_date, end_date)
        )
        DB_CONNECTION.commit()
        new_id = DB_CURSOR.lastrowid
        print(f"Successfully created Cycle ID {new_id}")

    @classmethod
    def get_current_cycle(cls):
        """Fetch the latest cycle from DB"""
        DB_CURSOR.execute("SELECT * FROM cycles ORDER BY cycle_id DESC LIMIT 1")
        row = DB_CURSOR.fetchone()
        if not row:
            print("No cycles found.")
            return None
        current = Cycle(row['cycle_id'], row['start_date'], row['end_date'], cls.get_cycle_recipient(row['cycle_id']))
        print(f"--- Current Status ---\n{current}")
        return current

    @classmethod
    def get_cycle_recipient(cls, cycle_id):
        """Get the recipient (if any) of a cycle from cycle_beneficiaries"""
        DB_CURSOR.execute(
            "SELECT member_id FROM cycle_beneficiaries WHERE cycle_id=%s AND received_funds=0 LIMIT 1",
            (cycle_id,)
        )
        row = DB_CURSOR.fetchone()
        return row['member_id'] if row else None

    @classmethod
    def update_recipient(cls, cycle_id, member_id):
        """Assign a member as recipient for a cycle"""
        # Check if member exists
        DB_CURSOR.execute("SELECT * FROM members WHERE member_id=%s", (member_id,))
        if not DB_CURSOR.fetchone():
            print(f"Error: Member ID {member_id} does not exist.")
            return

        # Insert or update cycle_beneficiaries
        DB_CURSOR.execute(
            "INSERT INTO cycle_beneficiaries (cycle_id, member_id, amount) "
            "VALUES (%s, %s, 0) "
            "ON DUPLICATE KEY UPDATE member_id=%s",
            (cycle_id, member_id, member_id)
        )
        DB_CONNECTION.commit()
        print(f"Recipient updated to {cls.get_member_name(member_id)} for Cycle {cycle_id}")

    @classmethod
    def get_cycle_history(cls):
        """Fetch all cycles and their recipients"""
        DB_CURSOR.execute("SELECT * FROM cycles ORDER BY cycle_id ASC")
        rows = DB_CURSOR.fetchall()
        print("\n--- Full Cycle History ---")
        for row in rows:
            recipient_id = cls.get_cycle_recipient(row['cycle_id'])
            c = Cycle(row['cycle_id'], row['start_date'], row['end_date'], recipient_id)
            print(c)


def cycle_menu():
    """UI Controller for Cycle operations"""
    while True:
        print("\n--- Cycle Management ---")
        print("1. Start New Cycle")
        print("2. View Current Cycle")
        print("3. Assign Recipient")
        print("4. View All History")
        print("5. Return to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            CycleManager.start_new_cycle()
        elif choice == "2":
            CycleManager.get_current_cycle()
        elif choice == "3":
            try:
                cycle_id = int(input("Enter cycle ID: "))
                m_id = int(input("Enter member ID: "))
                CycleManager.update_recipient(cycle_id, m_id)
            except ValueError:
                print("Invalid input! Please enter numeric IDs.")
        elif choice == "4":
            CycleManager.get_cycle_history()
        elif choice == "5":
            break
        else:
            print("Invalid selection.")