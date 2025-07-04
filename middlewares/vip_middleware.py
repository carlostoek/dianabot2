from aiogram import BaseMiddleware
from aiogram.types import Message
import sqlite3
from config import DATABASE_PATH

class VIPMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM vip_access va
            JOIN users u ON va.user_id = u.id
            WHERE u.telegram_id = ? AND va.is_active = 1 AND va.access_expires > datetime('now')
        """, (event.from_user.id,))
        is_vip = cursor.fetchone()[0] > 0

        conn.close()

        if not is_vip:
            await event.answer("🔒 Esta función es solo para usuarios VIP.")
            return

        return await handler(event, data)
