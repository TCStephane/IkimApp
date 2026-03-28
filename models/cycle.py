import datetime
from database.db_connection import DB_CONNECTION, DB_CURSOR

class CycleManager:

    
    def regenerate_schedule():
        """
        Automates the Ikimina 'Merry-Go-Round' schedule for a 12-month period.
        Call this whenever a member is added or removed.
        """
        try:
            # 1. Get all members (Ordered by join date to keep the 'queue' fair)
            DB_CURSOR.execute("SELECT member_id, member_name FROM members ORDER BY date_added ASC")
            members = DB_CURSOR.fetchall()
            
            if not members:
                print("[!] No members found. Cannot generate schedule.")
                return

            total_members = len(members)
            current_date = datetime.date.today()
            
            # 2. Clear future cycles that haven't been 'paid out' yet
            # This allows a fresh start for the new member count
            DB_CURSOR.execute("DELETE FROM cycle_beneficiaries WHERE received_funds = 0")
            DB_CURSOR.execute("DELETE FROM cycles WHERE start_date >= %s", (current_date,))
            
            print(f"--- Regenerating 12-Month Schedule for {total_members} members ---")

            # 3. Generate 12 Monthly Slots
            for i in range(12):
                # Calculate month offset
                # This handles month rollover (e.g., month 13 becomes January next year)
                start_of_month = (current_date.replace(day=1) + datetime.timedelta(days=32 * i)).replace(day=1)
                end_of_month = (start_of_month + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
                
                cycle_name = start_of_month.strftime("%B %Y")
                
                # Assign member using Modulo (%) logic
                # If 4 members, index 0, 4, and 8 all point to the same member
                member_to_benefit = members[i % total_members]
                
                # Insert into 'cycles'
                DB_CURSOR.execute(
                    "INSERT INTO cycles (cycle_name, start_date, end_date) VALUES (%s, %s, %s)",
                    (cycle_name, start_of_month, end_of_month)
                )
                new_cycle_id = DB_CURSOR.lastrowid
                
                # Insert into 'cycle_beneficiaries'
                # Note: 'amount' could be a fixed Ikimina contribution or calculated
                DB_CURSOR.execute(
                    "INSERT INTO cycle_beneficiaries (cycle_id, member_id, amount) VALUES (%s, %s, %s)",
                    (new_cycle_id, member_to_benefit['member_id'], 0.00) 
                )

            DB_CONNECTION.commit()
            print("[+] Success: 12-month rotation generated.")

        except Exception as e:
            DB_CONNECTION.rollback()
            print(f"[!] Error regenerating schedule: {e}")

    
    def mark_payout(beneficiary_id):
        """Records when a member actually receives the Ikimina pot."""
        today = datetime.date.today()
        query = """
            UPDATE cycle_beneficiaries 
            SET received_funds = 1, received_date = %s 
            WHERE cycle_benef_id = %s
        """
        try:
            DB_CURSOR.execute(query, (today, beneficiary_id))
            DB_CONNECTION.commit()
            print(f"Payout confirmed for ID {beneficiary_id}")
        except Exception as e:
            print(f"Error marking payout: {e}")

    
    def view_schedule(cls):
        """Displays the upcoming Merry-Go-Round queue with IDs for easy selection."""
        # Added cb.cycle_benef_id to the SELECT for the payout logic
        query = """
            SELECT 
                cb.cycle_benef_id, 
                c.cycle_name, 
                m.member_name, 
                cb.received_funds
            FROM cycles c
            JOIN cycle_beneficiaries cb ON c.cycle_id = cb.cycle_id
            JOIN members m ON cb.member_id = m.member_id
            ORDER BY c.start_date ASC
        """
        
        try:
            DB_CURSOR.execute(query)
            rows = DB_CURSOR.fetchall()
            
            if not rows:
                print("\n[!] No schedule found. Please regenerate.")
                return

            # Adjusted Header to include ID
            print(f"\n{'ID':<6} | {'Month':<18} | {'Beneficiary':<20} | {'Status'}")
            print("-" * 65)

            for row in rows:
                status = "PAID" if row['received_funds'] else "Pending"
                
                # Printing the cycle_benef_id on the far left
                print(
                    f"{row['cycle_benef_id']:<6} | "
                    f"{row['cycle_name']:<18} | "
                    f"{row['member_name']:<20} | "
                    f"{status}"
                )
            print("-" * 65)

        except Exception as e:
            print(f"[!] Error displaying schedule: {e}")

def cycle_menu():
    while True:
        print("\n--- Ikimina Cycle Management ---")
        print("1. View Full 12-Month Schedule")
        print("2. Regenerate Schedule ")
        print("3. Record Payout (Member Received Pot)")
        print("4. Return to Main Menu")

        choice = input("Action: ")

        if choice == "1":
            CycleManager.view_schedule()
        elif choice == "2":
            CycleManager.regenerate_schedule()
        elif choice == "3":
            CycleManager.view_schedule()
            try:
                b_id = int(input("Enter ID from left column to mark as PAID: "))
                CycleManager.mark_payout(b_id)
            except ValueError:
                print("Invalid ID.")
        elif choice == "4":
            break