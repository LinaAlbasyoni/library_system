import sqlite3

def get_connection():
    """Helper to maintain a consistent connection with foreign keys enabled."""
    conn = sqlite3.connect('library.db')
    conn.execute("PRAGMA foreign_keys = ON;") 
    return conn

def setup_database():
    """Creates the books, members, and borrowing tables with status and activity tracking."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            borrow_date TEXT,
            return_date TEXT,
            status TEXT DEFAULT 'Borrowed',
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(member_id) REFERENCES members(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- Book CRUD & Search ---

def add_book(title, author):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
    conn.commit()
    conn.close()

def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE is_active = 1')
    books = cursor.fetchall()
    conn.close()
    return books

def update_book(book_id, new_title, new_author):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET title = ?, author = ? WHERE id = ?', (new_title, new_author, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        if cursor.rowcount == 0:
            print("Error: Book ID not found.")
        else:
            conn.commit()
            print("Success: Book deleted.")
    except sqlite3.IntegrityError:
        print("Error: Cannot delete book. It is currently checked out.")
    conn.close()

def deactivate_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET is_active = 0 WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def search_books(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE (title LIKE ? OR author LIKE ?) AND is_active = 1", 
                   ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    conn.close()
    return results

# --- Member CRUD & Search ---

def add_member(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO members (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        print("Success: Member added.")
    except sqlite3.IntegrityError:
        print("Error: A member with this email already exists.")
    finally:
        conn.close()

def get_all_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members WHERE is_active = 1')
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
    cursor.execute("SELECT * FROM members WHERE (name LIKE ? OR email LIKE ?) AND is_active = 1", 
                   ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    conn.close()
    return results

def deactivate_member(member_id):
    """Soft deletes a member by setting is_active to 0."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE members SET is_active = 0 WHERE id = ?', (member_id,))
    conn.commit()
    conn.close()
    print("Success: Member deactivated.")

# --- Borrowing/Loans Operations ---

def borrow_book(book_id, member_id, borrow_date, return_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM books WHERE id = ? AND is_active = 1', (book_id,))
    if not cursor.fetchone():
        print("Error: Book not found or unavailable.")
        conn.close()
        return
    
    cursor.execute('SELECT id FROM members WHERE id = ? AND is_active = 1', (member_id,))
    if not cursor.fetchone():
        print("Error: Member not found or inactive.")
        conn.close()
        return

    cursor.execute('INSERT INTO borrowing (book_id, member_id, borrow_date, return_date) VALUES (?, ?, ?, ?)',
                   (book_id, member_id, borrow_date, return_date))
    conn.commit()
    conn.close()
    print("Success: Book checked out.")

def return_book(loan_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE borrowing SET status = "Returned" WHERE id = ?', (loan_id,))
    
    if cursor.rowcount > 0:
        conn.commit()
        print("Success: Book returned.")
    else:
        print("Error: Loan ID not found.")
    
    conn.close()

def get_all_borrowed_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT borrowing.id, books.title, members.name, borrowing.status 
        FROM borrowing
        JOIN books ON borrowing.book_id = books.id
        JOIN members ON borrowing.member_id = members.id
    ''')
    records = cursor.fetchall()
    conn.close()
    return records