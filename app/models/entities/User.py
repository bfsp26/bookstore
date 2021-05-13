from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id_u, user, password, usertype):
        self.id = id_u
        self.user = user
        self.password = password
        self.usertype = usertype

    @classmethod
    def check_password(cls, encrypted, password):
        return check_password_hash(encrypted, password)
