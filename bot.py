import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

from handlers.onboarding import router as onboarding_router
from handlers.backpack import router as backpack_router
from handlers.combination import router as combination_router
from handlers.vip_access import router as vip_access_router
from handlers.gamification import router as gamification_router
from handlers.notifications import router as notifications_router
from handlers.channel_access import router as channel_access_router

from middlewares.logging import LoggingMiddleware
from middlewares.auth import AdminAuthMiddleware
from middlewares.vip_middleware import VIPMiddleware
from middlewares.narrative_middleware import NarrativeContextMiddleware
from utils.middlewares import error_handler
from utils.scheduler import run_scheduler


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.message.middleware(error_handler)
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(NarrativeContextMiddleware())
    dp.message.middleware(AdminAuthMiddleware())
    dp.message.middleware(VIPMiddleware())

    dp.include_router(onboarding_router)
    dp.include_router(backpack_router)
    dp.include_router(combination_router)
    dp.include_router(vip_access_router)
    dp.include_router(gamification_router)
    dp.include_router(notifications_router)
    dp.include_router(channel_access_router)

    asyncio.create_task(run_scheduler(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
