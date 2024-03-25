import sqlite3
from typing import List

from sqlalchemy import func

from models.datasets import Datasets
from repository.cloud_sql_mysql.database import get_db


class DataSetsRepository:

    def insertBatch(self, datasets:List[Datasets]):
        print(f"{datasets} is inserted to datasets table")

        db = next(get_db())
        db.add_all(
            datasets
        )
        db.commit()
        db.close()
        return True

    def randomChoiseIdByUnprocessed(self):

        db = next(get_db())

        dataset_id = db.query(Datasets.id).filter(
            Datasets.status == 'unprocessed'
        ).order_by(func.random()).first()
        db.close()
        return dataset_id


    def findOneById(self, id: int):
        db = next(get_db())
        result = db.query(
            Datasets.cleaned_text
        ).filter(
            Datasets.id == id
        ).filter(
            Datasets.status == 'unprocessed'
        ).first()
        db.close()
        return result



