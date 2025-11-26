"""(Incomplete) Tests for Book class."""
from book import Book


def run_tests():
    """Test Book class."""

    # Test empty book with defaults
    print("Test empty book:")
    default_book = Book()
    print(repr(default_book))
    assert default_book.title == ""
    assert default_book.author == ""
    assert default_book.number_of_pages == 0
    assert default_book.is_completed is False

    # Test initial-value book
    print("Test initial-value book:")
    new_book = Book("Fish Fingers", "Dory", 501, True)
    # TODO: Write tests to show this initialisation works
    assert new_book.title == "Fish Fingers"
    assert new_book.author == "Dory"
    assert new_book.number_of_pages == 501
    assert new_book.is_completed is True
    print("Title:", new_book.title)
    print("Author:", new_book.author)
    print("Pages:", new_book.number_of_pages)
    print("Completed:", new_book.is_completed)
    print("Initial-value book test passed!\n")

    # Test mark_unread()
    # TODO: Write tests to show the mark_unread() method works
    print("Test mark_unread():")
    new_book.mark_unread()
    print(new_book)  # should now show status as unread
    assert new_book.is_completed is False
    print("mark_unread() test passed!\n")

    # Test mark_completed()
    print("Test mark_completed():")
    new_book.mark_completed()
    print(new_book)  # should now show status as completed
    assert new_book.is_completed is True
    print("mark_completed() test passed!\n")


    # Test is_long()
    # TODO: Write tests to show the is_long() method works
    print("Test is_long():")
    long_book = Book("Fish Fingers", "Dory", 5000, True)
    print(long_book.title , "- is_long:", long_book.is_long())
    short_book = Book("The Old Man and the Sea", "Ernest Hemingway", 127)

    print(short_book.title, "- is_long:", short_book.is_long())
    assert long_book.is_long() is True
    assert short_book.is_long() is False
    print("is_long() test passed!\n")

    # TODO: Add more tests, as appropriate
    # Extra test: string representation
    print("Test __str__():")
    assert str(new_book) == "Fish Fingers by Dory, 501 pages, completed"
    print("__str__() test passed!\n")

    print("🎉 All Book class tests passed successfully!")


run_tests()