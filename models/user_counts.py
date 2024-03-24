from sqlalchemy import Column, Integer, String, CHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserCounts(Base):
    __tablename__ = "user_counts"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), nullable=False)
    counts = Column(Integer, nullable=False)
    annotated_at = Column(DateTime, nullable=True)