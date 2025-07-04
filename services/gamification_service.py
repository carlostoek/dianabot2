import sqlite3
from config import DATABASE_PATH
from models.gamification import Mission, DailyGift

class GamificationService:
    def __init__(self):
        self.db = DATABASE_PATH

    async def get_daily_missions(self, telegram_id):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.id, m.mission_type, m.title, m.description, m.reward_besitos, m.reward_lore
            FROM missions m
            JOIN user_missions um ON m.id = um.mission_id
            JOIN users u ON um.user_id = u.id
            WHERE u.telegram_id = ? AND um.completed = 0
        """, (telegram_id,))

        results = cursor.fetchall()
        conn.close()

        return [Mission(*row) for row in results]

    async def claim_daily_gift(self, telegram_id):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
        user_id = cursor.fetchone()

        if not user_id:
            conn.close()
            return None

        cursor.execute("""
            SELECT claimed_at FROM daily_gifts
            WHERE user_id = ? AND date(claimed_at) = date('now')
        """, (user_id[0],))
        already_claimed = cursor.fetchone()

        if already_claimed:
            conn.close()
            return None

        besitos_reward = 10
        lore_reward = 1

        cursor.execute("""
            INSERT INTO daily_gifts (user_id, claimed_at, besitos_reward, lore_reward)
            VALUES (?, datetime('now'), ?, ?)
        """, (user_id[0], besitos_reward, lore_reward))

        conn.commit()
        conn.close()

        return DailyGift(None, user_id[0], None, besitos_reward, lore_reward)
