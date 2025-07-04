
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class LorePiece(Base):
    __tablename__ = "lore_pieces"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    rarity = Column(String, nullable=False)

class UserBackpack(Base):
    __tablename__ = "user_backpacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lore_piece_id = Column(Integer, ForeignKey("lore_pieces.id"), nullable=False)
    obtained_at = Column(DateTime, default=datetime.utcnow)
