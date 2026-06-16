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

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")