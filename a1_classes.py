"""Console program

The program assignment.py loads books from a CSV file into Book objects stored in a
BookCollection. The console program displays all books, add a new book, or mark
a book as completed.
Expected Time - 8 hours
Actual Time Taken - 12 hours
"""

import csv
from pathlib import Path

from book import Book
from bookcollection import BookCollection
from operator import attrgetter



# --------------------- CONFIGURATION CONSTANTS --------------------- #
DATA_FILE = "books.csv"
STATUS_TO_READ = "u"
STATUS_COMPLETED = "c"

MAIN_MENU = (
    "Options:\n"
    "D - Display books\n"
    "A - Add new book\n"
    "C - Complete a book\n"
    "Q - Quit application"
)


# ---------------------------- MAIN -------------------------------- #

def main():
    """Run the console application."""

    book_collection = BookCollection()
    load_csv_into_collection(DATA_FILE, book_collection)

    print(f"{len(book_collection.books)} records loaded from {DATA_FILE}.")

    user_choice = ""
    while user_choice != "q":
        print()
        print(MAIN_MENU)
        user_choice = input("Enter your choice: ").strip().lower()

        if user_choice == "d":
            display_books_details(book_collection)
        elif user_choice == "a":
            add_new_book(book_collection)
        elif user_choice == "c":
            complete_book(book_collection)
        elif user_choice == "q":
            save_collection_to_csv(DATA_FILE, book_collection)
            print(f"{len(book_collection.books)} books saved to {DATA_FILE}")
            print("So many books, so little time. Frank Zappa")
        else:
            print("Invalid menu choice.")


# ------------------------ INPUT HELPERS ---------------------------- #

def get_string_input(prompt_message: str) -> str:
    """Prompt until the user enters a non-empty string."""
    user_text = input(prompt_message).strip()
    while user_text == "":
        print("Input can not be blank")
        user_text = input(prompt_message).strip()
    return user_text


def get_positive_integer(prompt_message: str) -> int:
    """Prompt until the user enters an integer greater than zero."""
    is_valid_number = False
    positive_number = 0
    while not is_valid_number:
        user_text = input(prompt_message).strip()
        try:
            positive_number = int(user_text)
            if positive_number > 0:
                is_valid_number = True
            else:
                print("Number must be > 0")

        except ValueError:
            print("please enter a valid number.")
    return positive_number


# ----------------------- LOAD / SAVE CSV --------------------------- #

def load_csv_into_collection(filename: str, book_collection: BookCollection) -> None:
    """Load books from a CSV file into the given BookCollection."""
    file_path = Path(filename)
    if not file_path.exists():
        print(f"File '{filename}' not found. Starting with an empty list.")
        return

    with file_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) < 4:
                continue
            title_text, author_text, pages_text, status_text = row
            try:
                number_of_pages = int(pages_text)
            except ValueError:
                print(f"Skipping row (invalid page count): {row}")
                continue

            status_text = status_text.strip().lower()
            if status_text == STATUS_COMPLETED:
                is_completed = True
            else:
                is_completed = False

            book = Book(title_text, author_text, number_of_pages, is_completed)
            book_collection.add_book(book)


def save_collection_to_csv(filename: str, book_collection: BookCollection) -> None:
    """Save the books in the BookCollection back to the CSV file."""
    with open(filename, "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for book in book_collection.books:
            if book.is_completed:
                status_text = STATUS_COMPLETED
            else:
                status_text = STATUS_TO_READ
            csv_writer.writerow(
                [book.title, book.author, book.number_of_pages, status_text]
            )


# ------------------------- CORE FEATURES --------------------------- #

def get_author_title_key(book: Book):
    """Return a tuple used to sort books by author, then by title."""
    return book.author.lower(), book.title.lower()


def display_books_details(book_collection: BookCollection):
    """Display all books, sorted by author then title, with a summary."""
    if not book_collection.books:
        print("Your list is empty. Time to add some new books!")
        return

    """ Use attrgetter instead of lambda"""

    sorted_books = sorted(book_collection.books, key=attrgetter("author", "title"))

    maximum_title_length = max(len(book.title) for book in sorted_books)
    maximum_author_length = max(len(book.author) for book in sorted_books)

    total_unread_pages = 0
    number_of_unread_books = 0

    for index, book in enumerate(sorted_books, start=1):
        status_character = " " if book.is_completed else "*"
        print(
            f"{status_character}{index}. "
            f"{book.title:<{maximum_title_length}} by "
            f"{book.author:<{maximum_author_length}} "
            f"{book.number_of_pages:>4} pages"
        )

        if not book.is_completed:
            total_unread_pages += book.number_of_pages
            number_of_unread_books += 1

    print("--------------------")
    if number_of_unread_books > 0:
        print(f"You still need to read {total_unread_pages} pages in {number_of_unread_books} books.")
    else:
        print("Congratulations! All books read. Why not add a new book?")


def add_new_book(book_collection: BookCollection):
    """Prompt for details and add a new unread book to the collection."""
    title_text = get_string_input("Enter title of book: ")
    author_text = get_string_input("Enter name of author: ")
    number_of_pages = get_positive_integer("Enter number of pages: ")

    new_book = Book(title_text, author_text, number_of_pages, is_completed=False)
    book_collection.add_book(new_book)

    print(f"'{title_text}' by {author_text} ({number_of_pages} pages) added.")


def complete_book(book_collection: BookCollection):
    """Mark a selected unread book as completed, handling invalid index values."""
    unread_books = [book for book in book_collection.books if not book.is_completed]
    if not unread_books:
        print("You have no unread books to mark as completed. Well done!")
        return

    # Show the list in the same format before asking for a choice
    sorted_books = sorted(book_collection.books, key=get_author_title_key)
    display_books_details(book_collection)

    is_valid_selection = False
    while not is_valid_selection:
        selected_index = get_positive_integer(
            "Enter the number of the book to complete: "
        )
        try:
            chosen_book = sorted_books[selected_index - 1]
        except IndexError:
            print("Invalid book number selected.")
        else:
            if chosen_book.is_completed:
                print(f"'{chosen_book.title}' is already marked as completed.")
            else:
                chosen_book.mark_completed()
                print(
                    f"'{chosen_book.title}' by {chosen_book.author} "
                    f"is now marked as read. Great job!"
                )
            is_valid_selection = True


main()