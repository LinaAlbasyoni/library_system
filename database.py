import sqlite3

def get_connection():
    """Helper to maintain a consistent connection with foreign keys enabled."""
    conn = sqlite3.connect('library.db')
    conn.execute("PRAGMA foreign_keys = ON;") # This is the missing piece!
    return conn

def setup_database():
    """Creates the books, members, and borrowing tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            borrow_date TEXT,
            return_date TEXT,
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(member_id) REFERENCES members(id)
        )
    ''')
    
    conn.commit()
    conn.close()


def add_book(title, author):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
    conn.commit()
    conn.close()

def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return books

def update_book(book_id, new_title, new_author):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE books 
        SET title = ?, author = ? 
        WHERE id = ?
    ''', (new_title, new_author, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def search_books(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                   ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    conn.close()
    return results


def add_member(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO members (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Email already exists.")
    finally:
        conn.close()

def get_all_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members')
    members = cursor.fetchall()
    conn.close()
    return members

def update_member(member_id, new_name, new_email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE members SET name = ?, email = ? WHERE id = ?', (new_name, new_email, member_id))
    conn.commit()
    conn.close()

def delete_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM members WHERE id = ?', (member_id,))
    conn.commit()
    conn.close()

def search_members(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE name LIKE ? OR email LIKE ?", 
                   ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    conn.close()
    return results


def borrow_book(book_id, member_id, borrow_date, return_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM books WHERE id = ?', (book_id,))
    if not cursor.fetchone():
        print("Error: Book ID not found.")
        conn.close()
        return
    
    cursor.execute('SELECT id FROM members WHERE id = ?', (member_id,))
    if not cursor.fetchone():
        print("Error: Member ID not found.")
        conn.close()
        return

    cursor.execute('INSERT INTO borrowing (book_id, member_id, borrow_date, return_date) VALUES (?, ?, ?, ?)',
                   (book_id, member_id, borrow_date, return_date))
    conn.commit()
    conn.close()
    print("Success: Book checked out.")

def get_all_borrowed_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT borrowing.id, books.title, members.name, borrowing.borrow_date, borrowing.return_date 
        FROM borrowing
        JOIN books ON borrowing.book_id = books.id
        JOIN members ON borrowing.member_id = members.id
    ''')
    records = cursor.fetchall()
    conn.close()
    return records