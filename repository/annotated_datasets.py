import sqlite3
from typing import Literal
class AnnotateRepository:
    def __init__(self):
        self.conn = sqlite3.connect('public.sqlite')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def insert(self,text:str,annotation: Literal['good','bad','pending']):
        insert_statement = f"INSERT INTO annotations (text, annotation) VALUES ('{text}', '{annotation}')"
        self.c.execute(insert_statement)
        self.conn.commit()

    def read(self):
        self.c.execute("SELECT * FROM annotations")
        result = self.c.fetchall()
        return result

    def close(self):
        self.conn.close()

