import sqlite3

from models.users import User

from repository.cloud_sql_mysql.database import get_db
import hashlib


class UserRepository:

    def login(self, user_name: str, password: str):
        """
        Insert a new record to user table
        ユーザーを登録する。
        :param user_name:
        :param password:
        :return:
        """

        hash_password = hashlib.sha256(password.encode()).hexdigest()

        db = next(get_db())
        is_exist_user_can_login = db.query(
            User
        ).filter(
            User.user_name == user_name
        ).filter(
            User.password == hash_password
        ).first()
        db.close()
        if is_exist_user_can_login is not None:
            return True
        else:
            return False

    def register(self, user_name, password):
        """
        Insert a new record to user table
        ユーザーを登録する。
        :param user_name:
        :param password:
        :return:
        """
        if user_name is None or password is None:
            raise Exception("User name or password is empty")

        # how to hash password
        import hashlib
        hash_password = hashlib.sha256(password.encode()).hexdigest()

        register_user = self.findOneByUserName(user_name)
        if register_user is None:

            db = next(get_db())
            user = User(
                user_name=user_name,
                password=hash_password,
            )
            db.add(
                user
            )
            db.commit()
            db.close()

            return True
        else:
            raise Exception("User already exists")

    def findOneByUserName(self, user_name: str):
        db = next(get_db())
        user = db.query(
            User
        ).filter(
            User.user_name == user_name
        ).first()
        db.close()
        if user is None:
            return None
        else:
            return user.user_name
