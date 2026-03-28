from datetime import date
from database.db_connection import DB_CONNECTION, DB_CURSOR, execute_query
# Import the CycleManager to handle the automatic rotation logic
from models.cycle import CycleManager 

def add_member():
    """Add a new member and automatically update the Ikimina rotation."""
    print("\n--- Add Member ---")

    name = input("Enter member name: ").strip()
    email = input("Enter member email: ").strip()
    phone = input("Enter member phone: ").strip()
    address = input("Enter physical address: ").strip()

    if not name or not email or not phone or not address:
        print("[!] All fields are required.")
        return

    query = """
    INSERT INTO members (member_name, date_added, email_address, phone_number, physical_address)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (name, date.today(), email, phone, address)

    try:
        success = execute_query(query, params)

        if success:
            print(f"[+] {name} added successfully.")
            # Regenerate the 12-month schedule because the member count changed
            CycleManager.regenerate_schedule()
        else:
            print("[!] Failed to add member.")

    except Exception as e:
        print(f"[!] Error adding member: {e}")

def view_members():
    """Fetch and display ALL members with fresh data."""
    print("\n--- Members List ---")
    query = "SELECT * FROM members ORDER BY member_id ASC"

    try:
        cursor = DB_CONNECTION.cursor(dictionary=True)
        cursor.execute(query)
        members = cursor.fetchall()
        cursor.close()

        if not members:
            print("No members found in the system.")
            return

        print("-" * 85)
        print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Phone':<15} {'Joined'}")
        print("-" * 85)
        for m in members:
            print(
                f"{m['member_id']:<5} "
                f"{m['member_name']:<20} "
                f"{m['email_address']:<25} "
                f"{m['phone_number']:<15} "
                f"{m['date_added']}"
            )
        print("-" * 85)

    except Exception as e:
        print(f"[!] Failed to fetch members: {e}")

def remove_member():
    """Remove a member by ID """ 
    view_members()

    try:
        member_id_input = input("Enter Member ID to remove (or 'c' to cancel): ").strip()
        if member_id_input.lower() == 'c': return
        
        member_id = int(member_id_input)
    except ValueError:
        print("[!] Please enter a valid numeric ID.")
        return

    query = "DELETE FROM members WHERE member_id = %s"

    try:
        success = execute_query(query, (member_id,))

        if success:
            print(f"[+] Member {member_id} removed.")
            # Re-calculate the schedule since a slot is now empty
            CycleManager.regenerate_schedule()
        else:
            print(f"[!] Failed to remove member. ID {member_id} might not exist.")

    except Exception as e:
        print(f"[!] Error: Could not remove member. They might have transaction history.")

def manage_members_menu():
    """Admin Menu for Member Management."""
    while True:
        print("\n--- Manage Members ---")
        print("1. Add New Member (Auto-updates Schedule)")
        print("2. View Current Members")
        print("3. Remove Member (Auto-updates Schedule)")
        print("4. Return to Admin Menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_member()
        elif choice == "2": 
            view_members()
        elif choice == "3": 
            remove_member()
        elif choice == "4":
            break
        else:
            print("[!] Invalid choice, try again.")