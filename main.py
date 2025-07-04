import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

from config import BOT_TOKEN
from services.user_service import UserService
from services.vip_service import VIPService
from handlers.onboarding import onboarding_router
from handlers.backpack import backpack_router
from handlers.combination import combination_router
from handlers.vip_access import vip_router
from handlers.notifications import notifications_router
from handlers.gamification import gamification_router
from handlers.admin import admin_router
from middlewares.logging import LoggingMiddleware
from middlewares.vip_middleware import VIPMiddleware
from utils.notification_scheduler import notification_scheduler
from utils.helpers import get_onboarding_keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

user_service = UserService()
vip_service = VIPService()

dp.message.middleware(LoggingMiddleware())

dp.include_router(onboarding_router)
dp.include_router(backpack_router)
dp.include_router(combination_router)
dp.include_router(vip_router)
dp.include_router(notifications_router)
dp.include_router(gamification_router)
dp.include_router(admin_router)

@dp.message(CommandStart())
async def start_command(message: Message):
    """Send welcome menu and redeem VIP tokens if provided."""
    user = await user_service.get_or_create_user(message.from_user)

    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        token = parts[1]
        if await vip_service.redeem_token(user.telegram_id, token):
            await message.answer("🍿 Acceso VIP concedido. Bienvenido.")

    await message.answer(
        "El sistema está activo. ¿Qué te gustaría hacer?",
        reply_markup=get_onboarding_keyboard()
    )

async def main():
    scheduler_task = asyncio.create_task(notification_scheduler(bot))
    await dp.start_polling(bot)
    await scheduler_task

if __name__ == "__main__":
    asyncio.run(main())
