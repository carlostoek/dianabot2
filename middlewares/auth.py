from aiogram import BaseMiddleware
from aiogram.types import Message

ADMIN_IDS = [123456789]  # Sustituye por el ID real del administrador

class AdminAuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        if event.from_user.id not in ADMIN_IDS:
            await event.answer("🔒 Acceso restringido solo para administradores.")
            return
        return await handler(event, data)
