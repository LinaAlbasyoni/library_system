from database import setup_database, add_book, delete_book, search_books, view_books_from_db
import sqlite3

def seed_library():
    """Populates the database with initial classic books."""
    books_to_add = [
        ("Hamlet", "William Shakespeare"),
        ("Romeo and Juliet", "William Shakespeare"),
        ("A Tale of Two Cities", "Charles Dickens"),
        ("Oliver Twist", "Charles Dickens")
    ]
    for title, author in books_to_add:
        # Assuming you have a basic add_book function
        add_book(title, author)
    print("Initial classic books have been added!")
    
def main():
    setup_database()
    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Delete Book")
        print("4. Search Books")
        print("5. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            add_book(title, author)
            print("Book added successfully!")
            
        elif choice == '2':
            books = view_books_from_db()
            print("\n--- Current Library ---")
            if not books:
                print("The library is currently empty.")
            else:
                for book in books:
                    print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]}")
                    
        elif choice == '3':
            books = view_books_from_db()
            if not books:
                print("The library is empty. Nothing to delete.")
            else:
                for book in books:
                    print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]}")
                book_id = input("Enter the ID of the book to delete: ")
                delete_book(book_id)
                print("Book deleted!")
                
        elif choice == '4':
            term = input("Enter title or author to search: ")
            results = search_books(term)
            print("\n--- Search Results ---")
            if not results:
                print("No books found matching your search.")
            else:
                for book in results:
                    print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]}")
                    
        elif choice == '5':
            print("Exiting...")
            break
            
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()