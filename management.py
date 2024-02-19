import json
import re
import os

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.set_isbn(isbn)
        self.status = status

    def set_isbn(self, isbn):
        isbn_pattern = re.compile(r'^\d{4}-\d{4}-\d{4}$')
        if not isbn_pattern.match(isbn):
            raise ValueError("Invalid ISBN format. Please use the format: XXXX-XXXX-XXXX")
        self.isbn = isbn

class Library:
    def __init__(self, book_file="library_books.json"):
        self.book_file = book_file
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.book_file):
            with open(self.book_file, 'r') as file:
                books_data = json.load(file)
                return [Book(**book) for book in books_data]
        return []

    def save_books(self):
        books_data = [{"title": book.title, "author": book.author, "isbn": book.isbn, "status": book.status} for book in self.books]
        with open(self.book_file, 'w') as file:
            json.dump(books_data, file, indent=2)

    def add_book(self, title, author, isbn):
        try:
            new_book = Book(title, author, isbn)
            self.books.append(new_book)
            self.save_books()
            print("Book added successfully.")
        except ValueError as e:
            print(f"Error: {e}. Book not added.")

    def search_book(self, keyword, search_by="title"):
        if search_by not in ["title", "author"]:
            print("Invalid search criteria. Please choose 'title' or 'author'.")
            return []

        results = [book for book in self.books if keyword.lower() in getattr(book, search_by).lower()]
        return results

    def borrow_book(self, isbn):
        book = next((book for book in self.books if book.isbn == isbn), None)
        if book:
            if book.status == "available":
                book.status = "borrowed"
                self.save_books()
                print("Book borrowed successfully.")
            else:
                print("Book is not available for borrowing.")
        else:
            print("Book not found.")

    def return_book(self, isbn):
        book = next((book for book in self.books if book.isbn == isbn), None)
        if book:
            if book.status == "borrowed":
                book.status = "available"
                self.save_books()
                print("Book returned successfully.")
            else:
                print("Book is not borrowed.")
        else:
            print("Book not found.")

def main():
    library = Library()

    while True:
        print("\n1. Add a Book\n2. Borrow a Book\n3. Return a Book\n4. Search for a Book\n5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            title = input("Enter the book title: ")
            author = input("Enter the book author: ")
            isbn = input("Enter the book ISBN (format: XXXX-XXXX-XXXX): ")
            library.add_book(title, author, isbn)
        elif choice == '2':
            isbn = input("Enter ISBN of the book to borrow: ")
            library.borrow_book(isbn)
        elif choice == '3':
            isbn = input("Enter ISBN of the book to return: ")
            library.return_book(isbn)
        elif choice == '4':
            keyword = input("Enter search keyword: ")
            search_by = input("Search by title or author? ")
            results = library.search_book(keyword, search_by)
            for result in results:
                print(f"Title: {result.title}, Author: {result.author}, ISBN: {result.isbn}, Status: {result.status}")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
