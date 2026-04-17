import sqlite3
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "library.sqlite"


def ensure_schema(connection: sqlite3.Connection) -> None:
    """Create the books table if this is a new database file."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            year INTEGER,
            read BOOLEAN NOT NULL
        )
        """
    )
    connection.commit()


def add_book(
    connection: sqlite3.Connection,
    title: str,
    author: str,
    year: int,
    read: bool,
) -> None:
    connection.execute(
        """
        INSERT INTO books (title, author, year, read)
        VALUES (?, ?, ?, ?)
        """,
        (title, author, year, read),
    )
    connection.commit()
    print("Book added.")


def list_books(connection: sqlite3.Connection) -> None:
    cursor = connection.execute("SELECT * FROM books ORDER BY id")
    books = cursor.fetchall()
    if not books:
        print("No books in the library.")
        return
    for book in books:
        read_label = "Yes" if book[4] else "No"
        print(
            f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, "
            f"Year: {book[3]}, Read: {read_label}"
        )


def mark_as_read(connection: sqlite3.Connection, book_id: int) -> None:
    cursor = connection.execute(
        "UPDATE books SET read = 1 WHERE id = ?",
        (book_id,),
    )
    if cursor.rowcount == 0:
        print("No book with that ID.")
    else:
        print("Marked as read.")
    connection.commit()


def search_book(connection: sqlite3.Connection, book_title: str) -> None:
    cursor = connection.execute("SELECT * FROM books WHERE title LIKE ?", (f"%{book_title}%",))
    books = cursor.fetchall()
    if not books:
        print("No books found under this title")
        return
    for book in books:
        read_label = "Yes" if book[4] else "No"
        print(
            f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, "
            f"Year: {book[3]}, Read: {read_label}"
        )


def delete_book(connection: sqlite3.Connection, book_id: int) -> None:
    cursor = connection.execute(
        "SELECT id, title FROM books WHERE id = ?",
        (book_id,),
    )
    row = cursor.fetchone()
    if row is None:
        print("No book with that ID.")
        return
    title = row[1]
    confirmation = input(f'Are you sure you want to delete "{title}"? (y/n): ')
    if confirmation.lower() != "y":
        print("Cancelled.")
        return
    connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection.commit()
    print("Book deleted.")


def _prompt_int(message: str) -> int | None:
    raw = input(message).strip()
    try:
        return int(raw)
    except ValueError:
        print("Please enter a whole number.")
        return None


def run_menu(connection: sqlite3.Connection) -> None:
    while True:
        print()
        print("1. Add a book")
        print("2. List books")
        print("3. Mark a book as read")
        print("4. Delete a book")
        print("5. Search by title")
        print("6. Quit")
        choice = input("Choose an option (1–6): ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            year_raw = input("Year: ").strip()
            read_in = input("Already read? (y/n): ").strip().lower()
            try:
                year = int(year_raw)
            except ValueError:
                print("Year must be a number.")
                continue
            read = read_in in ("y", "yes")
            if not title:
                print("Title cannot be empty.")
                continue
            add_book(connection, title, author, year, read)

        elif choice == "2":
            list_books(connection)

        elif choice == "3":
            list_books(connection)
            book_id = _prompt_int("ID of the book to mark as read: ")
            if book_id is not None:
                mark_as_read(connection, book_id)

        elif choice == "4":
            list_books(connection)
            book_id = _prompt_int("ID of the book to delete: ")
            if book_id is not None:
                delete_book(connection, book_id)

        elif choice == "5":
            book_title = input("Title of the book you're searching: ").strip()
            print(book_title)
            if book_title is not None:
                search_book(connection, book_title)

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Pick 1 to 5.")


def main() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    # One connection for the whole session; commit() after each write persists data.
    with sqlite3.connect(DATA_FILE) as connection:
        ensure_schema(connection)
        print(f"Library database: {DATA_FILE}")
        run_menu(connection)


if __name__ == "__main__":
    main()
