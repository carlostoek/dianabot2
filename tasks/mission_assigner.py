import sqlite3
from config import DATABASE_PATH

async def assign_daily_missions(bot):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT id FROM missions")
    missions = cursor.fetchall()

    for user in users:
        for mission in missions:
            cursor.execute("""
                INSERT OR IGNORE INTO user_missions (user_id, mission_id)
                VALUES (?, ?)
            """, (user[0], mission[0]))

    conn.commit()
    conn.close()
    print("📅 Misiones diarias asignadas.")
