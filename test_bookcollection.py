"""Book Class
Expected Time - 10 hours
Actual Time Taken - 12 hours
GitHub URL: https://github.com/chiranjeebsatpathy405/a2-books-chiranjeebsatpathy405
"""
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
    print("\nTest loading books:")
    book_collection.load_books('books.json')
    print(book_collection)
    assert book_collection.books  # assuming data file is non-empty, list evaluates to True

    # Test adding a new Book with values
    print("\nTest adding new book:")
    book_collection.add_book(Book("War and Peace", "William Shakespeare", 999, False))
    print(book_collection)

    print("")
    print("\nTest sorting books (Author) starts:")

    book_collection.sort("author")
    print(book_collection)
    print("\nTest sorting books (Authors)  ends")

    # TODO: Add more sorting tests
    # Test sorting books
    print("\nTest sorting - title starts:")
    book_collection.sort("title")
    print(book_collection)
    print("\nTest sorting - title ends:")
    # TODO: Test get_unread_pages()

    print("\nTest get_unread_pages starts:")
    test_get_unread_pages()
    print("\nTest get_unread_pages ends:")

    # TODO: Test saving books (check data file manually to see results)
    collection = BookCollection()
    collection.books.append(Book("Geology", "Chiranjeeb Satpathy", 464, False))
    collection.books.append(Book("Fish Fingers", "Dory", 501, True))

    collection.save_books("books.json")

    # TODO: Add more tests, as appropriate

def test_get_unread_pages():

    print("Testing get_no_of_unread_pages...")
    # Create a new collection
    collection = BookCollection()

    # Add books: some unread, some completed
    collection.add_book(Book("Clean Code", "Robert C. Martin", 464, False))   # unread
    collection.add_book(Book("Fish Fingers", "Dory", 501, True))             # completed
    collection.add_book(Book("The Old Man and the Sea", "Ernest Hemingway", 127, False))  # unread

    # Call the method
    total_unread_pages = collection.get_no_of_unread_pages()

    # Print result
    print(f"Total unread pages: {total_unread_pages}")

    # Assert expected value: 464 + 127 = 591
    assert total_unread_pages == 591, f"Expected 591, got {total_unread_pages}"

    print("✅ get_no_of_unread_pages test passed!")


run_tests()
