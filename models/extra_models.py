import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, BigInteger, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class TriviaUserAnswer(Base):
    __tablename__ = "trivia_user_answers"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    trivia_id = Column(Integer, ForeignKey("trivias.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("trivia_questions.id"), nullable=False)
    answer = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)
    answered_at = Column(DateTime, default=func.now())


class ItemType(enum.Enum):
    CONSUMABLE = "consumable"
    KEY_ITEM = "key_item"
    COLLECTIBLE = "collectible"
    EQUIPMENT = "equipment"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    item_type = Column(Enum(ItemType), nullable=False)
    effect_data = Column(JSON, nullable=True)


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="inventory_items")
    item = relationship("Item")


class Hint(Base):
    __tablename__ = "hints"

    id = Column(Integer, primary_key=True)
    mission_id = Column(String, ForeignKey("missions.id"))
    hint_text = Column(String, nullable=False)
    unlock_after_minutes = Column(Integer, default=30)
    created_at = Column(DateTime, default=func.now())


class UserHint(Base):
    __tablename__ = "user_hints"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    hint_id = Column(Integer, ForeignKey("hints.id"))
    unlocked_at = Column(DateTime, default=func.now())


class Combination(Base):
    __tablename__ = "combinations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    required_items = Column(JSON, nullable=False)
    result_item_id = Column(Integer, ForeignKey("items.id"))
    created_at = Column(DateTime, default=func.now())


class UserCombination(Base):
    __tablename__ = "user_combinations"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    combination_id = Column(Integer, ForeignKey("combinations.id"))
    discovered_at = Column(DateTime, default=func.now())


class UserLevel(Base):
    __tablename__ = "user_levels"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    level_id = Column(Integer, ForeignKey("levels.level_id"))
    reached_at = Column(DateTime, default=func.now())


class UserDailyGift(Base):
    __tablename__ = "user_daily_gifts"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    claimed_at = Column(DateTime, default=func.now())
    gift_type = Column(String, nullable=False)
    gift_amount = Column(Integer, default=0)


class UserReferral(Base):
    __tablename__ = "user_referrals"

    id = Column(Integer, primary_key=True)
    referrer_id = Column(BigInteger, ForeignKey("users.id"))
    referred_id = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    owner_id = Column(BigInteger, ForeignKey("users.id"))
    uses = Column(Integer, default=0)
    max_uses = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())

