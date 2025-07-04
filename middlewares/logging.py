
import logging
from aiogram import BaseMiddleware
from aiogram.types import Message

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            logger.info(f"📥 Mensaje recibido de {event.from_user.id}: {event.text}")
        return await handler(event, data)
