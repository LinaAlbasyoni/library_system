# Library Management System by Lina Albasyoni

A terminal-based Library Management System built with Python and SQLite. This system allows for the comprehensive management of books, members, and borrowing records with data integrity and input validation.

Features
Book Management: Add, view, update, delete, and deactivate books.

Member Management: Add, view, update, delete, and deactivate members.

Borrowing System: Check out books to members and mark them as returned.

Data Integrity: Enforces foreign key constraints to prevent deleting books that are currently borrowed.

Validation: Uses Regular Expressions (Regex) to ensure valid email formats and DD-MM-YYYY date formats.

Error Handling: Prevents crashes from invalid user inputs (e.g., entering letters when an ID is required) or duplicate data entries (e.g., duplicate member emails).

# How to Run
Clone the repository:
git clone https://github.com/<your-username><repository-name>.git
cd <repository-name>

# Run the application:
python main.py

The system will automatically create the library.db file upon the first launch.

# Project Structure
main.py: Handles the user interface and menu navigation.

database.py: Contains all SQL logic, table creation, and data validation functions.

.gitignore: Keeps the repository clean by excluding local database files and temporary system files.

Built With
Python and SQLite3
