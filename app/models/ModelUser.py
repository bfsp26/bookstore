from .entities.User import User
from .entities.UserType import UserType


class ModelUser:
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT * FROM user WHERE user = '{0}'""".format(user.user)
            cursor.execute(sql)
            data = cursor.fetchone()
            if data is not None:
                match = User.check_password(data[2], user.password)
                if match:
                    logged_user = User(data[0], data[1], None, None)
                    return logged_user
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_id(cls, db, id_g):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT U.id, U.user, T.id, T.name
            FROM user U JOIN usertype T ON U.usertype_id = T.id
            WHERE U.id = {0}""".format(id_g)
            cursor.execute(sql)
            data = cursor.fetchone()
            usertype = UserType(data[2], data[3])
            logged_user = User(data[0], data[1], None, usertype)
            return logged_user
        except Exception as ex:
            raise Exception(ex)
