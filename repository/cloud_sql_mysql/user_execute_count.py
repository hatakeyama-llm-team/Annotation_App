import sqlite3
from datetime import timezone, timedelta, datetime
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from models.datasets import Datasets
from models.user_counts import UserCounts
from repository.cloud_sql_mysql.database import get_db


class UserExecuteRepository:
    def __init__(self):
        self.conn = sqlite3.connect('public.sqlite')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def upsert(self, user_name: str):
        """
        Insert a new record to user_counts table
        ユーザーの実行回数をカウントする。
        :param user_name:
        :return:
        """
        db = next(get_db())
        JST = timezone(timedelta(hours=+9), 'JST')
        now = datetime.now(JST)
        user_pre_count = db.query(
            UserCounts
        ).filter(
            UserCounts.user_name == user_name
        ).first()

        if user_pre_count is not None:
            # ある場合は更新する
            user_pre_count.counts += 1
            user_pre_count.annotated_at = now
            db.add(user_pre_count)
            db.commit()
            db.close()
        else:
            # ない場合は追加する
            user_count = UserCounts(
                user_name=user_name,
                counts=1,
                annotated_at=now
            )
            db.add(
                user_count
            )
            db.commit()
            db.close()

    def findCountByUserName(self, user_name: str):
        db = next(get_db())
        user_counts = db.query(
            UserCounts.counts
        ).filter(
            UserCounts.user_name == user_name
        ).first()

        if user_counts is None:
            user_counts = 0
        else:
            user_counts = user_counts[0]

        all_counts = db.query(
            Datasets
        ).count()

        unprocessed_counts = db.query(
            Datasets
        ).filter(
            Datasets.status == 'unprocessed'
        ).count()
        db.close()

        return user_counts, all_counts, unprocessed_counts
