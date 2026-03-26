from database.db_connection import DB_CONNECTION, DB_CURSOR

#Helper to print a better way
def display_transactions(rows):
    if not row:
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
def view_all_transaction():
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
            (member_id)
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
        DB_CURSOR.execute(query, (member_id))
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
    


#Main Menu
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

def process(choice):
    if choice == 1:
        print("oprion 1")
    elif choice == 2:
        print("oprion 2")
    elif choice == 3:
        print("oprion 3")
    elif choice == 4:
        print("oprion 4")
    