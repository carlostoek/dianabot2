import sqlite3
from config import DATABASE_PATH

async def check_subscriptions(bot):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE vip_access
        SET is_active = 0
        WHERE access_expires < datetime('now')
    """)
    conn.commit()
    conn.close()
    print("♻️ Suscripciones verificadas y expiradas desactivadas.")
