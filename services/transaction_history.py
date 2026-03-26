from database.db_connection import DB_CONNECTION, DB_CURSOR

#Helper to print a better way
def display_transactions(rows):
    if not rows:
        print("No transaction found")
        return
    
    print("\n" + "-" * 72)
    print(f"{'ID':<6} {'Member':<20} {'Amount':>10} {'Type':<18} {'Date':<12}")
    print("-" * 72)
 
    for row in rows:
        print(
            f"{row['contribution_id']:<6} "
            f"{row['member_name']:<20} "
            f"{row['amount']:>10.2f} "
            f"{row['payment_type']:<18} "
            f"{str(row['payment_date']):<12}"
        )
 
    print("-" * 72)
    print(f"Total transactions shown: {len(rows)}\n")


# OPTION 1- View all transactions
def view_all_transactions():
    query = """
        SELECT
            c.contribution_id,
            m.member_name,
            c.amount,
            c.payment_type,
            c.payment_date
        FROM contributions c
        JOIN members m ON c.member_id = m.member_id
        ORDER BY c.payment_date DESC
    """
    try:
        DB_CURSOR.execute(query)
        rows = DB_CURSOR.fetchall()
        display_transactions(rows)
    except Exception as e:
        print(f"Error fetching transaction: {e}")

#OPTION 2- View Transactions for one member
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
        print(f"No member found with ID {member_id}")
        return
    
    print(f"\nShowing transaction for: {member['member_name']}")

    query = """
        SELECT
            c.contribution_id,
            m.member_name,
            c.amount,
            c.payment_type,
            c.payment_date
        FROM contributions c
        JOIN members m ON c.member_id = m.member_id
        WHERE c.member_id = %s
        ORDER BY c.payment_date DESC
    """
    try:
        DB_CURSOR.execute(query, (member_id,))
        rows = DB_CURSOR.fetchall()
        display_transactions(rows)
    except Exception as e:
        print(f"Error fetching transactions: {e}")

#OPTION 3- View transactions within a cycle
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
            c.contribution_id,
            m.member_name,
            c.amount,
            c.payment_type,
            c.payment_date
        FROM contributions c
        JOIN members m ON c.member_id = m.member_id
        WHERE c.payment_date BETWEEN %s AND %s
        ORDER BY c.payment_date ASC
    """
    try:
        DB_CURSOR.execute(query, (cycle['start_date'], cycle['end_date']))
        rows = DB_CURSOR.fetchall()
        display_transactions(rows)
    except Exception as e:
        print(f"Error fetching transactions: {e}")

#OPTION 4- Viewing transactions for a member within a specific data range
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
            c.contribution_id,
            m.member_name,
            c.amount,
            c.payment_type,
            c.payment_date
        FROM contributions c
        JOIN members m ON c.member_id = m.member_id
        WHERE c.member_id = %s
          AND c.payment_date BETWEEN %s AND %s
        ORDER BY c.payment_date ASC
    """
    try:
        DB_CURSOR.execute(query, (member_id, start_date, end_date))
        rows = DB_CURSOR.fetchall()
        display_transactions(rows)
    except Exception as e:
        print(f"Error fetching transactions: {e}")


#Main Menu
def process(choice):
    if choice == 1:
        view_all_transactions()
    elif choice == 2:
        view_transactions_by_member()
    elif choice == 3:
        view_transactions_by_cycle()
    elif choice == 4:
        view_transactions_by_member_and_date()

def transaction_menu():
    while True:
        print("\n----Transaction History----")
        try:
            choice  = int(input("Do you want to\n1.view all transactions\n2.View transactions of a specific person\n3.view transaction of a specific cycle\n4.view transaction of a specific person at a specific time\n5.Back\n"))
            if choice == 5:
                break
            elif choice > 5 or choice < 1:
                print("Invalid Input")
            else:
                process(choice)
        except ValueError:
            print("Error Invalid Input. Enter a number in the options")
            continue


    