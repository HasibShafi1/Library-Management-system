from abc import ABC, abstractmethod
import json


class Person(ABC):
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    @abstractmethod
    def get_info(self):
        pass


class User(Person):
    def __init__(self, user_type, name, user_id):
        super().__init__(name, user_id)
        self.user_type = user_type
        self.borrowed_books = []
        self.activity_log = []

    def borrow_book(self, book):
        if book not in self.borrowed_books:
            self.borrowed_books.append(book)
            self.activity_log.append(f"Borrowed {book.get_title()}")
            print(f"{book.get_title()} borrowed successfully!")
        else:
            print(f"You already borrowed {book.get_title()}.")

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            self.activity_log.append(f"Returned {book.get_title()}")
            print(f"{book.get_title()} returned successfully!")
        else:
            print(f"You did not borrow {book.get_title()}.")

    def reserve_book(self, book):
        self.activity_log.append(f"Reserved {book.get_title()}")
        print(f"{book.get_title()} reserved successfully!")

    def view_borrowed_books(self):
        if self.borrowed_books:
            print("Your borrowed books:")
            for book in self.borrowed_books:
                print(f"- {book.get_title()}")
        else:
            print("No borrowed books.")

    def view_activity_log(self):
        if self.activity_log:
            print("Your activity log:")
            for log in self.activity_log:
                print(f"- {log}")
        else:
            print("No activity log available.")

    def add_book_rating(self, book, rating):
        print(f"Rating {rating} added to {book.get_title()}")
        self.activity_log.append(f"Rated {book.get_title()} with {rating} stars")

    def get_info(self):
        return f"Name: {self.name}, ID: {self.user_id}, Type: {self.user_type}"


class Student(User):
    def __init__(self, name, user_id):
        super().__init__("student", name, user_id)

    def get_info(self):
        return f"Student Name: {self.name}, ID: {self.user_id}"

class Staff(User):
    def __init__(self, name, user_id):
        super().__init__("staff", name, user_id)

    def get_info(self):
        return f"Staff Name: {self.name}, ID: {self.user_id}"


class Admin(Person):
    def __init__(self, username, password):
        super().__init__(username, "ADMIN")
        self.password = password

    def authenticate(self, username, password):
        return self.name == username and self.password == password

    def add_book(self, library, title, author, genre, isbn):
        library.add_book(title, author, genre, isbn)

    def remove_book(self, library, isbn):
        library.remove_book(isbn)

    def list_all_books(self, library):
        library.list_books()

    def list_all_users(self, library):
        library.list_users()

    def add_user(self, library, user):
        library.add_user(user)

    def get_info(self):
        return f"Admin Username: {self.name}"


class Book:
    def __init__(self, title, author, genre, isbn):
        self.title = title
        self.author = author
        self.genre = genre
        self.isbn = isbn

    def get_title(self):
        return self.title

    def get_info(self):
        return f"Title: {self.title}, Author: {self.author}, Genre: {self.genre}, ISBN: {self.isbn}"


class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.load_data()

    def add_book(self, title, author, genre, isbn):
        book = Book(title, author, genre, isbn)
        self.books.append(book)
        print(f"Book '{title}' added successfully.")
        self.save_data()

    def remove_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                print(f"Book with ISBN {isbn} removed successfully.")
                self.save_data()
                return
        print(f"Book with ISBN {isbn} not found.")

    def list_books(self):
        if self.books:
            print("Available books:")
            for book in self.books:
                print(f"- {book.get_info()}")
        else:
            print("No books available.")

    def add_user(self, user):
        self.users.append(user)
        print(f"User '{user.name}' added successfully.")
        self.save_data()

    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def list_users(self):
        if self.users:
            print("Registered users:")
            for user in self.users:
                print(f"- {user.get_info()}")
        else:
            print("No registered users.")

    def save_data(self):
        data = {
            "books": [
                {
                    "title": book.title,
                    "author": book.author,
                    "genre": book.genre,
                    "isbn": book.isbn
                } for book in self.books
            ],
            "users": [
                {
                    "name": user.name,
                    "user_id": user.user_id,
                    "user_type": user.user_type,
                    "borrowed_books": [book.get_title() for book in user.borrowed_books],
                    "activity_log": user.activity_log
                } for user in self.users
            ]
        }
        with open("library_data.json", "w") as file:
            json.dump(data, file)

    def load_data(self):
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)
            for book_data in data.get("books", []):
                self.books.append(Book(book_data["title"], book_data["author"], book_data["genre"], book_data["isbn"]))
            for user_data in data.get("users", []):
                user = Student(user_data["name"], user_data["user_id"]) if user_data["user_type"] == "student" else Staff(user_data["name"], user_data["user_id"])
                user.borrowed_books = [Book(book, "", "", "") for book in user_data["borrowed_books"]]
                user.activity_log = user_data["activity_log"]
                self.users.append(user)
        except FileNotFoundError:
            pass


