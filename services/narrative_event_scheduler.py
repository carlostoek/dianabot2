import asyncio
import logging
from aiogram import Bot

logger = logging.getLogger(__name__)


async def start(bot: Bot) -> None:
    """Placeholder scheduler for narrative events."""
    while True:
        logger.debug("Narrative scheduler tick")
        await asyncio.sleep(3600)
