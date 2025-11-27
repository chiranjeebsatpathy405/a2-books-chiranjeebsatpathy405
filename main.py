"""
Name: Chiranjeeb Satpathy
Date Started: 24th Nov 2025
Date Completed 28th Nov 2025
Brief Project Description:
This module defines the Kivy application for managing a reading list.
It uses the Book and BookCollection classes to load books from a JSON
file, display them as colour-coded buttons, allow the user to toggle
between completed and unread states, and add new books.

GitHub URL: https://github.com/chiranjeebsatpathy405/a2-books-chiranjeebsatpathy405

"""
# TODO: Create your main program in this file using the BooksToReadApp class

from bookcollection import BookCollection
from kivy.app import App


from operator import attrgetter
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout

from book import Book
from bookcollection import BookCollection

# --------------------- CONFIGURATION CONSTANTS --------------------- #

BOOKS_FILE = "books.json"

# RGBA colour constants for book buttons
COLOUR_UNREAD = (0, 0.4, 0.4, 1)
COLOUR_COMPLETED = (0.25, 0.25, 0.25, 1)

# Sort options shown in the spinner
SORT_OPTION_TITLE = "Title"
SORT_OPTION_AUTHOR = "Author"
SORT_OPTION_PAGES = "Pages"


class BooksGui(BoxLayout):
    """Root widget for the Books To Read 2.0 GUI."""

    pages_status_text = StringProperty("")
    bottom_status_text = StringProperty("")
    sort_options = ListProperty([SORT_OPTION_AUTHOR, SORT_OPTION_TITLE, SORT_OPTION_PAGES])

    def __init__(self, **kwargs):   # ✅ fixed constructor
        super().__init__(**kwargs)
        self.book_collection = BookCollection()

    # ---------------------- INITIALISATION ---------------------- #

    def initialise(self):
        """Load books from JSON and build the initial list of buttons."""
        try:
            self.book_collection.load_books(BOOKS_FILE)
        except FileNotFoundError:
            self.bottom_status_text = f"No {BOOKS_FILE} file found. Starting with an empty list."
        else:
            self.bottom_status_text = f"{len(self.book_collection.books)} books loaded."
        self.update_sort_order(SORT_OPTION_AUTHOR)
        self.refresh_book_buttons()
        self.update_pages_status()

    # ------------------------- SORTING -------------------------- #

    def update_sort_order(self, selected_text: str):
        """Sort books in the collection according to the spinner selection."""
        if selected_text == SORT_OPTION_AUTHOR:
            sort_key = attrgetter("author", "title")
        elif selected_text == SORT_OPTION_TITLE:
            sort_key = attrgetter("title")
        else:
            sort_key = attrgetter("no_of_pages", "title")

        self.book_collection.books.sort(key=sort_key)
        self.refresh_book_buttons()
        self.update_pages_status()
        self.bottom_status_text = f"Books sorted by {selected_text.lower()}."

    # ------------------ BOOK BUTTON CREATION -------------------- #

    def refresh_book_buttons(self):
        """Clear and rebuild the book buttons in the right-hand panel."""
        books_box = self.ids.books_box
        books_box.clear_widgets()

        for book in self.book_collection.books:
            book_button = self.create_book_button(book)
            books_box.add_widget(book_button)

    def create_book_button(self, book: Book):
        """Create a Button widget representing a single book."""
        from kivy.uix.button import Button

        if book.is_completed:
            background_colour = COLOUR_COMPLETED
            completed_text = " (completed)"
        else:
            background_colour = COLOUR_UNREAD
            completed_text = ""

        button_text = f"{book.title} by {book.author}, {book.no_of_pages} pages{completed_text}"

        book_button = Button(
            text=button_text,
            size_hint_y=None,
            height=60,
            background_color=background_colour
        )
        book_button.book = book
        book_button.bind(on_release=self.handle_book_button_press)
        return book_button

    # ------------------- BOOK BUTTON HANDLER -------------------- #

    def handle_book_button_press(self, button):
        """Toggle the completion state of the clicked book."""
        book = button.book
        if book.is_completed:
            book.mark_unread()
            self.bottom_status_text = f"You need to read {book.title}."
        else:
            book.mark_completed()
            if book.is_long():
                self.bottom_status_text = f"Completed {book.title}. That was a long book!"
            else:
                self.bottom_status_text = f"Completed {book.title}."

        self.refresh_book_buttons()
        self.update_pages_status()

    # --------------------- ADD / CLEAR BOOK --------------------- #

    def handle_add_book(self):
        """Validate fields and add a new book if the input is valid."""
        title_text = self.ids.title_input.text.strip()
        author_text = self.ids.author_input.text.strip()
        pages_text = self.ids.pages_input.text.strip()

        # --- Required fields check ---
        if title_text == "" or author_text == "" or pages_text == "":
            self.bottom_status_text = "Please complete all fields."
            return

        # --- Integer validation ---
        try:
            number_of_pages = int(pages_text)
        except ValueError:
            self.bottom_status_text = "Please enter a valid number."
            return

        # --- Positive pages check ---
        if number_of_pages <= 0:
            self.bottom_status_text = "The book must have some pages!"
            return

        # --- Add the book ---
        new_book = Book(title_text, author_text, number_of_pages, is_completed=False)
        self.book_collection.add_book(new_book)

        # --- Clear inputs + refresh list ---
        self.clear_inputs()
        self.refresh_book_buttons()
        self.update_pages_status()
        self.bottom_status_text = f"Added {new_book.title}."



    def clear_inputs(self):
        """Clear the text in the input fields and the bottom status label."""
        self.ids.title_input.text = ""
        self.ids.author_input.text = ""
        self.ids.pages_input.text = ""
        self.bottom_status_text = ""
        self.ids.title_input.focus = True

    def clear_read_list(self):
        """Remove all books from the collection."""
        self.book_collection.books.clear()
        self.refresh_book_buttons()
        self.update_pages_status()
        self.bottom_status_text = "Clear the entire book list."

    # ------------------------ STATUS TEXT ----------------------- #

    def update_pages_status(self):
        """Update the top status label with the total unread pages."""
        unread_pages = self.book_collection.get_no_of_unread_pages()
        self.pages_status_text = f"Pages to read: {unread_pages}"


class BooksApp(App):
    """Kivy application for the Books To Read GUI."""

    def build(self):
        self.title = "Books To Read 2.0"
        Builder.load_file("app.kv")
        root = BooksGui()  # ✅ explicitly create root
        root.initialise()
        return root


    def on_stop(self):
        root = self.root
        if isinstance(root, BooksGui):
            root.book_collection.save_books(BOOKS_FILE)


BooksApp().run()