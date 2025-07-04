
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS = [123456789]

DATABASE_URL = "sqlite+aiosqlite:///./dianabot.db"
