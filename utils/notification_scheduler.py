import asyncio
import sqlite3
from config import DATABASE_PATH
from aiogram import Bot

async def notification_scheduler(bot: Bot):
    while True:
        await asyncio.sleep(60)

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.telegram_id, n.message
            FROM notifications n
            JOIN users u ON n.user_id = u.id
            WHERE n.was_delivered = 0
        """)
        notifications = cursor.fetchall()

        for telegram_id, message in notifications:
            try:
                await bot.send_message(telegram_id, f"🎲 {message}")
                cursor.execute("""
                    UPDATE notifications SET was_delivered = 1
                    WHERE user_id = (SELECT id FROM users WHERE telegram_id = ?)
                """, (telegram_id,))
            except Exception as e:
                print(f"❌ Error enviando notificación a {telegram_id}: {e}")

        conn.commit()
        conn.close()
