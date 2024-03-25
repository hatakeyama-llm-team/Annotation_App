import sqlite3
from datetime import timezone, timedelta, datetime

from sqlalchemy.orm import Session

from models.evaluate_stautus import EvaluateStatus
from models.datasets import Datasets
from repository.cloud_sql_mysql.database import get_db


class EvaluateStatusRepository:

    def insert(self, dataset_id: int, evaluated_point: int,
               feedback_text:str, evaluated_text_category: str,
               ):
        """
        Insert a new record to evaluate_status table
        テキストを評価する。
        評価したテキストのstatusを'processed'に変更する。
        :param dataset_id:
        :param evaluated_point:
        :return:
        """

        db = next(get_db())
        JST = timezone(timedelta(hours=+9), 'JST')
        now = datetime.now(JST)
        evaluate_status = EvaluateStatus(
            dataset_id=dataset_id,
            evaluated_point=evaluated_point,
            feedback_text=feedback_text,
            evaluated_text_category=evaluated_text_category,
            annotated_at=now
        )
        db.add(
            evaluate_status
        )

        dataset_update = db.query(
            Datasets
        ).filter(
            Datasets.id == dataset_id
        ).first()
        dataset_update.status = 'processed'
        db.add(
            dataset_update
        )
        db.commit()
        db.close()

    def findOneByDatasetId(self, dataset_id: int):
        db = next(get_db())
        dataset = db.query(
            EvaluateStatus
        ).filter(
            EvaluateStatus.dataset_id == dataset_id
        ).first()
        db.close()

        return dataset

    def exportAll(self):
        db = next(get_db())
        datasets = db.query(
            Datasets.id,
            EvaluateStatus.evaluated_point,
            Datasets.cleaned_text,
            EvaluateStatus.feedback_text,
            EvaluateStatus.evaluated_text_category
        ).join(
            EvaluateStatus, EvaluateStatus.dataset_id == Datasets.id
        ).all()
        db.close()

        return datasets
