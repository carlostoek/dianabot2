
from aiogram import BaseMiddleware
from aiogram.types import Message
from config import ADMINS

class AdminAuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message) and event.from_user.id not in ADMINS:
            await event.answer("🚫 No tienes permisos para acceder a esta sección.")
            return None
        return await handler(event, data)
