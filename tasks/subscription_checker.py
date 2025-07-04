
from sqlalchemy.future import select
from database_init import get_db
from models.vip import VIPAccess
from datetime import datetime

async def check_expired_subscriptions(bot):
    async for session in get_db():
        result = await session.execute(
            select(VIPAccess).where(VIPAccess.is_active == True, VIPAccess.access_expires < datetime.utcnow())
        )
        expired_subs = result.scalars().all()

        for vip_access in expired_subs:
            vip_access.is_active = False
            await bot.send_message(vip_access.user_id, "🔒 Tu acceso VIP ha expirado.")
        await session.commit()
