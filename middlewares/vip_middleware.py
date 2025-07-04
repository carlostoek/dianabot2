
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.future import select
from database_init import get_db
from models.core import User
from models.vip import VIPAccess
from datetime import datetime

class VIPMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user_id = event.from_user.id
            async for session in get_db():
                result = await session.execute(select(User).where(User.telegram_id == user_id))
                user = result.scalar_one_or_none()

                if user:
                    vip_result = await session.execute(
                        select(VIPAccess)
                        .where(VIPAccess.user_id == user.id)
                        .where(VIPAccess.is_active == True)
                        .where(VIPAccess.access_expires > datetime.utcnow())
                    )
                    vip_access = vip_result.scalar_one_or_none()

                    if vip_access:
                        return await handler(event, data)

            await event.answer("🚫 No tienes acceso VIP válido.")
            return None

        return await handler(event, data)
