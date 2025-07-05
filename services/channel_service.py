from sqlalchemy.future import select
from database_init import get_db
from models.channel_management import (
    Channel,
    ChannelMembership,
    EntryToken,
    ChannelSettings,
)
from models.user import User
from datetime import datetime, timedelta
import secrets


class ChannelService:
    async def register_channel(self, name: str, invite_link: str = None, is_vip: bool = False) -> Channel:
        async for session in get_db():
            channel = Channel(name=name, invite_link=invite_link, is_vip=is_vip)
            session.add(channel)
            await session.commit()
            await session.refresh(channel)
            return channel

    async def create_entry_token(
        self,
        channel_id: int,
        is_vip: bool,
        days_valid: int = 1,
        max_uses: int = 1,
        delay_seconds: int = 0,
    ) -> EntryToken:
        token_str = secrets.token_urlsafe(8)
        expires_at = datetime.utcnow() + timedelta(days=days_valid)
        async for session in get_db():
            token = EntryToken(
                token=token_str,
                channel_id=channel_id,
                is_vip=is_vip,
                max_uses=max_uses,
                expires_at=expires_at,
                delay_seconds=delay_seconds,
            )
            session.add(token)
            await session.commit()
            await session.refresh(token)
            return token

    async def validate_token(self, telegram_id: int, token_str: str) -> bool:
        async for session in get_db():
            result = await session.execute(select(EntryToken).where(EntryToken.token == token_str))
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

            membership = ChannelMembership(
                user_id=user.id,
                channel_id=token.channel_id,
                is_vip=token.is_vip,
                is_pending=token.delay_seconds > 0,
                pending_until=(
                    datetime.utcnow() + timedelta(seconds=token.delay_seconds)
                    if token.delay_seconds > 0
                    else None
                ),
                expires_at=datetime.utcnow() + timedelta(days=30) if token.is_vip else None,
            )
            session.add(membership)
            await session.commit()
            return True

    async def expire_memberships(self, bot):
        async for session in get_db():
            result = await session.execute(
                select(ChannelMembership).where(
                    ChannelMembership.is_active == True,
                    ChannelMembership.expires_at != None,
                    ChannelMembership.expires_at < datetime.utcnow(),
                )
            )
            expired = result.scalars().all()
            for membership in expired:
                membership.is_active = False
                try:
                    await bot.send_message(membership.user_id, "🔒 Tu acceso ha expirado.")
                except Exception:
                    pass
            await session.commit()

    async def activate_pending(self, bot):
        async for session in get_db():
            result = await session.execute(
                select(ChannelMembership).where(
                    ChannelMembership.is_pending == True,
                    ChannelMembership.pending_until != None,
                    ChannelMembership.pending_until < datetime.utcnow(),
                )
            )
            pending = result.scalars().all()
            for membership in pending:
                membership.is_pending = False
                try:
                    await bot.send_message(membership.user_id, "✅ Ahora tienes acceso al canal.")
                except Exception:
                    pass
            await session.commit()
