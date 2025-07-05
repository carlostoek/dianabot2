
from sqlalchemy.future import select
from sqlalchemy import insert
from sqlalchemy.orm import Session
from models.vip import Tariff, VIPChannelAccess, VIPAccess
from models.user import User
from datetime import datetime, timedelta
import uuid
from config import BOT_USERNAME

class VIPService:
    @staticmethod
    async def add_tariff(db: Session, name: str, duration_days: int, cost: float) -> Tariff:
        new_tariff = Tariff(name=name, duration_days=duration_days, cost=cost)
        db.add(new_tariff)
        db.commit()
        db.refresh(new_tariff)
        return new_tariff

    @staticmethod
    async def get_all_tariffs(db: Session):
        return db.query(Tariff).all()

    @staticmethod
    async def get_tariff_by_id(db: Session, tariff_id: int) -> Tariff | None:
        return db.query(Tariff).filter(Tariff.id == tariff_id).first()

    @staticmethod
    async def generate_vip_token(db: Session, tariff_id: int, channel_id: int, admin_id: int) -> str:
        token_uuid = str(uuid.uuid4())
        new_token = VIPChannelAccess(
            token=token_uuid,
            tariff_id=tariff_id,
            channel_id=channel_id,
            generated_by_admin_id=admin_id,
            is_active=True
        )
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
        
        # Generate deep link
        deep_link = f"https://t.me/{BOT_USERNAME}?start=vip_token_{token_uuid}"
        return deep_link

    @staticmethod
    async def validate_vip_token(db: Session, user_telegram_id: int, token_str: str) -> int | None:
        token_record = db.query(VIPChannelAccess).filter(VIPChannelAccess.token == token_str).first()

        if not token_record or not token_record.is_active or token_record.used_by_user_id is not None:
            return None # Token not found, inactive, or already used

        user = db.query(User).filter(User.telegram_id == user_telegram_id).first()
        if not user:
            return None # User not found

        tariff = db.query(Tariff).filter(Tariff.id == token_record.tariff_id).first()
        if not tariff:
            return None # Tariff not found (data inconsistency)

        # Mark token as used
        token_record.used_by_user_id = user.id
        token_record.used_at = datetime.utcnow()
        token_record.is_active = False # A token can only be used once

        # Calculate expiry based on tariff duration
        access_expires = datetime.utcnow() + timedelta(days=tariff.duration_days)
        token_record.expires_at = access_expires

        # Create VIPAccess entry for the user
        vip_access = VIPAccess(
            user_id=user.id,
            channel_id=token_record.channel_id,
            access_granted=datetime.utcnow(),
            access_expires=access_expires,
            is_active=True,
            token_id=token_record.id
        )
        db.add(vip_access)

        # Update user role to VIP if not already
        if user.role != UserRole.VIP:
            user.role = UserRole.VIP
            db.add(user)

        db.commit()
        db.refresh(vip_access)
        db.refresh(token_record)
        db.refresh(user)

        return token_record.channel_id

