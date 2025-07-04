import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///dianabot.db')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Configuración del juego
    INITIAL_BESITOS = int(os.getenv('INITIAL_BESITOS', 100))
    DAILY_MISSION_RESET_HOUR = int(os.getenv('DAILY_MISSION_RESET_HOUR', 0))
    
    @classmethod
    def validate(cls):
        """Valida que las configuraciones críticas estén presentes"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN es requerido en el archivo .env")
        return True
