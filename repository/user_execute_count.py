import sqlite3
from datetime import timezone, timedelta, datetime

class UserExecuteRepository:
    def __init__(self):
        self.conn = sqlite3.connect('public.sqlite')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def upsert(self,user_name:str):
        """
        Insert a new record to user_counts table
        ユーザーの実行回数をカウントする。
        :param user_name:
        :return:
        """
        JST = timezone(timedelta(hours=+9), 'JST')
        now = datetime.now(JST)
        select_statement = (f"SELECT * FROM user_counts WHERE user_name = '{user_name}'")
        self.c.execute(select_statement)
        result = self.c.fetchone()
        if result:
            update_statement = (f"UPDATE user_counts SET counts = counts + 1 WHERE user_name = '{user_name}'")
            try:
                self.c.execute(update_statement)
            except Exception as e:
                print(e)
                if self.conn:
                    self.conn.rollback()
            finally:
                if self.conn:
                    self.conn.commit()
        else:
            insert_statement = (f"INSERT INTO user_counts (user_name, counts,annotated_at)"
                                f" VALUES ('{user_name}', 1,'{now}')")
            try:
                self.c.execute(insert_statement)
            except Exception as e:
                print(e)
                if self.conn:
                    self.conn.rollback()
            finally:
                if self.conn:
                    self.conn.commit()
    def findCountByUserName(self,user_name:str):

        if user_name is None:
            user_counts = 0
        else:
            select_statement = (f"SELECT counts FROM user_counts WHERE user_name = '{user_name}'")
            self.c.execute(select_statement)
            user_counts = self.c.fetchone()[0]
        all_counts_statment = (f"SELECT COUNT(*) FROM datasets")
        self.c.execute(all_counts_statment)
        all_counts = self.c.fetchone()[0]

        unprocessed_counts_statment = (f"SELECT COUNT(*) FROM datasets WHERE status = 'unprocessed'")
        self.c.execute(unprocessed_counts_statment)
        unprocessed_counts = self.c.fetchone()

        if all_counts is None:
            all_counts = 0
        if unprocessed_counts is None:
            unprocessed_counts = 0

        return user_counts,all_counts,unprocessed_counts[0]
