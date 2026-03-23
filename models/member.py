
"""members = []

def add_member(name):
    members.append(name)
    print(name, "added successfully.")

def view_members():
    if len(members) == 0:
        print("No members found.")
    else:
        for i in range(len(members)):
            print(i + 1, "-", members[i])

def remove_member(number):
    if number > 0 and number <= len(members):
        removed = members.pop(number - 1)
        print(removed, "removed successfully.")
    else:
        print("Invalid member number")

def manage_members_menu():
    while True:
        print("\n--- Manage Members ---")
        print("1. Add Member")
        print("2. View Members")
        print("3. Remove Member")
        print("4. Return to Admin Menu")

        choice = input("Choose option you want: ")

        if choice == "1":
            name = input("Enter member name: ")
            add_member(name)

        elif choice == "2":
            view_members()

        elif choice == "3":
            view_members()
            try:
                number = int(input("Enter member number to remove: "))
                remove_member(number)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            print("Returning to Admin Menu...")
            break

        else:
            print("Invalid choice, try again.")

#this one below  run when the file is exuted directly
"""


from datetime import date
from database.db import execute_query, fetch_all


def add_member():
    print("\n--- Add Member ---")
    name = input("Enter member name: ").strip()
    email = input("Enter member email: ").strip()
    phone = input("Enter member phone: ").strip()

    if not name or not email or not phone:
        print("All fields are required.")
        return

    query = """
    INSERT INTO members (member_name, date_added, email, phone)
    VALUES (?, ?, ?, ?)
    """
    params = (name, str(date.today()), email, phone)
    success =execute_query(query, params)
    if success:
        print("Member added successfully.")
    else:
        print("Failed to add member.")

    #print("Member added successfully.")


def view_members():
    print("\n--- Members ---")
    query = "SELECT * FROM members"
    members = fetch_all(query)

    if not members:
        print("No members found.")
        return

    for member in members:
        print(
            f"ID: {member['member_id']} | "
            f"Name: {member['member_name']} | "
            f"Email: {member['email']} | "
            f"Phone: {member['phone']} | "
            f"Date Added: {member['date_added']}"
        )


def remove_member():
    view_members()
    try:
        member_id = int(input("Enter Member ID to remove: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    query = "DELETE FROM members WHERE member_id = ?"
    execute_query(query, (member_id,))
    print("Member removed successfully.")


def manage_members_menu():
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
