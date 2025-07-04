import sqlite3
from config import DATABASE_PATH

class VIPService:
    def __init__(self):
        self.db = DATABASE_PATH

    async def redeem_token(self, telegram_id, token):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, max_uses, used_count, expires_at FROM vip_tokens
            WHERE token = ? AND used_count < max_uses AND expires_at > datetime('now')
        """, (token,))
        vip_token = cursor.fetchone()

        if vip_token:
            cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
            user_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO vip_access (user_id, channel_id, access_granted, access_expires, is_active)
                VALUES (?, 1, datetime('now'), datetime('now', '+30 days'), 1)
            """, (user_id,))

            cursor.execute("""
                UPDATE vip_tokens SET used_count = used_count + 1 WHERE id = ?
            """, (vip_token[0],))

            conn.commit()
            conn.close()
            return True

        conn.close()
        return False
