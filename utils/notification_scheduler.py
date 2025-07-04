
import asyncio
from aiogram import Bot
from sqlalchemy.future import select
from database_init import get_db
from models.core import User
from services.notification_service import NotificationService

async def send_random_notifications(bot: Bot):
    notification_service = NotificationService()

    while True:
        async for session in get_db():
            result = await session.execute(select(User))
            users = result.scalars().all()

            for user in users:
                notification = await notification_service.create_notification(user.telegram_id)
                if notification:
                    try:
                        await bot.send_message(user.telegram_id, f"{notification['character']} {notification['message']}")
                    except Exception:
                        pass

        await asyncio.sleep(3600)  # Ejecutar cada hora
