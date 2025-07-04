from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from .base import BaseModel

class GameSession(BaseModel):
    __tablename__ = 'game_sessions'
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_type = Column(String(50), nullable=False)
    status = Column(String(20), default='active')
    score = Column(Integer, default=0)
    max_score = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    current_data = Column(Text)
    time_spent = Column(Integer, default=0)
    besitos_earned = Column(Integer, default=0)
    experience_gained = Column(Integer, default=0)
    
    # Relaciones
    user = relationship("User")

class GameLeaderboard(BaseModel):
    __tablename__ = 'game_leaderboards'
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_type = Column(String(50), nullable=False)
    best_score = Column(Integer, default=0)
    total_games = Column(Integer, default=0)
    total_time = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    
    # Relaciones
    user = relationship("User")
