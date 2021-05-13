from .entities.Author import Author
from .entities.Book import Book


class ModelBook:
    @classmethod
    def list_books(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT B.isbn, B.title, B.year, B.price,
            A.lastnames, A.names
            FROM book B JOIN author A ON B.author_id = A.id
            ORDER BY B.title ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            books = []
            for row in data:
                author = Author(0, row[4], row[5])
                book = Book(row[0], row[1], author, row[2], row[3])
                books.append(book)
            return books
        except Exception as ex:
            raise Exception(ex)
