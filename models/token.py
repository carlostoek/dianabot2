from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from .base import Base

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    duration_days = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Token(id={self.id}, name='{self.name}', duration_days={self.duration_days}, price={self.price})>"
