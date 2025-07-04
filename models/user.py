from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import relationship
from .base import BaseModel

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
    
    # Relaciones (se definen después para evitar imports circulares)
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username='{self.username}', level={self.level})>"
    
    @property
    def display_name(self):
        """Retorna el nombre a mostrar del usuario"""
        return self.username or self.first_name or f"Usuario_{self.telegram_id}"
    
    def can_afford(self, cost):
        """Verifica si el usuario puede pagar un costo en besitos"""
        return self.besitos >= cost
