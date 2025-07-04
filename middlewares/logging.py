from aiogram import BaseMiddleware
from aiogram.types import Message

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        print(f"📥 Mensaje recibido: {event.text} de {event.from_user.id}")
        return await handler(event, data)
