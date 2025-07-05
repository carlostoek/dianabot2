from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from .base import BaseModel


class Channel(BaseModel):
    __tablename__ = "channels"

    name = Column(String, nullable=False)
    invite_link = Column(String, nullable=True)
    is_vip = Column(Boolean, default=False)


class ChannelMembership(BaseModel):
    __tablename__ = "channel_memberships"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    is_vip = Column(Boolean, default=False)
    is_pending = Column(Boolean, default=False)
    pending_until = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)


class EntryToken(BaseModel):
    __tablename__ = "entry_tokens"

    token = Column(String, unique=True, nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    is_vip = Column(Boolean, default=False)
    max_uses = Column(Integer, default=1)
    used_count = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=False)
    delay_seconds = Column(Integer, default=0)


class ChannelSettings(BaseModel):
    __tablename__ = "channel_settings"

    channel_id = Column(Integer, ForeignKey("channels.id"), unique=True, nullable=False)
    join_delay_seconds = Column(Integer, default=0)
    promo_message = Column(String, nullable=True)
