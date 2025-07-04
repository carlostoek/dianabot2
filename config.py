import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot_database.db")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN no encontrado. Verifica tus variables de entorno.")
