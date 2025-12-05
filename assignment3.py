import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Book:
    def _init_(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def _str_(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"


class LibraryInventory:
    def _init_(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        logging.info(f"Book added: {book.title}")

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        if not self.books:
            print("\nNo books in inventory.\n")
            return
        for b in self.books:
            print(b)


CATALOG_FILE = Path("catalog.json")

def save_to_file(inventory):
    try:
        data = [b.to_dict() for b in inventory.books]
        with open(CATALOG_FILE, "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Catalog saved to JSON.")
    except Exception as e:
        logging.error(f"Error saving catalog: {e}")

def load_from_file():
    inventory = LibraryInventory()
    try:
        if CATALOG_FILE.exists():
            with open(CATALOG_FILE, "r") as f:
                data = json.load(f)
            for entry in data:
                inventory.add_book(Book(**entry))
            logging.info("Catalog loaded from file.")
        else:
            logging.warning("Catalog file missing. Starting fresh.")
    except Exception as e:
        logging.error(f"Error loading catalog: {e}")
    return inventory


def main():
    inventory = load_from_file()

    while True:
        print("\n=========== LIBRARY MENU ===========")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")
        print("====================================")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input! Enter a number.")
            continue

        # 1. Add Book
        if choice == 1:
            try:
                title = input("Enter book title: ")
                author = input("Enter author: ")
                isbn = input("Enter ISBN: ")

                new_book = Book(title, author, isbn)
                inventory.add_book(new_book)
                save_to_file(inventory)

                print("\nBook added successfully!\n")
            except Exception as e:
                logging.error(f"Error adding book: {e}")

        # 2. Issue Book
        elif choice == 2:
            isbn = input("Enter ISBN to issue: ")
            book = inventory.search_by_isbn(isbn)
            if book:
                if book.issue():
                    print("Book issued successfully.")
                    save_to_file(inventory)
                else:
                    print("Book is already issued.")
            else:
                print("Book not found.")

        # 3. Return Book
        elif choice == 3:
            isbn = input("Enter ISBN to return: ")
            book = inventory.search_by_isbn(isbn)
            if book:
                if book.return_book():
                    print("Book returned successfully.")
                    save_to_file(inventory)
                else:
                    print("Book was not issued.")
            else:
                print("Book not found.")

        # 4. View All Books
        elif choice == 4:
            print("\n========== INVENTORY ==========\n")
            inventory.display_all()

        # 5. Search Book
        elif choice == 5:
            title = input("Enter book title to search: ")
            results = inventory.search_by_title(title)
            if results:
                print("\nSearch Results:")
                for book in results:
                    print(book)
            else:
                print("No matching books found.")

        # 6. Exit
        elif choice == 6:
            print("Exiting Library System. Goodbye!")
            save_to_file(inventory)
            break

        else:
            print("Invalid choice! Try again.")


if _name_ == "_main_":
    main()