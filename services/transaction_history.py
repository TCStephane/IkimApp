#import required modules
from database.db_connection import DB_CONNECTION, DB_CURSOR
from datetime import datetime
from models.member import view_members


def display_transactions(rows):
    """
    Formally displays transaction data in a tabular format.
    Ensures 'amount' is formatted to two decimal places.
    """
    if not rows:
        print("\n[!] No transactions found for this selection.")
        return

    # Header Definition
    print("\n" + "-" * 76)
    print(f"{'ID':<6} {'Member':<20} {'Amount':>10} {'Type':<18} {'Date & Time':<20}")
    print("-" * 76)

    # Data Rows
    for row in rows:
        print(
            f"{row['transaction_id']:<6} "
            f"{row['member_name']:<20} "
            f"{row['amount']:>10.2f} "
            f"{row['transaction_type']:<18} "
            f"{str(row['tx_datetime']):<20}"
        )

    print("-" * 76)
    print(f"Total transactions shown: {len(rows)}\n")


def view_all_transactions():
    """Fetches every transaction in the system, newest first."""
    query = """
        SELECT t.transaction_id, m.member_name, t.amount, t.transaction_type, t.tx_datetime
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        ORDER BY t.tx_datetime DESC
    """
    try:
        DB_CURSOR.execute(query)
        display_transactions(DB_CURSOR.fetchall())
    except Exception as e:
        print(f"Error fetching transactions: {e}")


def view_transactions_by_member():
    """Filters transactions based on a specific Member ID."""
    try:
        member_id = int(input("Enter Member ID: "))
        
        # Verify member exists and get name
        DB_CURSOR.execute("SELECT member_name FROM members WHERE member_id = %s", (member_id,))
        member = DB_CURSOR.fetchone()
        
        if not member:
            print(f"Member ID {member_id} not found.")
            return

        print(f"\n>> History for: {member['member_name']}")
        
        query = """
            SELECT t.transaction_id, m.member_name, t.amount, t.transaction_type, t.tx_datetime
            FROM transactions t
            JOIN members m ON t.member_id = m.member_id
            WHERE t.member_id = %s
            ORDER BY t.tx_datetime DESC
        """
        DB_CURSOR.execute(query, (member_id,))
        display_transactions(DB_CURSOR.fetchall())
    except ValueError:
        print("Invalid ID. Please enter a number.")
    except Exception as e:
        print(f"Database error: {e}")


def view_transactions_by_date_range():
    """
    Filters transactions for a member within a specific time period.
    Performs real-time validation for date existence and logical order.
    """
    try:
        #  Validate Member ID
        member_id_input = input("Enter Member ID: ").strip()
        if not member_id_input.isdigit():
            print("[!] Invalid Member ID. Please enter numbers only.")
            return
        member_id = int(member_id_input)

        # Input and Validate Start Date
        start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            print("[!] Invalid Start Date. Use YYYY-MM-DD format (e.g., 2026-01-31).")
            return

        # Input and Validate End Date
        end_date_str = input("Enter end date   (YYYY-MM-DD): ").strip()
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            print("[!] Invalid End Date. Use YYYY-MM-DD format.")
            return

        # Logical Check: Start must be before or equal to End
        if start_date > end_date:
            print(f"[!] Logic Error: Start date ({start_date_str}) cannot be after end date ({end_date_str}).")
            return

        #  Database Query        
        query = """
            SELECT t.transaction_id, m.member_name, t.amount, t.transaction_type, t.tx_datetime
            FROM transactions t
            JOIN members m ON t.member_id = m.member_id
            WHERE t.member_id = %s 
              AND DATE(t.tx_datetime) BETWEEN %s AND %s
            ORDER BY t.tx_datetime ASC
        """
        
        # We pass the original strings (start_date_str) to the SQL driver
        DB_CURSOR.execute(query, (member_id, start_date_str, end_date_str))
        results = DB_CURSOR.fetchall()
        
        display_transactions(results)

    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")

# --- NEW FEATURE: CYCLE BENEFICIARIES ---

def view_cycle_beneficiaries():
    """
    Displays the list of members scheduled to receive funds in a cycle.
    Shows the expected amount vs. actual received funds and date.
    """
    print("\n--- Cycle Beneficiary List ---")
    
    # SQL Query based on the cycle_beneficiaries table columns
    query = """
        SELECT 
            cb.cycle_benef_id,
            cb.cycle_id,
            m.member_name,
            cb.amount,
            cb.received_funds,
            cb.received_date
        FROM cycle_beneficiaries cb
        JOIN members m ON cb.member_id = m.member_id
        ORDER BY cb.cycle_id ASC, cb.cycle_benef_id ASC
    """
    
    try:
        DB_CURSOR.execute(query)
        rows = DB_CURSOR.fetchall()

        if not rows:
            print("[!] No beneficiary records found.")
            return

        # Table Header
        print("-" * 95)
        print(f"{'ID':<6} {'Cycle':<8} {'Member Name':<20} {'Expected':>10} {'Received':>10} {'Date Received':<15}")
        print("-" * 95)

        for row in rows:
            # Format 'None' or null dates and funds for cleaner reading
            received_amt = f"{row['received_funds']:>10.2f}" if row['received_funds'] is not None else f"{'Pending':>10}"
            received_dt = str(row['received_date']) if row['received_date'] else "Not Paid"

            print(
                f"{row['cycle_benef_id']:<6} "
                f"{row['cycle_id']:<8} "
                f"{row['member_name']:<20} "
                f"{row['amount']:>10.2f} "
                f"{received_amt} "
                f"{received_dt:<15}"
            )
        print("-" * 95)

    except Exception as e:
        print(f"[!] Error fetching beneficiaries: {e}")


def transaction_menu():
    """
    Main interface for Transaction and Beneficiary History.
    """
    while True:
        print("\n========= Transaction History Menu =========")
        print("1. View All Transactions")
        print("2. Filter by Specific Member")
        print("3. Filter by Member & Date Range") 
        print("4. View Cycle Beneficiaries") # <-- New Entry
        print("5. Back to Main Menu") 
        
        choice = input("Select an option: ").strip()

        if choice == "1":
            view_all_transactions()
        elif choice == "2":
            view_members() # show the member list so admin can select the right ID
            view_transactions_by_member()
        elif choice == "3":
            view_members() # show the member list so admin can select the right ID
            view_transactions_by_date_range() 
        elif choice == "4":
            view_cycle_beneficiaries()
        elif choice == "5":
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice. Please select 1-5.")
