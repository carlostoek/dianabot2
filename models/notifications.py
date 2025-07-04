
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notification_type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    tone = Column(String, nullable=False)
    character = Column(String, nullable=False)
    was_delivered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
