from database import (
    setup_database, 
    add_book, get_all_books, update_book, delete_book,
    add_member, get_all_members, update_member, delete_member
)

def main():
    setup_database()
    
    while True:
        print("\n--- Library Management System ---")
        print("1. Manage Books")
        print("2. Manage Members")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ")
        
        if choice == '1':
            book_menu()
        elif choice == '2':
            member_menu()
        elif choice == '3':
            print("Exiting system.")
            break
        else:
            print("Invalid choice.")

def book_menu():
    while True:
        print("\n--- Book Menu ---")
        print("1. Add Book | 2. View All | 3. Update | 4. Delete | 5. Back")
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
            break

def member_menu():
    while True:
        print("\n--- Member Menu ---")
        print("1. Add Member | 2. View All | 3. Update | 4. Delete | 5. Back")
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
            break

if __name__ == "__main__":
    main()