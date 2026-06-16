import re
from database import (
    setup_database, 
    add_book, get_all_books, update_book, delete_book, deactivate_book, search_books,
    add_member, get_all_members, update_member, delete_member, deactivate_member, search_members,
    borrow_book, return_book, get_all_borrowed_books
)

def get_int_input(prompt):
    """Safely gets an integer from the user to prevent crashes."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a number.")

def validate_date(date_text):
    """Checks if date is in DD-MM-YYYY format."""
    # Regex: 2 digits, hyphen, 2 digits, hyphen, 4 digits
    if re.match(r'^\d{2}-\d{2}-\d{4}$', date_text):
        return True
    return False

def validate_email(email):
    """Checks if the email looks like a standard email format."""
    # Regex: checks for text@text.text
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return True
    return False

def main():
    setup_database()
    while True:
        print("\n--- Library Management System ---")
        print("1. Manage Books | 2. Manage Members | 3. Manage Borrowing | 4. Exit")
        choice = input("Select an option (1-4): ")
        if choice == '1': book_menu()
        elif choice == '2': member_menu()
        elif choice == '3': borrowing_menu()
        elif choice == '4': break
        else: print("Invalid choice.")

def book_menu():
    while True:
        print("\n--- Book Menu ---")
        print("1. Add | 2. View | 3. Update | 4. Delete | 5. Deactivate | 6. Search | 7. Back")
        choice = input("Choice: ")
        if choice == '1': add_book(input("Title: "), input("Author: "))
        elif choice == '2': 
            for b in get_all_books(): print(f"ID: {b[0]} ('{b[1]}', '{b[2]}')")
        elif choice == '3': 
            update_book(get_int_input("ID: "), input("Title: "), input("Author: "))
        elif choice == '4': delete_book(get_int_input("ID: "))
        elif choice == '5': deactivate_book(get_int_input("ID to deactivate: "))
        elif choice == '6':
            for b in search_books(input("Search: ")): print(f"ID: {b[0]} ('{b[1]}', '{b[2]}')")
        elif choice == '7': break

def member_menu():
    while True:
        print("\n--- Member Menu ---")
        print("1. Add | 2. View | 3. Update | 4. Delete | 5. Deactivate | 6. Search | 7. Back")
        choice = input("Choice: ")
        if choice == '1': 
            name = input("Name: ")
            email = input("Email: ")
            while not validate_email(email):
                print("Error: Invalid email format.")
                email = input("Email: ")
            add_member(name, email)
        elif choice == '2': 
            for m in get_all_members(): print(f"ID: {m[0]} ('{m[1]}', '{m[2]}')")
        elif choice == '3': 
            update_member(get_int_input("ID: "), input("Name: "), input("Email: "))
        elif choice == '4': 
            delete_member(get_int_input("ID: "))
        elif choice == '5': 
            deactivate_member(get_int_input("ID to deactivate: "))
        elif choice == '6':
            for m in search_members(input("Search: ")): print(f"ID: {m[0]} ('{m[1]}', '{m[2]}')")
        elif choice == '7': break

def borrowing_menu():
    while True:
        print("\n--- Borrowing Menu ---")
        print("1. Check Out | 2. Return | 3. View All | 4. Back")
        choice = input("Choice: ")
        if choice == '1':
            book_id = get_int_input("Book ID: ")
            member_id = get_int_input("Member ID: ")
            
            borrow_date = input("Borrow Date (DD-MM-YYYY): ")
            while not validate_date(borrow_date):
                print("Error: Invalid date format. Use DD-MM-YYYY.")
                borrow_date = input("Borrow Date (DD-MM-YYYY): ")
            
            return_date = input("Return Date (DD-MM-YYYY): ")
            while not validate_date(return_date):
                print("Error: Invalid date format. Use DD-MM-YYYY.")
                return_date = input("Return Date (DD-MM-YYYY): ")
                
            borrow_book(book_id, member_id, borrow_date, return_date)
        elif choice == '2':
            return_book(get_int_input("Enter Loan ID to mark as returned: "))
        elif choice == '3':
            # This displays the tuple returned from database: (LoanID, Title, MemberName, Status)
            for r in get_all_borrowed_books(): print(r)
        elif choice == '4': break

if __name__ == "__main__":
    main()