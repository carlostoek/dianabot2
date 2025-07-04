
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class VIPAccess(Base):
    __tablename__ = "vip_access"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel_id = Column(Integer, nullable=False)
    access_granted = Column(DateTime, default=datetime.utcnow)
    access_expires = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

class VIPToken(Base):
    __tablename__ = "vip_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    max_uses = Column(Integer, default=1)
    used_count = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=False)
