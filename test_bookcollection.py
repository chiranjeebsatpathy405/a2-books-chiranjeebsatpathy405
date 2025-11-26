"""(Incomplete) Tests for BookCollection class."""
from book import Book
from bookcollection import BookCollection

def run_tests():
    """Test BookCollection class."""

    # Test empty BookCollection with defaults
    print("Test empty BookCollection:")
    book_collection = BookCollection()
    print(book_collection)
    assert not book_collection.books  # This list should evaluate to False since it is empty

    # Test loading books
    print("Test loading books:")
    book_collection.load_books('books.json')
    print(book_collection)
    assert book_collection.books  # assuming data file is non-empty, list evaluates to True

    # Test adding a new Book with values
    print("Test adding new book:")
    book_collection.add_book(Book("War and Peace", "William Shakespeare", 999, False))
    print(book_collection)

    # Test sorting books
    print("Test sorting - author:")
    book_collection.sort("author")
    print(book_collection)
    # TODO: Add more sorting tests

    # TODO: Test get_unread_pages()
    print("Test get_unread_pages():")

    # TODO: Test saving books (check data file manually to see results)

    # TODO: Add more tests, as appropriate


run_tests()
