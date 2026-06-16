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

def update_book(book_id, title, author):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title = ?, author = ? WHERE id = ?", (title, author, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Instead of deleting, we hide it
        cursor.execute("UPDATE books SET is_active = 0 WHERE id = ?", (book_id,))
        conn.commit()
    finally:
        conn.close()

def deactivate_book(book_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET is_active = 0 WHERE id = ?", (book_id,))
        conn.commit()
    finally:
        conn.close()

def search_books(query):
    conn = get_connection()
    cursor = conn.cursor()
    # Search by title or author
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + query + '%', '%' + query + '%'))
    records = cursor.fetchall()
    conn.close()
    return records

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

def update_member(member_id, name, email):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE members SET name = ?, email = ? WHERE id = ?", (name, email, member_id))
        conn.commit()
    finally:
        conn.close()

def delete_member(member_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        conn.commit()
    finally:
        conn.close()

def search_members(query):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE name LIKE ? OR email LIKE ?", ('%'+query+'%', '%'+query+'%'))
        return cursor.fetchall()
    finally:
        conn.close()

def deactivate_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    # Change 'active' to 'is_active' to match your table definition
    cursor.execute("UPDATE members SET is_active = 0 WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()
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

def add_borrowed(book_id, member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO borrowing (book_id, member_id, status) VALUES (?, ?, ?)", 
                   (book_id, member_id, 'Borrowed'))
    conn.commit()
    conn.close()

def update_borrowed_status(borrowed_id, new_status):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Ensure 'borrowing' table and 'status' column exist
        cursor.execute("UPDATE borrowing SET status = ? WHERE id = ?", (new_status, borrowed_id))
        conn.commit()
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
    finally:
        conn.close()

def delete_borrowed(borrowed_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM borrowing WHERE id = ?", (borrowed_id,))
        conn.commit()
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
    finally:
        conn.close()

def search_borrowed(query):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT borrowing.id, books.title, members.name, borrowing.status 
                          FROM borrowing 
                          JOIN books ON borrowing.book_id = books.id 
                          JOIN members ON borrowing.member_id = members.id 
                          WHERE books.title LIKE ? OR members.name LIKE ?''', ('%'+query+'%', '%'+query+'%'))
        return cursor.fetchall()
    finally:
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