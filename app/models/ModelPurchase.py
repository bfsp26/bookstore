from .entities.Buyout import Buyout
from .entities.Book import Book

class ModelPurchase:
    @classmethod
    def register_purchase(cls, db, purchase):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO buyout (uuid, book_isbn, user_id)
            VALUES (uuid(), '{0}', {1})""".format(purchase.book.isbn, purchase.user.id)
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def list_user_purchase(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT P.date, B.isbn, B.title, B.price
            FROM buyout P JOIN book B ON P.book_isbn = B.isbn
            WHERE P.user_id = {0}""".format(user.id)
            cursor.execute(sql)
            data = cursor.fetchall()
            purchases = []
            for row in data:
                book = Book(row[1], row[2], None, None, row[3])
                purchase = Buyout(None, book, user, row[0])
                purchases.append(purchase)
            return purchases
        except Exception as ex:
            raise Exception(ex)
