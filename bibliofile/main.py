import time
# import pyzmq
import sqlite3

DB_FILE = "bookshelf.db"

def main():
    init_db()
    print_header()
    welcome_page()


def print_header():
    print("░████████    ░██ ░██        ░██ ░██                 ░████ ░██ ░██             ")  
    print("░██    ░██       ░██        ░██                    ░██        ░██             ")
    print("░██    ░██   ░██ ░████████  ░██ ░██   ░███████  ░████████ ░██ ░██   ░███████  ")
    print("░████████    ░██ ░██    ░██ ░██ ░██  ░██    ░██    ░██    ░██ ░██  ░██    ░██ ")
    print("░██     ░██  ░██ ░██    ░██ ░██ ░██  ░██    ░██    ░██    ░██ ░██  ░█████████ ")
    print("░██     ░██  ░██ ░██    ░██ ░██ ░██  ░██    ░██    ░██    ░██ ░██  ░██        ")
    print("░█████████   ░██ ░███████   ░██ ░██   ░███████     ░██    ░██ ░██   ░███████  ")
                                                                        
def welcome_page():
    print("\n\nWelcome to Bibliofile:")
    print("A catalogue for your home library\n")
    selection = input("Press the Enter key to use the app or enter 0 to exit: ")
    while selection != "" and selection.strip() != "0":
        print(f"\nYou entered: {selection}. Please try again.")
        selection = input("Press the Enter key to use the app or enter 0 to exit: ")
    match selection:
        case "":
            home_menu_page()
        case "0": 
            print("Thanks for using Bibliofile!")
            time.sleep(3)
            quit()

def home_menu_page():
    print_header()
    print("~~~~~~~~~~~~~~~~~~~~\n Home Menu\n~~~~~~~~~~~~~~~~~~~~")
    print("1. Name My Collection")
    print("2. View My Collection")
    print("3. Add a book to My Collection")
    print("4. Return to previous page")
    selection = input("Enter selection: ")
    while selection not in ("1", '2', '3', '4'):
        print(f"\nYou entered: {selection}. Please try again.")
        input("Enter selection: ")

    match selection:
        case "1":
            name_collection_page()
        case "2":
            view_collection_page()
        case "3":
            add_book_page()
        case "4":
            welcome_page()

def init_db():
    """Initialize the database and default collection if needed."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # 1️⃣ Create metadata table to track active collection
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection_title (
                id INTEGER PRIMARY KEY,
                active_collection TEXT
            )
        ''')

        # 2️⃣ Check if an active collection is already set
        cursor.execute("SELECT active_collection FROM collection_title LIMIT 1")
        result = cursor.fetchone()

        if result:
            active_table = result[0]
            print(f"Active collection found: '{active_table}'")
        else:
            # No active collection — create default table
            active_table = "Unnamed Collection"
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS "{active_table}" (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author_first_name TEXT,
                    author_last_name TEXT,
                    title TEXT NOT NULL,
                    isbn INTEGER,
                    read BOOLEAN DEFAULT 0,
                    loaned BOOLEAN DEFAULT 0,
                    format TEXT CHECK(format IN ('Digital', 'Physical')),
                    rating INTEGER CHECK(rating >= 1 AND rating <= 5)
                )
            ''')
            # Set it as active collection
            cursor.execute("INSERT INTO collection_title (active_collection) VALUES (?)", (active_table,))
            print(f"Default collection '{active_table}' created and set as active.")

        conn.commit()
        return active_table  # useful to know current active table
    except sqlite3.Error as e:
        print(f"Database error during initialization:\n{e}")
    finally:
        conn.close()


def rename_collection(old_name: str, new_name: str):
    """Rename the active collection and update metadata."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Rename the table
        cursor.execute(f'ALTER TABLE "{old_name}" RENAME TO "{new_name}"')
        # Update metadata
        cursor.execute("UPDATE collection_title SET active_collection = ?", (new_name,))
        conn.commit()
        print(f"Collection renamed from '{old_name}' to '{new_name}'.")
    except sqlite3.Error as e:
        print(f"Database error during rename:\n{e}")
    finally:
        conn.close()

