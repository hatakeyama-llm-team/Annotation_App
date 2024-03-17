import sqlite3


class UserRepository:

    def __init__(self):
        self.conn = sqlite3.connect('public.sqlite')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def login(self,user_name:str,password:str):
        """
        Insert a new record to user table
        ユーザーを登録する。
        :param user_name:
        :param password:
        :return:
        """

        # how to hash password
        import hashlib
        hash_password = hashlib.sha256(password.encode()).hexdigest()

        login_statement = (f"SELECT * FROM users WHERE user_name = '{user_name}' AND password = '{hash_password}'")
        self.c.execute(login_statement)
        if self.c.fetchone() is not None:
            return True
        else:
            return False


    def register(self,user_name,password):
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
            insert_statement = (f"INSERT INTO users (user_name, password)"
                                f" VALUES ('{user_name}', '{hash_password}')")
            try:
                self.c.execute(insert_statement)
            except Exception as e:
                print(e)
                if self.conn:
                    self.conn.rollback()
            finally:
                if self.conn:
                    self.conn.commit()
            return True
        else:
            raise Exception("User already exists")



    def findOneByUserName(self,user_name:str):
        select_statement = (f"SELECT * FROM users WHERE user_name = '{user_name}'")
        self.c.execute(select_statement)
        return self.c.fetchone()