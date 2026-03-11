
members = []

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

        choice = input("Choose option: ")

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
if __name__ == "__main__":
    manage_members_menu()
