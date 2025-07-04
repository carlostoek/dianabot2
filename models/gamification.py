
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    mission_type = Column(String, nullable=False)  # daily o story
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    reward_besitos = Column(Integer, default=0)
    reward_lore = Column(Integer, ForeignKey("lore_pieces.id"), nullable=True)

class UserMission(Base):
    __tablename__ = "user_missions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    progress = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    claimed = Column(Boolean, default=False)

class DailyGift(Base):
    __tablename__ = "daily_gifts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    claimed_at = Column(DateTime, default=datetime.utcnow)
    besitos_reward = Column(Integer, default=10)
