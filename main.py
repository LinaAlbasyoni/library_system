from database import setup_database, add_book, delete_book
import sqlite3

def view_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    
    print("\n--- Current Library ---")
    for book in books:
        print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]}")

def main():
    setup_database()
    while True:
        print("\n1. Add Book\n2. View All Books\n3. Delete Book\n4. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            add_book(title, author)
            print("Book added successfully!")
        elif choice == '2':
            view_books()
        elif choice == '3':
            view_books() # Show IDs so the user knows what to delete
            book_id = input("Enter the ID of the book to delete: ")
            delete_book(book_id)
            print("Book deleted!")
        elif choice == '4':
            break

if __name__ == "__main__":
    main()