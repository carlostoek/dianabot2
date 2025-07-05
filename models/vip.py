
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from models.base import Base

class Tariff(Base):
    __tablename__ = "vip_tariffs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    duration_days = Column(Integer, nullable=False)  # Duration in days
    cost = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tokens = relationship("VIPChannelAccess", back_populates="tariff")

class VIPChannelAccess(Base):
    __tablename__ = "vip_channel_access"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    tariff_id = Column(Integer, ForeignKey("vip_tariffs.id"), nullable=False)
    channel_id = Column(Integer, nullable=False)  # The Telegram channel ID
    generated_by_admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    used_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    used_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True) # Calculated based on tariff duration when used
    created_at = Column(DateTime, default=datetime.utcnow)

    tariff = relationship("Tariff", back_populates="tokens")
    generated_by = relationship("User", foreign_keys=[generated_by_admin_id])
    used_by = relationship("User", foreign_keys=[used_by_user_id])

class VIPAccess(Base):
    __tablename__ = "vip_access"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel_id = Column(Integer, nullable=False)
    access_granted = Column(DateTime, default=datetime.utcnow)
    access_expires = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    token_id = Column(Integer, ForeignKey("vip_channel_access.id"), nullable=True) # Link to the token that granted access

    token = relationship("VIPChannelAccess")

