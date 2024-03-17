import sqlite3
from datetime import timezone, timedelta, datetime

class EvaluateStatusRepository:
    def __init__(self):
        self.conn = sqlite3.connect('public.sqlite')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def insert(self,dataset_id:int,evaluated_point: int,evaluate_text_category:str):
        """
        Insert a new record to evaluate_status table
        テキストを評価する。
        評価したテキストのstatusを'processed'に変更する。
        :param dataset_id:
        :param evaluated_point:
        :return:
        """
        JST = timezone(timedelta(hours=+9), 'JST')
        now = datetime.now(JST)
        insert_statement = (f"INSERT INTO evaluate_status (dataset_id, evaluated_point,evaluated_text_category,annotated_at)"
        
                            f" VALUES ('{dataset_id}', '{evaluated_point}',{evaluate_text_category},'{now}')")
        update_statement = (f"UPDATE datasets SET status = 'processed' WHERE id = '{dataset_id}'")
        try:
            self.c.execute(insert_statement)
            self.c.execute(update_statement)
        except Exception as e:
            print(e)
            if self.conn:
                self.conn.rollback()
        finally:
            if self.conn:
                self.conn.commit()


    def findOneByDatasetId(self,dataset_id:int):
        select_statement = (f"SELECT * FROM evaluate_status WHERE dataset_id = '{dataset_id}'")
        self.c.execute(select_statement)
        return self.c.fetchone()
    def exportAll(self):
        select_statement = (f"SELECT dataset_id,evaluated_point,text,evaluated_text_category FROM evaluate_status left join datasets on evaluate_status.dataset_id = datasets.id")
        self.c.execute(select_statement)
        return self.c.fetchall()

