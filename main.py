#!/usr/bin/env python3
"""
DianaBot - Punto de entrada principal
"""
import asyncio
import logging
import sys
import os

# Añadir el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.bot import DianaBot
from core.config import Config

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('dianabot.log')
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Función principal"""
    try:
        logger.info("🚀 Iniciando DianaBot...")
        
        # Verificar configuración
        if not Config.BOT_TOKEN:
            logger.error("❌ BOT_TOKEN no configurado en .env")
            sys.exit(1)
        
        logger.info(f"✅ Token configurado: {Config.BOT_TOKEN[:10]}...")
        logger.info(f"✅ Base de datos: {Config.DATABASE_URL}")
        
        # Crear y ejecutar bot
        bot = DianaBot()
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
  
