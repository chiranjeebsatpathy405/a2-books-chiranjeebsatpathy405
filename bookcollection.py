"""..."""


# TODO: Create your BookCollection class in this file


"""BookCollection class"""

import json
from typing import List
from book import Book

class BookCollection:
    """Represents a collection of Book objects."""

    def __init__(self):
        # Start with an empty list of books
        self.books = []

    def add_book(self, book):
        """Add a Book object to the collection."""
        self.books.append(book)

    def __str__(self):
        """Return a string showing all books in the collection."""
        if not self.books:
            return "No books in collection"
        return "\n".join(str(book) for book in self.books)

    def get_no_of_unread_pages(self) -> int:
        """Return the total number of pages for all unread books."""
        return sum(book.number_of_pages for book in self.books if not book.is_completed)

    def get_no_of_completed_pages(self) -> int:
        """Return the total number of pages for all completed books."""
        return sum(book.number_of_pages for book in self.books if book.is_completed)

    # --- Persistence (JSON load/save) ---

    def load_books(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as f:
            books_data = json.load(f)

        self.books = [
            Book(
                title=entry["title"],
                author=entry["author"],
                number_of_pages=entry["number_of_pages"],
                is_completed=entry.get("is_completed", False),
            )
            for entry in books_data
        ]

    def save_books(self, filename: str) -> None:
        """Save current books to a JSON file."""
        serialisable = [
            {
                "title": book.title,
                "author": book.author,
                "no_of_pages": book.number_of_pages,
                "is_completed": book.is_completed,
            }
            for book in self.books
        ]

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(serialisable, f, indent=2)

    # --- Sorting ---

    def sort(self, key: str) -> None:
        """First let us Sort books with given key, then by title.

        """
        key_map = {
            "title": "title",
            "author": "author",
            "pages": "pages",
            "is_completed": "is_completed",
            "completed": "is_completed",  # convenience alias
        }

        if key not in key_map:
            raise ValueError(f"Unsupported sort key: {key!r}")

        attr_name = key_map[key]
        self.books.sort(key=lambda book: (getattr(book, attr_name), book.title))
