from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel

class Mission(BaseModel):
    __tablename__ = 'missions'
    
    mission_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    reward_besitos = Column(Integer, default=0)
    required_level = Column(Integer, default=1)
    mission_type = Column(String(50), default='daily')
    is_daily = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    one_time_only = Column(Boolean, default=False)

class UserMission(BaseModel):
    __tablename__ = 'user_missions'
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    mission_id = Column(String(50), nullable=False)
    is_completed = Column(Boolean, default=False)
    completion_date = Column(String(10))  # YYYY-MM-DD format
    completion_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    progress_data = Column(Text)  # JSON para progreso específico
    
    # Relaciones
    user = relationship("User")
