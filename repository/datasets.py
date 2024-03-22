import sqlite3

class DataSetsRepository:
    def __init__(self):
        self.conn = sqlite3.connect('public.sqlite')
        self.c = self.conn.cursor()

        self.conn.commit()

    def __del__(self):
        self.conn.close()
    def insertBatch(self, data):
        print(f"{data} is inserted to datasets table")
        self.c.executemany('INSERT INTO datasets (cleaned_text,original_text, status, gz_path) VALUES (?,?,?,?)', data)
        self.conn.commit()

    def randomChoiseIdByUnprocessed(self):
        result = self.conn.execute('SELECT id FROM datasets WHERE status = "unprocessed" ORDER BY RANDOM() LIMIT 1')
        return result.fetchone()

    def findOneById(self, id: int):
        result = self.conn.execute('SELECT cleaned_text FROM datasets WHERE id = ? and status = "unprocessed"',
                          (id,))
        return result.fetchone()
