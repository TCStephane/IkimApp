from datetime import date
from database.db_connection import DB_CONNECTION,DB_CURSOR, execute_query


def add_member():
    """Add a new member to the database"""

    print("\n--- Add Member ---")

    # Collect user input
    name = input("Enter member name: ").strip()
    email = input("Enter member email: ").strip()
    phone = input("Enter member phone: ").strip()
    address = input("Enter physical address: ").strip()

    # Validate input
    if not name or not email or not phone or not address:
        print("All fields are required.")
        return

    # SQL query
    query = """
    INSERT INTO members (member_name, date_added, email_address, phone_number, physical_address)
    VALUES (%s, %s, %s, %s, %s)
    """

    params = (name, date.today(), email, phone, address)

    try:
        success = execute_query(query, params)

        if success:
            print("Member added successfully.")
        else:
            print("Failed to add member.")

    except Exception as e:
        print(f"Error adding member: {e}")

def view_members():
    """
    Fetch and display ALL members.
    Uses a fresh cursor each time to ensure up-to-date data.
    """

    print("\n--- Members ---")

    query = "SELECT * FROM members"

    try:
        #Create a NEW cursor (ensures fresh data from DB)
        cursor = DB_CONNECTION.cursor(dictionary=True)
        # Execute query
        cursor.execute(query)

        # Fetch results
        members = cursor.fetchall()

        # Close cursor after use (good practice)
        cursor.close()

    except Exception as e:
        print(f"Failed to fetch members: {e}")
        return

    # If no records found
    if not members:
        print("No members found.")
        return

    # Display members
    for member in members:
        print(
            f"ID: {member['member_id']} | "
            f"Name: {member['member_name']} | "
            f"Email: {member['email_address']} | "
            f"Phone: {member['phone_number']} | "
            f"Date Added: {member['date_added']}"
        )

from database.db_connection import DB_CONNECTION, execute_query

def remove_member():
    """Remove a member by ID""" 
    view_members()

    try:
        member_id = int(input("Enter Member ID to remove: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    query = "DELETE FROM members WHERE member_id = %s"

    try:
        # Execute delete
        success = execute_query(query, (member_id,))

        if success:
            print("Member removed successfully.")

            #Show updated list for user to see the current list
            print("\nUpdated member list:")
            view_members()

        else:
            print("Failed to remove member.")

    except Exception as e:
        print(f"Error removing member: {e}")

def manage_members_menu():
    """ 
    Each action calls functions that fetch fresh data from DB.
    """

    while True:
        print("\n--- Manage Members ---")
        print("1. Add Member")
        print("2. View Members")
        print("3. Remove Member")
        print("4. Return to Admin Menu")

        choice = input("Choose option you want: ")

        if choice == "1":
            add_member()

        elif choice == "2": 
            view_members()

        elif choice == "3": 
            remove_member()

        elif choice == "4":
            print("Returning to Admin Menu...")
            break

        else:
            print("Invalid choice, try again.")
