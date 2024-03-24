from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from google.cloud.sql.connector import Connector
import os
from dotenv import load_dotenv
# 環境変数から接続情報を取得

def init_db_connector():
    #DB接続ユーザ名。
    db_user = os.environ["DB_USER"]
    #DB接続パスワード
    db_pass = os.environ["DB_PASS"]
    #DB名
    db_name = os.environ["DB_NAME"]
    #接続するCloud SQLインスタンスを指定
    db_instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

    connector = Connector()
    return db_user,db_pass,db_name,db_instance_connection_name,connector

# Cloud SQL接続用インスタンスを取得。
def getconn():
    db_user, db_pass, db_name, db_instance_connection_name, connector = init_db_connector()
    conn = connector.connect(
        db_instance_connection_name,
        "pymysql",
        user=db_user,
        password=db_pass,
        db=db_name
    )
    return conn

# データベースセッションを取得するためのヘルパー関数を定義
def get_db():
    # SQLAlchemyのエンジンを作成
    engine = create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )

    # SessionLocalという名前のデータベースセッションクラスを作成
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # SQLAlchemyベースモデルを作成
    Base = declarative_base()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
