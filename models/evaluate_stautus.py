from sqlalchemy import Column, Integer, String, CHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EvaluateStatus(Base):
    __tablename__ = "evaluate_status"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer,nullable=False)
    evaluated_point = Column(Integer,nullable=False)
    feedback_text = Column(String(600), nullable=True)
    evaluated_text_category = Column(String(30), nullable=True)
    annotated_at = Column(DateTime, nullable=False)
