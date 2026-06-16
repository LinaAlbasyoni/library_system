from database import setup_database, add_book, get_all_books, update_book, delete_book

def seed_library():
    """Populates the database with initial classic books."""
    books_to_add = [
        ("Hamlet", "William Shakespeare"),
        ("Romeo and Juliet", "William Shakespeare"),
        ("A Tale of Two Cities", "Charles Dickens"),
        ("Oliver Twist", "Charles Dickens")
    ]
    for title, author in books_to_add:
        add_book(title, author)
    print("Initial classic books have been added!")

def main():
    setup_database()
    
    while True:
        print("\n--- Library Management System ---")
        print("1. Add a Book")
        print("2. View All Books")
        print("3. Update a Book")
        print("4. Delete a Book")
        print("5. Seed Initial Data (Classic Books)")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ")
        
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            add_book(title, author)
            print("Book added successfully!")
            
        elif choice == '2':
            books = get_all_books()
            print("\n--- Current Library ---")
            for book in books:
                print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]}")
                
        elif choice == '3':
            book_id = input("Enter the ID of the book you want to update: ")
            new_title = input("Enter the new title: ")
            new_author = input("Enter the new author: ")
            update_book(book_id, new_title, new_author)
            print("Book updated successfully!")
            
        elif choice == '4':
            book_id = input("Enter the ID of the book to delete: ")
            delete_book(book_id)
            print("Book deleted.")
            
        elif choice == '5':
            seed_library()
            
        elif choice == '6':
            print("Exiting system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()