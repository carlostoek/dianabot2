from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel
import enum

class ChannelType(enum.Enum):
    VIP = "vip"
    FREE = "free"

class Channel(BaseModel):
    __tablename__ = 'channels'

    channel_id = Column(BigInteger, unique=True, nullable=False, index=True)
    channel_name = Column(String(255), nullable=False)
    channel_type = Column(Enum(ChannelType), nullable=False)
    is_active = Column(Boolean, default=True)

    # Configuraciones específicas
    auto_accept = Column(Boolean, default=False)
    accept_delay = Column(Integer, default=0)
    welcome_message = Column(Text)

    # Relaciones
    tariffs = relationship("ChannelTariff", back_populates="channel")
    memberships = relationship("ChannelMembership", back_populates="channel")

class ChannelTariff(BaseModel):
    __tablename__ = 'channel_tariffs'

    channel_id = Column(BigInteger, ForeignKey('channels.id'), nullable=False)
    name = Column(String(100), nullable=False)
    duration_days = Column(Integer, nullable=False)
    price_besitos = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relaciones
    channel = relationship("Channel", back_populates="tariffs")
    tokens = relationship("EntryToken", back_populates="tariff")

class EntryToken(BaseModel):
    __tablename__ = 'entry_tokens'

    token = Column(String(255), unique=True, nullable=False, index=True)
    tariff_id = Column(BigInteger, ForeignKey('channel_tariffs.id'), nullable=False)
    created_by = Column(BigInteger, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)
    used_by = Column(BigInteger, nullable=True)
    used_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    tariff = relationship("ChannelTariff", back_populates="tokens")

class ChannelMembership(BaseModel):
    __tablename__ = 'channel_memberships'

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    channel_id = Column(BigInteger, ForeignKey('channels.id'), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    entry_token_id = Column(BigInteger, ForeignKey('entry_tokens.id'), nullable=True)

    # Relaciones
    user = relationship("User")
    channel = relationship("Channel", back_populates="memberships")
    entry_token = relationship("EntryToken")
