def transaction_menu():
    while True:
        print("\n------Transaction History------\n")
        try:
            choice  = int(input("Do you want to\n1.view all transactions\n2.View transactions of a specific person\n3.view transaction of a specific cycle\n4.view transaction of a specific person at aspecific time\n5.Back\n"))
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
    
menu()