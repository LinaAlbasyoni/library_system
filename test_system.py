import unittest
from database import setup_database, add_book, add_member, borrow_book, get_all_books

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        """Runs before every test: creates a fresh test database."""
        setup_database()

    def test_add_book(self):
        add_book("Test Title", "Test Author")
        books = get_all_books()
        self.assertTrue(any(b[1] == "Test Title" for b in books))

    def test_borrow_book_logic(self):
        add_book("Borrowable Book", "Author")
        add_member("Test Member", "test@example.com")
        borrow_book(1, 1, "16-06-2026", "20-06-2026")

if __name__ == '__main__':
    unittest.main()