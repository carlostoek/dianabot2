import sqlite3
from config import DATABASE_PATH
from models.core import User
from datetime import datetime

class UserService:
    def __init__(self):
        self.db = DATABASE_PATH

    async def get_or_create_user(self, tg_user):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (tg_user.id,))
        result = cursor.fetchone()

        if result:
            user = User(*result)
        else:
            now = datetime.utcnow().isoformat()
            cursor.execute(
                "INSERT INTO users (telegram_id, username, first_name, created_at) VALUES (?, ?, ?, ?)",
                (tg_user.id, tg_user.username, tg_user.first_name or "Usuario", now)
            )
            conn.commit()
            user_id = cursor.lastrowid
            user = User(user_id, tg_user.id, tg_user.username, tg_user.first_name or "Usuario", False, now)

        conn.close()
        return user

    async def mark_as_onboarded(self, telegram_id):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_onboarded = 1 WHERE telegram_id = ?", (telegram_id,))
        conn.commit()
        conn.close()