def main():
    library = Library()
    admin = Admin("hasib", "hasib1212")
    
    
    library.add_book("Alita", "Humayun Ahmed", "Novel", "10")
    library.add_book("Lal Salu", "Ashok Mitra", "Novel", "11")
    library.add_book("Naihshobder Gondo", "Salahuddin", "Poetry", "12")
    library.add_book("Amar Ekti Khola Chithi", "Selina Hossain", "Letters", "13")
    library.add_book("Bangladesh's Liberation War", "Shamsuzzaman Khan", "History", "14")
    library.add_book("The Story of the Universe", "Zafar Iqbal", "Science", "15")

    
    library.add_user(Student("Alif", "S001"))
    library.add_user(Staff("Rahim", "T001"))

    while True:
        print("\nLibrary Menu:")
        print("1. Add Book (Admin Only)")
        print("2. Remove Book (Admin Only)")
        print("3. Search Books")
        print("4. Add User (Admin Only)")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Reserve Book")
        print("8. View Borrowed Books")
        print("9. View User Activity Log")
        print("10. Add Book Rating")
        print("11. List All Books (Admin Only)")
        print("12. List All Users (Admin Only)")
        print("13. Admin Login")
        print("14. Exit")

        choice = input("Enter your choice: ")

        if choice == "1" or choice == "2" or choice == "4" or choice == "11" or choice == "12":
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            if admin.authenticate(username, password):
                if choice == "1":
                    title = input("Enter book title: ")
                    author = input("Enter book author: ")
                    genre = input("Enter book genre: ")
                    isbn = input("Enter book ISBN: ")
                    admin.add_book(library, title, author, genre, isbn)
                elif choice == "2":
                    isbn = input("Enter book ISBN to remove: ")
                    admin.remove_book(library, isbn)
                elif choice == "4":
                    name = input("Enter user name: ")
                    user_id = input("Enter user ID: ")
                    user_type = input("Enter user type (student/staff): ").lower()
                    if user_type == "student":
                        user = Student(name, user_id)
                    elif user_type == "staff":
                        user = Staff(name, user_id)
                    else:
                        print("Invalid user type!")
                        continue
                    admin.add_user(library, user)
                elif choice == "11":
                    admin.list_all_books(library)
                elif choice == "12":
                    admin.list_all_users(library)
            else:
                print("Invalid admin credentials!")

        elif choice == "3":
            search_query = input("Enter book title to search: ").lower()
            found_books = [book for book in library.books if search_query in book.get_title().lower()]
            if found_books:
                print("Search Results:")
                for book in found_books:
                    print(f"- {book.get_info()}")
            else:
                print("No books found!")

        elif choice == "5":
            user_id = input("Enter your user ID: ")
            user = library.get_user(user_id)
            if user:
                title = input("Enter the title of the book to borrow: ")
                for book in library.books:
                    if book.get_title().lower() == title.lower():
                        user.borrow_book(book)
                        library.save_data()
                        break
                else:
                    print("Book not found!")
            else:
                print("User not found!")

        elif choice == "6":
            user_id = input("Enter your user ID: ")
            user = library.get_user(user_id)
            if user:
                title = input("Enter the title of the book to return: ")
                for book in user.borrowed_books:
                    if book.get_title().lower() == title.lower():
                        user.return_book(book)
                        library.save_data()
                        break
                else:
                    print("Book not found in your borrowed list!")
            else:
                print("User not found!")

        elif choice == "7":
            user_id = input("Enter your user ID: ")
            user = library.get_user(user_id)
            if user:
                title = input("Enter the title of the book to reserve: ")
                for book in library.books:
                    if book.get_title().lower() == title.lower():
                        user.reserve_book(book)
                        library.save_data()
                        break
                else:
                    print("Book not found!")
            else:
                print("User not found!")

        elif choice == "8":
            user_id = input("Enter your user ID: ")
            user = library.get_user(user_id)
            if user:
                user.view_borrowed_books()
            else:
                print("User not found!")

        elif choice == "9":
            user_id = input("Enter your user ID: ")
            user = library.get_user(user_id)
            if user:
                user.view_activity_log()
            else:
                print("User not found!")

        elif choice == "10":
            user_id = input("Enter your user ID: ")
            user = library.get_user(user_id)
            if user:
                title = input("Enter the title of the book to rate: ")
                for book in library.books:
                    if book.get_title().lower() == title.lower():
                        rating = int(input("Enter your rating (1-5): "))
                        if 1 <= rating <= 5:
                            user.add_book_rating(book, rating)
                            library.save_data()
                        else:
                            print("Invalid rating. Please enter a value between 1 and 5.")
                        break
                else:
                    print("Book not found!")
            else:
                print("User not found!")

        elif choice == "13":
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            if admin.authenticate(username, password):
                print("Admin login successful!")
            else:
                print("Invalid admin credentials!")

        elif choice == "14":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
