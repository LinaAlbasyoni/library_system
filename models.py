class Book:
    def __init__(self, title, author, id=None):
        self.id = id
        self.title = title
        self.author = author

    def __repr__(self):
        return f"Book({self.title}, {self.author})"