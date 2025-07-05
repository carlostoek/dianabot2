
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS = os.getenv("ADMIN_IDS")

DATABASE_URL = "sqlite+aiosqlite:///./dianabot.db"
