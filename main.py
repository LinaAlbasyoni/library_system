from database import (
    setup_database, 
    add_book, get_all_books, update_book, delete_book, search_books,
    add_member, get_all_members, update_member, delete_member, search_members,
    borrow_book, get_all_borrowed_books
)

def main():
    setup_database()
    
    while True:
        print("\n--- Library Management System ---")
        print("1. Manage Books")
        print("2. Manage Members")
        print("3. Manage Borrowing")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        
        if choice == '1':
            book_menu()
        elif choice == '2':
            member_menu()
        elif choice == '3':
            borrowing_menu()
        elif choice == '4':
            print("Exiting system.")
            break
        else:
            print("Invalid choice.")

def book_menu():
    while True:
        print("\n--- Book Menu ---")
        print("1. Add | 2. View All | 3. Update | 4. Delete | 5. Search | 6. Back")
        choice = input("Choice: ")
        if choice == '1':
            add_book(input("Title: "), input("Author: "))
        elif choice == '2':
            for b in get_all_books(): print(b)
        elif choice == '3':
            update_book(input("ID: "), input("New Title: "), input("New Author: "))
        elif choice == '4':
            delete_book(input("ID to delete: "))
        elif choice == '5':
            query = input("Search term: ")
            results = search_books(query)
            if results:
                for b in results: print(b)
            else:
                print("Error: No books found.")
        elif choice == '6':
            break

def member_menu():
    while True:
        print("\n--- Member Menu ---")
        print("1. Add | 2. View All | 3. Update | 4. Delete | 5. Search | 6. Back")
        choice = input("Choice: ")
        if choice == '1':
            add_member(input("Name: "), input("Email: "))
        elif choice == '2':
            for m in get_all_members(): print(m)
        elif choice == '3':
            update_member(input("ID: "), input("New Name: "), input("New Email: "))
        elif choice == '4':
            delete_member(input("ID to delete: "))
        elif choice == '5':
            query = input("Search term: ")
            results = search_members(query)
            if results:
                for m in results: print(m)
            else:
                print("Error: No members found.")
        elif choice == '6':
            break

def borrowing_menu():
    print("\n--- Borrowing Menu ---")
    print("1. Check Out Book | 2. View All Borrowed Books")
    choice = input("Choice: ")
    
    if choice == '1':
        book_id = input("Enter Book ID: ")
        member_id = input("Enter Member ID: ")
        borrow_date = input("Enter Borrow Date (YYYY-MM-DD): ")
        return_date = input("Enter Return Date (YYYY-MM-DD): ")
        borrow_book(book_id, member_id, borrow_date, return_date)
    elif choice == '2':
        records = get_all_borrowed_books()
        if records:
            for r in records: print(r)
        else:
            print("No borrowed books found.")

if __name__ == "__main__":
    main()