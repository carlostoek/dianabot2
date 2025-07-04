
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, Command
from aiogram import Router
from database_init import init_db

async def main():
    await init_db()  # Esto debe ir aquí
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    ...

from config import BOT_TOKEN
from handlers import onboarding, backpack
from utils.middlewares import error_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Iniciar el bot"),
        BotCommand(command="/help", description="Ayuda general"),
        BotCommand(command="/backpack", description="Ver mi mochila"),
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.outer_middleware(error_handler)

    dp.include_router(onboarding.router)
    dp.include_router(backpack.router)

    await set_bot_commands(bot)
    logger.info("🚀 Bot iniciado con éxito")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
