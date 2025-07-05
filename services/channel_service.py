from sqlalchemy.future import select
from database_init import get_db
from models.channel import ChannelToken, ChannelAccess
from models.core import User
from datetime import datetime, timedelta
import secrets

class ChannelService:
    async def create_token(self, channel_id: int, is_vip: bool, days_valid: int = 1,
                          max_uses: int = 1, delay_seconds: int = 0) -> ChannelToken:
        token_str = secrets.token_urlsafe(8)
        expires_at = datetime.utcnow() + timedelta(days=days_valid)
        async for session in get_db():
            new_token = ChannelToken(
                token=token_str,
                channel_id=channel_id,
                is_vip=is_vip,
                max_uses=max_uses,
                expires_at=expires_at,
                delay_seconds=delay_seconds,
            )
            session.add(new_token)
            await session.commit()
            await session.refresh(new_token)
            return new_token

    async def validate_token(self, telegram_id: int, token_str: str) -> bool:
        async for session in get_db():
            result = await session.execute(
                select(ChannelToken).where(ChannelToken.token == token_str)
            )
            token = result.scalar_one_or_none()
            if not token:
                return False

            if token.used_count >= token.max_uses or token.expires_at < datetime.utcnow():
                return False

            token.used_count += 1
            await session.commit()

            user_result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = user_result.scalar_one_or_none()
            if not user:
                return False

            access = ChannelAccess(
                user_id=user.id,
                channel_id=token.channel_id,
                is_vip=token.is_vip,
                is_pending=token.delay_seconds > 0,
                pending_until=datetime.utcnow() + timedelta(seconds=token.delay_seconds) if token.delay_seconds > 0 else None,
                access_expires=datetime.utcnow() + timedelta(days=30) if token.is_vip else None,
            )
            session.add(access)
            await session.commit()
            return True

    async def expire_access(self, bot):
        async for session in get_db():
            result = await session.execute(
                select(ChannelAccess).where(
                    ChannelAccess.is_active == True,
                    ChannelAccess.access_expires != None,
                    ChannelAccess.access_expires < datetime.utcnow()
                )
            )
            expired = result.scalars().all()
            for access in expired:
                access.is_active = False
                try:
                    await bot.send_message(access.user_id, "🔒 Tu acceso ha expirado.")
                except Exception:
                    pass
            await session.commit()

    async def activate_pending(self, bot):
        async for session in get_db():
            result = await session.execute(
                select(ChannelAccess).where(
                    ChannelAccess.is_pending == True,
                    ChannelAccess.pending_until != None,
                    ChannelAccess.pending_until < datetime.utcnow()
                )
            )
            pending = result.scalars().all()
            for access in pending:
                access.is_pending = False
                try:
                    await bot.send_message(access.user_id, "✅ Ahora tienes acceso al canal.")
                except Exception:
                    pass
            await session.commit()
