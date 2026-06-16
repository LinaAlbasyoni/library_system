import sqlite3

def connect_db():
    return sqlite3.connect("library.db")

def setup_database():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                      (id INTEGER PRIMARY KEY, title TEXT, author TEXT)''')
    conn.commit()
    conn.close()

def add_book(title, author):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

def search_books(query):
    conn = connect_db()
    cursor = conn.cursor()
    # Search by title OR author using wildcards for partial matches
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                   ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    conn.close()
    return results

def view_books_from_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")