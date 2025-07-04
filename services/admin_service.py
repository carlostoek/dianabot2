import sqlite3
from config import DATABASE_PATH

class AdminService:
    def __init__(self):
        self.db = DATABASE_PATH

    async def get_all_vip_tokens(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("SELECT token, max_uses, used_count, expires_at FROM vip_tokens")
        tokens = cursor.fetchall()

        conn.close()
        return tokens

    async def create_vip_token(self, token, max_uses, expires_at):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO vip_tokens (token, max_uses, expires_at)
            VALUES (?, ?, ?)
        """, (token, max_uses, expires_at))

        conn.commit()
        conn.close()
