from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from psycopg2 import OperationalError
import sys

try:
    engine = create_engine("postgresql://postgres:baza@localhost:5432/postgres", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
except OperationalError as error:
    print(f"Connection error: {error}")
    exit()

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    author_id = Column(Integer, ForeignKey('authors.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    author = relationship('Author', back_populates='books')
    genre = relationship('Genre', back_populates='books')

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    books = relationship('Book', back_populates='author')

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    books = relationship('Book', back_populates='genre')

Base.metadata.create_all(engine)

def insert_author():
    name = input("Enter the author's name: ")
    if session.query(Author).filter_by(name=name).first():
        print("Author already exists.")
        return
    new_author = Author(name=name)
    session.add(new_author)
    session.commit()
    print("Author has been added.")

def insert_genre():
    name = input("Enter the genre name: ")
    if session.query(Genre).filter_by(name=name).first():
        print("Genre already exists.")
        return
    new_genre = Genre(name=name)
    session.add(new_genre)
    session.commit()
    print("Genre has been added.")

def delete_author():
    _id = int(input("Enter the author ID to delete >> "))
    author = session.query(Author).filter(Author.id == _id).first()
    if author:
        if session.query(Book).filter(Book.author_id == _id).count() > 0:
            print("Cannot delete author because they are associated with books.")
        else:
            session.delete(author)
            session.commit()
            print("Author has been deleted.")
    else:
        print("No author found with the given ID.")

def delete_genre():
    _id = int(input("Enter the genre ID to delete >> "))
    genre = session.query(Genre).filter(Genre.id == _id).first()
    if genre:
        if session.query(Book).filter(Book.genre_id == _id).count() > 0:
            print("Cannot delete genre because it is associated with books.")
        else:
            session.delete(genre)
            session.commit()
            print("Genre has been deleted.")
    else:
        print("No genre found with the given ID.")

def check_author_exists(author_id):
    existing_author = session.query(Author).filter_by(id=author_id).first()
    return existing_author is not None

def check_genre_exists(genre_id):
    existing_genre = session.query(Genre).filter_by(id=genre_id).first()
    return existing_genre is not None

def insert_book():
    print("Add a new book: ")
    _title = input("Book title: ")
    _author_id = input("Author ID: ")
    _genre_id = input("Genre ID: ")
    if check_author_exists(_author_id) and check_genre_exists(_genre_id):
        new_book = Book(title=_title, author_id=_author_id, genre_id=_genre_id)
        session.add(new_book)
        session.commit()
        print("Book has been added.")
    else:
        print("Author or genre with the given ID does not exist.")

def show_books():
    print("List of books:")
    for book in session.query(Book).all():
        print(f"ID: {book.id}, Title: {book.title}, Author ID: {book.author_id}, Genre ID: {book.genre_id}")

def show_authors():
    print("List of authors:")
    for author in session.query(Author).all():
        print(f"ID: {author.id}, Name: {author.name}")

def show_genres():
    print("List of genres:")
    for genre in session.query(Genre).all():
        print(f"ID: {genre.id}, Name: {genre.name}")

def edit_book():
    _id = int(input("Enter the book ID to edit >> "))
    book = session.query(Book).filter(Book.id == _id).first()
    if book:
        _title = input("New book title >> ")
        _author_id = input("New author ID >> ")
        _genre_id = input("New genre ID >> ")
        if check_author_exists(_author_id) and check_genre_exists(_genre_id):
            book.title = _title if _title else book.title
            book.author_id = _author_id if _author_id else book.author_id
            book.genre_id = _genre_id if _genre_id else book.genre_id
            session.commit()
            print("Book has been updated.")
        else:
            print("Author or genre with the given ID does not exist.")

def delete_book():
    _id = int(input("Enter the book ID to delete >> "))
    book = session.query(Book).filter(Book.id == _id).first()
    if book:
        session.delete(book)
        session.commit()
        print("Book has been deleted.")

def menu():
    while True:
        print("""Options:
        0. Exit.
        1. Show books.    
        2. Add a book.
        3. Delete a book.
        4. Edit a book.
        5. Show authors.
        6. Add an author.
        7. Delete an author.
        8. Show genres.
        9. Add a genre.
        10. Delete a genre.
        """)
        choice = input("Choose an option: ")
        if choice == "0":
            session.close()
            sys.exit()
        elif choice == "1":
            show_books()
        elif choice == "2":
            insert_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            edit_book()
        elif choice == "5":
            show_authors()
        elif choice == "6":
            insert_author()
        elif choice == "7":
            delete_author()
        elif choice == "8":
            show_genres()
        elif choice == "9":
            insert_genre()
        elif choice == "10":
            delete_genre()
        else:
            print("Try again.")

menu()