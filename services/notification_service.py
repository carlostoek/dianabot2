import sqlite3
from config import DATABASE_PATH

class NotificationService:
    def __init__(self):
        self.db = DATABASE_PATH

    async def create_notification(self, telegram_id, notification_type, message_text, tone, character):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
        user_id = cursor.fetchone()

        if user_id:
            cursor.execute("""
                INSERT INTO notifications (user_id, notification_type, message, tone, character, was_delivered)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (user_id[0], notification_type, message_text, tone, character))

            conn.commit()

        conn.close()
