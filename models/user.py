from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    VIP = "vip"
    FREE = "free"


class User(BaseModel):
    __tablename__ = 'users'

    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    level = Column(Integer, default=1)
    besitos = Column(Integer, default=100)
    total_besitos_earned = Column(BigInteger, default=100)
    current_story = Column(String(100), default="welcome")
    is_active = Column(Boolean, default=True)
    daily_streak = Column(Integer, default=0)

    # Sistema de roles
    role = Column(Enum(UserRole), default=UserRole.FREE)
    vip_expires_at = Column(DateTime(timezone=True), nullable=True)
    besitos_multiplier = Column(Float, default=1.0)

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username='{self.username}', role={self.role.value})>"

    @property
    def display_name(self):
        return self.username or self.first_name or f"Usuario_{self.telegram_id}"

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_vip(self):
        return self.role == UserRole.VIP

    @property
    def is_free(self):
        return self.role == UserRole.FREE

    @property
    def role_emoji(self):
        if self.is_admin:
            return "👑"
        elif self.is_vip:
            return "💎"
        else:
            return "🆓"

    def can_afford(self, cost):
        return self.besitos >= cost