def get_active_collection() -> str:
    """Return the name of the currently active collection."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT active_collection FROM collection_title LIMIT 1")
        result = cursor.fetchone()
        if result:
            return result[0]  # The active table name
        else:
            return None  # No collection set
    except sqlite3.Error as e:
        print(f"Database error while fetching active collection:\n{e}")
        return None
    finally:
        conn.close()


def name_collection_page():
    print_header()
    current_name = get_active_collection()
    print(f"\n~~~~~~~~~~~~~~~~~~~~\n {current_name}\n~~~~~~~~~~~~~~~~~~~~")
    print(f"\nThe current collection name is: {current_name}\n")
    new_name = input("\nPlease enter a new name for your collection or press Enter to return to the previous menu: ")
    while new_name != '':
        print(f"\nYou entered the new name: {new_name}\n")
        confirmed = input("Type confirm or retry: ").lower()
        while confirmed not in ["confirm",  "retry"]:
            print(f"\nYou entered the new name: {new_name}\n")
            confirmed = input("Type confirm or type retry: ").lower()
        if confirmed == "confirm":
            rename_collection(get_active_collection(), new_name)
            name_collection_page()
        else: 
            new_name = input("\nPlease enter a new name for your collection or press Enter to return to the previous menu: ")
    if new_name == "":
        home_menu_page()
    else: name_collection_page()

def view_collection_page():
    print_header()
    print(f"~~~~~~~~~~~~~~~~~~~~\n {get_active_collection()}\n~~~~~~~~~~~~~~~~~~~~")
    print("1. View entire collection")
    print("2. Sort and View Collection")
    print("3. Edit a book")
    print("4. Return to previous page")
    selection = input("Enter selection: ")
    while selection not in ("1", '2', '3', '4'):
        print(f"\nYou entered: {selection}. Please try again.")
        input("Enter selection: ")

    match selection:
        case "1":
            view_entire_collection_page()
        case "2":
            view_entire_collection_page()
        case "3":
            view_entire_collection_page()
        case "4":
            view_entire_collection_page()

def view_entire_collection_page():
    print_header()

    active_table = get_active_collection()
    if not active_table:
        print("No active collection found.")
        view_collection_page()
        return

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM "{active_table}"')
        books = cursor.fetchall()

        print(f"\n~~~~~~~~~~~~~~~~~~~~\n {active_table}\n~~~~~~~~~~~~~~~~~~~~")
        print(f"\nTotal books in this collection: {len(books)}\n")

        if not books:
            print("No books found in your collection yet.")
        else:
            # Print a table-like output
            print("{:<5} {:<15} {:<15} {:<30} {:<13} {:<6} {:<8} {:<9} {:<6}".format(
                "ID", "Author First", "Author Last", "Title", "ISBN", "Read", "Loaned", "Format", "Rating"
            ))
            print("-" * 110)
            for book in books:
                print("{:<5} {:<15} {:<15} {:<30} {:<13} {:<6} {:<8} {:<9} {:<6}".format(
                    book[0] or "",
                    book[1] or "",
                    book[2] or "",
                    book[3] or "",
                    book[4] or "",
                    "Yes" if book[5] else "No",
                    "Yes" if book[6] else "No",
                    book[7] or "",
                    book[8] or ""
                ))
    except sqlite3.Error as e:
        print(f"There was an error retrieving the collection:\n{e}")
    finally:
        conn.close()

    input("\nPress Enter to return to the collection menu...")
    view_collection_page()


def add_book_page():
    print_header()
    active_table = get_active_collection()

    if not active_table:
        print("No ollection was found.")
        time.sleep(2)
        home_menu_page()
        return

    print(f"\n~~~~~~~~~~~~~~~~~~~~\n Add a Book to {active_table}\n~~~~~~~~~~~~~~~~~~~~")

    # Gather book info from user
    author_first = input("Enter Author First Name (or press Enter to skip): ").strip()
    author_last = input("Enter Author Last Name (or press Enter to skip): ").strip()
    title = input("Enter Book Title (required): ").strip()
    while not title:
        print("Title cannot be empty.")
        title = input("Enter Book Title (required): ").strip()

    isbn_input = input("Enter ISBN number (or press Enter to skip): ").strip()
    isbn = int(isbn_input) if isbn_input.isdigit() else None

    # Boolean fields
    read_input = input("Have you read this book? (y/n): ").lower().strip()
    read = 1 if read_input in ("y", "yes") else 0

    loaned_input = input("Is this book loaned out? (y/n): ").lower().strip()
    loaned = 1 if loaned_input in ("y", "yes") else 0

    # Format
    format_input = input("Format (Digital/Physical): ").strip().capitalize()
    while format_input not in ("Digital", "Physical", ""):
        print("Invalid choice. Please enter 'Digital' or 'Physical'.")
        format_input = input("Format (Digital/Physical): ").strip().capitalize()
    format_value = format_input if format_input else None

    # Rating
    rating_input = input("Rating (1-5, or press Enter to skip): ").strip()
    rating = int(rating_input) if rating_input.isdigit() and 1 <= int(rating_input) <= 5 else None

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO "{active_table}" 
            (author_first_name, author_last_name, title, isbn, read, loaned, format, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (author_first, author_last, title, isbn, read, loaned, format_value, rating))
        conn.commit()
        print(f"\nBook '{title}' added successfully to {active_table}!\n")
    except sqlite3.Error as e:
        print(f"Database error while adding book:\n{e}")
    finally:
        conn.close()

    input("Press Enter to return to the Home Menu...")
    home_menu_page()

    

                      
if __name__ == "__main__":
    main()