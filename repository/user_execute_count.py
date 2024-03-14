import sqlite3
from datetime import timezone, timedelta, datetime

class EvaluateStatusRepository:
    def __init__(self):
        self.conn = sqlite3.connect('public.sqlite')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def insert(self,dataset_id:int,evaluation_point: int):
        JST = timezone(timedelta(hours=+9), 'JST')
        now = datetime.now(JST)
        insert_statement = (f"INSERT INTO evaluate_status (dataset_id, evaluation_point,annotated_at)"
                            f" VALUES ('{dataset_id}', '{evaluation_point}','{now}')")
        self.c.execute(insert_statement)
        self.conn.commit()

    def findOneByDatasetId(self,dataset_id:int):
        select_statement = (f"SELECT * FROM evaluate_status WHERE dataset_id = '{dataset_id}'")
        self.c.execute(select_statement)
        return self.c.fetchone()


