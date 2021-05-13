from werkzeug.security import generate_password_hash, check_password_hash


class Author:
    def __init__(self, id_a, lastnames, names, birth=None):
        self.id = id_a
        self.lastnames = lastnames
        self.names = names
        self.birth = birth

    def full_name(self):
        return "{0} {1}".format(self.lastnames, self.names)

    def encrypt_password(self, password):
        encrypted = generate_password_hash(password)
        value = check_password_hash(encrypted, password)
        return value
