from database.db_connection import DB_CONNECTION, DB_CURSOR


# Helper to print transactions in a formatted table
def display_transactions(rows):
    if not rows:
        print("No transactions found.")
        return

    print("\n" + "-" * 76)
    print(f"{'ID':<6} {'Member':<20} {'Amount':>10} {'Type':<18} {'Date & Time':<20}")
    print("-" * 76)

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


# OPTION 1 - View all transactions
def view_all_transactions():
    query = """
        SELECT
            t.transaction_id,
            m.member_name,
            t.amount,
            t.transaction_type,
            t.tx_datetime
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        ORDER BY t.tx_datetime DESC
    """
    try:
        DB_CURSOR.execute(query)
        rows = DB_CURSOR.fetchall()
        display_transactions(rows)
    except Exception as e:
        print(f"Error fetching transactions: {e}")


# OPTION 2 - View transactions for a specific member
def view_transactions_by_member():
    try:
        member_id = int(input("Enter Member ID: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    try:
        DB_CURSOR.execute(
            "SELECT member_name FROM members WHERE member_id = %s",
            (member_id,)
        )
        member = DB_CURSOR.fetchone()
    except Exception as e:
        print(f"Error looking up member: {e}")
        return

    if not member:
        print(f"No member found with ID {member_id}.")
        return

    print(f"\nShowing transactions for: {member['member_name']}")

    query = """
        SELECT
            t.transaction_id,
            m.member_name,
            t.amount,
            t.transaction_type,
            t.tx_datetime
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        WHERE t.member_id = %s
        ORDER BY t.tx_datetime DESC
    """
    try:
        DB_CURSOR.execute(query, (member_id,))
        rows = DB_CURSOR.fetchall()
        display_transactions(rows)
    except Exception as e:
        print(f"Error fetching transactions: {e}")


# OPTION 3 - View transactions within a specific cycle
def view_transactions_by_cycle():
    try:
        cycle_id = int(input("Enter Cycle ID: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    try:
        DB_CURSOR.execute(
            "SELECT cycle_id, cycle_name, start_date, end_date FROM cycles WHERE cycle_id = %s",
            (cycle_id,)
        )
        cycle = DB_CURSOR.fetchone()
    except Exception as e:
        print(f"Error looking up cycle: {e}")
        return

    if not cycle:
        print(f"No cycle found with ID {cycle_id}.")
        return

    print(
        f"\nShowing transactions for: {cycle['cycle_name']} "
        f"({cycle['start_date']} to {cycle['end_date']})"
    )

    query = """
        SELECT
            t.transaction_id,
            m.member_name,
            t.amount,
            t.transaction_type,
            t.tx_datetime
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        WHERE DATE(t.tx_datetime) BETWEEN %s AND %s
        ORDER BY t.tx_datetime ASC
    """
    try:
        DB_CURSOR.execute(query, (cycle['start_date'], cycle['end_date']))
        rows = DB_CURSOR.fetchall()
        display_transactions(rows)
    except Exception as e:
        print(f"Error fetching transactions: {e}")


# OPTION 4 - View transactions for a specific member within a date range
def view_transactions_by_member_and_date():
    try:
        member_id = int(input("Enter Member ID: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    try:
        DB_CURSOR.execute(
            "SELECT member_name FROM members WHERE member_id = %s",
            (member_id,)
        )
        member = DB_CURSOR.fetchone()
    except Exception as e:
        print(f"Error looking up member: {e}")
        return

    if not member:
        print(f"No member found with ID {member_id}.")
        return

    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date   = input("Enter end date   (YYYY-MM-DD): ").strip()

    if len(start_date) != 10 or len(end_date) != 10:
        print("Invalid date format. Use YYYY-MM-DD (e.g. 2026-01-01).")
        return

    print(
        f"\nShowing transactions for {member['member_name']} "
        f"from {start_date} to {end_date}"
    )

    query = """
        SELECT
            t.transaction_id,
            m.member_name,
            t.amount,
            t.transaction_type,
            t.tx_datetime
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        WHERE t.member_id = %s
          AND DATE(t.tx_datetime) BETWEEN %s AND %s
        ORDER BY t.tx_datetime ASC
    """
    try:
        DB_CURSOR.execute(query, (member_id, start_date, end_date))
        rows = DB_CURSOR.fetchall()
        display_transactions(rows)
    except Exception as e:
        print(f"Error fetching transactions: {e}")


# Routes choice to the correct function
def process(choice):
    if choice == 1:
        view_all_transactions()
    elif choice == 2:
        view_transactions_by_member()
    elif choice == 3:
        view_transactions_by_cycle()
    elif choice == 4:
        view_transactions_by_member_and_date()


# Main menu for Transaction History
def transaction_menu():
    while True:
        print("\n---- Transaction History ----")
        try:
            choice = int(input(
                "1. View all transactions\n"
                "2. View transactions of a specific member\n"
                "3. View transactions of a specific cycle\n"
                "4. View transactions of a specific member within a date range\n"
                "5. Back\n"
                "Enter choice: "
            ))
            if choice == 5:
                break
            elif choice < 1 or choice > 5:
                print("Invalid input. Enter a number between 1 and 5.")
            else:
                process(choice)
        except ValueError:
            print("Invalid input. Please enter a number.")