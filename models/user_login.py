from crud import user_crud


class UserLogin():
    def fromDB(self, user_login, db):
        self.__user = user_crud.get(db, user_login)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])
