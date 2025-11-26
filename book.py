"""..."""


# TODO: Create your Book class in this file

"""Represents a single book """
class Book:
    def __init__(self, title: str = "", author: str = "", number_of_pages: int = 0, is_completed: bool = False):
        """
        Each Book object will keep track of:
            title: Name of the book
            author:Person who wrote it
            no_of_pages: how many pages the book contains
            is_completed: whether finished reading (defaulted to False)
        """
        self.title = title
        self.author = author
        self.number_of_pages = number_of_pages
        self.is_completed = is_completed

    def __str__(self) -> str:  # <-- double underscores
        """Return unread or completed status description of the book."""
        status = "completed" if self.is_completed else "unread"
        return f"{self.title} by {self.author}, {self.number_of_pages} pages, {status}"

    # --- Status-changing methods (two methods, as required) ---

    def mark_completed(self) -> None:
        """Mark this book as completed"""
        self.is_completed = True

    def mark_unread(self) -> None:
        """Mark this book as unread."""
        self.is_completed = False

    # --- Other helper methods ---

    def is_long(self) -> bool:
        """Return True if the book is considered 'long' (>= 500 pages)."""
        return self.number_of_pages >= 500
