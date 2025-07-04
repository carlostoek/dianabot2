import sqlite3
from config import DATABASE_PATH
from models.narrative import LorePiece

class CombinationService:
    def __init__(self):
        self.db = DATABASE_PATH

    async def combine(self, telegram_id, code1, code2):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT l.combination_result
            FROM lore_pieces l
            WHERE l.code = ? OR l.code = ?
        """, (code1, code2))
        combination = cursor.fetchone()

        if combination and combination[0]:
            cursor.execute("SELECT * FROM lore_pieces WHERE code = ?", (combination[0],))
            new_piece = cursor.fetchone()

            if new_piece:
                cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
                user_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO user_backpacks (user_id, lore_piece_id, obtained_at)
                    VALUES (?, ?, datetime('now'))
                """, (user_id, new_piece[0]))

                conn.commit()
                conn.close()
                return LorePiece(*new_piece)

        conn.close()
        return None
