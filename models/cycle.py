import datetime

class Cycle: 
    def __init__(self, cycle_id, start_date, end_date, recipient_id=None):
        self.cycle_id = cycle_id
        self.start_date = start_date
        self.end_date = end_date
        self.recipient_id = recipient_id

    def __str__(self):
        recipient = CycleManager.members.get(self.recipient_id, "Not assigned")
        return (f"Cycle ID: {self.cycle_id} | Start: {self.start_date} | "
                f"End: {self.end_date} | Recipient: {recipient}")

class CycleManager:     
    # Mock Database - will be replaced by DB queries later
    cycles = [
        Cycle(1, "2026-03-01", "2026-03-07", 101),
        Cycle(2, "2026-03-08", "2026-03-14", 102),
    ]

    members = {
        101: "Alice",
        102: "Bob",
        103: "Charlie",
        104: "Diana"
    }

    @classmethod
    def start_new_cycle(cls):
        new_id = len(cls.cycles) + 1
        # Simple date logic for demonstration
        new_cycle = Cycle(new_id, "2026-03-15", "2026-03-21")
        cls.cycles.append(new_cycle)
        print(f"Successfully created Cycle ID {new_id}")

    @classmethod
    def get_current_cycle(cls):
        if not cls.cycles:
            print("No cycles found.")
            return None
        current = cls.cycles[-1]
        print(f"--- Current Status ---\n{current}")
        return current

    @classmethod
    def update_recipient(cls, member_id):
        if member_id not in cls.members:
            print(f"Error: Member ID {member_id} does not exist.")
            return

        current = cls.cycles[-1]
        current.recipient_id = member_id
        print(f"Recipient updated to {cls.members[member_id]} for Cycle {current.cycle_id}")

    @classmethod
    def get_cycle_history(cls):
        print("\n--- Full Cycle History ---")
        for c in cls.cycles:
            print(c)

def cycle_menu():
    """UI Controller for Cycle operations"""
    manager = CycleManager()
    
    while True:
        print("\n--- Cycle Management ---")
        print("1. Start New Cycle")
        print("2. View Current Cycle")
        print("3. Assign Recipient")
        print("4. View All History")
        print("5. Return to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            manager.start_new_cycle()
        elif choice == "2":
            manager.get_current_cycle()
        elif choice == "3":
            try:
                m_id = int(input("Enter member ID: "))
                manager.update_recipient(m_id)
            except ValueError:
                print("Invalid input! Please enter a numeric ID.")
        elif choice == "4":
            manager.get_cycle_history()
        elif choice == "5":
            break
        else:
            print("Invalid selection.")