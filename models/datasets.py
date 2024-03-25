from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Datasets(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String(400), nullable=False)
    cleaned_text = Column(String(400), nullable=False)
    status = Column(String(400), nullable=False)
    gz_path = Column(String(400), nullable=False)
