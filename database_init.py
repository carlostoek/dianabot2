import sqlite3
from config import DATABASE_PATH

def initialize_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            is_onboarded INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lore_pieces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            title TEXT,
            description TEXT,
            rarity TEXT,
            combination_result TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_backpacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lore_piece_id INTEGER,
            obtained_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vip_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE,
            max_uses INTEGER,
            used_count INTEGER DEFAULT 0,
            expires_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vip_access (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            channel_id INTEGER,
            access_granted TEXT,
            access_expires TEXT,
            is_active INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            notification_type TEXT,
            message TEXT,
            tone TEXT,
            character TEXT,
            was_delivered INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mission_type TEXT,
            title TEXT,
            description TEXT,
            reward_besitos INTEGER,
            reward_lore INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mission_id INTEGER,
            progress INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            claimed INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_gifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            claimed_at TEXT,
            besitos_reward INTEGER,
            lore_reward INTEGER
        )
    """)

    conn.commit()
    conn.close()
