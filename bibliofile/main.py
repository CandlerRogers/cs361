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
    selection = input("Enter 1 to use the app or 0 to exit: ")
    while selection.strip() != "1" and selection.strip() != "0":
        print(f"\nYou entered: {selection}. Please try again.")
        selection = input("Enter 1 to use the app or 0 to exit: ")
    match selection:
        case "1":
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
            view_collection_page
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
    new_name = input("\nPlease enter a new name for your collection or 0 to return to the previous menu: ")
    while new_name != '0':
        print(f"\nYou entered the new name: {new_name}\n")
        confirmed = input("Type confirm or retry: ").lower()
        while confirmed not in ["confirm",  "retry"]:
            print(f"\nYou entered the new name: {new_name}\n")
            confirmed = input("Type confirm or type retry: ").lower()
        if confirmed == "confirm":
            rename_collection(get_active_collection(), new_name)
            name_collection_page()
        else: 
            new_name = input("\nPlease enter a new name for your collection or 0 to return to the previous menu: ")
    if new_name == "0":
        home_menu_page()
    else: name_collection_page()

def view_collection_page():
    return

def add_book_page():
    return
    
    
                      
if __name__ == "__main__":
    main()