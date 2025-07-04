
from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f"❌ Error no controlado: {e}", exc_info=True)
            if isinstance(event, Message):
                await event.answer("⚙️ Algo ha salido terriblemente mal. Intenta de nuevo más tarde.")
            return None

error_handler = ErrorHandlerMiddleware()
