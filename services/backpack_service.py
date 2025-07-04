import sqlite3
from config import DATABASE_PATH
from models.narrative import LorePiece, UserBackpack

class BackpackService:
    def __init__(self):
        self.db = DATABASE_PATH

    async def get_user_backpack(self, telegram_id):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT l.id, l.code, l.title, l.description, l.rarity
            FROM user_backpacks ub
            JOIN users u ON ub.user_id = u.id
            JOIN lore_pieces l ON ub.lore_piece_id = l.id
            WHERE u.telegram_id = ?
        """, (telegram_id,))

        results = cursor.fetchall()
        conn.close()

        return [LorePiece(*row) for row in results]
